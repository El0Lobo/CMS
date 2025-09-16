from django.contrib.auth.decorators import login_required
from django.shortcuts import render

SAMPLE = [
    {"title":"Home","slug":"home","updated":"today","notes":""},
    {"title":"About","slug":"about","updated":"yesterday","notes":"Sample page"},
]

@login_required
def index(request):
    return render(request, "pages/index.html", {"rows": SAMPLE})

@login_required
def create(request):
    return render(request, "pages/form.html", {"mode":"create"})

@login_required
def edit(request, slug):
    item = next((r for r in SAMPLE if r.get("slug")==slug), None)
    return render(request, "pages/form.html", {"mode":"edit","item":item})
