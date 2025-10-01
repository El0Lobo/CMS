"""Views for event management in the CMS."""

from __future__ import annotations

from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from app.events.forms import EventForm, EventPerformerFormSet
from app.events.models import Event
from app.shifts.models import Shift, ShiftTemplate


@login_required
def index(request: HttpRequest) -> HttpResponse:
    q = request.GET.get("q", "").strip()
    events = Event.objects.all()
    if q:
        events = events.filter(title__icontains=q)
    events = events.select_related("created_by", "updated_by").prefetch_related("categories")

    event_form = EventForm(user=request.user)
    performer_formset = EventPerformerFormSet(prefix="performers")

    return render(
        request,
        "events/index.html",
        {
            "events": events,
            "search_query": q,
            "event_form": event_form,
            "performer_formset": performer_formset,
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
    sync_event_standard_shifts(event, user=request.user)

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
            sync_event_standard_shifts(event, user=request.user)
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
    return render(request, "events/detail.html", {"event": event})


@login_required
@transaction.atomic
def delete(request: HttpRequest, slug: str) -> HttpResponse:
    event = get_object_or_404(Event, slug=slug)
    if request.method != "POST":
        return HttpResponseBadRequest("POST required")

    event.delete()
    messages.success(request, "Event deleted.")
    return redirect("events:index")


def sync_event_standard_shifts(event: Event, *, user):
    print(f"Syncing shifts for event {event} with templates: {list(event.standard_shifts.values_list('id', flat=True))}")
    # ...existing code...
    """Ensure standard shift template selections are reflected in actual shifts."""

    template_ids = list(event.standard_shifts.values_list("id", flat=True))
    if not event.requires_shifts:
        event.shifts.filter(template__isnull=False).delete()
        return

    existing_by_template = {
        (shift.template_id, shift.template_segment, shift.template_staff_position): shift
        for shift in event.shifts.filter(template__isnull=False)
    }

    expected_keys = set()

    for template_id in template_ids:
        try:
            template = ShiftTemplate.objects.get(pk=template_id)
        except ShiftTemplate.DoesNotExist:  # pragma: no cover - defensive
            continue

        segments = template.segment_schedule(event)
        for segment in segments:
            for staff_index in range(1, max(template.capacity, 1) + 1):
                key = (template.id, segment["index"], staff_index)
                expected_keys.add(key)
                shift = existing_by_template.get(key)
                title = segment["title"]
                if template.capacity > 1:
                    title = f"{segment['title']} - Slot {staff_index}"
                if shift:
                    shift.title = title
                    shift.description = template.description
                    shift.start_at = segment["start"]
                    shift.end_at = segment["end"]
                    shift.capacity = 1
                    shift.allow_signup = template.allow_signup
                    shift.visibility_key = template.visibility_key
                    shift.template = template
                    shift.template_segment = segment["index"]
                    shift.template_staff_position = staff_index
                    shift.updated_by = user
                    shift.save()
                else:
                    Shift.objects.create(
                        event=event,
                        template=template,
                        template_segment=segment["index"],
                        template_staff_position=staff_index,
                        title=title,
                        description=template.description,
                        start_at=segment["start"],
                        end_at=segment["end"],
                        capacity=1,
                        allow_signup=template.allow_signup,
                        visibility_key=template.visibility_key,
                        created_by=user,
                        updated_by=user,
                    )

    # Remove shifts whose templates or segments are no longer selected
    for key, shift in existing_by_template.items():
        if key not in expected_keys:
            shift.delete()
