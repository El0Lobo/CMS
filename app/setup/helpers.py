from .models import SiteSettings, VisibilityRule

def get_settings():
    return SiteSettings.get_solo()

def is_allowed(user, key: str) -> bool:
    try:
        rule = VisibilityRule.objects.get(key=key, is_enabled=True)
    except VisibilityRule.DoesNotExist:
        return True  # no rule means visible
    if user.is_superuser:
        return True
    if not rule.allowed_groups.exists():
        return False
    return rule.allowed_groups.filter(id__in=user.groups.values_list("id", flat=True)).exists()
