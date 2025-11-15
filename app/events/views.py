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

from app.events.forms import EventCategoryForm, EventFilterForm, EventForm, EventPerformerFormSet
from app.events.models import Event, EventCategory
from app.events.scheduling import build_occurrence_series, refresh_event_schedule
from app.shifts.services import sync_event_standard_shifts


def _add_months(dt, delta):
    month = dt.month - 1 + delta
    year = dt.year + month // 12
    month = month % 12 + 1
    day = min(dt.day, calendar.monthrange(year, month)[1])
    return dt.replace(year=year, month=month, day=day)


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
        .prefetch_related("categories")
        .annotate(
            effective_start=Coalesce(
                "starts_at",
                "recurrence_next_start_at",
                output_field=DateTimeField(),
            )
        )
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

    def build_card(event_obj, start_dt, doors_dt):
        start_local = to_local(start_dt)
        doors_local = to_local(doors_dt)
        return {
            "event": event_obj,
            "start": start_local,
            "start_label": start_local.strftime("%a, %b %d · %H:%M") if start_local else "TBD",
            "doors_label": doors_local.strftime("%H:%M") if doors_local else "",
            "has_shifts": event_obj.requires_shifts,
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
            refresh_event_schedule(
                event,
                max_occurrences=64,
                horizon_end=recurrence_horizon,
            )
            occurrences = build_occurrence_series(
                event,
                max_occurrences=64,
                include_past=True,
                horizon_end=recurrence_horizon,
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
                    build_card(event, occ.start, occ.doors)
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
        },
    )


@login_required
def detail(request: HttpRequest, slug: str) -> HttpResponse:
    event = get_object_or_404(Event.objects.prefetch_related("performers", "categories"), slug=slug)
    occurrences = build_occurrence_series(
        event,
        max_occurrences=64,
        include_past=True,
        horizon_end=_add_months(timezone.now(), 6),
    )
    return render(request, "events/detail.html", {"event": event, "occurrences": occurrences})


@login_required
@transaction.atomic
def delete(request: HttpRequest, slug: str) -> HttpResponse:
    event = get_object_or_404(Event, slug=slug)
    if request.method != "POST":
        return HttpResponseBadRequest("POST required")

    event.delete()
    messages.success(request, "Event deleted.")
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
