import os

import httpx
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "http://api.currencylayer.com/"
API_KEY = os.getenv("PR2_API_KEY")

# список поддерживаемых валют
currency = httpx.request(
    method="GET", url=f"{BASE_URL}/list?access_key={API_KEY}"
).json()["currencies"]

for short, full in currency.items():
    print(short, full)

# Необходимо протестировать API Currency Layer, путём создания запроса
# об исторических курсах валют для 22 февраля 2018 года, для евро, фунтов стер-
# лингов и иен с исходной валютой доллар США.

currency = httpx.request(
    method="GET",
    url=f"{BASE_URL}/historical?access_key={API_KEY}&date=2018-02-22&currencies=EUR, GBP, JPY",
).json()[
    "quotes"
]  # default Source Currency is USD

for currency, price in currency.items():
    print(currency, price)


# Получить исторические данные о курсе евро к доллару США, начиная с
# 25 февраля 2016 по 21 февраля 2017 года.
currency = httpx.request(
    method="GET",
    url=f"{BASE_URL}/timeframe?access_key={API_KEY}&start_date=2016-02-25&end_date=2017-02-21&currencies=EUR",
).json()[
    "quotes"
]  # default Source Currency is USD
for date, info in currency.items():
    print(f"date = {date}, price = {info['USDEUR']}")

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
WEATHER_BASE_URL = "http://api.openweathermap.org/data/2.5"
#
map = httpx.request(
    method="GET",
    url=f"http://api.openweathermap.org/geo/1.0/direct?q=Minsk,BY&appid={WEATHER_API_KEY}",
).json()[0]
lat = map["lat"]
lon = map["lon"]

# {'cod': 401, 'message': 'Invalid API key. Please see https://openweathermap.org/faq#error401 for more info.'}
weather = httpx.request(
    method="GET",
    # url=f"{WEATHER_BASE_URL}/forecast/daily?lat={lat}&lon={lon}&cnt=16&APPID={WEATHER_API_KEY}",
    url=f"{WEATHER_BASE_URL}/forecast?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}&units=metric",
).json()
print(weather)

london = httpx.request(
    method="GET",
    url=f"http://api.openweathermap.org/data/2.5/weather?q=Minsk,by&APPID={WEATHER_API_KEY}",
)
print(london.json())


# OPEN METEO
weather = httpx.request(
    method="GET",
    url="https://api.open-meteo.com/v1/forecast?"
    "latitude=53.9&longitude=27.56&current=temperature_2m&daily=temperature_2m_max,"
    "temperature_2m_min&timezone=Europe%2FMinsk",
).json()["current"]
for info, value in weather.items():
    print(f"{info}: {value}")

coordin = httpx.request(
    method="GET",
    url="https://geocoding-api.open-meteo.com/v1/search",
    params={"name": "Minsk", "count": 1, "language": "ru", "format": "json"},
).json()
latitude = coordin["results"][0]["latitude"]
longitude = coordin["results"][0]["longitude"]
forecast_params = {
    "latitude": latitude,
    "longitude": longitude,
    "daily": [
        "temperature_2m_max",
        "temperature_2m_min",
        "apparent_temperature_max",  # Макс. температура по ощущениям (°C)
        "precipitation_sum",  # Сумма осадков (мм)
        "windspeed_10m_max",  # Макс. скорость ветра (км/ч)
    ],
    "timezone": "auto",
    "forecast_days": 16,
}
forecast = httpx.request(
    method="GET", url="https://api.open-meteo.com/v1/forecast", params=forecast_params
).json()["daily"]


print("Minsk Forecast")
for i in range(16):
    print(f"""date: {forecast['time'][i]},
          temperature_2m_max: {forecast['temperature_2m_max'][i]},
          temperature_2m_min: {forecast['temperature_2m_min'][i]},
          apparent_temperature_max: {forecast['apparent_temperature_max'][i]},
          precipitation_sum: {forecast['precipitation_sum'][i]},
          windspeed_10m_ma: {forecast['windspeed_10m_max'][i]}""")
