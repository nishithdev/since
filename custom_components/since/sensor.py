from datetime import datetime, timedelta

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.event import async_track_time_interval

from .const import DOMAIN

UPDATE_INTERVAL = timedelta(hours=1)


def format_time_delta(delta: timedelta) -> str:
    days = delta.days
    hours = delta.seconds // 3600

    parts = []
    if days > 0:
        parts.append(f"{days} days")
    if hours > 0 or days == 0:  # Always show hours if no days
        parts.append(f"{hours} hrs")

    return " ".join(parts)


async def async_setup_entry(hass, entry, async_add_entities):
    name = entry.data["name"]
    since_str = entry.data["since"]

    sensor = SinceSensor(name, since_str)
    async_add_entities([sensor], True)


class SinceSensor(SensorEntity):
    def __init__(self, name: str, since_str: str):
        self._attr_name = f"Since: {name}"
        self._attr_unique_id = f"since_{name.lower().replace(' ', '_')}"
        self._since = datetime.strptime(since_str, "%Y-%m-%d %H:%M:%S")
        self._attr_extra_state_attributes = {
            "task": name,
            "since": self._since.isoformat(),
        }
        self._attr_icon = "mdi:calendar-clock"
        self._attr_should_poll = False

    async def async_added_to_hass(self):
        async_track_time_interval(self.hass, self.async_update, UPDATE_INTERVAL)

    async def async_update(self, _now=None):
        now = datetime.now()
        delta = now - self._since
        self._attr_native_value = format_time_delta(delta)
        self._attr_extra_state_attributes["seconds_passed"] = int(delta.total_seconds())
        self.async_write_ha_state()