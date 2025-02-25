import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import SearchHistory
from .serializers import SearchHistorySerializer
from django.conf import settings


class WeatherAPIView(APIView):
    """
    API view to fetch weather data for a specified city
    """

    def get(self, request):
        # Get city from query parameter
        city = request.query_params.get("city")
        if not city:
            return Response(
                {"error": "City parameter is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Fetch weather data with error handling
        try:
            # OpenWeather API URL and params
            url = "https://api.openweathermap.org/data/2.5/weather"
            params = {
                "q": city,
                "appid": settings.OPENWEATHER_API_KEY,
                "units": "metric",  # For Celsius temperature
            }
            response = requests.get(url, params=params)
            if response.status_code == 200:
                weather_data = response.json()
                result = {
                    "city": city,
                    "temperature": weather_data["main"]["temp"],
                    "feels_like": weather_data["main"]["feels_like"],
                    "humidity": weather_data["main"]["humidity"],
                    "pressure": weather_data["main"]["pressure"],
                    "weather": weather_data["weather"][0]["main"],
                    "description": weather_data["weather"][0]["description"],
                    "wind_speed": weather_data["wind"]["speed"],
                    "timestamp": weather_data["dt"],
                }
                # Save successful search to history
                SearchHistory.objects.create(city_name=city)
                return Response(result, status=status.HTTP_200_OK)
            elif response.status_code == 404:
                return Response(
                    {"error": f"City '{city}' not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            else:
                return Response(
                    {"error": "Weather API error"}, status=response.status_code
                )
        except requests.exceptions.RequestException as e:
            return Response(
                {"error": f"Failed to connect to weather service: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class WeatherHistoryAPIView(APIView):
    """
    API view to get history of weather searches
    """
    def get(self, request):
        # Retrieve all search history, ordered by most recent first
        history = SearchHistory.objects.all()
        serializer = SearchHistorySerializer(history, many=True)
        return Response(serializer.data)
