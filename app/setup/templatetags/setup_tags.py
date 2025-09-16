# app/setup/templatetags/setup_tags.py
from django import template
from django.urls import reverse
from django.contrib.auth.models import Group
from django.utils.safestring import mark_safe
from app.setup.helpers import is_allowed, get_settings

register = template.Library()

@register.simple_tag(takes_context=True)
def visibility_cog(context, key, label=""):
    request = context.get("request")
    if not request or not request.user.is_superuser:
        return ""
    has_groups = Group.objects.exists()
    if not has_groups:
        link = reverse("setup:setup") + "#roles"
        html = f'<a class="cfg-cog muted" href="{link}" title="Define roles first">⚙️</a>'
        return mark_safe(html)
    url = reverse("setup:visibility_edit") + f"?key={key}&label={label}"
    html = f'<a class="cfg-cog" href="{url}" title="Visibility for {key}">⚙️</a>'
    return mark_safe(html)

@register.simple_tag(takes_context=True)
def visibility_cog_inline(context, key, label=""):
    """
    Inline <span> version that’s safe to place inside <a>...</a>
    """
    request = context.get("request")
    if not request or not request.user.is_superuser:
        return ""
    has_groups = Group.objects.exists()
    if not has_groups:
        link = reverse("setup:setup") + "#roles"
        html = f'<span class="cfg-cog muted" title="Define roles first" onclick="location.href=\'{link}\'">⚙️</span>'
        return mark_safe(html)
    url = reverse("setup:visibility_edit") + f"?key={key}&label={label}"
    html = (
        f'<span class="cfg-cog" title="Visibility for {key}" '
        f'role="link" tabindex="0" '
        f'onclick="location.href=\'{url}\'" '
        f'onkeydown="if(event.key===\"Enter\")location.href=\'{url}\'">⚙️</span>'
    )
    return mark_safe(html)

@register.filter
def allow_for(user, key):
    return is_allowed(user, key)

@register.simple_tag
def site_settings():
    return get_settings()

@register.simple_tag(takes_context=True)
def visibility_cog_inline(context, key, label=""):
    from django.urls import reverse
    from django.contrib.auth.models import Group
    from django.utils.safestring import mark_safe

    request = context.get("request")
    if not request or not request.user.is_superuser:
        return ""
    if not Group.objects.exists():
        link = reverse("setup:setup") + "#roles"
        html = (
            f'<span class="cfg-cog muted" title="Define roles first" '
            f'role="button" tabindex="0" onclick="window.location.href=\'{link}\'">⚙️</span>'
        )
        return mark_safe(html)

    url = reverse("setup:visibility_picker")
    # NOTE: hx-target is the closest .nav-inline; hx-swap appends inside that container
    html = (
        f'<span class="cfg-cog" title="Visibility for {key}" '
        f'role="button" tabindex="0" '
        f'hx-get="{url}?key={key}&label={label}" '
        f'hx-trigger="click consume" '
        f'hx-target="closest .nav-inline" '
        f'hx-swap="beforeend">⚙️</span>'
    )
    return mark_safe(html)
@register.filter
def allow_for(user, key):
    return is_allowed(user, key)

@register.simple_tag
def site_settings():
    return get_settings()