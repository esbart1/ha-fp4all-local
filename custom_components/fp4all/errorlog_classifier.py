"""Non-destructive classification for FP4All error-log entries."""
from __future__ import annotations

from datetime import date, datetime
import logging

from astral import Observer
from astral.sun import sun
from homeassistant.util import dt as dt_util

_LOGGER = logging.getLogger(__name__)
DEFAULT_SUNSET_MARGIN_MINUTES = 45

_MONTHS = {
    "jan": 1, "feb": 2, "mar": 3, "apr": 4,
    "may": 5, "jun": 6, "jul": 7, "aug": 8,
    "sep": 9, "oct": 10, "nov": 11, "dec": 12,
}


def _parse_local_datetime(value: str | None, tzinfo) -> datetime | None:
    """Parse the logger's English date format as local HA time."""
    if not value or value.strip().lower() == "active":
        return None
    try:
        day_text, month_text, year_text, time_text = value.strip().split()
        return datetime(
            int(year_text), _MONTHS[month_text[:3].lower()],
            int(day_text), int(time_text[:2]), int(time_text[3:5]),
            tzinfo=tzinfo,
        )
    except (KeyError, TypeError, ValueError):
        return None


def _sun_events(hass, event_date: date, tzinfo):
    """Calculate historical sunrise/sunset using HA's configured location."""
    observer = Observer(
        latitude=hass.config.latitude,
        longitude=hass.config.longitude,
        elevation=hass.config.elevation,
    )
    events = sun(observer, date=event_date, tzinfo=tzinfo)
    return events["sunrise"], events["sunset"]


def _option(options: dict, key: str, default, cast):
    try:
        return cast(options.get(key, default))
    except (TypeError, ValueError):
        return default


def _classify_one(
    hass, error: dict, tzinfo, options: dict,
    power_confirmed: bool = False, current_event: bool = False
) -> dict:
    """Return metadata for one error without changing the original record."""
    code = (error.get("code") or "").strip().lower()
    message = (error.get("message") or "").strip()
    occurred = _parse_local_datetime(error.get("date_time"), tzinfo)
    recovered = _parse_local_datetime(error.get("recovery"), tzinfo)

    result = {
        "date_time": error.get("date_time"),
        "code": error.get("code"),
        "message": message,
        "severity": "warning",
        "classification": "unclassified",
        "is_expected": False,
        "explanation": "Deze melding is nog niet automatisch beoordeeld.",
    }

    if code == "0x00000820" or message.lower() == "bus-low-fail":
        result.update(
            classification="bus_low_fail_unconfirmed",
            explanation="DC-busspanning te laag; tijdstip en herstel worden getoetst aan de werkelijke zonstanden.",
        )
        if occurred is None:
            return result

        # One symmetric margin replaces the former before/after settings.
        # For existing entries that have not saved the new form yet, retain
        # the wider of the two old margins so the effective window is not
        # accidentally narrowed during the transition.
        legacy_before = _option(options, "sunset_before_minutes", DEFAULT_SUNSET_MARGIN_MINUTES, int)
        legacy_after = _option(options, "sunset_after_minutes", DEFAULT_SUNSET_MARGIN_MINUTES, int)
        sunset_margin = _option(
            options,
            "sunset_margin_minutes",
            max(legacy_before, legacy_after),
            int,
        )

        try:
            _, sunset = _sun_events(hass, occurred.date(), tzinfo)
        except Exception as err:
            _LOGGER.debug("Cannot calculate sunset for FP4All error: %s", err)
            return result

        sunset_delta = (occurred - sunset).total_seconds() / 60
        if abs(sunset_delta) > sunset_margin:
            result.update(
                classification="bus_low_fail_daytime",
                explanation=(
                    "Bus-Low-Fail viel buiten het ingestelde venster rond zonsondergang; "
                    "dit is geen automatisch verwachte nachtelijke overgang."
                ),
            )
            return result

        if recovered is None:
            result.update(
                classification="bus_low_fail_night_pending_recovery",
                explanation=(
                    "Bus-Low-Fail trad rond zonsondergang op, maar er is nog geen "
                    "herstelmoment geregistreerd. Wacht op herstel rond zonsopkomst."
                ),
            )
            return result

        try:
            sunrise, _ = _sun_events(hass, recovered.date(), tzinfo)
        except Exception as err:
            _LOGGER.debug("Cannot calculate sunrise for FP4All error: %s", err)
            return result

        # Sunrise is calculated from Home Assistant's location. There is no
        # fixed recovery cutoff after sunrise: cloud cover may delay normal
        # operation and production by considerably more than one hour.
        # A recovery timestamp before sunrise is not accepted as morning recovery.
        if recovered < sunrise:
            result.update(
                classification="bus_low_fail_recovery_before_sunrise",
                explanation=(
                    "De fout begon rond zonsondergang, maar het herstel is "
                    "vóór de berekende zonsopkomst geregistreerd. Dit geldt "
                    "niet als ochtendherstel."
                ),
            )
            return result

        if current_event:
            result.update(
                classification="bus_low_fail_waiting_for_production",
                explanation=(
                    "De fout begon rond zonsondergang en herstelde rond zonsopkomst. "
                    "Wacht op bevestiging dat de omvormer weer vermogen levert."
                ),
            )
        else:
            result.update(
                classification="bus_low_fail_night_pattern_unverified",
                explanation=(
                    "Het tijdspatroon past bij een nachtelijke overgang. Voor deze "
                    "historische melding is geen historische vermogensmeting rond herstel "
                    "beschikbaar; daarom wordt zij niet achteraf als OK bevestigd."
                ),
            )
        if power_confirmed:
            result.update(
                severity="normal",
                classification="bus_low_fail_expected_night",
                is_expected=True,
                explanation=(
                    "De nachtelijke Bus-Low-Fail viel binnen de ingestelde marge rond "
                    "zonsondergang; na zonsopkomst is gedurende de ingestelde tijd "
                    "voldoende vermogen geleverd."
                ),
            )
        return result

    if code in {
        "0x20020200", "0x20060200", "0x20520200",
        "0x0000001c", "0x0000001d",
    } or message.lower() == "no-utility":
        result.update(
            classification="grid_voltage_unavailable",
            explanation=(
                "De omvormer meldt geen bruikbare netspanning. De originele "
                "foutcode en eventuele meetwaarde blijven beschikbaar."
            ),
        )
        return result

    if code == "0x00040000" or message.lower() == "pv insulation low":
        result.update(
            severity="error",
            classification="pv_insulation_low",
            explanation=(
                "De omvormer meldt een te lage isolatieweerstand tussen PV en aarde. "
                "Dit wordt niet als normale nachtelijke overgang gezien."
            ),
        )
        return result

    if code in {"0x20500000", "0x00500000"} or message.lower().startswith("fac,zac,vac"):
        result.update(
            classification="master_slave_measurement_difference",
            explanation="De omvormer meldt een verschil tussen Master- en Slave-metingen.",
        )
        return result

    return result


def classify_error_log(
    hass, errors: list[dict], coordinator=None, options: dict | None = None
) -> list[dict]:
    """Classify errors separately; preserve input order and source records."""
    if not errors:
        return []
    tzinfo = dt_util.get_time_zone(hass.config.time_zone)
    if tzinfo is None:
        return [
            {
                "date_time": item.get("date_time"),
                "code": item.get("code"),
                "message": item.get("message", ""),
                "severity": "warning",
                "classification": "unclassified",
                "is_expected": False,
                "explanation": "Tijdzone van Home Assistant is niet beschikbaar.",
            }
            for item in errors
        ]
    options = options or {}
    today = dt_util.now().date()
    classified = []
    for index, item in enumerate(errors):
        # Live power can only validate the most recent event recovered today.
        # It must never retroactively validate older historical events.
        recovered = _parse_local_datetime(item.get("recovery"), tzinfo)
        current_event = (
            index == 0 and recovered is not None and recovered.date() == today
        )
        current_event_power_confirmed = (
            current_event
            and coordinator is not None
            and coordinator.recovery_power_confirmed_after(recovered)
        )
        classified.append(
            _classify_one(
                hass,
                item,
                tzinfo,
                options,
                current_event_power_confirmed,
                current_event,
            )
        )
    return classified
