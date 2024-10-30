from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("<username>/", views.profile_detail_view),
    path("", views.profile_list_view),
]
