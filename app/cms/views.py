from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from app.inventory.models import InventoryItem
from app.inventory.utils import user_can_see_inventory_dashboard


@login_required
def dashboard(request):
    cards = []
    inventory_alerts = []
    if user_can_see_inventory_dashboard(request.user):
        inventory_alerts = list(
            InventoryItem.objects.filter(needs_reorder=True)
            .order_by("name")
            .values("name", "current_stock", "desired_stock", "location")[:8]
        )
    return render(request, "cms/dashboard.html", {"cards": cards, "inventory_alerts": inventory_alerts})


@login_required
def account(request):
    return render(request, "cms/account.html")
