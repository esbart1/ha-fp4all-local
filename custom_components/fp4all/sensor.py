"""
FP4All Local for Home Assistant

Sensor platform for FP4All.
"""

from __future__ import annotations

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfPower,
    UnitOfTemperature,
    UnitOfTime,
    UnitOfFrequency,
)

from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, MANUFACTURER
from .coordinator import FP4AllCoordinator


SENSORS = (
    (
        "power",
        "Power",
        UnitOfPower.WATT,
        SensorDeviceClass.POWER,
        SensorStateClass.MEASUREMENT,
    ),
    (
        "temp",
        "Temperature",
        UnitOfTemperature.CELSIUS,
        SensorDeviceClass.TEMPERATURE,
        SensorStateClass.MEASUREMENT,
    ),
    (
        "vpv",
        "PV Voltage",
        UnitOfElectricPotential.VOLT,
        SensorDeviceClass.VOLTAGE,
        SensorStateClass.MEASUREMENT,
    ),
    (
        "vac",
        "AC Voltage",
        UnitOfElectricPotential.VOLT,
        SensorDeviceClass.VOLTAGE,
        SensorStateClass.MEASUREMENT,
    ),
    (
        "fac",
        "AC Frequency",
        UnitOfFrequency.HERTZ,
        SensorDeviceClass.FREQUENCY,
        SensorStateClass.MEASUREMENT,
    ),
    (
        "iac",
        "AC Current",
        UnitOfElectricCurrent.AMPERE,
        SensorDeviceClass.CURRENT,
        SensorStateClass.MEASUREMENT,
    ),
    (
        "today",
        "Energy Today",
        "kWh",
        SensorDeviceClass.ENERGY,
        SensorStateClass.TOTAL_INCREASING,
    ),
    (
        "total",
        "Energy Total",
        "kWh",
        SensorDeviceClass.ENERGY,
        SensorStateClass.TOTAL_INCREASING,
    ),
    (
        "hours",
        "Operating Hours",
        UnitOfTime.HOURS,
        SensorDeviceClass.DURATION,
        SensorStateClass.TOTAL_INCREASING,
    ),

    #
    # Extra uit status.htm
    #

    (
        "capacity",
        "Inverter Capacity",
        UnitOfPower.WATT,
        SensorDeviceClass.POWER,
        None,
    ),
    (
        "vac_min",
        "AC Voltage Min",
        UnitOfElectricPotential.VOLT,
        SensorDeviceClass.VOLTAGE,
        None,
    ),
    (
        "vac_max",
        "AC Voltage Max",
        UnitOfElectricPotential.VOLT,
        SensorDeviceClass.VOLTAGE,
        None,
    ),
    (
        "fac_min",
        "AC Frequency Min",
        UnitOfFrequency.HERTZ,
        SensorDeviceClass.FREQUENCY,
        None,
    ),
    (
        "fac_max",
        "AC Frequency Max",
        UnitOfFrequency.HERTZ,
        SensorDeviceClass.FREQUENCY,
        None,
    ),
    (
        "vpv_start",
        "PV Start Voltage",
        UnitOfElectricPotential.VOLT,
        SensorDeviceClass.VOLTAGE,
        None,
    ),
    (
        "t_start",
        "Start Delay",
        UnitOfTime.SECONDS,
        SensorDeviceClass.DURATION,
        None,
    ),
    (
        "mode",
        "Operating Mode",
        None,
        None,
        None,
    ),
    (
        "timestamp",
        "Timestamp",
        None,
        None,
        None,
    ),
    (
        "mode_text",
        "Operating Mode Text",
        None,
        None,
        None,
    ),

    (
        "communication",
        "Communication",
        None,
        None,
        None,
    ),

    (
        "etotalh",
        "Energy Total High",
        "kWh",
        SensorDeviceClass.ENERGY,
        None,
    ),

    (
        "etotall",
        "Energy Total Low",
        "kWh",
        SensorDeviceClass.ENERGY,
        None,
    ),

    (
        "htotalh",
        "Operating Hours High",
        UnitOfTime.HOURS,
        SensorDeviceClass.DURATION,
        None,
    ),

    (
        "htotall",
        "Operating Hours Low",
        UnitOfTime.HOURS,
        SensorDeviceClass.DURATION,
        None,
    ),
    (
        "today_generated",
        "Today's Generated Energy",
        "kWh",
        SensorDeviceClass.ENERGY,
        SensorStateClass.TOTAL_INCREASING,
    ),

    (
        "lifetime_generated",
        "Lifetime Generated Energy",
        "kWh",
        SensorDeviceClass.ENERGY,
        SensorStateClass.TOTAL_INCREASING,
    ),

    (
        "lifetime_hours",
        "Lifetime Operating Hours",
        UnitOfTime.HOURS,
        SensorDeviceClass.DURATION,
        SensorStateClass.TOTAL_INCREASING,
    ),

    (
        "co2_saved",
        "Lifetime CO₂ Saved",
        "kg",
        None,
        SensorStateClass.TOTAL_INCREASING,
    ),

    (
        "earned",
        "Lifetime Earnings",
        "€",
        None,
        None,
    ),
    (
        "daily_max_power_w",
        "Maximum Power Today",
        UnitOfPower.WATT,
        SensorDeviceClass.POWER,
        SensorStateClass.MEASUREMENT,
    ),
    (
        "max_power_time",
        "Max Power Time",
        None,
        None,
        None,
    ),
    (
        "bus_low_fail_status",
        "Bus-Low-Fail Status",
        None,
        None,
        None,
    ),
    (
        "error_log",
        "Error Log",
        None,
        None,
        None,
    ),
    )
# Existing entities in this set are reassigned to the dedicated child
# "Statuspaneel" device. Their unique IDs remain unchanged.
_STATUS_PANEL_KEYS = {
    # Communication, operating state and fault information.
    "communication",
    "mode",
    "mode_text",
    "bus_low_fail_status",
    "error_log",
    "panel_last_error",
    "panel_last_recovery_time",
    "panel_sunrise",
    "panel_sunset",
    # Fixed or semi-fixed technical and operating information.
    "capacity",
    "vac",
    "fac",
    "vac_min",
    "vac_max",
    "fac_min",
    "fac_max",
    "vpv_start",
    "t_start",
    "hours",
    "htotalh",
    "htotall",
    "lifetime_hours",
    "etotalh",
    "etotall",
    "timestamp",
    "max_power_time",
}

# Additional status-panel entities for information not already exposed as a
# dedicated sensor by the original integration.
STATUS_PANEL_SENSORS = (
    ("panel_last_error", "Laatste Bus-Low-Fail", None, None, None),
    ("panel_last_recovery_time", "Laatste fout-/herstelregistratie", None, None, None),
    ("panel_sunrise", "Zonsopkomst", None, None, None),
    ("panel_sunset", "Zonsondergang", None, None, None),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: FP4AllCoordinator = hass.data[DOMAIN][entry.entry_id]

    # Add inverter entities before status-panel entities so the parent device
    # exists before the child device resolves its via_device_id.
    entities = [
        FP4AllSensor(coordinator, entry, *description)
        for description in SENSORS
        if description[0] not in _STATUS_PANEL_KEYS
    ]
    entities.extend(
        FP4AllSensor(coordinator, entry, *description)
        for description in SENSORS
        if description[0] in _STATUS_PANEL_KEYS
    )
    entities.extend(
        FP4AllStatusPanelSensor(coordinator, entry, *description)
        for description in STATUS_PANEL_SENSORS
    )
    async_add_entities(entities)


class FP4AllSensor(
    CoordinatorEntity,
    SensorEntity,
):
    """FP4All sensor."""

    def __init__(
        self,
        coordinator,
        entry,
        key,
        name,
        unit,
        device_class,
        state_class,
    ):
        super().__init__(coordinator)

        self._key = key

        # Use translation keys for every entity name and translatable state.
        # Unique IDs are unchanged, so existing entity registry entries remain
        # associated with the same sensors.
        self._attr_unique_id = f"{entry.entry_id}_{key}"
        self._attr_native_unit_of_measurement = unit
        self._attr_device_class = device_class
        self._attr_state_class = state_class
        self._attr_has_entity_name = True
        self._attr_translation_key = key

        self._entry = entry

    @property
    def device_info(self):
        """Return device information."""

        status = self.coordinator.status
        manufacturer = (
            status.get("manufacturer")
            or self.coordinator._manufacturer
            or MANUFACTURER
        )

        if self._key in _STATUS_PANEL_KEYS:
            return DeviceInfo(
                identifiers={(DOMAIN, f"{self._entry.entry_id}_status_panel")},
                via_device_id=dr.async_get_device_id_by_identifier(
                    self.coordinator.hass,
                    (DOMAIN, self._entry.entry_id),
                    config_entry_id=self._entry.entry_id,
                ),
                manufacturer=manufacturer,
                # Reuse the detected inverter model for the child status device.
                # The status page may report a generic "FP4All Status" label.
                model=(
                    self.coordinator._model
                    or status.get("model")
                    or "FP4All Status"
                ),
                name=f"{self._entry.title} - Status",
                configuration_url=f"http://{self.coordinator.host}",
            )

        return DeviceInfo(
            identifiers={(DOMAIN, self._entry.entry_id)},
            manufacturer=manufacturer,
            model=(
                status.get("model")
                or self.coordinator._model
                or "FP4All Logger"
            ),
            sw_version=(
                status.get("firmware")
                or self.coordinator._firmware
            ),
            serial_number=(
                status.get("serial")
                or self.coordinator._serial
            ),
            name=self._entry.title,
            configuration_url=f"http://{self.coordinator.host}",
        )


    def _latest_bus_low_fail(self):
        """Return the newest Bus-Low-Fail record and its classification."""
        errors = self.coordinator.data.get("error_log", [])
        from .errorlog_classifier import classify_error_log

        classified = classify_error_log(
            self.hass,
            errors,
            coordinator=self.coordinator,
            options=self._entry.options,
        )
        for error, result in zip(errors, classified):
            code = (error.get("code") or "").strip().lower()
            message = (error.get("message") or "").strip().lower()
            if code == "0x00000820" or message == "bus-low-fail":
                return error, result
        return None, None

    @property
    def native_value(self):
        """Return sensor value."""
        if self._key == "max_power_time":
            value = self.coordinator.data.get("daily_max_power_time")
            if not value:
                return None
            try:
                from datetime import datetime
                parsed = datetime.fromisoformat(value)
                return parsed.strftime("%Y%m%d %H:%M")
            except (TypeError, ValueError):
                return value

        if self._key == "communication":
            value = self.coordinator.data.get("communication")
            changed_at = self.coordinator.data.get("communication_changed_at")
            try:
                from datetime import datetime
                timestamp = datetime.fromisoformat(changed_at).astimezone().strftime("%H:%M") if changed_at else None
            except (TypeError, ValueError):
                timestamp = None

            # Communication status is intentionally displayed in English.
            # The time is appended only when a status-change timestamp exists.
            if value == "Connected":
                label = "Connected"
            elif value == "Communication lost":
                label = "Connection lost"
            else:
                return "Unavailable"
            return f"{label} {timestamp}" if timestamp else label

        if self._key == "mode_text":
            # The coordinator may deliberately override the displayed mode to
            # Warning during a communication outage. Translate the current
            # textual mode, rather than relying only on the retained numeric code.
            value = (self.coordinator.data.get("mode_text") or "").strip().lower()
            mode_states = {
                "standby": "standby",
                "normal operation": "normal_operation",
                "fault": "fault",
                "warning": "warning",
                "starting": "starting",
                "stopping": "stopping",
                "test": "test",
            }
            if value.startswith("unknown"):
                return "unknown"
            return mode_states.get(value, "unknown")

        if self._key == "bus_low_fail_status":
            error, result = self._latest_bus_low_fail()
            if result is None:
                return "no_bus_low_fail"

            recovery = (error.get("recovery") or "").strip()
            if recovery and recovery.lower() != "active":
                return "recovery_registered"
            return "active_waiting_for_recovery"

        if self._key == "error_log":
            errors = self.coordinator.data.get("error_log", [])
            if not errors:
                return "no_errors_recorded"

            latest = errors[0]
            message = (latest.get("message") or "").strip()
            code = (latest.get("code") or "").strip().lower()

            # Known No-Utility codes are also normalized, in case the logger
            # supplies a different wording for the message field.
            no_utility_codes = {
                "0x20020200",
                "0x20060200",
                "0x20520200",
                "0x0000001c",
                "0x0000001d",
            }
            if (
                message.lower() in {"no-utility", "no utility", "no grid voltage detected"}
                or code in no_utility_codes
            ):
                return "no_utility"

            # Bus-Low-Fail is the logger's technical message for a low DC bus
            # voltage. Keep the raw code and message in Error Log attributes,
            # but show a short localized description as the sensor state.
            if (
                code == "0x00000820"
                or message.lower() in {
                    "bus-low-fail",
                    "bus low fail",
                    "dc bus voltage is too low",
                    "dc bus voltage too low",
                }
            ):
                return "bus_low_fail"

            if code == "0x00040000" or message.lower() == "pv insulation low":
                return "pv_insulation_low"

            if (
                code in {"0x20500000", "0x00500000"}
                or message.lower().startswith("fac,zac,vac")
            ):
                return "master_slave_measurement_difference"

            # Unknown logger messages are deliberately preserved verbatim so
            # diagnostics are not lost or incorrectly translated.
            return message or "error_recorded"

        value = self.coordinator.data.get(
            self._key
        )

        if value is None:
            value = self.coordinator.status.get(
                self._key
            )

        return value
#		
    @property
    def extra_state_attributes(self):
        """Expose a compact view; the complete history remains in persistent cache."""
        if self._key == "daily_max_power_w":
            # Expose the peak time on Max Power Today, while keeping the
            # separate max_power_time entity available for existing dashboards.
            value = self.coordinator.data.get("daily_max_power_time")

            # The coordinator also keeps this value in memory and in its
            # last-good cache. Use those as fallbacks if the current update
            # payload does not contain the timestamp.
            if value in (None, ""):
                value = getattr(self.coordinator, "_daily_max_power_time", None)
            if value in (None, ""):
                value = getattr(self.coordinator, "_last_good_data", {}).get(
                    "daily_max_power_time"
                )

            if value in (None, ""):
                return {"time": "Unavailable"}

            try:
                from datetime import datetime
                from homeassistant.util import dt as dt_util

                if isinstance(value, datetime):
                    parsed = value
                else:
                    parsed = datetime.fromisoformat(str(value))

                if parsed.tzinfo is not None:
                    parsed = dt_util.as_local(parsed)
                value = parsed.strftime("%Y%m%d %H:%M")
            except (TypeError, ValueError, OverflowError):
                # Preserve an unparseable source value rather than hiding it.
                value = str(value)

            return {"time": value}

        if self._key != "error_log":
            return None

        errors = self.coordinator.data.get("error_log", [])

        from .errorlog_classifier import classify_error_log

        classified_errors = classify_error_log(
            self.hass,
            errors,
            coordinator=self.coordinator,
            options=self._entry.options,
        )

        # Keep only a small recent sample in entity attributes. The coordinator's
        # persistent Store continues to retain the complete, unmodified error_log.
        # The original logger message/description stay available for diagnostics;
        # explanatory text is exposed separately through translatable scalar attrs.
        recent_errors = []
        for error, classification in zip(errors[:5], classified_errors[:5]):
            recent_errors.append({
                **error,
                "severity": classification.get("severity"),
                "classification": classification.get("classification"),
                "is_expected": classification.get("is_expected"),
            })

        # Compact totals across the complete cached history.
        classification_summary = {}
        for classification in classified_errors:
            category = classification.get("classification", "unclassified")
            classification_summary[category] = (
                classification_summary.get(category, 0) + 1
            )

        latest_classification = classified_errors[0] if classified_errors else {}
        classification_key = latest_classification.get("classification", "unclassified")
        severity_key = latest_classification.get("severity", "warning")
        communication_value = self.coordinator.data.get("communication")
        if communication_value == "Connected":
            communication_state = "connected"
        elif communication_value == "Communication lost":
            communication_state = "communication_lost"
        else:
            communication_state = "unavailable"

        return {
            "last_error": errors[0] if errors else None,
            "last_error_classification": {
                "classification": classification_key,
                "is_expected": latest_classification.get("is_expected", False),
            } if latest_classification else None,
            "last_error_severity": severity_key,
            "last_error_explanation": classification_key,
            "error_count": len(errors),
            "communication": communication_state,
            "classification_summary": classification_summary,
            "recent_errors": recent_errors,
        }

    @property	
    def suggested_display_precision(self):
        """Display precision."""

        if self._key in (
            "fac",
            "fac_min",
            "fac_max",
        ):
            return 2

        if self._key in (
            "vac",
		    "vac_min",
			"vac_max",
            "vpv",
			"vpv_start",
            "iac",
            "temp",
        ):
            return 1

        if self._key in (
            "today",
            "today_generated",
        ):
            return 3

        if self._key in (
            "total",
            "lifetime_generated",
        ):
            return 1

        if self._key == "earned":
            return 2

        if self._key == "co2_saved":
            return 2

        return None




class FP4AllStatusPanelSensor(FP4AllSensor):
    """Compact diagnostic entities for the dedicated inverter status panel."""

    def __init__(self, coordinator, entry, key, name, unit, device_class, state_class):
        super().__init__(coordinator, entry, key, name, unit, device_class, state_class)
        self._attr_unique_id = f"{entry.entry_id}_status_panel_{key}"

    def _sun_time(self, event_name: str):
        from astral import Observer
        from astral.sun import sun
        from homeassistant.util import dt as dt_util

        now = dt_util.now()
        observer = Observer(
            latitude=self.hass.config.latitude,
            longitude=self.hass.config.longitude,
            elevation=self.hass.config.elevation,
        )
        return sun(observer, date=now.date(), tzinfo=now.tzinfo)[event_name].strftime("%H:%M")

    @property
    def native_value(self):
        """Return the compact status-panel values."""
        if self._key == "panel_last_error":
            error, _result = self._latest_bus_low_fail()
            if error is None:
                return "no_bus_low_fail"
            # Show the date and time of the latest Bus-Low-Fail record as the
            # sensor state. The message/code remain available in attributes.
            timestamp = (error.get("date_time") or "").strip()
            return timestamp or "no_datetime"

        if self._key == "panel_last_recovery_time":
            # The error log is returned newest first. Show the latest record's
            # recovery timestamp when present; otherwise show the fault date so
            # the panel still gives the user a meaningful date instead of an
            # ambiguous "Geen herstelmoment" state.
            errors = self.coordinator.data.get("error_log", [])
            if not errors:
                return "no_data"

            latest = errors[0]
            recovery = (latest.get("recovery") or "").strip()
            if recovery and recovery.lower() not in {
                "active", "unknown", "none", "n/a", "-"
            }:
                return recovery

            fault_time = (latest.get("date_time") or "").strip()
            return fault_time or "no_data"

        if self._key == "panel_sunrise":
            try:
                return self._sun_time("sunrise")
            except Exception:
                return "unavailable"

        if self._key == "panel_sunset":
            try:
                return self._sun_time("sunset")
            except Exception:
                return "unavailable"

        return super().native_value

    @property
    def extra_state_attributes(self):
        """Keep the status-panel timestamp entities concise: date and time only."""
        if self._key in {"panel_last_error", "panel_last_recovery_time"}:
            return {}

        return super().extra_state_attributes
