"""
FP4All Local for Home Assistant

Version : 0.3
Build   : 2.1
File    : fp4allstatus.py

All Status  from the FP4All logger.
"""

from __future__ import annotations

import logging
import time

from homeassistant.helpers.aiohttp_client import async_get_clientsession

_LOGGER = logging.getLogger(__name__)


async def download_status(coordinator) -> str | None:
    """Download the realtime status page."""

    url = f"http://{coordinator.host}/status.htm"

    _LOGGER.debug("Downloading %s", url)

    session = async_get_clientsession(coordinator.hass)

    start = time.monotonic()

    try:
        async with session.get(url, timeout=15) as response:
            response.raise_for_status()
            html = await response.text()

    except Exception as err:
        _LOGGER.error(
            "Unable to download status.htm from %s: %s",
            coordinator.host,
            err,
        )
        return None

    elapsed = time.monotonic() - start

    _LOGGER.debug(
        "Downloaded status.htm from %s (%d bytes in %.2f sec)",
        coordinator.host,
        len(html),
        elapsed,
    )

    return html
✅ v0.3 Build 1 (klaar)
Realtime waarden
VAC
FAC
status_parser
DeviceInfo
Juiste precisie




🔜 v0.3 Build 2

Nu gaan we de rest uit status.htm benutten.

Extra sensoren:

VPV Start
Start Time
Capacity
VAC Min
VAC Max
FAC Min
FAC Max
Mode	