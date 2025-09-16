from django.urls import path
from .views import dashboard, account
urlpatterns = [
    path("dashboard/", dashboard, name="dashboard"),
    path("account/", account, name="account"),
]
