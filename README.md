# homeassistant-rgb-ir-light

This repo is written in Python and is made to be used as a HACS repository in Home Assitant

## Why?

Wanted to use a IR RGB strip as a light component in Home Assistant

## How?

Matching the colors of the remote to the ones in Home Assistant using the nearest color

## Installation

1. Add this repository to Home Assistant HACS
2. Install it
3. Restart Home Assistant
4. Learn the following commands from your IR controller using a single device name (OFF, ON, WHITE, RED, GREEN, BLUE, BRIGHTNESS_UP, BRIGHTNESS_DOWN)
5. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "rgb ir light"
6. Set your IR controller entity_id and the device name you gave when learning remote commands
