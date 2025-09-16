from django.contrib.auth.decorators import login_required
from django.shortcuts import render
SAMPLE = [{"title":"Welcome","slug":"welcome","status":"draft","updated":"today"}]
@login_required
def index(request): return render(request,"blog/index.html",{"rows":SAMPLE})
@login_required
def create(request): return render(request,"blog/form.html",{"mode":"create"})
@login_required
def edit(request, slug):
    item = next((r for r in SAMPLE if r.get("slug")==slug), None)
    return render(request,"blog/form.html",{"mode":"edit","item":item})
