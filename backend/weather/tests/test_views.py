from unittest.mock import MagicMock, patch

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from weather.models import SearchHistory
from weather.serializers import SearchHistorySerializer


@pytest.fixture 
def api_client():
    return APIClient()

@pytest.fixture
def mock_weather_response():
    return {
        "main": {
            "temp": 20.5,
            "feels_like": 19.8,
            "humidity": 65,
            "pressure": 1012
        },
        "weather": [
            {
                "main": "Clear",
                "description": "clear sky"
            }
        ],
        "wind": {
            "speed": 3.6
        },
        "dt": 1615478576
    }


# WeatherAPIView Tests
@pytest.mark.django_db
class TestWeatherAPIView:
    def test_missing_city_param(self, api_client):
        """Test that API returns 400 when city parameter is missing"""
        url = reverse('weather')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['error'] == 'City parameter is required'

    @patch('weather.views.requests.get')
    def test_successful_weather_fetch(self, mock_get, api_client, mock_weather_response):
        """Test successful weather data retrieval"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_weather_response
        mock_get.return_value = mock_response

        url = reverse('weather')
        response = api_client.get(url, {'city': 'London'})

        assert response.status_code == status.HTTP_200_OK
        assert response.data['city'] == 'London'
        assert response.data['temperature'] == 20.5
        assert response.data['weather'] == 'Clear'
        assert response.data['description'] == 'clear sky'

        assert SearchHistory.objects.filter(city_name='London').exists()
    
    @patch('weather.views.requests.get')
    def test_city_not_found(self, mock_get, api_client):
        """Test handling of city not found error"""
        # Configure mock
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        # Make API request
        url = reverse('weather')
        response = api_client.get(url, {'city': 'NonExistentCity'})
        
        # Assertions
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "not found" in response.data['error']
        
        # Verify search history was NOT saved
        assert not SearchHistory.objects.filter(city_name='NonExistentCity').exists()

    @patch('weather.views.requests.get')
    def test_weather_api_error(self, mock_get, api_client):
        """Test handling of other API errors"""
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        url = reverse('weather')
        response = api_client.get(url, {'city': 'London'})
        assert response.status_code == 500
        assert response.data['error'] == 'Weather API error'


# WeatherHistoryAPIView Tests
@pytest.mark.django_db
class TestWeatherHistoryAPIView:
    
    def test_empty_history(self, api_client):
        """Test fetching empty search history"""
        url = reverse('history')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 0
    
    def test_populated_history(self, api_client):
        """Test fetching populated search history"""
        # Create test search history entries
        cities = ['London', 'Paris', 'New York']
        for city in cities:
            SearchHistory.objects.create(city_name=city)
        
        # Fetch history
        url = reverse('history')
        response = api_client.get(url)
        
        # Assertions
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 3
        
        # Verify response matches serialized data
        history = SearchHistory.objects.all()
        expected_data = SearchHistorySerializer(history, many=True).data
        assert response.data == expected_data