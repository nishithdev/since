from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import async_get_platforms
from homeassistant.helpers.entity_component import async_add_entities

from .const import DOMAIN
from .entity import SinceEntity


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data

    name = entry.data["name"]
    since_str = entry.data["since"]

    async_add_entities = hass.helpers.entity_component.async_add_entities
    async_add_entities([SinceEntity(name, since_str)])

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    hass.data[DOMAIN].pop(entry.entry_id, None)
    return True