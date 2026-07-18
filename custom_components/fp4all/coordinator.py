"""
FP4All Local for Home Assistant

Version : 0.3
Build : 2.6
File    : coordinator.py

DataUpdateCoordinator for FP4All Local.
"""
from __future__ import annotations

import logging
import xml.etree.ElementTree as ET

from aiohttp import ClientError

from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import (
    DEFAULT_SCAN_INTERVAL,
    STATUS_XML,
)
from .history import download_history
from .status import download_status
from .index import download_index
from .index_parser import parse_index
from .status_parser import parse_status
from .helpers.combine_high_low import combine_high_low

_LOGGER = logging.getLogger(__name__)


class FP4AllCoordinator(DataUpdateCoordinator):
    """Coordinator for FP4All."""

    def __init__(
        self,
        hass: HomeAssistant,
        host: str,
        entry,
    ) -> None:
        """Initialize coordinator."""

        self.host = host
        self.entry = entry

        #
        # Filled after parsing status.htm
        #
        self.status = {}
        self.history = []

        super().__init__(
            hass,
            _LOGGER,
            name=f"FP4All {host}",
            update_interval=DEFAULT_SCAN_INTERVAL,
        )

    async def _async_update_data(self):
        """Fetch realtime values."""
        # ----------------------------------------------------
        #
        # First read status.xml
        #
        url = f"http://{self.host}/{STATUS_XML}"

        session = async_get_clientsession(self.hass)

        try:
            async with session.get(url, timeout=10) as response:
                response.raise_for_status()
                xml = await response.text()

        except ClientError as err:
            raise UpdateFailed(
                f"Cannot connect to {self.host}: {err}"
            ) from err

        try:
            root = ET.fromstring(xml)

            data = {
                "power": float(root.findtext("gauge_power", "0")),
                "temp": float(root.findtext("gauge_temp", "0")),
                "vpv": float(root.findtext("gauge_vpv", "0")),
                "iac": float(root.findtext("gauge_iac", "0")),
                "today": float(root.findtext("energy_today", "0")),
                "total": float(root.findtext("energy_total", "0")),
                "hours": int(root.findtext("hours_total", "0")),
                "timestamp": root.findtext("time_stamp", ""),
            }

        except Exception as err:
            raise UpdateFailed(
                f"Invalid XML received from {self.host}: {err}"
            ) from err

        #
        # Future enhancement
        #
        # The helper combine_high_low() is available for combining
        # High/Low counter values.
        #
        # It is intentionally not used yet because the exact FP4All
        # counter format has not been fully verified on all inverter
        # types. Lifetime energy and operating hours are currently
        # taken from index.htm.
        #

        #
        # Now read status.htm
        #
        try:
            html = await download_status(self)

            if html:

                self.status = parse_status(html)
                #
                # realtime waarden uit status.htm
                #
                if self.status.get("pac") is not None:
                    data["power"] = self.status["pac"]

                for key in (
                    "vac",
                    "fac",
                    "vpv",
                    "iac",
                    "temp",
                ):
                    if self.status.get(key) is not None:
                        data[key] = self.status[key]

                #
                # extra statuswaarden
                #
                for key in (
                    "capacity",
                    "vac_min",
                    "vac_max",
                    "fac_min",
                    "fac_max",
                    "vpv_start",
                    "t_start",
                    "mode",
                    "etotalh",
                    "etotall",
                    "htotalh",
                    "htotall",
                ):
                    if self.status.get(key) is not None:
                        data[key] = self.status[key]

        except Exception as err:
            _LOGGER.warning(
                "Unable to parse status.htm from %s: %s",
                self.host,
                err,
            )
        #
        # Now read index.htm
        #
        try:
            html = await download_index(self)

            if html:

                index = parse_index(html)

#                _LOGGER.warning(
#                    "INDEX PARSER = %s",
#                    index,
#                )

                for key, value in index.items():
                    if value is not None:
                        data[key] = value

        except Exception as err:
            _LOGGER.warning(
                "Unable to parse index.htm from %s: %s",
                self.host,
                err,
            )
        return data

    async def async_update_history(self) -> None:
        """Download history."""

        await download_history(self)