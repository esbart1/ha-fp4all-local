"""
FP4All Local for Home Assistant

Version : 0.4
Build   : 3.1.9
File    : coordinator.py

DataUpdateCoordinator for FP4All Local.
"""
from __future__ import annotations

import asyncio
import json
from pathlib import Path
import logging
import xml.etree.ElementTree as ET
from datetime import timedelta, datetime

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

        self._day = None
        self._max_today = 0.0

        #
        # Filled after parsing status.htm
        #
        self.status = {}
        self.history = []

        #
        # Device information
        #
        self._manufacturer: str | None = None
        self._model: str | None = None
        self._serial: str | None = None
        self._firmware: str | None = None

        #
        # Last valid dataset (used during temporary communication loss)
        #
        self._last_index: dict = {}

        #
        # Last valid operating mode
        #
        self._last_mode = None

        #
        # Temporary mode filter
        #
        self._shutdown_since = None

        #
        # Last successful communication
        #
        self._last_successful_update = None 

        #
        # Last inverter timestamp
        #
        self._last_inverter_timestamp = None

        #
        # Communication state
        #
        self._communication_lost = False

        scan_interval = int(
            entry.options.get(
                "update_interval",
                DEFAULT_SCAN_INTERVAL.total_seconds(),
            )
        )

        ##
        #
        # Communication timeout
        # 3 × update interval
        # Maximum 11 minutes
        #
        self._communication_timeout = min(
            scan_interval * 3,
            660,
        )

        super().__init__(
            hass,
            _LOGGER,
            name=f"FP4All {host}",
            update_interval=timedelta(seconds=scan_interval),
        )

        #
        # Cache directory
        #
        self._cache_dir = Path(
            hass.config.path(
                "custom_components",
                "fp4all",
                "fp4all_cache",
            )
        )

        self._cache_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        #
        # Eén cachebestand per omvormer (op basis van IP)
        #
        self._cache_file = (
            self._cache_dir
            / f"{self.host.replace('.', '_')}.json"
        )

        #
        # Lees cachebestand asynchroon
        #
        self.hass.async_create_task(self._read_cache())

    async def _read_cache(self) -> None:
        """Read cache without blocking Home Assistant."""

        if not self._cache_file.exists():
            return

        try:
            text = await asyncio.to_thread(
                self._cache_file.read_text,
                encoding="utf-8",
            )

            self._last_good_data = json.loads(text)
            ##
            #
            # Restore remembered device information
            #
            self._manufacturer = self._last_good_data.get("manufacturer")
            self._model = self._last_good_data.get("model")
            self._serial = self._last_good_data.get("serial")
            self._firmware = self._last_good_data.get("firmware")

            self._communication_lost = self._last_good_data.get(
                "_communication_lost",
                False,
            )
            ##

        except Exception as err:
            _LOGGER.warning(
                "Cannot read cache file: %s",
                err,
            )


    async def _write_cache(self) -> None:
        """Write cache without blocking Home Assistant."""

        try:
            await asyncio.to_thread(
                self._cache_file.write_text,
                json.dumps(
                    self._last_good_data,
                    indent=2,
                ),
                encoding="utf-8",
            )

        except Exception as err:
            _LOGGER.warning(
                "Cannot write cache file: %s",
                err,
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


        ##################

        except (
            ClientError,
            TimeoutError,
            OSError,
        ) as err:

            if self._last_good_data:

                #
                # Communication lost
                #
                cached_data = self._last_good_data.copy()

                cached_data["communication"] = "Communication lost"
                cached_data["mode"] = 3
                cached_data["mode_text"] = "Warning"

                #
                # Remember communication state
                #
                self._communication_lost = True

                return cached_data

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

            #
            # Remember inverter timestamp
            #
            inverter_timestamp = data.get("timestamp")

            if inverter_timestamp:
                self._last_inverter_timestamp = inverter_timestamp

        except Exception as err:

            if self._last_good_data:

                _LOGGER.warning(
                    "Invalid XML from %s, using cached data",
                    self.host,
                )
                return self._last_good_data

            raise UpdateFailed(
                f"Invalid XML received from {self.host}: {err}"
            ) from err

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
                    "manufacturer",
                    "model",
                    "firmware",
                    "serial",				
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

                #  
                #  Combine 16-bit High/Low counters into one value
                #
                energy_total = combine_high_low(
                    self.status.get("etotalh"),
                    self.status.get("etotall"),
                )

                if energy_total is not None:
                    data["total"] = energy_total
                 
                hours_total = combine_high_low(
                    self.status.get("htotalh"),
                    self.status.get("htotall"),
                )


        except Exception as err:

            if self._last_index:
                _LOGGER.warning(
                    "Using cached index.htm for %s",
                    self.host,
                )
                index = self._last_index.copy()

                for key, value in index.items():
                    if value is not None:
                        data[key] = value

            else:
                _LOGGER.warning(
                    "Unable to parse index.htm from %s: %s",
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

                self._last_index = index.copy()

                for key, value in index.items():
                    if value is not None:
                        data[key] = value

        except Exception as err:

            if self._last_index:
                _LOGGER.warning(
                    "Using cached index.htm for %s",
                    self.host,
                )

                index = self._last_index.copy()

                for key, value in index.items():
                    if value is not None:
                        data[key] = value
        #
        # Stable operating mode filter
        #
        mode = data.get("mode")

        #
        # Dynamic PV threshold
        # 70% of inverter start voltage
        # with 90V minimum fallback
        #
        pv_start = data.get("vpv_start")

        if pv_start is None or pv_start <= 0:
            pv_threshold = 90
        else:
            pv_threshold = pv_start * 0.70

            if pv_threshold < 90:
                pv_threshold = 90


        pv_ok = data.get("vpv", 0) >= pv_threshold
        power_ok = data.get("power", 0) > 0

        inverter_running = pv_ok and power_ok


        if inverter_running:

            #
            # Real production detected
            #
            self._shutdown_since = None

            #
            # Unknown (7) is not accepted during production
            #
            if mode == 7 and self._last_mode is not None:
                data["mode"] = self._last_mode

            elif mode != 7:
                self._last_mode = mode


        elif mode == 7:


            #
            # Possible transition to night mode
            #
            if self._shutdown_since is None:
                self._shutdown_since = datetime.now()

            elapsed = (
                datetime.now() - self._shutdown_since
            ).total_seconds()

            #
            # Ignore short Unknown (7) during transition
            #
            if elapsed < 30 and self._last_mode is not None:
                data["mode"] = self._last_mode


        #
        # Remember last valid operating mode
        #
        if data.get("mode") is not None and data.get("mode") != 7:
            self._last_mode = data.get("mode")


        #
        # Stable operating mode text
        #
        mode_text_map = {
            1: "Normal Operation",
            7: "Unknown (7)",
        }

        ##
        if data.get("mode") in mode_text_map:
            data["mode_text"] = mode_text_map[data["mode"]]

        today = datetime.now().date()
		
        #
        # New day detected
        #
        if self._day != today:

            self._day = today
            self._max_today = 0.0

            #
            # Reset daily values until inverter reports new production
            #
            data["today"] = 0.0
            data["today_generated"] = 0.0
            data["power"] = 0.0
            data["vpv"] = 0.0
            data["iac"] = 0.0

            #
            # Last day used for cache reset
            #  20260805
            #   self._last_cache_day = None			

        value = data.get("today_generated")

        if value is not None:

            if value > self._max_today:
                self._max_today = value

            data["today_generated"] = self._max_today
			
            # oude sensor ook dezelfde waarde geven
            data["today"] = self._max_today

        #
        # Store last valid dataset
        #
        self._last_good_data = data.copy()


        #
        # Remember device information
        #
        if data.get("manufacturer"):
            self._manufacturer = data["manufacturer"]

        if data.get("model"):
            self._model = data["model"]

        if data.get("serial"):
            self._serial = data["serial"]

        if data.get("firmware"):
            self._firmware = data["firmware"]

        #
        # Schrijf cache asynchroon weg
        #
        await self._write_cache()

        #
        # Communication restored
        #
        if self._communication_lost:

            _LOGGER.warning(
                "FP4All %s communication restored",
                self.host,
            )

            self._communication_lost = False

        #
        # Remember last successful update
        #
        self._last_successful_update = datetime.now()

        #
        # Communication state
        #
        data["communication"] = "Connected"

        return data

        ##
