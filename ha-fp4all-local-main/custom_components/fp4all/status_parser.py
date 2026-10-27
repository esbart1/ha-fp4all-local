"""
FP4All Local for Home Assistant

Version : 0.4
Build   : 3.0.2
File    : status_parser.py

Parses status.htm from the FP4All logger.
"""
from __future__ import annotations

import logging
import re

_LOGGER = logging.getLogger(__name__)

def _find_value(html: str, label: str) -> str | None:
    """Return the value belonging to a table label."""

    patterns = [
        # normale tabel
        rf"<td[^>]*>\s*{re.escape(label)}\s*</td>\s*"
        rf"<td[^>]*>\s*([^<]+)",

        # waarde in div (zoals Serial)
        rf"<td[^>]*>\s*{re.escape(label)}\s*</td>\s*"
        rf"<td[^>]*>.*?<div[^>]*>\s*([^<]+)",
    ]

    for pattern in patterns:
        match = re.search(
            pattern,
            html,
            re.IGNORECASE | re.DOTALL,
        )

        if match:
            value = match.group(1).strip()

            _LOGGER.debug(
                "FOUND %s = %s",
                label,
                value,
            )

            return value

    _LOGGER.warning(
        "NOT FOUND: %s",
        label,
    )

    return None
	
def _to_float(value: str | None) -> float | None:
    """Convert a value to float."""

    if value is None:
        return None

    value = (
        value.replace("kWh", "")
        .replace("Hz", "")
        .replace("Sec", "")
        .replace("hrs", "")
        .replace("V", "")
        .replace("A", "")
        .replace("W", "")
        .replace("C", "")
        .strip()
    )

    try:
        return float(value)
    except ValueError:
        _LOGGER.warning("FLOAT CONVERSION FAILED: %s", value)
        return None

def _to_int(value: str | None) -> int | None:
    """Convert a value to integer."""

    if value is None:
        return None

    digits = re.findall(r"\d+", value)

    if not digits:
        return None

    return int(digits[0])

def _combine_counter(
    high: float | int | None,
    low: float | int | None,
    multiplier: int,
) -> float | None:
    """Combine high and low counter."""

    if high is None:
        return None

    if low is None:
        low = 0

    return float(high) * multiplier + float(low)


def _mode_text(mode: int | None) -> str | None:
    """Return human readable inverter mode."""

    modes = {
        0: "Standby",
        1: "Normal Operation",
        2: "Fault",
        3: "Warning",
        4: "Starting",
        5: "Stopping",
        6: "Test",
    }

    if mode is None:
        return None

    return modes.get(mode, f"Unknown ({mode})")

def parse_status(html: str) -> dict:
    """Parse status.htm."""

    data: dict = {}

    #
    # Live inverter values
    #
    data["temp"] = _to_float(_find_value(html, "TEMP"))
    data["vpv"] = _to_float(_find_value(html, "VPV"))
    data["iac"] = _to_float(_find_value(html, "IAC"))
    data["vac"] = _to_float(_find_value(html, "VAC"))
    data["fac"] = _to_float(_find_value(html, "FAC"))
    data["pac"] = _to_float(_find_value(html, "PAC"))

    #
    # Energy counters
    #
    #data["today"] = _to_float(_find_value(html, "ETODAY"))
    data["etotalh"] = _to_float(_find_value(html, "ETOTALH"))
    data["etotall"] = _to_float(_find_value(html, "ETOTALL"))

    data["htotalh"] = _to_int(_find_value(html, "HTOTALH"))
    data["htotall"] = _to_int(_find_value(html, "HTOTALL"))

    #
    # Device information
    #
    data["manufacturer"] = _find_value(html, "Manuf")
    data["model"] = _find_value(html, "Model")
    data["firmware"] = _find_value(html, "Firmware")
    data["serial"] = _find_value(html, "Serial")
    data["capacity"] = _to_int(_find_value(html, "Capacity"))

    #
    # Operating limits
    #
    data["vpv_start"] = _to_float(
        _find_value(html, "VPV-START")
    )

    data["t_start"] = _to_float(
        _find_value(html, "T-START")
    )

    data["vac_min"] = _to_float(
        _find_value(html, "VAC-MIN")
    )

    data["vac_max"] = _to_float(
        _find_value(html, "VAC-MAX")
    )

    data["fac_min"] = _to_float(
        _find_value(html, "FAC-MIN")
    )

    data["fac_max"] = _to_float(
        _find_value(html, "FAC-MAX")
    )

    #
    # Operating mode
    #
    data["mode"] = _to_int(
        _find_value(html, "MODE")
    )

    data["mode_text"] = _mode_text(
        data["mode"]
    )

    # Debug hulp zie log file
    # _LOGGER.debug("Parsed status.htm: %s", data)
    # _LOGGER.warning("Parsed status.htm: %s", data)

    #LOGGER.warning(
    #   "PARSED ENERGY H=%s L=%s",
    #   data["etotalh"],
    #   data["etotall"],
    #

    # _LOGGER.warning("STATUS PARSED = %s", data)

    return data