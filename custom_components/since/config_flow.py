from __future__ import annotations
import datetime
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers.selector import TextSelector, DateSelector, TimeSelector
from .const import DOMAIN


class SinceConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            name = user_input["name"]
            date = user_input["date"]
            time = user_input["time"]

            if not name.strip():
                errors["name"] = "Name is required"
            else:
                combined = f"{date} {time}"
                try:
                    datetime.datetime.strptime(combined, "%Y-%m-%d %H:%M:%S")
                    return self.async_create_entry(
                        title=name,
                        data={
                            "name": name,
                            "since": combined,
                        },
                    )
                except ValueError:
                    errors["base"] = "Invalid date or time format"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required("name"): TextSelector(),
                    vol.Required("date"): DateSelector(),
                    vol.Required("time"): TimeSelector(),
                }
            ),
            errors=errors,
        )