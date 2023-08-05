"""Helper Class for Weatherflow Rest module."""
from __future__ import annotations

import datetime as dt
import logging
import re

from pyweatherbitdata.const import CONDITION_CLASSES, UNIT_TYPE_METRIC
from pyweatherbitdata.data import BeaufortDescription

UTC = dt.timezone.utc

_LOGGER = logging.getLogger(__name__)

class Conversions:
    """Conversion functions."""

    def __init__(self, units: str, homeassistant: bool) -> None:
        """Initialize class."""
        self.units = units
        self.homeassistant = homeassistant

    def temperature(self, value) -> float:
        """Return celcius to Fahrenheit."""
        if value is None or self.units == UNIT_TYPE_METRIC or self.homeassistant:
            return value
        return round(value * 1.8 + 32, 1)

    def pressure(self, value, no_convert: bool = False) -> float:
        """Return inHg from mb/hPa."""
        if value is None:
            return None
        if no_convert or self.units == UNIT_TYPE_METRIC:
            return value
        return round(value * 0.029530, 3)

    def rain(self, value) -> float:
        """Convert rain units."""
        if value is None:
            return None

        if self.units == UNIT_TYPE_METRIC:
            return round(value, 2)
        return round(value * 0.03937007874, 2)

    def density(self, value) -> float:
        """Convert air density."""
        if value is None:
            return None

        if self.units == UNIT_TYPE_METRIC:
            return round(value, 1)

        return round(value * 0.06243, 1)

    def distance(self, value) -> float:
        """Convert km to mi."""
        if value is None:
            return None

        if self.units == UNIT_TYPE_METRIC:
            return round(value, 1)

        return round(value * 0.6213688756, 1)

    def windspeed(self, value) -> float:
        """Return miles per hour from m/s."""
        if value is None:
            return value

        if self.units == UNIT_TYPE_METRIC:
            return round(value, 1)

        return round(value * 2.236936292, 1)

    def windspeed_knots(self, wind_speed) -> float:
        """Return m/s to knots."""
        if wind_speed is None:
            return None
        return round(wind_speed * 1.943844, 1)

    def windspeed_kmh(self, value: float) -> float:
        """Return km/h from m/s."""
        if value is None:
            return value

        return round(value * 3.6, 1)

    def utc_from_timestamp(self, timestamp: int) -> dt.datetime:
        """Return a UTC time from a timestamp."""
        return dt.datetime.utcfromtimestamp(timestamp).replace(tzinfo=UTC)

    def utc_from_datestring(self, datestring: str) -> dt.datetime:
        """Return a UTC time from a date string."""
        date_obj = dt.datetime.strptime(f"{datestring} 00:00", "%Y-%m-%d %H:%M")
        dt_obj = date_obj.astimezone(UTC)
        return dt_obj.strftime("%Y-%m-%dT%H:%M:%S+00:00")

    def utc_from_datetimestring(self, datestring: str) -> dt.datetime:
        """Return a UTC time from a datetime string."""
        date_obj = dt.datetime.strptime(f"{datestring}", "%Y-%m-%d %H:%M")
        return date_obj.astimezone(UTC)

    def alert_descriptions(self, alert_text: str):
        """Return alert description in English and Local language."""
        if alert_text is None:
            return None

        try:
            desc_split = alert_text.split("\n")
            if desc_split[0][:7] == "English":
                loc_alert = self.trim_alert_text(desc_split[1])
                en_alert = self.trim_alert_text(desc_split[0])
            else:
                loc_alert = self.trim_alert_text(desc_split[0])
                en_alert = self.trim_alert_text(desc_split[1])

            return en_alert, loc_alert
        except Exception as e:
            _LOGGER.error("An error occured splitting alert message. Error message is %s", str(e))
            return None, None

    def trim_alert_text(self, alert: str) -> str:
        """Return a trimmed version of the ALert Text."""
        index = alert.find(":")
        return alert[index + 2:]

    def condition_from_code(self, weather_code: int, is_night: bool = False, alt_condition: bool = False) -> str:
        """Return a Home Assistant weather condition from code."""
        if weather_code is None:
            return None
        wcode = int(weather_code)
        night_codes = [800, 801, 802] if alt_condition else [800]
        if is_night and wcode in night_codes:
            wcode = wcode * 10
        return next(
            (k for k, v in CONDITION_CLASSES.items() if wcode in v),
            None,
        )

class Calculations:
    """Calculate entity values."""

    def is_raining(self, rain):
        """Return true if it is raining."""
        if rain is None:
            return None

        rain_rate = rain * 60
        return rain_rate > 0

    def is_freezing(self, temperature):
        """Return true if temperature below 0."""
        if temperature is None:
            return None

        return temperature < 0

    def uv_description(self, uv: float) -> str:
        """Return a Description based on uv value."""
        if uv is None:
            return None

        if uv >= 10.5:
            return "extreme"
        if uv >= 7.5:
            return "very-high"
        if uv >= 5.5:
            return "high"
        if uv >= 2.5:
            return "moderate"
        if uv > 0:
            return "low"

        return "none"

    def wind_direction(self, wind_bearing: int) -> str:
        """Return Wind Directions String from Wind Bearing."""
        if wind_bearing is None:
            return None

        direction_array = [
            "n",
            "nne",
            "ne",
            "ene",
            "e",
            "ese",
            "se",
            "sse",
            "s",
            "ssw",
            "sw",
            "wsw",
            "w",
            "wnw",
            "nw",
            "nnw",
            "n",
        ]
        return direction_array[int((wind_bearing + 11.25) / 22.5)]

    def beaufort(self, wind_speed: float) -> BeaufortDescription:
        """Return Beaufort Value and Description."""
        mapping_text = {
            "32.7": [12, "hurricane"],
            "28.5": [11, "violent_storm"],
            "24.5": [10, "storm"],
            "20.8": [9, "strong_gale"],
            "17.2": [8, "fresh_gale"],
            "13.9": [7, "moderate_gale"],
            "10.8": [6, "strong_breeze"],
            "8.0": [5, "fresh_breeze"],
            "5.5": [4, "moderate_breeze"],
            "3.4": [3, "gentle_breeze"],
            "1.6": [2, "light_breeze"],
            "0.3": [1, "light_air"],
            "-1": [0, "calm"],
        }
        for k, v in mapping_text.items():
            if wind_speed > float(k):
                return BeaufortDescription(value=v[0], description=v[1])
        return None

    def aqi_level(self, aqi_index: int) -> str:
        """Return AQI Level from Index."""
        if aqi_index is None:
            return None

        if aqi_index > 300:
            return "Hazardous"
        elif aqi_index > 200:
            return "Very Unhealthy"
        elif aqi_index > 150:
            return "Unhealthy"
        elif aqi_index > 100:
            return "Unhealthy for Sensitive Groups"
        elif aqi_index > 50:
            return "Moderate"
        else:
            return "Good"
