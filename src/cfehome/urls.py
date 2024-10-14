from django.contrib import admin
from django.urls import path
from .views import home_page_view 

urlpatterns = [
    path("onme/", home_page_view),
    path('admin/', admin.site.urls),
]
