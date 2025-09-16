from django.urls import path
from .public_views import blog_index
urlpatterns = [path("blog/", blog_index, name="public_blog_index")]
