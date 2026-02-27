import httpx
from fastapi import APIRouter, HTTPException

from ..schemas import WeatherResponse

router = APIRouter(prefix="/api/weather", tags=["weather"])

OPEN_METEO = "https://api.open-meteo.com/v1/forecast"


@router.get("", response_model=WeatherResponse)
async def get_weather(lat: float | None = None, lon: float | None = None, city: str = "London"):
    params = {
        "latitude": lat or 51.5074,
        "longitude": lon or -0.1278,
        "current": "temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m,apparent_temperature",
    }
    if lat is None and lon is None:
        geo = await _geocode(city)
        if geo:
            params["latitude"] = geo["lat"]
            params["longitude"] = geo["lon"]

    async with httpx.AsyncClient() as client:
        r = await client.get(OPEN_METEO, params=params, timeout=10.0)
    if r.status_code != 200:
        raise HTTPException(502, "Weather service unavailable")

    data = r.json()
    curr = data.get("current", {})
    code = curr.get("weather_code", 0)
    desc, icon = _wmo_code(code)

    return WeatherResponse(
        temp=curr.get("temperature_2m", 0),
        feels_like=curr.get("apparent_temperature", 0),
        description=desc,
        icon=icon,
        humidity=int(curr.get("relative_humidity_2m", 0)),
        wind_speed=curr.get("wind_speed_10m", 0),
        city=city,
    )


async def _geocode(city: str) -> dict | None:
    url = "https://geocoding-api.open-meteo.com/v1/search"
    async with httpx.AsyncClient() as client:
        r = await client.get(url, params={"name": city, "count": 1}, timeout=5.0)
    if r.status_code != 200:
        return None
    data = r.json()
    results = data.get("results", [])
    if not results:
        return None
    return {"lat": results[0]["latitude"], "lon": results[0]["longitude"]}


def _wmo_code(code: int) -> tuple[str, str]:
    mapping = {
        0: ("Clear", "01d"),
        1: ("Mainly clear", "01d"),
        2: ("Partly cloudy", "02d"),
        3: ("Overcast", "04d"),
        45: ("Foggy", "50d"),
        48: ("Depositing rime fog", "50d"),
        51: ("Light drizzle", "09d"),
        61: ("Slight rain", "10d"),
        63: ("Moderate rain", "10d"),
        71: ("Slight snow", "13d"),
        80: ("Slight rain showers", "09d"),
        95: ("Thunderstorm", "11d"),
    }
    for k, v in sorted(mapping.items(), reverse=True):
        if code >= k:
            return v
    return ("Unknown", "01d")
