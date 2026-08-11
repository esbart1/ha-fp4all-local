"""
FP4All Local for Home Assistant

Version : 0.4
Build   : 3.0.0
File    : index_parser.py

Parser for index.htm.
"""

from __future__ import annotations

import logging
import re

_LOGGER = logging.getLogger(__name__)


def _find_big_value(html: str, label: str) -> str | None:
    """Find a <big> value behind a table label."""

    pattern = (
        rf"{re.escape(label)}</td>"
        rf"\s*<td><big>(.*?)</big>"
    )

    match = re.search(
        pattern,
        html,
        re.IGNORECASE | re.DOTALL,
    )

    if not match:
        return None

    return match.group(1).strip()


def _find_lifetime_hours(html: str) -> int | None:
    """Find lifetime operating hours."""

    pattern = (
        r"Lifetime generated energy</td>"
        r"\s*<td><big>.*?</big>\s*in\s*(\d+)\s*hours"
    )

    match = re.search(
        pattern,
        html,
        re.IGNORECASE | re.DOTALL,
    )

    if not match:
        return None

    return int(match.group(1))


def _to_float(value: str | None) -> float | None:
    """Convert value to float."""

    if value is None:
        return None

    value = (
        value.replace("kWh", "")
        .replace("kg", "")
        .replace("€", "")
        .replace(",", ".")
        .strip()
    )

    try:
        return float(value)

    except ValueError:
        return None


def parse_index(html: str) -> dict:
    """Parse index.htm."""

    data: dict = {}

    data["today_generated"] = _to_float(
        _find_big_value(
            html,
            "Todays generated energy",
        )
    )

    data["lifetime_generated"] = _to_float(
        _find_big_value(
            html,
            "Lifetime generated energy",
        )
    )

    data["lifetime_hours"] = _find_lifetime_hours(
        html
    )

    data["co2_saved"] = _to_float(
        _find_big_value(
            html,
            "Lifetime CO2 savings",
        )
    )

    data["earned"] = _to_float(
        _find_big_value(
            html,
            "Lifetime Earnings estimation",
        )
    )

    _LOGGER.debug(
        "Parsed index.htm: %s",
        data,
    )

    return data