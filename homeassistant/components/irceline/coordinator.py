"""Coordinator to fetch data from IRCEL - CELINE periodically."""

from datetime import UTC, date, datetime, timedelta
import logging
from typing import Any

from open_irceline import (
    FeatureValue,
    ForecastFeature,
    IrcelineApiError,
    IrcelineForecastClient,
    IrcelineRioClient,
    RioFeature,
    belaqi_index_forecast_daily,
    belaqi_index_rio_hourly,
)

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_LATITUDE, ATTR_LONGITUDE, CONF_ZONE
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    DOMAIN,
    FORECAST_POLLUTANT,
    IRCEL_CELINE,
    POLLUTANT_TO_FEATURE,
    RIO_HOURLY_POLLUTANT,
)
from .utils import get_config_value

_LOGGER = logging.getLogger(__name__)


class IrcelineCoordinator(DataUpdateCoordinator):
    """Coordinator to update data from IRCEL - CELINE."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Set up coordinator internals."""
        super().__init__(
            hass, _LOGGER, name="IRCEL - CELINE", update_interval=timedelta(minutes=30)
        )

        self._rio_client = IrcelineRioClient(session=async_get_clientsession(hass))
        self._forecast_client = IrcelineForecastClient(
            session=async_get_clientsession(hass)
        )
        self._zone = get_config_value(entry, CONF_ZONE)
        self.shared_device_info = DeviceInfo(
            entry_type=DeviceEntryType.SERVICE,
            identifiers={(DOMAIN, entry.entry_id)},
            manufacturer=IRCEL_CELINE,
            name=f"{entry.title}",
        )

    async def _async_update_data(self) -> dict[str, Any]:
        if (zone := self.hass.states.get(self._zone)) is None:
            raise UpdateFailed(f"Zone '{self._zone}' not found")
        position = (zone.attributes[ATTR_LATITUDE], zone.attributes[ATTR_LONGITUDE])

        try:
            rio_data: dict[RioFeature, FeatureValue] = await self._rio_client.get_data(
                features=[POLLUTANT_TO_FEATURE[p] for p in RIO_HOURLY_POLLUTANT],
                timestamp=datetime.now(UTC),
                position=position,
            )
        except IrcelineApiError as e:
            raise UpdateFailed("Could not get RIO hourly data") from e

        try:
            forecast_data: dict[
                tuple[ForecastFeature, date], FeatureValue
            ] = await self._forecast_client.get_data(
                features=[POLLUTANT_TO_FEATURE[p] for p in FORECAST_POLLUTANT],
                timestamp=date.today(),
                position=position,
            )
        except IrcelineApiError as e:
            raise UpdateFailed("Could not get forecast data") from e

        try:
            belaqi_forecast: dict[
                date, FeatureValue
            ] = await belaqi_index_forecast_daily(
                forecast_client=self._forecast_client,
                timestamp=date.today(),
                position=position,
            )
        except IrcelineApiError as e:
            raise UpdateFailed("Could not get BelAQI forecast data") from e

        try:
            belaqi: FeatureValue = await belaqi_index_rio_hourly(
                rio_client=self._rio_client,
                timestamp=datetime.now(UTC),
                position=position,
            )
        except IrcelineApiError as e:
            raise UpdateFailed("Could not get current BelAQI forecast") from e

        return {
            "rio": rio_data,
            "forecast": forecast_data,
            "belaqi_forecast": belaqi_forecast,
            "belaqi": belaqi,
        }
