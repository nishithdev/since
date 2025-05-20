from __future__ import annotations
import datetime
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.helpers.selector import (
    TextSelector,
    TextSelectorConfig,
    DateSelector,
    DateSelectorConfig,
    TimeSelector,
    TimeSelectorConfig,
)

from .const import DOMAIN


class SinceConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            name = user_input["name"]
            date = user_input["date"]
            time = user_input["time"]

            # Ensure time includes seconds
            if len(time.split(":")) == 2:
                time += ":00"

            # Combine date and time to a datetime string
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
                errors["base"] = "invalid_datetime"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required("name"): TextSelector(TextSelectorConfig()),
                    vol.Required("date"): DateSelector(DateSelectorConfig()),
                    vol.Required("time"): TimeSelector(TimeSelectorConfig()),
                }
            ),
            errors=errors,
        )