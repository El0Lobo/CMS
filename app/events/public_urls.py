from django.urls import path
from .public_views import public_list, public_detail
urlpatterns = [
    path("events/", public_list, name="public_events"),
    path("events/sample-event/", public_detail, name="public_event_detail"),
]
