"""Constants for the IRCEL - CELINE: Air quality Belgium integration."""

from open_irceline import RioFeature

from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.const import CONCENTRATION_MICROGRAMS_PER_CUBIC_METER

DOMAIN = "irceline"
IRCEL_CELINE = "Belgian Interregional Environment Agency (IRCEL - CELINE)"
ATTRIBUTION = f"Air quality data from the {IRCEL_CELINE}"

RIO_HOURLY_POLLUTANT = {"current_no2_hmean", "current_pm25_hmean", "current_o3_hmean"}

POLLUTANT_TO_FEATURE = {
    "current_no2_hmean": RioFeature.NO2_HMEAN,
    "current_pm25_hmean": RioFeature.PM25_HMEAN,
    "current_o3_hmean": RioFeature.O3_HMEAN,
}

POLLUTANT_TO_SENSOR_DEVICE_CLASS = {
    "current_no2_hmean": SensorDeviceClass.NITROGEN_DIOXIDE,
    "current_pm25_hmean": SensorDeviceClass.PM25,
    "current_o3_hmean": SensorDeviceClass.OZONE,
}

POLLUTANT_TO_UNIT = {
    "current_no2_hmean": CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    "current_pm25_hmean": CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    "current_o3_hmean": CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
}
