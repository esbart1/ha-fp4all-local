"""Diagnostic button for manually testing the FP4All coordinator refresh."""

from __future__ import annotations

from homeassistant.components.button import ButtonEntity
from homeassistant.const import EntityCategory
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import FP4AllCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the diagnostic refresh button."""
    coordinator: FP4AllCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([FP4AllTestRefreshButton(coordinator, entry)])


class FP4AllTestRefreshButton(CoordinatorEntity, ButtonEntity):
    """Run a coordinator refresh on demand for diagnostics."""

    _attr_has_entity_name = True
    _attr_name = "Test Daily Refresh"
    _attr_icon = "mdi:refresh"
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(self, coordinator: FP4AllCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._entry = entry
        self._attr_unique_id = f"{entry.entry_id}_test_daily_refresh"

    @property
    def device_info(self):
        """Attach the test button to the corresponding FP4All device."""
        return {
            "identifiers": {(DOMAIN, self._entry.entry_id)},
        }

    async def async_press(self) -> None:
        """Request a complete coordinator refresh for all FP4All sensors."""
        await self.coordinator.async_request_refresh()
