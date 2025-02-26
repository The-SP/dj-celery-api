from datetime import timedelta

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
    yesterday = today - timedelta(days=1)
    
    # Get searches from the past 24 hours
    daily_searches = SearchHistory.objects.filter(
        timestamp__date=yesterday
    )
    total_searches = daily_searches.count()
    
    # Get most searched cities (top 5)
    most_searched = (
        daily_searches.values("city_name")
        .annotate(count=Count("city_name"))
        .order_by("-count")[:5]
    )

    # Prepare email
    subject = f"Weather API Statistics for {yesterday.strftime('%Y-%m-%d')}"
    message = f"""
======================================================
🌤️  WEATHER API DAILY STATISTICS REPORT  🌤️
======================================================
Report Date: {yesterday.strftime('%A, %B %d, %Y')}
Total Searches: {total_searches}

🏙️ TOP SEARCHED CITIES
------------------------------------------------------
"""
    if most_searched:
        for city in most_searched:
            message += f"- {city['city_name']}: {city['count']} searches\n"
    else:
        message += "No searches were made yesterday\n"

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[settings.ADMIN_EMAIL],
        fail_silently=False,
    )

    return f"Email sent with statistics for {yesterday}: {total_searches} total searches"
