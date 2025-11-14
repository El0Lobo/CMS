from __future__ import annotations

from django.contrib.auth.views import LoginView
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import NoReverseMatch, reverse

from app.setup.models import SiteSettings

from .models import Page
from .navigation import build_nav_payload


def _public_enabled_or_404() -> SiteSettings:
    settings_obj = SiteSettings.get_solo()
    if not settings_obj.public_pages_enabled:
        raise Http404("Public site is disabled.")
    return settings_obj


def _published_queryset():
    return Page.objects.filter(status=Page.Status.PUBLISHED, is_visible=True)


def _nav_payload_for(page: Page):
    if not page.show_navigation_bar:
        return []
    override = [slug for slug in (page.custom_nav_items or []) if slug]
    if not override:
        return []
    return build_nav_payload(override)


def _render_page(request, page: Page) -> HttpResponse:
    rendered, footer = page.render_content_segments(request=request)
    nav_entries = _nav_payload_for(page)
    context = {
        "page": page,
        "page_rendered": rendered,
        "page_footer": footer,
        "nav_label": page.title,
        "public_pages": nav_entries,
        "page_show_nav": bool(nav_entries),
    }
    return render(request, "public/page_detail.html", context)


def _first_available_page():
    qs = _published_queryset()
    home = qs.filter(slug="home").first()
    if home:
        return home
    return qs.order_by("navigation_order", "title").first()


def home(request):
    _public_enabled_or_404()
    page = _first_available_page()
    if not page:
        return render(
            request,
            "public/empty_site.html",
            {"page_show_nav": False, "page_footer": ""},
            status=404,
        )
    if page.slug != "home":
        return redirect(page.get_absolute_url())
    return _render_page(request, page)


def page_detail(request, slug):
    _public_enabled_or_404()
    page = get_object_or_404(_published_queryset(), slug=slug)
    return _render_page(request, page)


class CMSLoginView(LoginView):
    template_name = "registration/login.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = (
            Page.objects.filter(slug="login", status=Page.Status.PUBLISHED, is_visible=True)
            .first()
        )
        if page:
            context["page"] = page
            main_html, footer_html = page.render_content_segments(request=self.request)
            context["page_rendered"] = main_html
            context["page_footer"] = footer_html
            if page.show_navigation_bar:
                nav_payload = build_nav_payload(page.custom_nav_items or [])
            else:
                nav_payload = []
            context["public_pages"] = nav_payload
            context["page_show_nav"] = bool(nav_payload)
            context["nav_label"] = page.title
        else:
            context.setdefault("public_pages", [])
            context.setdefault("page_show_nav", False)
            context.setdefault("nav_label", "Login")
            context["page_rendered"] = ""
            context["page_footer"] = ""
        try:
            context["password_reset_url"] = reverse("password_reset")
        except NoReverseMatch:
            context["password_reset_url"] = None
        return context
