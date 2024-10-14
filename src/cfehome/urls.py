from django.contrib import admin
from django.urls import path
from .views import home_view, about_view

urlpatterns = [
    path("", home_view), #index page -> root page
    path("about/", about_view),
    path("hello-world/", home_view),
    path("hello-world.html", home_view),
    path("admin/", admin.site.urls),
]
