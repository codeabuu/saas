from django.contrib import admin
from django.urls import path, include
from .views import home_view, about_view, pw_protected_view, user_only_view, staff_only_view
from auth import views as auth_views
from subscriptions import views as subscription_views
from checkouts import views as checkout_views

urlpatterns = [
    path("", home_view, name='home'), #index page -> root page
    # path("login/", auth_views.login_view, name='account_login'),
    # path("register/", auth_views.register_view, name='account_signup'),
    path("checkout/sub-price/<int:price_id>/", checkout_views.product_price_redirect_view,
         name="sub-price-checkout"),
    path("checkout/start", checkout_views.checkout_redirect_view,
         name='stripe-checkout-start'),
    path("checkout/success", checkout_views.checkout_finalize_view,
         name="stripe-checkout-end"),
    path("pricing", subscription_views.subscription_price_view, name='pricing'),
    path("pricing/<str:interval>", subscription_views.subscription_price_view, name='pricing_interval'),
    path("about/", about_view),
    path("hello-world/", home_view),
    path("hello-world.html", home_view),
    path('accounts/billing', subscription_views.user_subscription_view, name='user_subscription'),
    path('accounts/billing/cancel', subscription_views.user_subscription_cancel_view, name='user_subscription_cancel'),
    path('accounts/', include('allauth.urls')),
    path('protected/', pw_protected_view),
    path('protected/user-only', user_only_view),
    path('protected/staff-only', staff_only_view),
    path("profiles/", include('profiles.urls')),
    path("admin/", admin.site.urls),
]
