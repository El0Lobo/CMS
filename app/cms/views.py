from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q, Sum
from django.shortcuts import render
from django.utils import timezone

from app.events.models import Event
from app.inventory.models import InventoryItem
from app.inventory.utils import user_can_see_inventory_dashboard
from app.shifts.models import Shift, ShiftAssignment


@login_required
def dashboard(request):
    cards = []
    inventory_alerts = []
    shift_glance = None

    if user_can_see_inventory_dashboard(request.user):
        inventory_alerts = list(
            InventoryItem.objects.filter(needs_reorder=True)
            .order_by("name")
            .values("name", "current_stock", "desired_stock", "location")[:8]
        )

    start = timezone.now()
    end = start + timedelta(days=7)
    upcoming_shifts = (
        Shift.objects.filter(start_at__gte=start, start_at__lt=end)
        .select_related("event")
        .annotate(
            filled=Count(
                "assignments",
                filter=Q(
                    assignments__status__in=[
                        ShiftAssignment.Status.ASSIGNED,
                        ShiftAssignment.Status.COMPLETED,
                    ]
                ),
            )
        )
    )
    total_slots = upcoming_shifts.aggregate(total=Sum("capacity")).get("total") or 0
    open_items = []
    open_total = 0
    open_by_event = {}
    for shift in upcoming_shifts:
        open_slots = max(shift.capacity - getattr(shift, "filled", 0), 0)
        if open_slots > 0 and shift.event:
            key = shift.event.pk
            open_by_event.setdefault(
                key,
                {
                    "event": shift.event,
                    "open": 0,
                },
            )
            open_by_event[key]["open"] += open_slots
            open_total += open_slots
    open_items = sorted(open_by_event.values(), key=lambda item: item["event"].starts_at)[:5]
    if total_slots:
        shift_glance = {
            "total": total_slots,
            "filled": total_slots - open_total,
            "open": open_total,
            "open_items": open_items,
        }

    recent_events = list(
        Event.objects.filter(recurrence_parent__isnull=True)
        .order_by("-created_at")
        .only("title", "starts_at", "slug")[:3]
    )

    context = {
        "cards": cards,
        "inventory_alerts": inventory_alerts,
        "shift_glance": shift_glance,
        "recent_events": recent_events,
    }
    return render(request, "cms/dashboard.html", context)


@login_required
def account(request):
    return render(request, "cms/account.html")
