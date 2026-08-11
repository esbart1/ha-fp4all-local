# Changelog

All notable changes to the FP4All Local integration are documented in this file.

The format is based on **Keep a Changelog** and uses the internal Build number for development tracking.
---

# FP4All Local for Home Assistant




# Version 0.4
### Build 3.1.9 Final
Added
- Device information is now cached locally.
- Manufacturer, model, firmware and serial number remain available after a Home Assistant restart, even when the inverter is temporarily unreachable.
- Device information is automatically restored from cache before the first successful connection.

Improved
- Device information remains stable after:
- Home Assistant restart
- Home Assistant reboot
- Temporary network interruption
- UTP cable disconnected during startup
- Cache handling for DeviceInfo is now fully asynchronous.



Fixed

- Device no longer falls back to:
   FP4All Logger
   by FP4All
   after a restart without network connection.

- Device manufacturer, model, firmware and serial number are restored automatically from cache.
- Reload of the integration is no longer required after reconnecting the inverter.


Tested
- Normal operation
-  Home Assistant restart
-  Full HA reboot
- UTP disconnected during startup
- UTP reconnected while running
-  Cache recreation after deleting all JSON files
-  Multiple inverters
-  Device information remains correct in all tested scenarios

Internal
- Added cached DeviceInfo variables:
  _manufacturer
  _model
  _serial
  _firmware
- DeviceInfo now uses cached values whenever live data is temporarily unavailable.





# Version 0.4
### Build 3.1.6final
-----

### Added
- Async cache loading
- Async cache writing
- Cache survives Home Assistant restart
- Cache survives temporary network loss
- Automatic recovery after reconnect
- Separate cache per inverter
- Second cache based on manufacturer/model/serial
- Timestamp remains valid during communication loss

### Fixed
- Removed blocking file I/O
- Removed Home Assistant event loop warnings
- Improved communication recovery
- Improved cache reliability
---




# Version 0.4
### Build 3.1.5

- Added persistent JSON cache.
- Cache survives Home Assistant restart.
- Cache automatically recreated if missing.
- Added second cache using manufacturer + serial.
- Removed blocking file I/O.
- Improved communication loss handling.
- Improved reconnect behaviour.



---


# Version 0.4
###Build 3.1.3

### Added
- Cachebestand per logger.
- Cachebestanden verplaatst naar:
  custom_components/fp4all/fp4all_cache/

### Improved
- Laatste waarden blijven behouden na herstart.
- Laatste waarden blijven behouden na reboot.
- Elke logger gebruikt zijn eigen cachebestand.

### Tested
- Home Assistant restart
- Home Assistant reboot
- Logger offline (UTP los)
- Logger online
- Cache herstel



---

# Version 0.4
### Build 3.1.1

### Added
- JSON cache toegevoegd (fp4all_last_good_data.json)
- Laatste geldige meetwaarden worden automatisch opgeslagen
- Meetwaarden worden na Home Assistant herstart direct hersteld
- Geen lege sensoren meer tijdens tijdelijk netwerkverlies


### Improved
- today_generated gebruikt hoogste waarde van de dag
- Compatibiliteit behouden voor bestaande sensor "today"
- Automatisch herstel zodra logger weer online komt

### Fixed
- Realtime waarden blijven beschikbaar tijdens communicatieverlies
- Energy Today blijft correct na herstart



---
# Version 0.4.1
### Build 3.1.0

### Fixed
- Energy Today resetting after temporary communication loss.


### Added
- Today's Generated Energy sensor.
- Lifetime Generated Energy sensor.
- Lifetime Operating Hours sensor.
- Lifetime CO₂ Saved sensor.
- Lifetime Earnings sensor.


### Changed
-  Improved discovery after unavailable index.htm.
-  Improved operating mode filtering
-  cleaned coordinator logging

### Fixed
-  combined 16-bit high/low counters for Energy Total.
-  combined 16-bit high/low counters for Operating Hours.



---
## Build 3.0.9

### Added
- Device information is now exposed correctly to Home Assistant:
- Manufacturer
- Model
- Firmware
- Serial number
- Capacity
- Added support for multiple inverter manufacturers (SMA and PHOENIXTEC).
- Added parsing of Today's generated energy from the realtime index.htm page.

### Changed
- Device information is no longer reported as unknown.
- Improved parsing of inverter identification fields.
- Today's Generated Energy now uses the realtime value from index.htm.
- status.htm (ETODAY) is retained as a fallback source.
- Improved robustness of the daily energy sensor after Home Assistant reloads.

### Fixed
- Correct manufacturer detection.
- Correct firmware detection.
- Correct model detection.
- Correct serial number detection.
- Fixed incorrect daily energy values after Home Assistant reload.
- Prevented stale ETODAY values from replacing newer realtime values.
- Improved compatibility with SMA WR33-014.
- Improved compatibility with Phoenixtec PV2800.


---
## Build 3.0.8

### Added
- Transition state filtering.
- Operating mode cache.
- Temporary mode confirmation counter.
- Configurable fallback PV start voltage (90 V).

### Changed
- Operating mode is only updated after confirmation.
- Improved behaviour during inverter startup and shutdown.
- Reduced false mode transitions.

### Fixed
- Eliminated most temporary `Unknown (7)` operating mode events.

---

## Build 3.0.7

### Added
- Cached realtime dataset (`self._last_good_data`).
- Automatic recovery after temporary communication failures.
- Automatic recovery after invalid XML responses.
- Last valid dataset is preserved until valid communication returns.

### Changed
- Improved coordinator stability.
- Improved communication error handling.

### Fixed
- Prevented unnecessary sensor unavailability during short communication interruptions.

---

## Build 3.0.6

### Added
- Configurable update interval.
- Options Flow.
- Automatic integration reload after changing options.
- High/Low 16-bit counter support.
- Improved logging.
- Multi-inverter support.
- Tested with two independent FP4All installations.

### Changed
- Improved configuration management.

---

## Build 3.0.4

### Changed
- Entity names now use the Config Entry title instead of the IP address.
- Improved Home Assistant naming.
- Cleaner entity IDs.

---

# Version 0.4.0

## Build 3.0.0

### Added
- `status.htm` parser.
- `index.htm` parser.
- High/Low counter support.
- Lifetime sensors.
- Improved precision.
- Extended device information.

### Fixed
- Restored `hours_total`.
- Correct High/Low energy counter calculation.
- Home Assistant 2026 compatibility.

---

# Version 0.3.0

## Build 2.0.6

### Added
- Config Flow.
- Local communication.
- Multiple FP4All devices.
- Realtime sensors.
- History download service.

---

# Version 0.2

Initial public release.