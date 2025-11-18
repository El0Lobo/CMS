"""Views for event management in the CMS."""

from __future__ import annotations

from datetime import datetime, timedelta
import calendar
from urllib.parse import urlencode

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import DateTimeField, Q
from django.db.models.functions import Coalesce
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.dateparse import parse_datetime

from app.events.forms import (
    EventCategoryForm,
    EventFilterForm,
    EventForm,
    EventPerformerFormSet,
    HolidayWindowForm,
)
from app.events.models import Event, EventCategory, EventRecurrenceException, HolidayWindow
from app.events.scheduling import build_occurrence_series, refresh_event_schedule
from app.shifts.services import sync_event_standard_shifts


def _add_months(dt, delta):
    month = dt.month - 1 + delta
    year = dt.year + month // 12
    month = month % 12 + 1
    day = min(dt.day, calendar.monthrange(year, month)[1])
    return dt.replace(year=year, month=month, day=day)


def _parse_occurrence_param(value: str | None) -> datetime | None:
    if not value:
        return None
    parsed = parse_datetime(value)
    if not parsed:
        return None
    if timezone.is_naive(parsed):
        parsed = timezone.make_aware(parsed, timezone.get_current_timezone())
    return parsed


def _serialize_occurrence_param(dt: datetime | None) -> str | None:
    if not dt:
        return None
    if timezone.is_naive(dt):
        dt = timezone.make_aware(dt, timezone.get_current_timezone())
    return timezone.localtime(dt, timezone.get_current_timezone()).isoformat()


def _close_shifts_for_window(events, window, *, allow_signup: bool, status: str | None = None):
    """Batch update shifts in a window to open/close without deleting them."""

    for event in events:
        qs = event.shifts.filter(
            start_at__gte=window.starts_at,
            start_at__lte=window.ends_at,
        )
        update_kwargs = {"allow_signup": allow_signup}
        if status:
            update_kwargs["status"] = status
        qs.update(**update_kwargs)


def _compute_blackout_exceptions(window, events):
    """Create holiday exceptions for occurrences inside the window."""

    for event in events:
        if (event.event_type == Event.EventType.PUBLIC and not window.applies_to_public) or (
            event.event_type == Event.EventType.INTERNAL and not window.applies_to_internal
        ):
            continue
        occurrences = build_occurrence_series(
            event,
            max_occurrences=128,
            include_past=True,
            horizon_end=window.ends_at,
            holiday_windows=[window],
        )
        for occ in occurrences:
            if window.starts_at <= occ.start <= window.ends_at:
                EventRecurrenceException.objects.update_or_create(
                    event=event,
                    occurrence_start=occ.start,
                    defaults={
                        "exception_type": EventRecurrenceException.ExceptionType.HOLIDAY,
                        "override_event": None,
                    },
                )
        refresh_event_schedule(
            event,
            max_occurrences=64,
            horizon_end=_add_months(timezone.now(), 6),
            holiday_windows=[window],
            exceptions=event.recurrence_exceptions.all(),
        )


def _affected_recurring_events(window):
    """Return recurring events that intersect the provided holiday window."""

    recurring = Event.objects.exclude(recurrence_frequency=Event.RecurrenceFrequency.NONE)
    return recurring.filter(
        Q(starts_at__range=(window.starts_at, window.ends_at))
        | Q(recurrence_next_start_at__range=(window.starts_at, window.ends_at))
        | Q(
            recurrence_exceptions__occurrence_start__range=(window.starts_at, window.ends_at),
            recurrence_exceptions__exception_type=EventRecurrenceException.ExceptionType.HOLIDAY,
        )
    ).distinct()


@login_required
def index(request: HttpRequest) -> HttpResponse:
    filter_form = EventFilterForm(request.GET or None)
    if filter_form.is_valid():
        filters = filter_form.cleaned_data
    else:
        filters = {}

    search_query = filters.get("q") or request.GET.get("q", "").strip()

    events = (
        Event.objects.select_related("created_by", "updated_by")
        .prefetch_related("categories", "recurrence_exceptions__override_event")
        .annotate(
            effective_start=Coalesce(
                "starts_at",
                "recurrence_next_start_at",
                output_field=DateTimeField(),
            )
        )
        .filter(recurrence_parent__isnull=True)
    )

    if search_query:
        events = events.filter(title__icontains=search_query)

    tz = timezone.get_current_timezone()
    now = timezone.now()
    local_now = timezone.localtime(now, tz)
    recurrence_horizon = _add_months(now, 6)
    include_past = bool(filters.get("include_past"))
    timeframe = filters.get("timeframe") or EventFilterForm.Timeframe.MONTH
    offset = filters.get("period_offset") or 0

    def to_local(dt):
        if not dt:
            return None
        if timezone.is_naive(dt):
            return timezone.make_aware(dt, tz)
        return timezone.localtime(dt, tz)

    def build_card(event_obj, start_dt, doors_dt, *, occurrence=None, base_event=None):
        start_local = to_local(start_dt)
        doors_local = to_local(doors_dt)
        scope_label = None
        if occurrence and base_event and base_event.is_recurring:
            scope_label = "Custom occurrence" if occurrence.is_override else "Single occurrence"
        occurrence_param = _serialize_occurrence_param(occurrence.start) if occurrence else None
        query_string = urlencode({"occurrence": occurrence_param}) if occurrence_param else ""
        if occurrence and base_event and base_event.is_recurring:
            if occurrence.is_override:
                edit_url = reverse("events:edit", args=[event_obj.slug])
            else:
                edit_url = reverse("events:occurrence_edit", args=[base_event.slug])
                if query_string:
                    edit_url = f"{edit_url}?{query_string}"
            delete_url = reverse("events:occurrence_delete", args=[base_event.slug])
        else:
            edit_url = reverse("events:edit", args=[event_obj.slug])
            delete_url = reverse("events:delete", args=[event_obj.slug])

        return {
            "event": event_obj,
            "start": start_local,
            "start_label": start_local.strftime("%a, %b %d · %H:%M") if start_local else "TBD",
            "doors_label": doors_local.strftime("%H:%M") if doors_local else "",
            "has_shifts": event_obj.requires_shifts,
            "scope_label": scope_label,
            "occurrence_param": occurrence_param,
            "is_override": bool(occurrence and occurrence.is_override),
            "is_occurrence": occurrence is not None,
            "edit_url": edit_url,
            "delete_url": delete_url,
        }

    future_placeholder = now + timedelta(days=365 * 10)
    start_local = None
    end_local = None

    if timeframe == EventFilterForm.Timeframe.WEEK:
        base = (local_now - timedelta(days=local_now.weekday())).replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        start_local = base + timedelta(weeks=offset)
        end_local = start_local + timedelta(weeks=1)
    elif timeframe == EventFilterForm.Timeframe.MONTH:
        base = local_now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        start_local = _add_months(base, offset)
        end_local = _add_months(start_local, 1)
    elif timeframe == EventFilterForm.Timeframe.YEAR:
        base = local_now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        start_local = base.replace(year=base.year + offset)
        end_local = start_local.replace(year=start_local.year + 1)

    lower_bound = None
    if include_past:
        lower_bound = start_local
    else:
        if timeframe == EventFilterForm.Timeframe.ALL:
            lower_bound = now
        else:
            candidates = [dt for dt in [now, start_local] if dt is not None]
            lower_bound = max(candidates) if candidates else None

    recurring_filter = ~Q(recurrence_frequency=Event.RecurrenceFrequency.NONE)
    single_filter = Q(recurrence_frequency=Event.RecurrenceFrequency.NONE)

    if lower_bound is not None:
        events = events.filter(
            (single_filter & (Q(effective_start__isnull=True) | Q(effective_start__gte=lower_bound)))
            | recurring_filter
        )

    if end_local is not None:
        events = events.filter(
            (single_filter & (Q(effective_start__isnull=True) | Q(effective_start__lte=end_local)))
            | recurring_filter
        )

    if timeframe == EventFilterForm.Timeframe.WEEK and start_local and end_local:
        range_label = f"{start_local.strftime('%b %d')} – {(end_local - timedelta(days=1)).strftime('%b %d')}"
    elif timeframe == EventFilterForm.Timeframe.MONTH and start_local:
        range_label = start_local.strftime("%B %Y")
    elif timeframe == EventFilterForm.Timeframe.YEAR and start_local:
        range_label = start_local.strftime("%Y")
    else:
        range_label = "All events" if include_past else "Upcoming events"

    show_navigation = timeframe != EventFilterForm.Timeframe.ALL
    prev_url = next_url = None
    if show_navigation:
        def build_nav(delta: int) -> str:
            params = request.GET.copy()
            params["timeframe"] = timeframe
            new_offset = offset + delta
            if new_offset:
                params["period_offset"] = str(new_offset)
            elif "period_offset" in params:
                del params["period_offset"]
            return f"{request.path}?{params.urlencode()}"

        prev_url = build_nav(-1)
        next_url = build_nav(1)

    timeframe_label = dict(EventFilterForm.Timeframe.choices).get(timeframe, "")

    window_start = lower_bound
    window_end = end_local
    holiday_windows = list(HolidayWindow.overlapping(window_start, recurrence_horizon))

    events = events.order_by("effective_start", "title")
    all_events = list(events)

    # Prepare display data
    recurring_series = []
    recurring_seen = set()
    scheduled_cards = []
    unscheduled_cards = []

    for event in all_events:
        start_val = getattr(event, "effective_start", None)
        event_start_local = to_local(start_val)

        if event.is_recurring:
            event_exceptions = list(event.recurrence_exceptions.all())
            refresh_event_schedule(
                event,
                max_occurrences=64,
                horizon_end=recurrence_horizon,
                holiday_windows=holiday_windows,
                exceptions=event_exceptions,
            )
            occurrences = build_occurrence_series(
                event,
                max_occurrences=64,
                include_past=True,
                horizon_end=recurrence_horizon,
                holiday_windows=holiday_windows,
                exceptions=event_exceptions,
            )
            visible = []
            for occ in occurrences:
                if window_start and occ.start < window_start:
                    continue
                if window_end and occ.start >= window_end:
                    continue
                visible.append(occ)
            has_any = bool(occurrences)
            has_visible = bool(visible)
            event.recurrence_has_any = has_any
            event.recurrence_has_window = has_visible
            event.recurrence_preview = visible[:4]
            for occ in visible:
                scheduled_cards.append(
                    build_card(
                        occ.event,
                        occ.start,
                        occ.doors or occ.event.doors_at,
                        occurrence=occ,
                        base_event=event,
                    )
                )
            if event.pk not in recurring_seen:
                recurring_series.append(event)
                recurring_seen.add(event.pk)
            continue

        event.recurrence_preview = []

        card = build_card(event, start_val, event.doors_at)

        if event_start_local:
            scheduled_cards.append(card)
        else:
            unscheduled_cards.append(card)

    scheduled_cards.sort(key=lambda e: e["start"] or future_placeholder)
    unscheduled_cards.sort(key=lambda e: e["event"].title.lower())

    recurring_series.sort(key=lambda e: e.title.lower())

    event_form = EventForm(user=request.user)
    performer_formset = EventPerformerFormSet(prefix="performers")
    category_form = EventCategoryForm()
    categories = EventCategory.objects.order_by("name")

    return render(
        request,
        "events/index.html",
        {
            "scheduled_events": scheduled_cards,
            "unscheduled_events": unscheduled_cards,
            "recurring_series": recurring_series,
            "search_query": search_query,
            "filter_form": filter_form,
            "filter_range_label": range_label,
            "filter_nav_prev_url": prev_url,
            "filter_nav_next_url": next_url,
            "filter_nav_show": show_navigation,
            "filter_timeframe_label": timeframe_label,
            "period_offset": offset,
            "event_form": event_form,
            "performer_formset": performer_formset,
            "category_form": category_form,
            "categories": categories,
        },
    )


@login_required
@transaction.atomic
def create(request: HttpRequest) -> HttpResponse:
    if request.method != "POST":
        return HttpResponseBadRequest("POST required")

    form = EventForm(request.POST, request.FILES, user=request.user)
    formset = EventPerformerFormSet(request.POST, request.FILES, prefix="performers")

    if not (form.is_valid() and formset.is_valid()):
        messages.error(request, "Please correct the errors in the event form.")
        return render(
            request,
            "events/partials/event_form_body.html",
            {"event_form": form, "performer_formset": formset},
            status=400,
        )

    event = form.save()
    formset.instance = event
    formset.save()
    form.save_m2m()
    sync_event_standard_shifts(event, user=request.user, max_occurrences=4)

    messages.success(request, "Event created.")

    if request.htmx:
        response = HttpResponse(status=204)
        response["Hx-Trigger"] = "event:created"
        response["Hx-Redirect"] = reverse("events:index")
        return response

    return redirect("events:edit", slug=event.slug)


@login_required
def edit(request: HttpRequest, slug: str) -> HttpResponse:
    event = get_object_or_404(Event, slug=slug)

    if request.method == "POST":
        form = EventForm(request.POST, request.FILES, instance=event, user=request.user)
        formset = EventPerformerFormSet(
            request.POST, request.FILES, instance=event, prefix="performers"
        )
        if form.is_valid() and formset.is_valid():
            event = form.save()
            formset.save()
            form.save_m2m()
            sync_event_standard_shifts(event, user=request.user, max_occurrences=64)
            messages.success(request, "Event updated.")
            if request.htmx:
                response = HttpResponse(status=204)
                response["Hx-Trigger"] = "event:updated"
                return response
            return redirect("events:edit", slug=event.slug)
    else:
        form = EventForm(instance=event, user=request.user)
        formset = EventPerformerFormSet(instance=event, prefix="performers")

    return render(
        request,
        "events/edit.html",
        {
            "event": event,
            "event_form": form,
            "performer_formset": formset,
            "occurrence_mode": event.is_override,
            "occurrence_start": event.recurrence_parent_start,
            "occurrence_parent": event.recurrence_parent,
        },
    )


@login_required
def detail(request: HttpRequest, slug: str) -> HttpResponse:
    event = get_object_or_404(
        Event.objects.prefetch_related("performers", "categories", "recurrence_exceptions__override_event"),
        slug=slug,
    )
    horizon = _add_months(timezone.now(), 6)
    holiday_windows = list(HolidayWindow.overlapping(timezone.now(), horizon))
    event_exceptions = list(event.recurrence_exceptions.all())
    occurrences = build_occurrence_series(
        event,
        max_occurrences=64,
        include_past=True,
        horizon_end=horizon,
        holiday_windows=holiday_windows,
        exceptions=event_exceptions,
    )
    return render(request, "events/detail.html", {"event": event, "occurrences": occurrences})


@login_required
@transaction.atomic
def delete(request: HttpRequest, slug: str) -> HttpResponse:
    event = get_object_or_404(Event, slug=slug)
    if request.method != "POST":
        return HttpResponseBadRequest("POST required")

    parent = event.recurrence_parent
    parent_start = event.recurrence_parent_start
    event.delete()
    if parent and parent_start:
        EventRecurrenceException.objects.update_or_create(
            event=parent,
            occurrence_start=parent_start,
            defaults={
                "exception_type": EventRecurrenceException.ExceptionType.SKIP,
                "override_event": None,
            },
        )
        refresh_event_schedule(parent, max_occurrences=64, horizon_end=_add_months(timezone.now(), 6))
    messages.success(request, "Event deleted.")
    return redirect("events:index")


@login_required
@transaction.atomic
def edit_occurrence(request: HttpRequest, slug: str) -> HttpResponse:
    event = get_object_or_404(Event, slug=slug)
    if not event.is_recurring:
        return redirect("events:edit", slug=event.slug)

    occurrence_value = request.GET.get("occurrence") or request.POST.get("occurrence")
    occurrence_dt = _parse_occurrence_param(occurrence_value)
    if not occurrence_dt:
        return HttpResponseBadRequest("Missing or invalid occurrence.")

    exception = (
        EventRecurrenceException.objects.select_for_update()
        .select_related("override_event")
        .filter(event=event, occurrence_start=occurrence_dt)
        .first()
    )
    override_event = exception.override_event if exception and exception.override_event else None

    if not override_event:
        override_event = event.clone_for_occurrence(occurrence_dt)
        EventRecurrenceException.objects.update_or_create(
            event=event,
            occurrence_start=occurrence_dt,
            defaults={
                "exception_type": EventRecurrenceException.ExceptionType.OVERRIDE,
                "override_event": override_event,
            },
        )

    messages.info(request, "You are editing a single occurrence. Other dates remain unchanged.")
    return redirect("events:edit", slug=override_event.slug)


@login_required
@transaction.atomic
def delete_occurrence(request: HttpRequest, slug: str) -> HttpResponse:
    if request.method != "POST":
        return HttpResponseBadRequest("POST required")

    event = get_object_or_404(Event, slug=slug)
    occurrence_value = request.POST.get("occurrence")
    occurrence_dt = _parse_occurrence_param(occurrence_value)
    if not occurrence_dt:
        return HttpResponseBadRequest("Missing or invalid occurrence.")

    exception, _ = EventRecurrenceException.objects.select_for_update().get_or_create(
        event=event,
        occurrence_start=occurrence_dt,
        defaults={
            "exception_type": EventRecurrenceException.ExceptionType.SKIP,
        },
    )
    if exception.override_event:
        exception.override_event.delete()
    exception.override_event = None
    exception.exception_type = EventRecurrenceException.ExceptionType.SKIP
    exception.save()
    refresh_event_schedule(event, max_occurrences=64, horizon_end=_add_months(timezone.now(), 6))
    messages.success(request, "Occurrence removed from the recurrence.")
    return redirect("events:index")


@login_required
def categories(request: HttpRequest) -> HttpResponse:
    categories_qs = EventCategory.objects.order_by("name")
    if request.method == "POST":
        form = EventCategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            messages.success(request, f"Category '{category.name}' created.")
            return redirect("events:categories")
    else:
        form = EventCategoryForm()

    return render(
        request,
        "events/categories.html",
        {
            "categories": categories_qs,
            "category_form": form,
        },
    )


@login_required
def category_create(request: HttpRequest) -> HttpResponse:
    if request.method != "POST":
        return HttpResponseBadRequest("POST required")

    form = EventCategoryForm(request.POST)
    if form.is_valid():
        category = form.save()
        messages.success(request, f"Category '{category.name}' created.")
    else:
        errors = "; ".join([" ".join(values) for values in form.errors.values()])
        if errors:
            messages.error(request, f"Could not create category: {errors}")
        else:
            messages.error(request, "Could not create category.")
    return redirect("events:index")


@login_required
def category_edit(request: HttpRequest, pk: int) -> HttpResponse:
    category = get_object_or_404(EventCategory, pk=pk)
    if request.method == "POST":
        form = EventCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, f"Category '{category.name}' updated.")
            return redirect("events:categories")
    else:
        form = EventCategoryForm(instance=category)

    return render(
        request,
        "events/category_edit.html",
        {
            "category": category,
            "category_form": form,
        },
    )


@login_required
def category_delete(request: HttpRequest, pk: int) -> HttpResponse:
    category = get_object_or_404(EventCategory, pk=pk)
    if request.method != "POST":
        return HttpResponseBadRequest("POST required")
    category.delete()
    messages.success(request, f"Category '{category.name}' deleted.")
    return redirect("events:categories")


@login_required
def holidays(request: HttpRequest) -> HttpResponse:
    holidays_qs = HolidayWindow.objects.order_by("-starts_at")
    if request.method == "POST":
        form = HolidayWindowForm(request.POST, user=request.user)
        if form.is_valid():
            window = form.save()
            affected_events = list(_affected_recurring_events(window))
            _compute_blackout_exceptions(window, affected_events)
            # Only close shifts for events the window applies to
            applicable_events = [
                e for e in affected_events
                if (e.event_type == Event.EventType.PUBLIC and window.applies_to_public)
                or (e.event_type == Event.EventType.INTERNAL and window.applies_to_internal)
            ]
            _close_shifts_for_window(applicable_events, window, allow_signup=False, status="closed")
            messages.success(request, f"Holiday '{window.name}' saved.")
            return redirect("events:holidays")
    else:
        form = HolidayWindowForm()

    return render(
        request,
        "events/holidays.html",
        {
            "holidays": holidays_qs,
            "holiday_form": form,
        },
    )


@login_required
def holiday_delete(request: HttpRequest, pk: int) -> HttpResponse:
    window = get_object_or_404(HolidayWindow, pk=pk)
    if request.method != "POST":
        return HttpResponseBadRequest("POST required")
    affected_events = list(_affected_recurring_events(window))
    # Remove holiday exceptions only for events the window applied to
    EventRecurrenceException.objects.filter(
        exception_type=EventRecurrenceException.ExceptionType.HOLIDAY,
        occurrence_start__range=(window.starts_at, window.ends_at),
        event__event_type__in=[
            Event.EventType.PUBLIC if window.applies_to_public else None,
            Event.EventType.INTERNAL if window.applies_to_internal else None,
        ],
    ).exclude(event__event_type=None).delete()
    window.delete()
    applicable_events = [
        e for e in affected_events
        if (e.event_type == Event.EventType.PUBLIC and window.applies_to_public)
        or (e.event_type == Event.EventType.INTERNAL and window.applies_to_internal)
    ]
    _close_shifts_for_window(applicable_events, window, allow_signup=True, status="open")
    active_holidays = list(HolidayWindow.overlapping(timezone.now(), _add_months(timezone.now(), 6)))
    for event in affected_events:
        event_exceptions = list(event.recurrence_exceptions.all())
        refresh_event_schedule(
            event,
            max_occurrences=64,
            horizon_end=_add_months(timezone.now(), 6),
            holiday_windows=active_holidays,
            exceptions=event_exceptions,
        )
        sync_event_standard_shifts(
            event,
            user=request.user,
            max_occurrences=64,
        )
    messages.success(request, f"Holiday '{window.name}' removed.")
    return redirect("events:holidays")


@login_required
def holiday_edit(request: HttpRequest, pk: int) -> HttpResponse:
    window = get_object_or_404(HolidayWindow, pk=pk)
    if request.method == "POST":
        form = HolidayWindowForm(request.POST, instance=window, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f"Holiday '{window.name}' updated.")
            return redirect("events:holidays")
    else:
        form = HolidayWindowForm(instance=window, user=request.user)

    return render(
        request,
        "events/holiday_edit.html",
        {
            "holiday": window,
            "holiday_form": form,
        },
    )
