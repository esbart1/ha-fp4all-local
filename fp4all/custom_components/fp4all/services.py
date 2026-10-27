"""
FP4All Local for Home Assistant

Version : 0.4
Build   : 3.0.0
File    : service.py

Sservices platform for FP4All.
"""
from __future__ import annotations

import logging

from homeassistant.core import HomeAssistant

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

_SERVICES_REGISTERED = False


async def async_register_services(hass: HomeAssistant) -> None:
    """Register FP4All services."""

    global _SERVICES_REGISTERED

    if _SERVICES_REGISTERED:
        return

    async def handle_download_history(call) -> None:
        """Download history from every configured FP4All."""

        _LOGGER.warning("FP4All service download_history gestart")

        for coordinator in hass.data.get(DOMAIN, {}).values():
            _LOGGER.warning(
                "Download history van %s",
                coordinator.host,
            )

            await coordinator.async_update_history()

        _LOGGER.warning("FP4All service gereed")

    hass.services.async_register(
        DOMAIN,
        "download_history",
        handle_download_history,
    )

    _SERVICES_REGISTERED = True

    _LOGGER.info("FP4All services registered")