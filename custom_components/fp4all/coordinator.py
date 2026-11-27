"""
FP4All Local for Home Assistant

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
from homeassistant.helpers.storage import Store
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.util import dt as dt_util

from .const import (
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
    STATUS_XML,
    ERRORLOG_HTML,
)
from .status import download_status
from .errorlog_parser import parse_errorlog
from .index import download_index
from .index_parser import parse_index
from .status_parser import parse_status
from .helpers.combine_high_low import combine_high_low

_LOGGER = logging.getLogger(__name__)

# These values describe the inverter/logger, not its momentary operating state.
# A temporarily incomplete status.htm must never erase a previously valid value.
_DEVICE_INFO_TEXT_KEYS = ("manufacturer", "model", "firmware", "serial")
_DEVICE_INFO_NUMBER_KEYS = (
    "capacity", "vac_min", "vac_max", "fac_min", "fac_max", "vpv_start", "t_start"
)
_DEVICE_INFO_KEYS = _DEVICE_INFO_TEXT_KEYS + _DEVICE_INFO_NUMBER_KEYS


def _valid_device_info_value(key: str, value) -> bool:
    """Return True only for a meaningful, non-empty device-information value."""
    if key in _DEVICE_INFO_TEXT_KEYS:
        return isinstance(value, str) and bool(value.strip()) and value.strip().lower() not in {
            "none", "unknown", "n/a", "null", "0"
        }
    try:
        number = float(value)
    except (TypeError, ValueError):
        return False
    return number > 0 and number < float("inf")


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
        self._daily_max_power_w = 0.0
        self._daily_max_power_time = None

        # Filled after parsing status.htm.
        self.status = {}

        # Device information.
        self._manufacturer: str | None = None
        self._model: str | None = None
        self._serial: str | None = None
        self._firmware: str | None = None

        # Last valid dataset (used during temporary communication loss).
        self._last_index: dict = {}
        self._last_good_data: dict = {}

        # Last valid operating mode.
        self._last_mode = None
        self._shutdown_since = None
        self._last_successful_update = None
        self._last_inverter_timestamp = None
        self._communication_lost = False
        self._communication_changed_at = None
        # Live evidence that the inverter has resumed producing after sunrise.
        self._power_above_since = None

        scan_interval = int(
            entry.options.get(
                "update_interval",
                DEFAULT_SCAN_INTERVAL.total_seconds(),
            )
        )

        self._communication_timeout = min(scan_interval * 3, 660)

        super().__init__(
            hass,
            _LOGGER,
            name=f"FP4All {host}",
            update_interval=timedelta(seconds=scan_interval),
        )

        # Persistent cache managed by Home Assistant.
        self._store = Store(
            hass,
            1,
            f"{DOMAIN}_{self.host.replace('.', '_')}_cache",
        )

        # Old cache location, used only for one-time migration.
        self._legacy_cache_file = Path(
            hass.config.path(
                "custom_components",
                "fp4all",
                "fp4all_cache",
                f"{self.host.replace('.', '_')}.json",
            )
        )

    async def async_load_cache(self) -> None:
        """Load Home Assistant storage, migrating the old JSON cache once."""
        try:
            cached_data = await self._store.async_load()
            if isinstance(cached_data, dict) and cached_data:
                self._last_good_data = cached_data
            else:
                def read_legacy_cache():
                    if self._legacy_cache_file.is_file():
                        return self._legacy_cache_file.read_text(encoding="utf-8")
                    return None

                legacy_text = await asyncio.to_thread(read_legacy_cache)

                if legacy_text is not None:
                    legacy_data = json.loads(legacy_text)
                    if isinstance(legacy_data, dict):
                        self._last_good_data = legacy_data
                        await self._store.async_save(legacy_data)
                        _LOGGER.info(
                            "Migrated FP4All cache for %s to Home Assistant storage",
                            self.host,
                        )

            self._manufacturer = self._last_good_data.get("manufacturer")
            self._model = self._last_good_data.get("model")
            self._serial = self._last_good_data.get("serial")
            self._firmware = self._last_good_data.get("firmware")
            self._communication_lost = self._last_good_data.get(
                "_communication_lost", False
            )
            self._communication_changed_at = self._last_good_data.get(
                "communication_changed_at"
            )

            # Daily values are only restored when the cache belongs to today.
            # Older caches without a date are treated as stale to avoid showing
            # yesterday's production after an upgrade/restart.
            today = dt_util.now().date()
            cached_day = self._last_good_data.get("today_cache_date")
            if cached_day == today.isoformat():
                self._day = today
                cached_today = self._last_good_data.get(
                    "today_generated",
                    self._last_good_data.get("today", 0.0),
                )
                try:
                    self._max_today = max(0.0, float(cached_today or 0.0))
                except (TypeError, ValueError):
                    self._max_today = 0.0
                self._last_good_data["today"] = self._max_today
                self._last_good_data["today_generated"] = self._max_today
            else:
                self._day = today
                self._max_today = 0.0
                self._last_good_data["today"] = 0.0
                self._last_good_data["today_generated"] = 0.0
                self._last_good_data["today_cache_date"] = today.isoformat()

            # Restore today's maximum live power and its timestamp only when
            # the persisted record belongs to the current local calendar day.
            if self._last_good_data.get("daily_max_power_date") == today.isoformat():
                try:
                    self._daily_max_power_w = max(
                        0.0, float(self._last_good_data.get("daily_max_power_w", 0.0))
                    )
                except (TypeError, ValueError):
                    self._daily_max_power_w = 0.0
                self._daily_max_power_time = self._last_good_data.get(
                    "daily_max_power_time"
                )
            else:
                self._daily_max_power_w = 0.0
                self._last_good_data["daily_max_power_date"] = today.isoformat()
                self._last_good_data["daily_max_power_w"] = 0.0
                self._daily_max_power_time = dt_util.now().replace(
                    hour=0, minute=10, second=0, microsecond=0
                ).isoformat(timespec="seconds")
                self._last_good_data["daily_max_power_time"] = self._daily_max_power_time
                await self._write_cache()

        except (OSError, ValueError, TypeError) as err:
            _LOGGER.warning("Cannot load FP4All cache for %s: %s", self.host, err)

    def recovery_power_confirmed_after(self, recovered_at) -> bool:
        """Check fresh sustained output that started no earlier than recovery."""
        if recovered_at is None or self._communication_lost:
            return False
        try:
            recovery_power_w = float(self.entry.options.get("recovery_power_w", 5))
            current_data = self.data or {}
            if current_data.get("communication") == "Communication lost":
                return False
            # A power reading alone is not enough: the inverter must report
            # Normal Operation (numeric operating mode 1).
            if current_data.get("mode") != 1:
                return False
            current_power = float(current_data.get("power", 0))
        except (TypeError, ValueError):
            return False
        if current_power <= 0 or current_power < recovery_power_w:
            return False

        # If output was already above threshold before the log's recovery time,
        # start a fresh confirmation interval at this first post-recovery check.
        if self._power_above_since is None or self._power_above_since < recovered_at:
            self._power_above_since = dt_util.now()

        try:
            duration_minutes = int(
                self.entry.options.get("recovery_power_duration_minutes", 5)
            )
        except (TypeError, ValueError):
            duration_minutes = 5
        return (
            dt_util.now() - self._power_above_since
        ).total_seconds() >= duration_minutes * 60

    async def _write_cache(self) -> None:
        """Persist the last valid dataset using Home Assistant storage."""
        try:
            await self._store.async_save(self._last_good_data)
        except (OSError, ValueError, TypeError) as err:
            _LOGGER.warning("Cannot save FP4All cache for %s: %s", self.host, err)

    async def _apply_offline_daily_rollover(self, data: dict) -> None:
        """Reset daily counters after midnight even when the inverter is offline.

        Only daily fields are copied into the persistent last-good cache.
        Cached measurements such as temperature, voltage and energy totals remain
        untouched; the temporary Power=0 W outage value is never cached.
        """
        today = dt_util.now().date()
        if self._day == today:
            return

        self._day = today
        self._max_today = 0.0
        self._daily_max_power_w = 0.0
        self._daily_max_power_time = dt_util.now().replace(
            hour=0, minute=10, second=0, microsecond=0
        ).isoformat(timespec="seconds")

        daily_values = {
            "today": 0.0,
            "today_generated": 0.0,
            "today_cache_date": today.isoformat(),
            "daily_max_power_w": 0.0,
            "daily_max_power_time": self._daily_max_power_time,
            "daily_max_power_date": today.isoformat(),
        }
        data.update(daily_values)
        # Persist only the intentional daily rollover, not transient outage data.
        self._last_good_data.update(daily_values)
        await self._write_cache()
        _LOGGER.info("FP4All %s daily counters reset for %s while offline", self.host, today)

    async def _async_update_data(self):
        """Fetch realtime values."""
        url = f"http://{self.host}/{STATUS_XML}"
        session = async_get_clientsession(self.hass)

        try:
            async with session.get(url, timeout=10) as response:
                response.raise_for_status()
                xml = await response.text()
        except (ClientError, TimeoutError, OSError) as err:
            self._power_above_since = None
            # Power is deliberately 0 W whenever communication is lost.
            # Keep all other last-known values in the returned data/cache.
            cached_data = self._last_good_data.copy()
            cached_data["power"] = 0.0
            if not self._communication_lost:
                self._communication_changed_at = dt_util.now().isoformat(timespec="seconds")
            cached_data["communication_changed_at"] = self._communication_changed_at
            cached_data["communication"] = "Communication lost"
            cached_data["mode"] = 3
            cached_data["mode_text"] = "Warning"
            self._communication_lost = True
            await self._apply_offline_daily_rollover(cached_data)
            if not self._last_good_data:
                _LOGGER.warning("Cannot connect to %s; no cached data available: %s", self.host, err)
            return cached_data

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
            inverter_timestamp = data.get("timestamp")
            if inverter_timestamp:
                self._last_inverter_timestamp = inverter_timestamp
        except Exception as err:
            self._power_above_since = None
            _LOGGER.warning("Invalid XML from %s; using last-known data: %s", self.host, err)
            cached_data = self._last_good_data.copy()
            cached_data["power"] = 0.0
            if not self._communication_lost:
                self._communication_changed_at = dt_util.now().isoformat(timespec="seconds")
            cached_data["communication_changed_at"] = self._communication_changed_at
            cached_data["communication"] = "Communication lost"
            cached_data["mode"] = 3
            cached_data["mode_text"] = "Warning"
            self._communication_lost = True
            await self._apply_offline_daily_rollover(cached_data)
            return cached_data

        # Read status.htm.
        try:
            html = await download_status(self)
            if html:
                self.status = parse_status(html)
                if self.status.get("pac") is not None:
                    data["power"] = self.status["pac"]

                for key in ("vac", "fac", "vpv", "iac", "temp"):
                    if self.status.get(key) is not None:
                        data[key] = self.status[key]

                for key in _DEVICE_INFO_KEYS:
                    value = self.status.get(key)
                    if _valid_device_info_value(key, value):
                        data[key] = value

                for key in ("mode", "etotalh", "etotall", "htotalh", "htotall"):
                    if self.status.get(key) is not None:
                        data[key] = self.status[key]

                # Keep FP4all's HIGH/LOW counter calculation unchanged.
                energy_total = combine_high_low(
                    self.status.get("etotalh"),
                    self.status.get("etotall"),
                )
                if energy_total is not None:
                    data["total"] = energy_total

        except Exception as err:
            if self._last_index:
                _LOGGER.warning("Using cached index.htm for %s", self.host)
                for key, value in self._last_index.copy().items():
                    if value is not None:
                        data[key] = value
            else:
                _LOGGER.warning("Unable to parse status.htm from %s: %s", self.host, err)

        # Read index.htm. Track whether today's value came from a fresh page;
        # a cached index must not reintroduce yesterday's production after midnight.
        index_is_fresh = False
        try:
            html = await download_index(self)
            if html:
                index = parse_index(html)
                index_is_fresh = True
                self._last_index = index.copy()
                for key, value in index.items():
                    if value is not None:
                        data[key] = value
        except Exception:
            if self._last_index:
                _LOGGER.warning("Using cached index.htm for %s", self.host)
                for key, value in self._last_index.copy().items():
                    if value is not None:
                        data[key] = value

        # Preserve the last known valid device information if status.htm is
        # temporarily empty, incomplete, or still starting up at sunrise.
        for key in _DEVICE_INFO_KEYS:
            if not _valid_device_info_value(key, data.get(key)):
                cached_value = self._last_good_data.get(key)
                if _valid_device_info_value(key, cached_value):
                    data[key] = cached_value

        # Read errorlog.htm independently from the regular status/energy parsers.
        # If the page is temporarily unavailable, retain the last known history.
        try:
            errorlog_url = f"http://{self.host}/{ERRORLOG_HTML}"
            async with session.get(errorlog_url, timeout=10) as response:
                response.raise_for_status()
                errorlog_html = await response.text()
            data["error_log"] = parse_errorlog(errorlog_html)
        except Exception as err:
            data["error_log"] = self._last_good_data.get("error_log", [])
            _LOGGER.debug(
                "Unable to download/parse errorlog.htm from %s; keeping cached log: %s",
                self.host,
                err,
            )

        # A cumulative lifetime counter must never move backwards. This also
        # protects against temporary zero/partial values during logger startup.
        # Compare the combined total only; HIGH=0 can be valid by itself.
        previous_total = self._last_good_data.get("total")
        current_total = data.get("total")
        try:
            previous_total_value = (
                float(previous_total) if previous_total is not None else None
            )
            current_total_value = (
                float(current_total) if current_total is not None else None
            )
        except (TypeError, ValueError):
            previous_total_value = None
            current_total_value = None

        if (
            previous_total_value is not None
            and current_total_value is not None
            and current_total_value < previous_total_value
        ):
            _LOGGER.warning(
                "Ignoring lower lifetime total from %s (%.3f < %.3f); "
                "keeping last valid value",
                self.host,
                current_total_value,
                previous_total_value,
            )
            data["total"] = previous_total_value

        # Keep the raw mode reported by this poll for measurement gating.
        # The display mode below may briefly retain the previous mode during
        # transitions, but cached measurements must use the actual reported mode.
        reported_mode = data.get("mode")

        # Stable operating mode filter.
        mode = data.get("mode")
        pv_start = data.get("vpv_start")
        if pv_start is None or pv_start <= 0:
            pv_threshold = 90
        else:
            pv_threshold = max(90, pv_start * 0.70)

        pv_ok = data.get("vpv", 0) >= pv_threshold
        power_ok = data.get("power", 0) > 0
        inverter_running = pv_ok and power_ok

        if inverter_running:
            self._shutdown_since = None
            if mode == 7 and self._last_mode is not None:
                data["mode"] = self._last_mode
            elif mode != 7:
                self._last_mode = mode
        elif mode == 7:
            if self._shutdown_since is None:
                self._shutdown_since = datetime.now()
            elapsed = (datetime.now() - self._shutdown_since).total_seconds()
            if elapsed < 30 and self._last_mode is not None:
                data["mode"] = self._last_mode

        if data.get("mode") is not None and data.get("mode") != 7:
            self._last_mode = data.get("mode")

        # Sunrise/startup guard: only accept these cumulative/grid measurements
        # while the inverter explicitly reports Normal Operation (mode 1).
        # In every other mode, retain the last known values so transient startup
        # zeros cannot overwrite the persistent cache or create graph dips.
        # The guard is deliberately limited to values that should remain stable
        # while the inverter is stopped; live production values such as power,
        # PV voltage/current and daily energy are handled separately.
        _MODE_1_ONLY_CACHE_KEYS = (
            "vac",
            "fac",
            "hours",
            "lifetime_hours",
            "htotalh",
            "htotall",
            "etotalh",
            "etotall",
            "total",
        )
        if reported_mode != 1:
            for key in _MODE_1_ONLY_CACHE_KEYS:
                cached_value = self._last_good_data.get(key)
                if cached_value is not None:
                    data[key] = cached_value

        mode_text_map = {1: "Normal Operation", 7: "Unknown (7)"}
        if data.get("mode") in mode_text_map:
            data["mode_text"] = mode_text_map[data["mode"]]

        # Capture this update's live power before daily energy rollover resets
        # display values. XML was fetched successfully above, so this is a fresh
        # measurement (cached outage paths return earlier).
        observed_power = data.get("power")
        observed_at = dt_util.now()

        # Use Home Assistant's configured local timezone for the day boundary.
        today = observed_at.date()
        new_day = self._day != today
        if new_day:
            self._day = today
            self._max_today = 0.0
            self._daily_max_power_w = 0.0
            self._daily_max_power_time = observed_at.replace(
                hour=0, minute=10, second=0, microsecond=0
            ).isoformat(timespec="seconds")
            data["today"] = 0.0
            data["today_generated"] = 0.0
            data["power"] = 0.0
            # Do not clear PV voltage at midnight: it is held at its last
            # known valid value until mode 1 supplies a fresh measurement.
            data["iac"] = 0.0

        value = data.get("today_generated")
        if new_day and not index_is_fresh:
            # Do not carry forward a cached index value across the day boundary.
            value = None

        if value is not None:
            if value > self._max_today:
                self._max_today = value

        # Keep the daily sensors aligned with the in-memory/cache high-water mark,
        # including when index.htm is temporarily unavailable.
        data["today_generated"] = self._max_today
        data["today"] = self._max_today

        # Track the highest fresh live power sample for this local day.
        try:
            numeric_power = float(observed_power)
        except (TypeError, ValueError):
            numeric_power = 0.0
        if numeric_power > self._daily_max_power_w:
            self._daily_max_power_w = numeric_power
            self._daily_max_power_time = observed_at.isoformat(timespec="seconds")

        data["daily_max_power_w"] = self._daily_max_power_w
        data["daily_max_power_time"] = self._daily_max_power_time
        data["daily_max_power_date"] = today.isoformat()

        # Record the date belonging to the daily values in the persistent cache.
        data["today_cache_date"] = today.isoformat()

        # Track sustained real-time output. A cached value or a PV voltage alone
        # is not sufficient evidence that the inverter has resumed production.
        try:
            recovery_power_w = float(self.entry.options.get("recovery_power_w", 5))
        except (TypeError, ValueError):
            recovery_power_w = 5.0
        current_power = data.get("power")
        now = dt_util.now()
        try:
            has_output = (
                current_power is not None
                and float(current_power) > 0
                and float(current_power) >= recovery_power_w
            )
        except (TypeError, ValueError):
            has_output = False
        # Count recovery evidence only while the inverter reports
        # Normal Operation (mode 1) and delivers sufficient real power.
        if has_output and data.get("mode") == 1:
            if self._power_above_since is None:
                self._power_above_since = now
        else:
            self._power_above_since = None

        # Record the moment communication became/restored connected. Keep the
        # timestamp stable during ordinary polling updates.
        previous_communication = self._last_good_data.get("communication")
        if self._communication_lost or previous_communication != "Connected":
            self._communication_changed_at = dt_util.now().isoformat(timespec="seconds")
        elif self._communication_changed_at is None:
            self._communication_changed_at = self._last_good_data.get(
                "communication_changed_at", dt_util.now().isoformat(timespec="seconds")
            )
        data["communication_changed_at"] = self._communication_changed_at
        data["communication"] = "Connected"

        # Store last valid dataset.
        self._last_good_data = data.copy()

        if _valid_device_info_value("manufacturer", data.get("manufacturer")):
            self._manufacturer = data["manufacturer"]
        if _valid_device_info_value("model", data.get("model")):
            self._model = data["model"]
        if _valid_device_info_value("serial", data.get("serial")):
            self._serial = data["serial"]
        if _valid_device_info_value("firmware", data.get("firmware")):
            self._firmware = data["firmware"]

        # Once the device has been registered, update its visible HA device
        # information automatically when a fresh valid status page is read.
        # This also repairs a generic "FP4All Logger" entry without manual reload.
        registry = dr.async_get(self.hass)
        main_identifier = (DOMAIN, self.entry.entry_id)
        if hasattr(registry, "async_get_device_by_identifier"):
            device = registry.async_get_device_by_identifier(
                main_identifier, self.entry.entry_id
            )
        else:
            # Compatibility with Home Assistant versions before 2026.8.
            device = registry.async_get_device(identifiers={main_identifier})
        if device is not None:
            device_info_updates = {}
            if self._manufacturer:
                device_info_updates["manufacturer"] = self._manufacturer
            if self._model:
                device_info_updates["model"] = self._model
            if self._firmware:
                device_info_updates["sw_version"] = self._firmware
            if self._serial:
                device_info_updates["serial_number"] = self._serial
            if device_info_updates:
                registry.async_update_device(device.id, **device_info_updates)

        # Keep the separate FP4All Status device entry in sync with the actual
        # inverter model/manufacturer shown on the main device.
        status_identifier = (DOMAIN, f"{self.entry.entry_id}_status_panel")
        if hasattr(registry, "async_get_device_by_identifier"):
            status_device = registry.async_get_device_by_identifier(
                status_identifier, self.entry.entry_id
            )
        else:
            # Compatibility with Home Assistant versions before 2026.8.
            status_device = registry.async_get_device(
                identifiers={status_identifier}
            )
        if status_device is not None:
            status_updates = {}
            if self._manufacturer:
                status_updates["manufacturer"] = self._manufacturer
            if self._model:
                status_updates["model"] = self._model
            if status_updates:
                dr.async_get(self.hass).async_update_device(
                    status_device.id, **status_updates
                )

        await self._write_cache()

        if self._communication_lost:
            _LOGGER.warning("FP4All %s communication restored", self.host)
            self._communication_lost = False

        self._last_successful_update = datetime.now()
        return data
