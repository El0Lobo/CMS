from django.contrib import admin
from .models import SiteSettings, MembershipTier, OpeningHour, VisibilityRule

class TierInline(admin.TabularInline):
    model = MembershipTier
    extra = 1

class HourInline(admin.TabularInline):
    model = OpeningHour
    extra = 0
    max_num = 7
    can_delete = False

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    inlines = [TierInline, HourInline]
    list_display = ("mode","org_name","membership_enabled","default_currency","updated_at")

@admin.register(VisibilityRule)
class VisibilityRuleAdmin(admin.ModelAdmin):
    list_display = ("key","label","is_enabled")
    list_filter = ("is_enabled",)
    filter_horizontal = ("allowed_groups",)
