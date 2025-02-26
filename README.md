# Django Weather API

A RESTful API service built with Django REST Framework that provides weather information for cities using the OpenWeather API. The application tracks search history and includes asynchronous task processing with Celery.

## Features

- Weather data retrieval by city name
- Search history tracking and retrieval
- Rate limiting/throttling
- Scheduled tasks with Celery
- Docker containerization

## Setup Instructions

### Prerequisites

- Python 3.8+
- Redis (for Celery)
- OpenWeather API key

### Local Development Setup

1. Clone the repository:
   ```
   git clone https://github.com/The-SP/dj-celery-api.git
   cd dj-celery-api
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file inside the `backend/` folder, using the provided `.env.sample` as a template

5. Run migrations:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

6. Start the development server:
   ```
   python manage.py runserver
   ```

### Starting Celery

1. In a new terminal, start the Celery worker:
   ```
   celery -A backend worker -l info
   ```

2. In another terminal, start the Celery beat scheduler:
   ```
   celery -A backend beat -l info
   ```

## Docker Setup

1. Make sure Docker and Docker Compose are installed on your system

2. Build and start the containers:
   ```
   docker-compose up --build
   ```

3. The application will be available at http://localhost:8000


## API Documentation

### Endpoints

#### Get Weather Data
- **URL**: `/weather`
- **Method**: `GET`
- **Parameters**: `city` (required) - Name of the city
- **Response**: 
  ```json
  {
    "city": "london",
    "temperature": 7.73,
    "feels_like": 4.69,
    "humidity": 78,
    "pressure": 1010,
    "weather": "Clouds",
    "description": "broken clouds",
    "wind_speed": 5.14,
    "timestamp": 1740590988
  }
  ```
- **Error Response**:
  ```json
  {
    "error": "City not found",
    "status": 404
  }
  ```

#### Get Search History
- **URL**: `/history`
- **Method**: `GET`
- **Parameters**: None
- **Response**:
  ```json
  {
    "searches": [
      {
        "city_name": "London",
        "timestamp": "2025-02-26T12:30:45Z"
      },
      {
        "city_name": "Paris",
        "timestamp": "2025-02-26T12:29:30Z"
      }
    ]
  }
  ```

## Celery Tasks

### Scheduled Tasks
- **Daily Email Report**: Sends a daily summary email to the admin 