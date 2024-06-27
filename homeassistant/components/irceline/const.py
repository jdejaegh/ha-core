"""Constants for the IRCEL - CELINE: Air quality Belgium integration."""

from open_irceline import ForecastFeature, RioFeature

from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.const import CONCENTRATION_MICROGRAMS_PER_CUBIC_METER, Platform

DOMAIN = "irceline"
PLATFORMS: list[Platform] = [Platform.SENSOR]

IRCEL_CELINE = "Belgian Interregional Environment Agency (IRCEL - CELINE)"
ATTRIBUTION = f"Air quality data from the {IRCEL_CELINE}"

RIO_HOURLY_POLLUTANT = {
    "current_bc_24hmean",
    "current_bc_hmean",
    "current_no2_hmean",
    "current_o3_hmean",
    "current_pm10_24hmean",
    "current_pm10_hmean",
    "current_pm25_24hmean",
    "current_pm25_hmean",
}

FORECAST_POLLUTANT = {
    "forecast_no2_maxhmean",
    "forecast_o3_maxhmean",
    "forecast_pm10_dmean",
    "forecast_pm25_dmean",
}

# noinspection DuplicatedCode
POLLUTANT_TO_FEATURE = {
    "current_bc_24hmean": RioFeature.BC_24HMEAN,
    "current_bc_hmean": RioFeature.BC_HMEAN,
    "current_no2_hmean": RioFeature.NO2_HMEAN,
    "current_o3_hmean": RioFeature.O3_HMEAN,
    "current_pm10_24hmean": RioFeature.PM10_24HMEAN,
    "current_pm10_hmean": RioFeature.PM10_HMEAN,
    "current_pm25_24hmean": RioFeature.PM25_24HMEAN,
    "current_pm25_hmean": RioFeature.PM25_HMEAN,
    "forecast_no2_maxhmean": ForecastFeature.NO2_MAXHMEAN,
    "forecast_o3_maxhmean": ForecastFeature.O3_MAXHMEAN,
    "forecast_pm10_dmean": ForecastFeature.PM10_DMEAN,
    "forecast_pm25_dmean": ForecastFeature.PM25_DMEAN,
}


# noinspection DuplicatedCode
POLLUTANT_TO_SENSOR_DEVICE_CLASS = {
    # Have to put None for the classes that are not available in SensorDeviceClass, else mypy linter complains when
    # setting _attr_device_class in sensor __init__:
    # > error: Incompatible types in assignment (expression has type "StrEnum", variable has type
    # "SensorDeviceClass | None")  [assignment]
    "current_bc_24hmean": None,
    "current_bc_hmean": None,
    "current_no2_hmean": SensorDeviceClass.NITROGEN_DIOXIDE,
    "current_o3_hmean": SensorDeviceClass.OZONE,
    "current_pm10_24hmean": SensorDeviceClass.PM10,
    "current_pm10_hmean": SensorDeviceClass.PM10,
    "current_pm25_24hmean": SensorDeviceClass.PM25,
    "current_pm25_hmean": SensorDeviceClass.PM25,
    "forecast_no2_maxhmean": SensorDeviceClass.NITROGEN_DIOXIDE,
    "forecast_o3_maxhmean": SensorDeviceClass.OZONE,
    "forecast_pm10_dmean": SensorDeviceClass.PM10,
    "forecast_pm25_dmean": SensorDeviceClass.PM25,
}

POLLUTANT_TO_UNIT = {
    "current_bc_24hmean": CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    "current_bc_hmean": CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    "current_no2_hmean": CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    "current_o3_hmean": CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    "current_pm10_24hmean": CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    "current_pm10_hmean": CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    "current_pm25_24hmean": CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    "current_pm25_hmean": CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    "forecast_no2_maxhmean": CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    "forecast_o3_maxhmean": CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    "forecast_pm10_dmean": CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    "forecast_pm25_dmean": CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
}
