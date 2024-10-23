from django.contrib import admin
from django.urls import path, include
from .views import home_view, about_view
from auth import views as auth_views

urlpatterns = [
    path("", home_view, name='home'), #index page -> root page
    path("login/", auth_views.login_view, name='account_login'),
    path("register/", auth_views.register_view, name='account_signup'),
    path("about/", about_view),
    path("hello-world/", home_view),
    path("hello-world.html", home_view),
    path('accounts/', include('allauth.urls')),
    path("admin/", admin.site.urls),
]
