# Changelog

All notable changes to FP4All Local are documented in this file.

## [3.1.12]

### English

- Migrated logger cache storage to Home Assistant's `.storage` system.
- Verified that cached sensor data persists across Home Assistant restarts.
- Tested recovery after temporary communication loss with the logger.
- Tested a fresh integration installation and operation with two inverters.
- No errors were observed in the tested Home Assistant logs.
- Existing helper files for possible future history and status/error functionality are retained; these features are not part of the active functionality in this release.

### Nederlands

- De opslag van logger-cachegegevens is verplaatst naar het `.storage`-systeem van Home Assistant.
- Getest dat opgeslagen sensorgegevens behouden blijven na een herstart van Home Assistant.
- Herstel na tijdelijk communicatieverlies met de logger getest.
- Een nieuwe installatie van de integratie en de werking met twee omvormers getest.
- In de gecontroleerde Home Assistant-logboeken zijn geen fouten waargenomen.
- Bestaande hulpprogrammabestanden voor mogelijke toekomstige geschiedenis- en status-/foutinformatie zijn behouden. Deze functies zijn in deze versie nog niet actief.

### Compatibility / Compatibiliteit

- The tested hardware consists of older FP4All logger models. Newer logger generations have not been tested separately; similar-looking web pages do not confirm compatibility.
- De geteste hardware bestaat uit oudere FP4All-loggermodellen. Nieuwere generaties zijn niet afzonderlijk getest; vergelijkbare webpagina's bewijzen geen compatibiliteit.

## [3.1.11]

- Documentation cleanup: remove duplicated and outdated release notes from README.md and link to this changelog.
- Release-preparation update only; no intended functional changes.

## [3.1.10]

- HACS release-only update to address the timing/order of HACS release steps.
- No functional changes compared with version 3.1.9.

## [3.1.9]

### Added
- Communication status reporting, including `Connected` and `Communication lost` states.
- Local cache support to retain the last valid sensor data for each logger.
- Automatic, more recognizable sensor Friendly Names using available logger and inverter information.

### Improved
- Recovery after temporary network or logger communication loss.
- Sensor availability and cached data handling during Home Assistant reloads and restarts.
- Operating-mode reporting during communication loss, using a warning state.
- Handling of inverter details, including manufacturer, model, firmware, serial number, capacity, voltage and frequency limits, PV start voltage, and start delay.
- Handling of energy-production and operating-hours data.

### Compatibility
- Existing entity IDs are intended to remain unchanged when Friendly Names are improved.
- The cache uses one file per logger; the additional manufacturer/model/serial cache file is no longer required.

## [2.6]

- Previous generation of the FP4All Local integration.

---

For installation and configuration instructions, see [README.md](README.md).
