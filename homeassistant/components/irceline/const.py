"""Constants for the IRCEL - CELINE: Air quality Belgium integration."""

from enum import StrEnum

from open_irceline import RioFeature

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

POLLUTANT_TO_FEATURE = {
    "current_bc_24hmean": RioFeature.BC_24HMEAN,
    "current_bc_hmean": RioFeature.BC_HMEAN,
    "current_no2_hmean": RioFeature.NO2_HMEAN,
    "current_o3_hmean": RioFeature.O3_HMEAN,
    "current_pm10_24hmean": RioFeature.PM10_24HMEAN,
    "current_pm10_hmean": RioFeature.PM10_HMEAN,
    "current_pm25_24hmean": RioFeature.PM25_24HMEAN,
    "current_pm25_hmean": RioFeature.PM25_HMEAN,
}


class IrcelineSensorDeviceClass(StrEnum):
    """Enum extending SensorDeviceClass to include some values that are needed for this integration."""

    BC = "black_carbon"


POLLUTANT_TO_SENSOR_DEVICE_CLASS = {
    "current_bc_24hmean": IrcelineSensorDeviceClass.BC,
    "current_bc_hmean": IrcelineSensorDeviceClass.BC,
    "current_no2_hmean": SensorDeviceClass.NITROGEN_DIOXIDE,
    "current_o3_hmean": SensorDeviceClass.OZONE,
    "current_pm10_24hmean": SensorDeviceClass.PM10,
    "current_pm10_hmean": SensorDeviceClass.PM10,
    "current_pm25_24hmean": SensorDeviceClass.PM25,
    "current_pm25_hmean": SensorDeviceClass.PM25,
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
}
