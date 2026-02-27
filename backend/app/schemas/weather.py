from pydantic import BaseModel


class WeatherResponse(BaseModel):
    temp: float
    feels_like: float
    description: str
    icon: str
    humidity: int
    wind_speed: float
    city: str
