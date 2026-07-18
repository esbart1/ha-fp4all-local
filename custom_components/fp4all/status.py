"""Download status.htm from the FP4All logger."""

from __future__ import annotations

import logging

from homeassistant.helpers.aiohttp_client import async_get_clientsession

_LOGGER = logging.getLogger(__name__)


async def download_status(coordinator) -> str | None:
    """Download status.htm."""

    url = f"http://{coordinator.host}/status.htm"

    session = async_get_clientsession(coordinator.hass)

    try:
        async with session.get(url, timeout=10) as response:
            response.raise_for_status()
            html = await response.text()

    except Exception as err:
        _LOGGER.warning(
            "Unable to download status.htm from %s: %s",
            coordinator.host,
            err,
        )
        return None

    _LOGGER.debug(
        "Downloaded status.htm (%d bytes)",
        len(html),
    )

    return html