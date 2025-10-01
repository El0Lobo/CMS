from django.contrib import admin

from app.events.models import Event, EventCategory, EventPerformer


class EventPerformerInline(admin.TabularInline):
    model = EventPerformer
    extra = 0
    autocomplete_fields = ["band"]


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ["title", "starts_at", "status", "requires_shifts", "featured"]
    list_filter = ["status", "requires_shifts", "featured", "categories"]
    search_fields = ["title", "teaser"]
    inlines = [EventPerformerInline]
    filter_horizontal = ["categories"]
    autocomplete_fields = ["created_by", "updated_by"]
    prepopulated_fields = {"slug": ("title",)}


@admin.register(EventCategory)
class EventCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "is_active"]
    search_fields = ["name", "slug"]
