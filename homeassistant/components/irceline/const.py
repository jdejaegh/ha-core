"""Constants for the IRCEL - CELINE: Air quality Belgium integration."""

from open_irceline import ForecastFeature, RioFeature, RioIfdmFeature

from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.const import CONCENTRATION_MICROGRAMS_PER_CUBIC_METER, Platform

DOMAIN = "irceline"
PLATFORMS: list[Platform] = [Platform.SENSOR]

IRCEL_CELINE = "Belgian Interregional Environment Agency (IRCEL - CELINE)"
ATTRIBUTION = f"Air quality data from the {IRCEL_CELINE}"

RIO_HOURLY_POLLUTANT = {"current_bc_hmean"}

RIO_IFDM_HOURLY_POLLUTANT = {
    "current_belaqi",
    "current_no2_hmean",
    "current_o3_hmean",
    "current_pm10_hmean",
    "current_pm25_hmean",
}

FORECAST_POLLUTANT = {
    "forecast_belaqi",
    "forecast_no2_dmean",
    "forecast_no2_maxhmean",
    "forecast_o3_maxhmean",
    "forecast_pm10_dmean",
    "forecast_pm25_dmean",
}

# noinspection DuplicatedCode
POLLUTANT_TO_FEATURE = {
    "current_bc_hmean": RioFeature.BC_HMEAN,
    "current_belaqi": RioIfdmFeature.BELAQI,
    "current_no2_hmean": RioIfdmFeature.NO2_HMEAN,
    "current_o3_hmean": RioIfdmFeature.O3_HMEAN,
    "current_pm10_hmean": RioIfdmFeature.PM10_HMEAN,
    "current_pm25_hmean": RioIfdmFeature.PM25_HMEAN,
    "forecast_belaqi": ForecastFeature.BELAQI,
    "forecast_no2_dmean": ForecastFeature.NO2_DMEAN,
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
    "current_bc_hmean": None,
    "current_belaqi": SensorDeviceClass.AQI,  # Not really AQI but close: the scale is 1-10
    "current_no2_hmean": SensorDeviceClass.NITROGEN_DIOXIDE,
    "current_o3_hmean": SensorDeviceClass.OZONE,
    "current_pm10_hmean": SensorDeviceClass.PM10,
    "current_pm25_hmean": SensorDeviceClass.PM25,
    "forecast_belaqi": SensorDeviceClass.AQI,  # Not really AQI but close: the scale is 1-10
    "forecast_no2_dmean": SensorDeviceClass.NITROGEN_DIOXIDE,
    "forecast_no2_maxhmean": SensorDeviceClass.NITROGEN_DIOXIDE,
    "forecast_o3_maxhmean": SensorDeviceClass.OZONE,
    "forecast_pm10_dmean": SensorDeviceClass.PM10,
    "forecast_pm25_dmean": SensorDeviceClass.PM25,
}

POLLUTANT_TO_UNIT = {
    "current_bc_hmean": CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    "current_belaqi": None,
    "current_no2_hmean": CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    "current_o3_hmean": CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    "current_pm10_hmean": CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    "current_pm25_hmean": CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    "forecast_belaqi": None,
    "forecast_no2_dmean": CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    "forecast_no2_maxhmean": CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    "forecast_o3_maxhmean": CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    "forecast_pm10_dmean": CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    "forecast_pm25_dmean": CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
}
