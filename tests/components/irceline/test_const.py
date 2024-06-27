"""Test over the constants of irceline integration."""

from homeassistant.components.irceline.const import (
    POLLUTANT_TO_FEATURE,
    POLLUTANT_TO_SENSOR_DEVICE_CLASS,
    POLLUTANT_TO_UNIT,
    RIO_HOURLY_POLLUTANT,
)


def test_consistency_const():
    """Test that all the POLLUTANT are also in the map structure of the constants."""

    for pollutant in RIO_HOURLY_POLLUTANT:
        assert pollutant in POLLUTANT_TO_FEATURE
        assert pollutant in POLLUTANT_TO_SENSOR_DEVICE_CLASS
        assert pollutant in POLLUTANT_TO_UNIT
