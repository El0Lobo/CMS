import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBase
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST

from .forms import PageForm, PagePreviewForm
from .models import Page
from .serializers import serialize_page


@login_required
def index(request):
    pages = (
        Page.objects.all()
        .select_related("created_by", "updated_by")
        .order_by("navigation_order", "title")
    )
    return render(
        request,
        "pages/index.html",
        {
            "pages": pages,
        },
    )


def _handle_form(request, *, instance: Page | None = None):
    if request.method == "POST":
        form = PageForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            page = form.save(commit=False)
            is_new = page.pk is None
            if is_new and not page.created_by:
                page.created_by = request.user
            page.updated_by = request.user
            if page.status == Page.Status.PUBLISHED and not page.published_at:
                page.published_at = timezone.now()
            page.save()
            form.save_m2m()
            messages.success(request, "Page saved.")
            return redirect("pages_edit", slug=page.slug)
    else:
        form = PageForm(instance=instance)
    return form


@login_required
def create(request):
    form_or_response = _handle_form(request)
    if isinstance(form_or_response, HttpResponseBase):
        return form_or_response
    form = form_or_response
    initial_preview = ""
    try:
        initial_preview = form.instance.render_content(request=request)
    except AttributeError:
        initial_preview = ""
    context = {
        "mode": "create",
        "form": form,
        "page": None,
        "preview_url": reverse("pages_preview"),
        "builder_boot": json.dumps(
            {
                "mode": "create",
                "page": serialize_page(form.instance, request),
                "preview_html": initial_preview or "",
                "urls": {
                    "save": reverse("pages_api_create"),
                    "preview": reverse("pages_api_preview_html"),
                    "events": reverse("pages_api_events"),
                    "menu": reverse("pages_api_menu"),
                    "site": reverse("pages_api_site"),
                    "assets": reverse("pages_api_assets"),
                    "detail": None,
                },
            }
        ),
    }
    return render(request, "pages/form.html", context)


@login_required
def edit(request, slug):
    page = get_object_or_404(Page, slug=slug)
    form_or_response = _handle_form(request, instance=page)
    if isinstance(form_or_response, HttpResponseBase):
        # Successful POST will redirect here
        return form_or_response
    form = form_or_response
    initial_preview = page.render_content(request=request)
    context = {
        "mode": "edit",
        "form": form,
        "page": page,
        "preview_url": reverse("pages_preview"),
        "page_rendered": initial_preview,
        "builder_boot": json.dumps(
            {
                "mode": "edit",
                "page": serialize_page(page, request),
                "preview_html": initial_preview or "",
                "urls": {
                    "save": reverse("pages_api_detail", args=[page.slug]),
                    "preview": reverse("pages_api_preview_html"),
                    "events": reverse("pages_api_events"),
                    "menu": reverse("pages_api_menu"),
                    "site": reverse("pages_api_site"),
                    "assets": reverse("pages_api_assets"),
                    "detail": reverse("pages_api_detail", args=[page.slug]),
                },
            }
        ),
    }
    return render(request, "pages/form.html", context)


@login_required
@require_POST
def preview(request):
    """
    Render a live preview of an in-flight page edit in a new tab/window.
    """

    form = PagePreviewForm(request.POST, request.FILES)
    if not form.is_valid():
        return render(
            request,
            "pages/preview_error.html",
            {"form": form},
            status=400,
        )

    page = form.save(commit=False)
    page.pk = None
    page.created_at = page.created_at or timezone.now()
    page.updated_at = timezone.now()
    if page.status == Page.Status.PUBLISHED and not page.published_at:
        page.published_at = timezone.now()
    try:
        if page.hero_image:
            _ = page.hero_image.url
    except Exception:
        page.hero_image = None
    rendered = page.render_content(request=request)

    return render(
        request,
        "public/page_detail.html",
        {
            "page": page,
            "nav_label": page.title,
            "is_preview": True,
            "page_rendered": rendered,
        },
    )
