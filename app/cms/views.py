from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def dashboard(request):
    # sample cards; replace with real queries
    cards = [
        {"title": "Upcoming Event", "body": "Open Mic Night — Sat 20:00"},
        {"title": "Shifts needing staff", "body": "3 open slots this week"},
        {"title": "Low stock", "body": "Limes, IPA Keg"},
    ]
    return render(request, "cms/dashboard.html", {"cards": cards})

@login_required
def account(request):
    return render(request, "cms/account.html")
