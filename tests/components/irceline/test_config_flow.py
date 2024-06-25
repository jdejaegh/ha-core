"""Test the IRCEL - CELINE: Air quality Belgium config flow."""

from unittest.mock import AsyncMock, patch

from homeassistant import config_entries
from homeassistant.components.irceline.const import DOMAIN
from homeassistant.components.zone import ENTITY_ID_HOME
from homeassistant.const import CONF_ZONE
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType


async def test_form(hass: HomeAssistant, mock_setup_entry: AsyncMock) -> None:
    """Test we get the form."""
    hass.states.async_set(
        ENTITY_ID_HOME,
        0,
        {"latitude": 50.73, "longitude": 4.05},
    )
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] == FlowResultType.FORM
    assert result["errors"] == {}

    with patch(
        "homeassistant.components.irceline.config_flow.IrcelineRioClient.get_data",
        return_value={"some_value": "here"},
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"], {CONF_ZONE: ENTITY_ID_HOME}
        )
        await hass.async_block_till_done()

    assert result["type"] == FlowResultType.CREATE_ENTRY
    assert result["title"] == "home"
    assert result["data"] == {CONF_ZONE: ENTITY_ID_HOME}
    assert len(mock_setup_entry.mock_calls) == 1


async def test_form_cannot_connect(
    hass: HomeAssistant, mock_setup_entry: AsyncMock
) -> None:
    """Test we handle cannot connect error."""

    hass.states.async_set(
        ENTITY_ID_HOME,
        0,
        {"latitude": 50.73, "longitude": 4.05},
    )

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "homeassistant.components.irceline.config_flow.IrcelineRioClient.get_data",
        return_value={},
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"], {CONF_ZONE: ENTITY_ID_HOME}
        )

    assert result["type"] == FlowResultType.FORM
    assert result["errors"] == {"base": "cannot_connect"}

    # Make sure the config flow tests finish with either an
    # FlowResultType.CREATE_ENTRY or FlowResultType.ABORT so
    # we can show the config flow is able to recover from an error.

    with patch(
        "homeassistant.components.irceline.config_flow.IrcelineRioClient.get_data",
        return_value={"some_value": "here"},
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"], {CONF_ZONE: ENTITY_ID_HOME}
        )
        await hass.async_block_till_done()

    assert result["type"] == FlowResultType.CREATE_ENTRY
    assert result["title"] == "home"
    assert result["data"] == {CONF_ZONE: ENTITY_ID_HOME}
    assert len(mock_setup_entry.mock_calls) == 1


async def test_form_unknown_zone(
    hass: HomeAssistant, mock_setup_entry: AsyncMock
) -> None:
    """Test we return an error when the zone does not exist."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "homeassistant.components.irceline.config_flow.IrcelineRioClient.get_data",
        return_value={"key": "value"},
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"], {CONF_ZONE: "zone.unknown"}
        )

    assert result["type"] == FlowResultType.FORM
    assert result["errors"] == {CONF_ZONE: "zone_not_exist"}


async def test_form_unknown_error(
    hass: HomeAssistant, mock_setup_entry: AsyncMock
) -> None:
    """Test we handle cannot connect error."""

    hass.states.async_set(
        ENTITY_ID_HOME,
        0,
        {"latitude": 50.73, "longitude": 4.05},
    )

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "homeassistant.components.irceline.config_flow.IrcelineRioClient.get_data",
        side_effect=ValueError,
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"], {CONF_ZONE: ENTITY_ID_HOME}
        )

    assert result["type"] == FlowResultType.FORM
    assert result["errors"] == {"base": "unknown"}

    # Make sure the config flow tests finish with either an
    # FlowResultType.CREATE_ENTRY or FlowResultType.ABORT so
    # we can show the config flow is able to recover from an error.

    with patch(
        "homeassistant.components.irceline.config_flow.IrcelineRioClient.get_data",
        return_value={"some_value": "here"},
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"], {CONF_ZONE: ENTITY_ID_HOME}
        )
        await hass.async_block_till_done()

    assert result["type"] == FlowResultType.CREATE_ENTRY
    assert result["title"] == "home"
    assert result["data"] == {CONF_ZONE: ENTITY_ID_HOME}
    assert len(mock_setup_entry.mock_calls) == 1
