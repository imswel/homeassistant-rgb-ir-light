"""Constants for rgb_ir_light."""
# Base component constants
NAME = "RGB IR Light"
DOMAIN = "rgb_ir_light"
DOMAIN_DATA = f"{DOMAIN}_data"
VERSION = "0.0.1"
ATTRIBUTION = "Data provided by http://jsonplaceholder.typicode.com/"
ISSUE_URL = "https://github.com/betogontijo/homeassistant-rgb-ir-light/issues"

# Icons
ICON = "mdi:format-quote-close"

# Device classes
BINARY_SENSOR_DEVICE_CLASS = "connectivity"

# Platforms
LIGHT = "light"
PLATFORMS = [LIGHT]


# Configuration and options
CONF_ENABLED = "enabled"
CONF_NAME = "name"
CONF_ENTITY_ID = "entity_id"
CONF_DEVICE = "device"

# Defaults
DEFAULT_NAME = DOMAIN


STARTUP_MESSAGE = f"""
-------------------------------------------------------------------
{NAME}
Version: {VERSION}
This is a custom integration!
If you have any issues with this you need to open an issue here:
{ISSUE_URL}
-------------------------------------------------------------------
"""
