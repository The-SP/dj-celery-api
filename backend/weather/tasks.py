from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Count
from django.utils import timezone

from .models import SearchHistory


@shared_task
def send_daily_stats_email():
    """
    Sends an email with daily weather search statistics to admin
    """
    today = timezone.now().date()
    search_history = SearchHistory.objects.all()
    total_searches = search_history.count()
    # Get most searched cities (top 5)
    most_searched = (
        search_history.values("city_name")
        .annotate(count=Count("city_name"))
        .order_by("-count")[:5]
    )

    # Prepare email
    subject = f"Weather API Statistics for {today.strftime('%Y-%m-%d')}"
    message = f"""
        Daily Weather API Statistics:

        Date: {today.strftime('%Y-%m-%d')}
        Total Searches: {total_searches}
        
        Top Most Searched Cities:
    """
    for city in most_searched:
        message += f"- {city['city_name']}: {city['count']} searches \n"

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[settings.ADMIN_EMAIL],
        fail_silently=False,
    )

    return f"Email sent with {total_searches} searches for {today}"