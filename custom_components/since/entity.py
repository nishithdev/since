from datetime import datetime, timedelta
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.const import STATE_UNKNOWN

from .const import DOMAIN


def format_time_delta(delta: timedelta) -> str:
    days = delta.days
    hours = delta.seconds // 3600
    parts = []
    if days > 0:
        parts.append(f"{days} days")
    if hours > 0 or days == 0:
        parts.append(f"{hours} hrs")
    return " ".join(parts)


class SinceEntity(Entity):
    def __init__(self, name: str, since_str: str):
        self._name = name
        self._since = datetime.strptime(since_str, "%Y-%m-%d %H:%M:%S")
        self._attr_unique_id = f"since_{name.lower().replace(' ', '_')}"
        self._attr_icon = "mdi:calendar-clock"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, "since_tracker")},
            name="Since Tracker",
            manufacturer="Custom",
            model="SinceEntity",
        )

    @property
    def name(self):
        return f"Since: {self._name}"

    @property
    def state(self):
        now = datetime.now()
        delta = now - self._since
        return format_time_delta(delta)

    @property
    def extra_state_attributes(self):
        return {
            "since": self._since.isoformat(),
            "seconds_passed": int((datetime.now() - self._since).total_seconds()),
        }