"""Test over the constants of irceline integration."""

from homeassistant.components.irceline.const import (
    POLLUTANT_TO_FEATURE,
    POLLUTANT_TO_SENSOR_DEVICE_CLASS,
    POLLUTANT_TO_UNIT,
    RIO_HOURLY_POLLUTANT,
    IrcelineSensorDeviceClass,
)
from homeassistant.components.sensor import SensorDeviceClass


def test_consistency_const():
    """Test that all the POLLUTANT are also in the map structure of the constants."""

    for pollutant in RIO_HOURLY_POLLUTANT:
        assert pollutant in POLLUTANT_TO_FEATURE
        assert pollutant in POLLUTANT_TO_SENSOR_DEVICE_CLASS
        assert pollutant in POLLUTANT_TO_UNIT


def test_ensure_non_colliding_enums():
    """Test that the values in SensorDeviceClass and IrcelineSensorDeviceClass are all different to avoid clashes."""
    device_class_irceline = {str(v) for v in IrcelineSensorDeviceClass}
    device_class_builtin = {str(v) for v in SensorDeviceClass}

    assert not device_class_builtin.intersection(device_class_irceline)
