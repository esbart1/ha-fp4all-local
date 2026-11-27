"""
FP4All Local for Home Assistant

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
    """Handle FP4All options in two clearly separated steps."""

    async def async_step_init(self, user_input=None):
        """Configure the update interval first."""
        if user_input is not None:
            self._options = dict(self.config_entry.options)
            self._options.update(user_input)
            return await self.async_step_bus_low_fail()

        options = self.config_entry.options
        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        "update_interval",
                        default=str(options.get("update_interval", "30")),
                    ): vol.In(
                        {
                            "1": "1 s",
                            "10": "10 s",
                            "30": "30 s",
                            "60": "1 min",
                            "300": "5 min",
                        }
                    ),
                }
            ),
        )

    async def async_step_bus_low_fail(self, user_input=None):
        """Configure the Bus-Low-Fail sun and power confirmation windows."""
        if user_input is not None:
            options = getattr(self, "_options", dict(self.config_entry.options))
            options.update(user_input)
            # Remove obsolete options after the user saves the simplified form.
            options.pop("sunset_before_minutes", None)
            options.pop("sunset_after_minutes", None)
            options.pop("sunrise_window_minutes", None)
            return self.async_create_entry(title="", data=options)

        options = self.config_entry.options
        return self.async_show_form(
            step_id="bus_low_fail",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        "sunset_margin_minutes",
                        default=int(
                            options.get(
                                "sunset_margin_minutes",
                                max(
                                    int(options.get("sunset_before_minutes", 45)),
                                    int(options.get("sunset_after_minutes", 45)),
                                ),
                            )
                        ),
                    ): vol.All(vol.Coerce(int), vol.Range(min=0, max=240)),
                    vol.Required(
                        "recovery_power_w",
                        default=float(options.get("recovery_power_w", 5)),
                    ): vol.All(vol.Coerce(float), vol.Range(min=0, max=5000)),
                    vol.Required(
                        "recovery_power_duration_minutes",
                        default=int(options.get("recovery_power_duration_minutes", 5)),
                    ): vol.All(vol.Coerce(int), vol.Range(min=1, max=120)),
                }
            ),
        )
