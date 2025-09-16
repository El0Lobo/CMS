from django.contrib.auth.decorators import login_required
from django.shortcuts import render

SAMPLE = [{'title': 'Open Mic Night', 'slug': 'open-mic-night', 'event': 'Open Mic Night', 'role': 'Bar', 'slots': '3', 'filled': '1'}]

@login_required
def index(request):
    return render(request, "shifts/index.html", {"rows": SAMPLE})

@login_required
def create(request):
    return render(request, "shifts/form.html", {"mode":"create"})

@login_required
def edit(request, slug):
    item = next((r for r in SAMPLE if r.get("slug")==slug), None)
    return render(request, "shifts/form.html", {"mode":"edit","item":item})
