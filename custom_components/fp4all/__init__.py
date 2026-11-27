"""
FP4All Local for Home Assistant

Home Assistant integration for FP4All.
"""
from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.event import async_track_time_change

from .const import DOMAIN
from .coordinator import FP4AllCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["sensor", "button"]


async def async_setup(
    hass: HomeAssistant,
    config: dict,
) -> bool:
    """Set up FP4All component."""

    return True


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """Set up FP4All from a config entry."""

    coordinator = FP4AllCoordinator(
        hass=hass,
        host=entry.data["host"],
        entry=entry,
    )

    await coordinator.async_load_cache()
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(
        entry,
        PLATFORMS,
    )

    #
    # Reload integration after changing OptionsFlow settings
    #
    entry.async_on_unload(
        entry.add_update_listener(
            async_reload_entry
        )
    )

    # Refresh all FP4All sensors shortly after local midnight. This is a normal
    # coordinator refresh, not a full integration reload. If the inverter is
    # offline, the coordinator still applies the daily counter rollover.
    async def _async_daily_refresh(_now):
        _LOGGER.debug("Running scheduled FP4All daily refresh for %s", entry.title)
        await coordinator.async_request_refresh()

    entry.async_on_unload(
        async_track_time_change(
            hass,
            _async_daily_refresh,
            hour=0,
            minute=10,
            second=0,
        )
    )

    _LOGGER.info(
        "FP4All '%s' initialized (%s)",
        entry.title,
        coordinator.host,
    )

    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """Unload FP4All."""

    unload_ok = await hass.config_entries.async_unload_platforms(
        entry,
        PLATFORMS,
    )

    if unload_ok:
        hass.data[DOMAIN].pop(
            entry.entry_id,
            None,
        )

    return unload_ok


async def async_reload_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> None:
    """Reload config entry after options change."""

    await hass.config_entries.async_reload(
        entry.entry_id
    )