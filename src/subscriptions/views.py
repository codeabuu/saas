from django.shortcuts import render
from subscriptions.models import SubscriptionPrice
# Create your views here.

def subscription_price_view(request):
    qs = SubscriptionPrice.objects.filter(featured=True)
    monthly_qs = qs.filter(interval = SubscriptionPrice.IntervalChoices.MONTHLY)
    yearly_qs = qs.filter(interval = SubscriptionPrice.IntervalChoices.YEARLY)
    return render(request, "subscriptions/pricing.html", {
        "monthly_qs": monthly_qs,
        "yearly_qs": yearly_qs
    })
