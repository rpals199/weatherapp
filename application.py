from flask import Flask, render_template, request
import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry

application = Flask(__name__)

# Set up Open-Meteo API client with cache and retry
cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

@application.route('/')
def index():
    return render_template('index.html')

@application.route('/weather', methods=['POST'])
def weather():
    city = request.form.get('city')
    if not city:
        return render_template('index.html', error='City cannot be empty')

    # Make API request to Open-Meteo API
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 52.52,
        "longitude": 13.41,
        "hourly": "temperature_2m"
    }
    responses = openmeteo.weather_api(url, params=params)

    # Process and print the data
    response = responses[0]
    temperature = response.Hourly().Variables(0).ValuesAsNumpy()[0]

    return render_template('weather.html', city=city, temperature=temperature)

if __name__ == '__main__':
    application.run(debug=False)
