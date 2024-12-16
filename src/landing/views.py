from django.shortcuts import render
from visits.models import PageVisit
import helpers.numbers
from dashboard.views import dashboard_view

# Create your views here.
def landing_page_view(request):
    if request.user.is_authenticated:
        return dashboard_view(request)
    qs = PageVisit.objects.all()
    PageVisit.objects.create(path=request.path)
    page_views_formatted = helpers.numbers.shorten_number(qs.count() * 100_000)
    social_views_formatted = helpers.numbers.shorten_number(qs.count() * 23_000)
    return render(request, 'landing/main.html', {"page_view_count": page_views_formatted, "social_views_count": social_views_formatted})