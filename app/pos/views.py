from django.contrib.auth.decorators import login_required
from django.shortcuts import render

SAMPLE = [{'title': 'Walkup #12', 'slug': 'walkup-12', 'tab': 'Walkup #12', 'items': '3', 'total': '€21.50', 'status': 'Paid'}]

@login_required
def index(request):
    return render(request, "pos/index.html", {"rows": SAMPLE})

@login_required
def create(request):
    return render(request, "pos/form.html", {"mode":"create"})

@login_required
def edit(request, slug):
    item = next((r for r in SAMPLE if r.get("slug")==slug), None)
    return render(request, "pos/form.html", {"mode":"edit","item":item})
