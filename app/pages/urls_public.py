# app/pages/urls_public.py
from django.urls import path, re_path
from . import views_public as views

app_name = "public"

urlpatterns = [
    path("", views.home, name="home"),
    path("events/", views.events, name="events"),
    path("blog/", views.blog, name="blog"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("menu/", views.menu, name="menu"),
    path("gallery/", views.gallery, name="gallery"),
    path("shows/", views.shows, name="shows"),
    path("music/", views.music, name="music"),
    path("videos/", views.videos, name="videos"),
    path("store/", views.store, name="store"),
    path("posts/", views.posts, name="posts"),
    path("archive/", views.archive, name="archive"),
    path("menu/", views.menu, name="menu"),
    # Catch-all page detail (last): /<slug>/
    re_path(r"^(?P<slug>[-a-z0-9]+)/$", views.page_detail, name="page-detail"),
]
