# FP4All Local — Home Assistant Integration

**Monitor your FP4All solar inverter locally in Home Assistant — without requiring PVOutput or a cloud service for local monitoring.**

[🇬🇧 English](#english) · [🇳🇱 Nederlands](#nederlands) · [Installation](#installation) · [Configuration](#configuration) · [Changelog](#changelog) · [Support](#support)

---

<a id="english"></a>
## 🇬🇧 English

FP4All Local is a custom integration for [Home Assistant](https://www.home-assistant.io/) that reads locally available data from an FP4All logger over your local network.

The integration makes inverter information available to Home Assistant and can help you build energy automations based on solar production. For example, you can use solar production data to control an EV charger, heat pump, washing machine or other electrical loads.

### Features

- Direct communication with the FP4All logger over the local network.
- Local monitoring without requiring PVOutput for this integration.
- Inverter and energy information exposed as Home Assistant sensors.
- Retention of the last valid sensor values during temporary communication problems.
- Improved recovery after network interruptions and Home Assistant restarts.
- Friendly sensor names while preserving existing entity IDs where applicable.

**Hardware compatibility:** The integration was originally developed and tested with an older generation FP4All unit. Compatibility with newer generations has not yet been confirmed.

## Installation

### Option 1 — HACS

Once FP4All Local is available in the HACS default store:

1. Open **HACS** in Home Assistant.
2. Search for **FP4All Local**.
3. Open the integration and select **Download**.
4. Restart Home Assistant if requested.
5. Continue with the configuration instructions below.

If the repository is not yet listed in the HACS default store, you may be able to add it as a custom repository in HACS, using the repository URL:

`https://github.com/esbart1/ha-fp4all-local`

Select **Integration** as the repository category.

See the [official HACS documentation](https://www.hacs.xyz/docs/use/repositories/dashboard/) for details.

### Option 2 — Manual installation

1. Download or clone this repository.
2. Copy the `custom_components/fp4all` directory into the `custom_components` directory of your Home Assistant configuration.
3. Check that the integration files are located in:

   `config/custom_components/fp4all/`

4. Restart Home Assistant.
5. Continue with the configuration instructions below.

Make a backup of your Home Assistant configuration before replacing an existing installation.

## Configuration

After installing FP4All Local and restarting Home Assistant:

1. Open **Settings → Devices & services**.
2. Select **Add integration**.
3. Search for **FP4All Local**.
4. Enter the IP address of your FP4All logger.

![Enter the IP address of the FP4All logger](screenshots/setup-ip-address.png)

Make sure the logger is reachable over your local network. If the integration cannot connect, check the logger's network connection and review the Home Assistant logs for relevant errors.

### Update interval

Open the options for the FP4All Local integration to select the update interval.

![Select the update interval](screenshots/scan-interval-selection.png)

Available intervals:

- Realtime — 1 second
- 10 seconds
- 30 seconds (default)
- 1 minute
- 5 minutes

## Support

- [Report a bug or request help](https://github.com/esbart1/ha-fp4all-local/issues)
- [View the source code](https://github.com/esbart1/ha-fp4all-local)
- [Home Assistant documentation](https://www.home-assistant.io/docs/)

---

<a id="nederlands"></a>
## 🇳🇱 Nederlands

FP4All Local is een custom integratie voor [Home Assistant](https://www.home-assistant.io/) die lokaal beschikbare gegevens van een FP4All-unit via het eigen netwerk uitleest.

De integratie maakt informatie over de omvormer beschikbaar als sensoren in Home Assistant. Daarmee kun je energie-automatiseringen maken op basis van de actuele zonneproductie. Denk bijvoorbeeld aan het aansturen van een laadpaal, warmtepomp, wasmachine of andere elektrische verbruikers wanneer er voldoende zonne-energie beschikbaar is.

### Mogelijkheden

- Rechtstreekse communicatie met de FP4All-unit via het lokale netwerk.
- Lokale monitoring zonder dat PVOutput voor deze integratie nodig is.
- Omvormer- en energiegegevens als Home Assistant-sensoren.
- Behoud van de laatst geldige sensorwaarden bij tijdelijke communicatieproblemen.
- Verbeterd herstel na netwerkonderbrekingen en herstarts van Home Assistant.
- Verbeterde, herkenbare sensornamen met behoud van bestaande entity-ID's waar van toepassing.

**Hardwarecompatibiliteit:** De integratie is oorspronkelijk ontwikkeld en getest met een oudere generatie FP4All-unit. De werking met nieuwere generaties is nog niet bevestigd.

## Installatie

### Optie 1 — HACS

Zodra FP4All Local beschikbaar is in de standaardlijst van HACS:

1. Open **HACS** in Home Assistant.
2. Zoek naar **FP4All Local**.
3. Open de integratie en selecteer **Download**.
4. Herstart Home Assistant als daarom wordt gevraagd.
5. Volg daarna de configuratiestappen hieronder.

Staat de integratie nog niet in de standaardlijst, dan kun je de repository mogelijk als aangepaste repository aan HACS toevoegen met deze URL:

`https://github.com/esbart1/ha-fp4all-local`

Kies als categorie **Integration**.

Bekijk de [officiële HACS-documentatie](https://www.hacs.xyz/docs/use/repositories/dashboard/) voor meer informatie.

### Optie 2 — Handmatige installatie

1. Download of clone deze repository.
2. Kopieer de map `custom_components/fp4all` naar de map `custom_components` in je Home Assistant-configuratie.
3. Controleer of de integratiebestanden staan in:

   `config/custom_components/fp4all/`

4. Herstart Home Assistant.
5. Volg daarna de configuratiestappen hieronder.

Maak een back-up van je Home Assistant-configuratie voordat je een bestaande installatie vervangt.

## Configuratie

Na installatie van FP4All Local en een herstart van Home Assistant:

1. Open **Instellingen → Apparaten en diensten**.
2. Kies **Integratie toevoegen**.
3. Zoek naar **FP4All Local**.
4. Vul het IP-adres van je FP4All-unit in.

![Vul het IP-adres van de FP4All-unit in](screenshots/setup-ip-address.png)

Zorg ervoor dat de FP4All-unit bereikbaar is via je lokale netwerk. Lukt de verbinding niet? Controleer dan de netwerkverbinding en bekijk zo nodig de Home Assistant-logboeken op relevante foutmeldingen.

### Updatefrequentie

Open de opties van de FP4All Local-integratie om de updatefrequentie te kiezen.

![Kies de updatefrequentie](screenshots/scan-interval-selection.png)

Beschikbare intervallen:

- Realtime — 1 seconde
- 10 seconden
- 30 seconden (standaard)
- 1 minuut
- 5 minuten

## Ondersteuning

- [Een probleem melden of hulp vragen](https://github.com/esbart1/ha-fp4all-local/issues)
- [De broncode bekijken](https://github.com/esbart1/ha-fp4all-local)
- [Home Assistant-documentatie](https://www.home-assistant.io/docs/)

---

<a id="changelog"></a>
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
