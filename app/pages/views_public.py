# app/pages/views_public.py
from django.shortcuts import render, get_object_or_404
from django.apps import apps
from django.utils import timezone
from django.db.models import Q

# Helper: try to load a model if that app exists
def _get_model(label, model_name):
    try:
        return apps.get_model(label, model_name)
    except Exception:
        return None

def home(request):
    return render(request, "public/home.html", {})

def events(request):
    Event = _get_model("app.events", "Event")
    events = Event.objects.upcoming() if Event and hasattr(Event.objects, "upcoming") else (Event.objects.all() if Event else [])
    return render(request, "public/events.html", {"events": events})

def blog(request):
    Post = _get_model("app.blog", "Post")
    posts = Post.objects.published().order_by("-published_at") if Post and hasattr(Post.objects, "published") else (Post.objects.all().order_by("-id") if Post else [])
    return render(request, "public/blog.html", {"posts": posts})

def about(request):
    return render(request, "public/about.html", {})

def contact(request):
    return render(request, "public/contact.html", {})

def menu(request):
    # Expect structure: [{"title": "...", "items": [{"name": "...", "price_display": "..."}]}]
    MenuSection = _get_model("app.cms", "MenuSection") or _get_model("app.pos", "MenuSection")
    if MenuSection:
        sections = MenuSection.objects.prefetch_related("items").all()
        menu_sections = [{"title": s.title, "items": [{"name": i.name, "price_display": getattr(i, "price_display", str(getattr(i, "price_minor", "")))} for i in s.items.all()]} for s in sections]
    else:
        menu_sections = []
    return render(request, "public/menu.html", {"menu_sections": menu_sections})

def gallery(request):
    # Expect simple list of images with url/caption
    GalleryImage = _get_model("app.cms", "GalleryImage") or _get_model("app.publicthemes", "GalleryImage")
    images = GalleryImage.objects.all() if GalleryImage else []
    return render(request, "public/gallery.html", {"images": images})

def shows(request):
    Show = _get_model("app.events", "Show") or _get_model("app.band", "Show")
    shows = Show.objects.all().order_by("date") if Show else []
    return render(request, "public/shows.html", {"shows": shows})

def music(request):
    return render(request, "public/music.html", {})

def videos(request):
    Video = _get_model("app.social", "Video") or _get_model("app.cms", "Video")
    videos = Video.objects.all().order_by("-id") if Video else []
    return render(request, "public/videos.html", {"videos": videos})

def store(request):
    Product = _get_model("app.merch", "Product") or _get_model("app.pos", "Product")
    products = Product.objects.available() if Product and hasattr(Product.objects, "available") else (Product.objects.all() if Product else [])
    return render(request, "public/store.html", {"products": products})

def posts(request):
    Post = _get_model("app.blog", "Post")
    posts = Post.objects.published().order_by("-published_at") if Post and hasattr(Post.objects, "published") else (Post.objects.all().order_by("-id") if Post else [])
    return render(request, "public/posts.html", {"posts": posts})

def archive(request):
    # Build a simple archive structure: [(month_start_date, [posts])]
    Post = _get_model("app.blog", "Post")
    archive = []
    if Post:
        qs = Post.objects.published() if hasattr(Post.objects, "published") else Post.objects.all()
        qs = qs.order_by("-published_at")
        buckets = {}
        for p in qs:
            if not getattr(p, "published_at", None):
                continue
            key = p.published_at.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            buckets.setdefault(key, []).append(p)
        archive = sorted(buckets.items(), key=lambda kv: kv[0], reverse=True)
    return render(request, "public/archive.html", {"archive": archive})

def page_detail(request, slug):
    # Generic CMS page fallback
    Page = _get_model("app.pages", "Page") or _get_model("app.cms", "Page")
    if Page:
        page = get_object_or_404(Page, slug=slug)
        return render(request, "public/page_detail.html", {"page": page})
    # If no Page model, render a minimal stand-in
    fake = type("Page", (), {"title": slug.replace("-", " ").title(), "body": "<p>Content coming soon.</p>", "created_at": timezone.now()})
    return render(request, "public/page_detail.html", {"page": fake})

from django.shortcuts import render
from app.menu.models import Category

def menu(request):
    roots = (
        Category.objects
        .filter(parent__isnull=True)
        .prefetch_related(
            "children__children",
            "items__variants",
            "children__items__variants",
        )
        .order_by("name")
    )
    return render(request, "public/menu.html", {"roots": roots})
