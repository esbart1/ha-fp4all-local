# FP4All Local — Home Assistant Integration

**Monitor your FP4All solar inverter locally in Home Assistant — without requiring PVOutput or a cloud service for local monitoring.**

[🇬🇧 English](#english) · [🇳🇱 Nederlands](#nederlands) · [Installation](#installation) · [Configuration](#configuration) · [Changelog](CHANGELOG.md) · [Support](#support)

---

<a id="english"></a>
## 🇬🇧 English

FP4All Local is a custom integration for [Home Assistant](https://www.home-assistant.io/) that reads locally available data from an FP4All logger over your local network.

It exposes inverter and energy information as Home Assistant sensors. These values can be used in automations, for example to coordinate an EV charger, heat pump, washing machine or other electrical loads with solar production.

### Features

- Direct communication with the FP4All logger over the local network.
- Local monitoring without requiring PVOutput or a cloud service for this integration.
- Inverter and energy information exposed as Home Assistant sensors.
- Retention of the last valid sensor values during temporary communication problems.
- Recovery after network interruptions and Home Assistant reloads or restarts.
- More recognizable sensor Friendly Names while preserving existing entity IDs where applicable.

**Hardware compatibility:** The integration was originally developed and tested with an older generation FP4All unit. Compatibility with newer generations has not yet been confirmed.

<a id="installation"></a>
## Installation

### Option 1 — HACS

If FP4All Local is available in the HACS default store:

1. Open **HACS** in Home Assistant.
2. Search for **FP4All Local**.
3. Open the integration and select **Download**.
4. Restart Home Assistant if requested.
5. Follow the configuration instructions below.

If it is not listed in the default store, add it as a custom repository in HACS:

1. Open HACS and choose the option to add a custom repository.
2. Enter the repository URL: `https://github.com/esbart1/ha-fp4all-local`
3. Select **Integration** as the category.
4. Add the repository and install FP4All Local.

See the [official HACS repository documentation](https://www.hacs.xyz/docs/use/repositories/dashboard/) for details.

### Option 2 — Manual installation

1. Download or clone this repository.
2. Copy the `custom_components/fp4all` directory into the `custom_components` directory of your Home Assistant configuration.
3. Check that the integration files are located in `config/custom_components/fp4all/`.
4. Restart Home Assistant.
5. Follow the configuration instructions below.

Make a backup of your Home Assistant configuration before replacing an existing installation.

<a id="configuration"></a>
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

<a id="support"></a>
## Support

- [Report a bug or request help](https://github.com/esbart1/ha-fp4all-local/issues)
- [View the source code](https://github.com/esbart1/ha-fp4all-local)
- [Home Assistant documentation](https://www.home-assistant.io/docs/)

---

<a id="nederlands"></a>
## 🇳🇱 Nederlands

FP4All Local is een custom integratie voor [Home Assistant](https://www.home-assistant.io/) die lokaal beschikbare gegevens van een FP4All-unit via het eigen netwerk uitleest.

De integratie maakt omvormer- en energiegegevens beschikbaar als sensoren in Home Assistant. Je kunt deze gegevens gebruiken voor automatiseringen, bijvoorbeeld om een laadpaal, warmtepomp, wasmachine of andere elektrische verbruikers af te stemmen op de zonneproductie.

### Mogelijkheden

- Rechtstreekse communicatie met de FP4All-unit via het lokale netwerk.
- Lokale monitoring zonder dat PVOutput of een cloudservice voor deze integratie nodig is.
- Omvormer- en energiegegevens als Home Assistant-sensoren.
- Behoud van de laatst geldige sensorwaarden bij tijdelijke communicatieproblemen.
- Herstel na netwerkonderbrekingen en herstarts of herladen van Home Assistant.
- Herkenbaardere Friendly Names met behoud van bestaande entity-ID's waar van toepassing.

**Hardwarecompatibiliteit:** De integratie is oorspronkelijk ontwikkeld en getest met een oudere generatie FP4All-unit. De werking met nieuwere generaties is nog niet bevestigd.

<a id="installatie"></a>
## Installatie

### Optie 1 — HACS

Als FP4All Local beschikbaar is in de standaardlijst van HACS:

1. Open **HACS** in Home Assistant.
2. Zoek naar **FP4All Local**.
3. Open de integratie en selecteer **Download**.
4. Herstart Home Assistant als daarom wordt gevraagd.
5. Volg daarna de configuratiestappen hieronder.

Staat de integratie niet in de standaardlijst, voeg deze dan als aangepaste repository toe aan HACS:

1. Open HACS en kies de optie om een aangepaste repository toe te voegen.
2. Vul de repository-URL in: `https://github.com/esbart1/ha-fp4all-local`
3. Kies als categorie **Integration**.
4. Voeg de repository toe en installeer FP4All Local.

Bekijk de [officiële HACS-documentatie over repositories](https://www.hacs.xyz/docs/use/repositories/dashboard/) voor meer informatie.

### Optie 2 — Handmatige installatie

1. Download of clone deze repository.
2. Kopieer de map `custom_components/fp4all` naar de map `custom_components` in je Home Assistant-configuratie.
3. Controleer of de integratiebestanden staan in `config/custom_components/fp4all/`.
4. Herstart Home Assistant.
5. Volg daarna de configuratiestappen hieronder.

Maak een back-up van je Home Assistant-configuratie voordat je een bestaande installatie vervangt.

<a id="configuratie"></a>
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

<a id="ondersteuning"></a>
## Ondersteuning

- [Een probleem melden of hulp vragen](https://github.com/esbart1/ha-fp4all-local/issues)
- [De broncode bekijken](https://github.com/esbart1/ha-fp4all-local)
- [Home Assistant-documentatie](https://www.home-assistant.io/docs/)

---

## Version history / Versiegeschiedenis

See [CHANGELOG.md](CHANGELOG.md) for the version history and release-specific changes. The changelog distinguishes release-preparation updates from functional software changes.

## About

**FP4All Local**

**Local · Realtime · No PVOutput required**
