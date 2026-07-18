"""
FP4All Local for Home Assistant

Version : 0.3
Build   : 2.0
File    : config_flow.py

const platform for FP4All.
"""
from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_HOST

from .const import DOMAIN


class FP4AllConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for FP4All."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""

        if user_input is not None:
            await self.async_set_unique_id(user_input[CONF_HOST])
            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title=f"FP4All {user_input[CONF_HOST]}",
                data=user_input,
            )
##
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_HOST): str,
                }
            ),
        )