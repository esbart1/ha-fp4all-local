Fp4all Home Assistant integration

Why this integration?

FP4All is used with solar inverter installations to monitor inverter data. This integration was created to make the locally available FP4All data directly usable in Home Assistant.

Instead of retrieving solar production data through an online service such as PVOutput, this integration communicates directly with the FP4All logger over the local network.

This makes the current inverter information available directly in Home Assistant. The update frequency depends on the FP4All configuration and can range from real-time updates to approximately every 5 minutes.

This is particularly useful for Home Assistant energy automations. The current solar production can, for example, be used to control an EV charger, heat pump, washing machine or other electrical loads when sufficient solar power is available.

The integration was originally developed and tested with an older generation FP4All unit. The newer generation of FP4All units has not yet been tested because I do not have access to one of these units. Compatibility with newer hardware is therefore currently unconfirmed.


Nederlandse beschrijving

FP4All wordt gebruikt voor het monitoren van zonne-omvormers. Deze integratie maakt de lokaal beschikbare gegevens van de FP4All-unit rechtstreeks beschikbaar in Home Assistant.

In plaats van de zonneproductie via een online dienst zoals PVOutput op te halen, maakt deze integratie rechtstreeks verbinding met de FP4All-unit via het lokale netwerk.

Daardoor zijn de actuele gegevens van de omvormer direct beschikbaar in Home Assistant. De updatefrequentie is afhankelijk van de instelling van de FP4All-software en kan variëren van realtime tot ongeveer iedere 5 minuten.

Dit maakt de integratie bijzonder geschikt voor energie-automatiseringen in Home Assistant. De actuele zonneproductie kan bijvoorbeeld worden gebruikt om een laadpaal, warmtepomp, wasmachine of andere elektrische verbruiker aan te sturen wanneer er voldoende zonne-energie beschikbaar is.

De integratie is oorspronkelijk ontwikkeld en getest met een oudere generatie FP4All-unit. De nieuwere generatie FP4All-units is nog niet getest, omdat ik daar zelf niet over beschik. De werking met deze nieuwere hardware is daarom op dit moment nog niet bevestigd.
# Changelog

All notable changes to **FP4All Local for Home Assistant** are documented here.

---

# Version 3.1.10

## Major improvements

Version **3.1.10** is a significant improvement over the previous Build 2.6 release.

The main focus of this release is **local realtime operation, reliability and recovery when the FP4All logger is temporarily unavailable**.

### Local realtime communication

* Direct local communication with the FP4All logger.
* Realtime inverter information is available directly in Home Assistant.
* No PVOutput.org connection is required for the local integration.
* No cloud service is required for realtime local monitoring.

### Communication fallback

Added a communication fallback mechanism.

When the FP4All logger becomes temporarily unavailable:

* the existing sensors remain available;
* the last valid sensor values are retained;
* the communication sensor changes to `Communication lost`;
* the operating mode changes to warning state;
* the operating mode text changes to `Warning`.

When communication is restored:

* realtime data is retrieved again;
* the communication state returns to `Connected`;
* the normal operating mode information is restored.

### Home Assistant reload and restart

Improved behaviour when the FP4All logger is unavailable during:

* Home Assistant reload;
* Home Assistant restart.

The last valid data can be restored from the local cache.

This prevents sensors from disappearing simply because the FP4All web interface is temporarily unavailable.

### Local cache

The cache system has been simplified.

There is now one cache file per FP4All logger:

```text
fp4all_cache/
├── 192_168_178_8.json
└── 192_168_178_9.json
```

The additional manufacturer/model/serial cache file is no longer required.

### Operating mode

Improved handling of the inverter operating mode.

Communication loss results in:

```text
Operating Mode = 3
Operating Mode Text = Warning
```

Normal inverter operation continues to use the actual operating mode reported by the inverter.

### Friendly Names

Added automatic, more recognizable Friendly Names for sensors.

Friendly Names can include:

* FP4All logger IP address;
* inverter model;
* last four digits of the inverter serial number;
* sensor description.

Example:

```text
FP4All 192.168.178.9 PV 2800 (0505) Power
```

### Entity IDs

Existing entity IDs are preserved.

For example:

```text
sensor.garage_fp4all_192_168_178_9_power
```

remains unchanged even when the Friendly Name is improved.

This helps preserve existing:

* dashboards;
* automations;
* scripts;
* templates;
* Home Assistant configurations.

### Sensor persistence

Improved persistence of sensors and their values.

Sensors remain available after:

* temporary network loss;
* FP4All web interface unavailable;
* Home Assistant reload;
* Home Assistant restart.

### Additional inverter information

Improved handling of inverter information including:

* manufacturer;
* model;
* firmware;
* serial number;
* inverter capacity;
* voltage limits;
* frequency limits;
* PV start voltage;
* start delay;
* operating mode.

### Start Delay

The `Start Delay` sensor is now retained through the cache system when the FP4All web interface is unavailable.

### Energy data

Improved handling of:

* today's generated energy;
* lifetime generated energy;
* total energy;
* operating hours.

Daily generated energy is protected against values unexpectedly dropping during normal operation.

---

# Version 2.6

Previous release.

Version 2.6 provided the earlier FP4All Local integration and documentation.

Version 3.1.10 builds on this version with improved:

* local realtime operation;
* communication handling;
* cache recovery;
* sensor persistence;
* Friendly Names;
* entity ID preservation.

---

# Notes

Version 3.1.10 has been tested with multiple FP4All installations and with both normal operation and temporary loss of communication.

Tested situations include:

* normal realtime operation;
* UTP/network disconnection;
* communication recovery;
* Home Assistant reload;
* Home Assistant restart;
* FP4All logger unavailable during restart;
* operation with multiple FP4All loggers.

---

# Upgrade from Build 2.6

Before upgrading, make a backup of the existing Home Assistant configuration.

Replace the existing `custom_components/fp4all` integration with the version from 3.1.10.

Existing entity IDs are intended to remain unchanged.

After upgrading:

1. Restart Home Assistant.
2. Check the FP4All integration.
3. Check the sensors.
4. Verify the Friendly Names.
5. Check the communication sensor.
6. Confirm that existing dashboards and automations still use the same entity IDs.

---

# Version

**FP4All Local 3.1.10**

**Local · Realtime · No PVOutput required**
