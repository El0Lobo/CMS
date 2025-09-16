from django.contrib.auth.decorators import login_required
from django.shortcuts import render

SAMPLE = [{'title': 'Open Mic Night', 'slug': 'open-mic-night', 'date': 'Sat 20:00', 'status': 'published'}, {'title': 'Trivia Tuesday', 'slug': 'trivia-tuesday', 'date': 'Tue 19:00', 'status': 'draft'}]

@login_required
def index(request):
    return render(request, "events/index.html", {"rows": SAMPLE})

@login_required
def create(request):
    return render(request, "events/form.html", {"mode":"create"})

@login_required
def edit(request, slug):
    item = next((r for r in SAMPLE if r.get("slug")==slug), None)
    return render(request, "events/form.html", {"mode":"edit","item":item})
