import requests
import pandas as pd
from datetime import datetime

# OpenWeatherMap API key and city
API_KEY = "bb89c8b567dbee10c4be18d77d05fe03"
CITY = "Paris"
URL = f"http://api.openweathermap.org/data/2.5/forecast?q={CITY}&appid={API_KEY}&units=metric"

response = requests.get(URL)
data = response.json()

print(data)

weather_list = []

for item in data['list']:
    weather_list.append({
        "city": CITY,
        "datetime": item['dt_txt'],
        "temperature": item['main']['temp'],    
        "humidity": item['main']['humidity'],
        "windSpeed": item['wind']['speed'],
        "description": item['weather'][0]['description']
    })


# Save CSV locally
df = pd.DataFrame(weather_list)
df.to_csv("../data/weather_data.csv", index=False)
print("Weather data collected and saved to data/weather_data.csv")
