from django.contrib.auth.decorators import login_required
from django.shortcuts import render

SAMPLE = [{'title': 'IPA Keg', 'slug': 'ipa-keg', 'item': 'IPA Keg 30L', 'on hand': '2', 'reorder': '2', 'location': 'Cold store'}]

@login_required
def index(request):
    return render(request, "inventory/index.html", {"rows": SAMPLE})

@login_required
def create(request):
    return render(request, "inventory/form.html", {"mode":"create"})

@login_required
def edit(request, slug):
    item = next((r for r in SAMPLE if r.get("slug")==slug), None)
    return render(request, "inventory/form.html", {"mode":"edit","item":item})
