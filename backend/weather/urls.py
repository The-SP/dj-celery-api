from django.urls import path
from .views import WeatherAPIView, WeatherHistoryAPIView

urlpatterns = [
    path("weather/", WeatherAPIView.as_view(), name="weather"),
    path("history/", WeatherHistoryAPIView.as_view(), name="history"),
]
