from pydantic import BaseModel


class ForecastPeriodOut(BaseModel):
    name: str                              # "Tonight", "Friday", "Friday Night"
    temperature: int                       # 72
    temperature_unit: str                  # "F"
    wind_speed: str                        # "10 to 15 mph"
    wind_direction: str                    # "NW"
    short_forecast: str                    # "Mostly Sunny"
    detailed_forecast: str                 # Full description
    is_daytime: bool
    start_time: str
    end_time: str
    icon: str                              # NWS icon URL
    precipitation_chance: int | None = None
