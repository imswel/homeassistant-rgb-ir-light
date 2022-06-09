"""Sample API Client."""
import logging
import asyncio
import socket
from typing import Optional
import aiohttp
import async_timeout
from homeassistant.core import HomeAssistant

TIMEOUT = 10


_LOGGER: logging.Logger = logging.getLogger(__package__)

HEADERS = {"Content-type": "application/json; charset=UTF-8"}


class IntegrationBlueprintApiClient:
    """Config flow for Blueprint."""

    def __init__(self, entity_id: str, device: str, hass: HomeAssistant) -> None:
        """Sample API Client."""
        self._entity_id = entity_id
        self._device = device
        self._hass = hass

    async def async_get_data(self) -> dict:
        """Get data from the API."""

    async def async_set_color(self, value: str) -> None:
        """Get data from the API."""
        await self._hass.services.async_call(
            "remote",
            "send_command",
            {"device": self._device, "command": value},
            True,
            None,
            None,
            {"entity_id": self._entity_id},
        )

    async def async_set_brightness(self, value: str, repeat: int) -> None:
        """Get data from the API."""
        await self._hass.services.async_call(
            "remote",
            "send_command",
            {
                "device": self._device,
                "command": value,
                "num_repeats": repeat,
                # "delay_secs": 1,
                # "hold_secs": 0.5,
            },
            True,
            None,
            None,
            {"entity_id": self._entity_id},
        )
