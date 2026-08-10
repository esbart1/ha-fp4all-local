"""
FP4All Local for Home Assistant

Version : 0.4
Build   : 3.1.9
File    : __init__.py

Home Assistant integration for FP4All.
"""
from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .coordinator import FP4AllCoordinator
from .services import async_register_services

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["sensor"]


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

    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(
        entry,
        PLATFORMS,
    )

    await async_register_services(hass)

    #
    # Reload integration after changing OptionsFlow settings
    #
    entry.async_on_unload(
        entry.add_update_listener(
            async_reload_entry
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