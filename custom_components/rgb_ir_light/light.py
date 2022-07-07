"""Switch platform for integration_blueprint."""
import datetime
import numpy as np
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.components.light import (
    ATTR_BRIGHTNESS,
    ATTR_HS_COLOR,
    LightEntity,
    ColorMode,
)

from .const import CONF_NAME, DOMAIN, ICON, VERSION, ATTRIBUTION, LIGHT

color_points = {
    "RED": [360.0, 100.0],
    "GREEN": [120.0, 100.0],
    "BLUE": [240.0, 100.0],
    "WHITE": [0.0, 0.0],
}
nodes = np.asarray(list(color_points.values()))


async def async_setup_entry(hass, entry, async_add_devices):
    """Setup sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_devices([RGBLight(coordinator, entry)])


def closest_node(node):
    """Find closest color."""
    if node[1] == 0:
        return list(color_points.keys()).index("WHITE")
    dist_1 = np.sum((nodes - node) ** 2, axis=1)
    dist_2 = np.sum((nodes - [360 - node[0], node[1]]) ** 2, axis=1)
    min_1 = np.min(dist_1)
    min_2 = np.min(dist_2)
    if min_1 <= min_2:
        return np.argmin(dist_1)
    return np.argmin(dist_2)


class RGBLight(LightEntity, CoordinatorEntity):
    """rgb light class."""

    def __init__(self, coordinator, config_entry):
        super().__init__(coordinator)
        self.config_entry = config_entry
        self._name = config_entry.data.get(CONF_NAME)
        self._requested_power = None
        self._requested_brightness = None
        self._requested_hs = None
        self._requested_state_at = None
        self._brightness_hops = 252 / 5

    @property
    def unique_id(self):
        """Return a unique ID to use for this entity."""
        return self.config_entry.entry_id

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self.unique_id)},
            "name": self._name,
            "model": VERSION,
            "manufacturer": self._name,
        }

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return {
            "attribution": ATTRIBUTION,
            "id": str(self.unique_id),
            "integration": DOMAIN,
        }

    @property
    def name(self):
        """Return the name of the switch."""
        return self._name

    @property
    def icon(self):
        """Return the icon of this switch."""
        return ICON

    @property
    def color_mode(self):
        return ColorMode.HS

    @property
    def supported_color_modes(self):
        return [self.color_mode]

    @property
    def is_on(self):
        return self._requested_power if self._requested_power is not None else False

    @property
    def brightness(self):
        return self._requested_brightness

    @property
    def min_mireds(self):
        return 143

    @property
    def max_mireds(self):
        return 454

    @property
    def color_temp(self):
        return 5

    @property
    def hs_color(self):
        return self._requested_hs

    @property
    def assumed_state(self) -> bool:
        last_refresh_success = (
            self.coordinator.data
            and self.config_entry.entry_id in self.coordinator.data
        )
        return not last_refresh_success

    async def _set_state(self, power_on, brightness=None, hs=None):
        if self.is_on and power_on is False:
            await self.coordinator.api.async_set_color(
                "OFF"
            )
            return
        else:
            if not self.is_on and power_on is True:
                await self.coordinator.api.async_set_color(
                    "ON"
                )
            if hs is not None and self.hs_color != hs:
                await self.coordinator.api.async_set_color(
                    list(color_points.keys())[closest_node(hs)]
                )
            if brightness is not None and brightness != self.brightness:
                brightness = brightness - 3
                brightness_diff = brightness - (
                    self._requested_brightness
                    if self._requested_brightness is not None
                    else 0
                )
                hops = int(abs(brightness_diff / self._brightness_hops))
                if brightness_diff > 0:
                    await self.coordinator.api.async_set_brightness(
                        "BRIGHTNESS_UP", hops if hops < 5 else hops * 2
                    )
                else:
                    await self.coordinator.api.async_set_brightness(
                        "BRIGHTNESS_DOWN", hops if hops < 5 else hops * 2
                    )
                self._requested_brightness = (brightness - brightness_diff) + (
                    int(brightness_diff / self._brightness_hops) * self._brightness_hops
                )
        self._requested_power = power_on
        self._requested_hs = hs if hs is not None else color_points.get("WHITE")
        self._requested_state_at = datetime.datetime.now(datetime.timezone.utc)
        self.async_write_ha_state()

    async def async_turn_on(self, **kwargs):
        brightness = None
        hs = None
        if ATTR_HS_COLOR in kwargs:
            hs = kwargs[ATTR_HS_COLOR]
        if ATTR_BRIGHTNESS in kwargs:
            brightness = kwargs[ATTR_BRIGHTNESS]
        await self._set_state(True, brightness, hs)

    async def async_turn_off(self, **kwargs):
        await self._set_state(False)
