"""Adds config flow for Blueprint."""
from homeassistant import config_entries
from homeassistant.core import callback
import voluptuous as vol

from .api import IntegrationBlueprintApiClient
from .const import (
    CONF_NAME,
    CONF_ENTITY_ID,
    CONF_DEVICE,
    DOMAIN,
    PLATFORMS,
)


class BlueprintFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Blueprint."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    def __init__(self):
        """Initialize."""
        self._errors = {}

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        self._errors = {}

        if user_input is not None:
            valid = await self._test_credentials(
                user_input[CONF_ENTITY_ID], user_input[CONF_DEVICE]
            )
            if valid is not True:
                self._errors["base"] = "auth"
            return self.async_create_entry(title=user_input[CONF_NAME], data=user_input)

        user_input = {}
        # Provide defaults for form
        user_input[CONF_NAME] = ""
        user_input[CONF_ENTITY_ID] = ""
        user_input[CONF_DEVICE] = ""

        return await self._show_config_form(user_input)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return BlueprintOptionsFlowHandler(config_entry)

    async def _show_config_form(self, user_input):  # pylint: disable=unused-argument
        """Show the configuration form to edit location data."""
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_NAME, default=user_input[CONF_NAME]): str,
                    vol.Required(
                        CONF_ENTITY_ID, default=user_input[CONF_ENTITY_ID]
                    ): str,
                    vol.Required(CONF_DEVICE, default=user_input[CONF_DEVICE]): str,
                }
            ),
            errors=self._errors,
        )

    async def _test_credentials(self, entity_id, device):
        """Return true if credentials is valid."""
        try:
            IntegrationBlueprintApiClient(entity_id, device, self.hass)
            return True
        except Exception:  # pylint: disable=broad-except
            pass
        return False


class BlueprintOptionsFlowHandler(config_entries.OptionsFlow):
    """Blueprint config flow options handler."""

    def __init__(self, config_entry):
        """Initialize HACS options flow."""
        self.config_entry = config_entry
        self.options = dict(config_entry.options)

    async def async_step_init(self, user_input=None):  # pylint: disable=unused-argument
        """Manage the options."""
        return await self.async_step_user()

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        if user_input is not None:
            self.options.update(user_input)
            return await self._update_options()

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(x, default=self.options.get(x, True)): bool
                    for x in sorted(PLATFORMS)
                }
            ),
        )

    async def _update_options(self):
        """Update config entry options."""
        return self.async_create_entry(
            title=self.config_entry.data.get(CONF_ENTITY_ID), data=self.options
        )
