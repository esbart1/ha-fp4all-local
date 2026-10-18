# Changelog

All notable changes to FP4All Local are documented in this file.

## [3.1.10] - Current release

### Added
- Automatic, more recognizable sensor Friendly Names using available logger and inverter information.
- A communication status sensor with `Connected` and `Communication lost` states.
- Local cache support to retain the last valid sensor data for each logger.

### Improved
- Recovery after temporary network or logger communication loss.
- Sensor availability and cached data handling during Home Assistant reloads and restarts.
- Operating-mode reporting during communication loss, using a warning state.
- Handling of inverter details, including manufacturer, model, firmware, serial number, capacity, voltage and frequency limits, PV start voltage, and start delay.
- Handling of energy-production and operating-hours data.

### Compatibility
- Existing entity IDs are intended to remain unchanged when Friendly Names are improved.
- The cache uses one file per logger; the additional manufacturer/model/serial cache file is no longer required.

## [2.6] - Previous release

- Previous generation of the FP4All Local integration.
- Version 3.1.10 builds on this release with improvements to local monitoring, communication recovery, caching, sensor persistence, and Friendly Names.

---

For installation and configuration instructions, see [README.md](README.md).
