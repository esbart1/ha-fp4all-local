"""
FP4All Local for Home Assistant

Version : 0.4
Build   : 3.1.9
File    : sensor.py

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

    )
#		
##
async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:

    coordinator: FP4AllCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        FP4AllSensor(coordinator, entry, *description)
        for description in SENSORS
    )


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

#        self._attr_name = name
        model = coordinator._model or "FP4All"
        serial = coordinator._serial or ""

        if serial:
            suffix = serial[-4:]
            self._attr_name = f"{model} ({suffix}) {name}"
        else:
            self._attr_name = f"{model} {name}"

        self._attr_unique_id = (
            f"{entry.entry_id}_{key}"
        )

        self._attr_native_unit_of_measurement = unit

        self._attr_device_class = device_class

        self._attr_state_class = state_class

        self._attr_has_entity_name = True

        self._entry = entry

    @property
    def device_info(self):
        """Return device information."""

        status = self.coordinator.status

        return DeviceInfo(
            identifiers={
                (DOMAIN, self._entry.entry_id)
            },
            manufacturer=(
                status.get("manufacturer")
                or self.coordinator._manufacturer
                or MANUFACTURER
            ),

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

##
#    @property
#    def native_value(self):
#        """Return sensor value."""

#        return self.coordinator.data.get(
#            self._key
#        )
#
    @property
    def native_value(self):
        """Return sensor value."""

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


