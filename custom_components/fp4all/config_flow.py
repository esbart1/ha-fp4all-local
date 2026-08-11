"""
FP4All Local for Home Assistant

Version : 0.4
Build   : 3.1.9
File    : config_flow.py

Configuration and options flow for FP4All.
"""

from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_HOST
from homeassistant.core import callback

from .const import DOMAIN


class FP4AllConfigFlow(
    config_entries.ConfigFlow,
    domain=DOMAIN,
):
    """Handle a config flow for FP4All."""

    VERSION = 1

    async def async_step_user(
        self,
        user_input=None,
    ):
        """Handle the initial setup."""

        if user_input is not None:
            await self.async_set_unique_id(
                user_input[CONF_HOST]
            )

            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title=f"FP4All {user_input[CONF_HOST]}",
                data=user_input,
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_HOST): str,
                }
            ),
        )

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry,
    ):
        """Return options flow."""

        return FP4AllOptionsFlow()


class FP4AllOptionsFlow(
    config_entries.OptionsFlow,
):
    """Handle FP4All options."""

    async def async_step_init(
        self,
        user_input=None,
    ):
        """Manage integration options."""

        if user_input is not None:
            return self.async_create_entry(
                title="",
                data=user_input,
            )

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        "update_interval",
                        default=self.config_entry.options.get(
                            "update_interval",
                            "30",
                        ),
                    ): vol.In(
                        {
                            "1": "Realtime (1 seconde)",
                            "10": "10 seconden",
                            "30": "30 seconden",
                            "60": "1 minuut",
                            "300": "5 minuten",
                        }
                    ),
                }
            ),
        )