from django.shortcuts import render
from app.menu.models import Category
from django.utils import timezone

def menu_page(request):
    drinks = Category.objects.filter(parent__isnull=True, kind=Category.KIND_DRINK).first()
    food = Category.objects.filter(parent__isnull=True, kind=Category.KIND_FOOD).first()
    return render(request, "public/menu.html", {
    "roots": roots,   
})
