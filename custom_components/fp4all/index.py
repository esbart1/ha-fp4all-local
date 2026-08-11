"""
FP4All Local for Home Assistant

Version : 0.4
Build   : 3.0.0
File    : index.py

Download index.htm from the FP4All logger.
"""

from __future__ import annotations

import logging

from aiohttp import ClientError
from homeassistant.helpers.aiohttp_client import async_get_clientsession

_LOGGER = logging.getLogger(__name__)


async def download_index(coordinator) -> str | None:
    """Download index.htm."""

    session = async_get_clientsession(
        coordinator.hass
    )

    url = (
        f"http://{coordinator.host}/index.htm"
    )

    try:
        async with session.get(
            url,
            timeout=10,
        ) as response:

            response.raise_for_status()

            html = await response.text()

            _LOGGER.debug(
                "Downloaded index.htm from %s",
                coordinator.host,
            )

            return html

    except ClientError as err:

        _LOGGER.warning(
            "Unable to download index.htm from %s: %s",
            coordinator.host,
            err,
        )

    return None