"""
FP4All Local for Home Assistant

Version : 0.4
Build   : 3.0.0
File    : history.py

History handling for FP4All Local.
"""
from __future__ import annotations

import logging
import time
from pathlib import Path

from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import HISTORY_FOLDER, HISTORY_HTML

_LOGGER = logging.getLogger(__name__)


def _write_history_file(
    history_dir: Path,
    filename: Path,
    content: str,
) -> None:
    """Write the downloaded history HTML to disk."""
    history_dir.mkdir(exist_ok=True)
    filename.write_text(content, encoding="utf-8")


async def download_history(coordinator) -> None:
    """Download the history page."""

    url = f"http://{coordinator.host}/{HISTORY_HTML}"

    _LOGGER.warning("FP4All: download_history gestart")
    _LOGGER.info("====================================================")
    _LOGGER.info("FP4All history download")
    _LOGGER.info("Host : %s", coordinator.host)

    session = async_get_clientsession(coordinator.hass)

    start = time.monotonic()

    try:
        async with session.get(url, timeout=30) as response:
            response.raise_for_status()
            html = await response.text()

    except Exception as err:
        _LOGGER.error("Download failed: %s", err)
        _LOGGER.info("====================================================")
        return

    elapsed = time.monotonic() - start

    history_dir = Path(
        coordinator.hass.config.path(HISTORY_FOLDER)
    )

    filename = history_dir / (
        coordinator.host.replace(".", "_") + ".html"
    )

    await coordinator.hass.async_add_executor_job(
        _write_history_file,
        history_dir,
        filename,
        html,
    )

    _LOGGER.info("Saved : %s", filename)
    _LOGGER.info("Size  : %d bytes", len(html))
    _LOGGER.info("Rows  : %d", html.lower().count("<tr"))
    _LOGGER.info("Time  : %.2f sec", elapsed)
    _LOGGER.info("====================================================")