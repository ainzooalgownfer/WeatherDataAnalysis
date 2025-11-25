import pandas as pd
import requests
from datetime import datetime

# Load CSV
df = pd.read_csv("../data/weather_data.csv")

# Spring Boot API endpoint
URL = "http://localhost:8080/api/weather"

for index, row in df.iterrows():
    # Convert datetime to ISO format (2025-11-23T21:00:00)
    dt_iso = datetime.strptime(row['datetime'], "%Y-%m-%d %H:%M:%S").isoformat()

    payload = {
        "datetime": dt_iso,
        "temperature": float(row['temperature']),
        "humidity": float(row['humidity']),
        "windSpeed": float(row['windSpeed']),
        "description": str(row['description'])
    }

    response = requests.post(URL, json=payload)

    if response.status_code in [200, 201]:
        print(f"Row {index} uploaded successfully")
    else:
        print(f"Failed to upload row {index}, status code: {response.status_code}")
        print("Response:", response.text)
