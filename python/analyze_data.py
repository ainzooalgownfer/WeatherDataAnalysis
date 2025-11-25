import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# ------------------------------
# 1️ Load CSV
# ------------------------------
csv_path = Path(__file__).parent.parent / "data" / "weather_data.csv"
df = pd.read_csv(csv_path)

# Convert datetime column
df['datetime'] = pd.to_datetime(df['datetime'])
df['date'] = df['datetime'].dt.date  # extract date for daily aggregation

# ------------------------------
# 2️ Basic Statistics
# ------------------------------
print("=== Basic Statistics ===")
print(df.describe(), "\n")

print("Max temperature:", df['temperature'].max())
print("Min temperature:", df['temperature'].min())
print("Average humidity:", df['humidity'].mean())
print("Weather type counts:\n", df['description'].value_counts(), "\n")

# ------------------------------
# 3️ Daily Aggregations
# ------------------------------
daily_avg_temp = df.groupby('date')['temperature'].mean()
daily_max_wind = df.groupby('date')['windSpeed'].max()

print("Daily average temperature:\n", daily_avg_temp, "\n")
print("Daily maximum wind speed:\n", daily_max_wind, "\n")

# ------------------------------
# 4️ Correlation Analysis
# ------------------------------
numeric_df = df[['temperature', 'humidity', 'windSpeed']]  # only numeric columns
print("Correlation between numeric variables:\n", numeric_df.corr(), "\n")

plt.figure(figsize=(6,4))
sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm')
plt.title("Correlation between Variables")
plt.show()

# ------------------------------
# 5️  Temperature Trend Plot
# ------------------------------
plt.figure(figsize=(10,5))
plt.plot(df['datetime'], df['temperature'], marker='o', label='Temperature')
plt.title("Temperature over Time")
plt.xlabel("Datetime")
plt.ylabel("Temperature (°C)")
plt.grid(True)
plt.legend()
plt.show()

# ------------------------------
# 6️  Humidity Trend Plot
# ------------------------------
plt.figure(figsize=(10,5))
plt.plot(df['datetime'], df['humidity'], marker='x', color='purple', label='Humidity')
plt.title("Humidity over Time")
plt.xlabel("Datetime")
plt.ylabel("Humidity (%)")
plt.grid(True)
plt.legend()
plt.show()

# ------------------------------
# 7️  Wind Speed Trend Plot
# ------------------------------
plt.figure(figsize=(10,5))
plt.plot(df['datetime'], df['windSpeed'], marker='s', color='green', label='Wind Speed')
plt.title("Wind Speed over Time")
plt.xlabel("Datetime")
plt.ylabel("Wind Speed (m/s)")
plt.grid(True)
plt.legend()
plt.show()

# ------------------------------
# 8️  Weather Type Frequency
# ------------------------------
plt.figure(figsize=(8,4))
sns.countplot(x='description', data=df)
plt.xticks(rotation=45)
plt.title("Frequency of Weather Types")
plt.show()

# ------------------------------
# 9️ clee Rainy Hours
# ------------------------------
rain_hours = df[df['description'].str.contains('rain')]
print("Number of hours with rain:", len(rain_hours))
print(rain_hours[['datetime', 'temperature', 'humidity', 'windSpeed', 'description']])
