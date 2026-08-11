# FP4All Local for Home Assistant

**Version 3.1.9**

> **Local · Realtime · No PVOutput required**

A local Home Assistant integration for FP4All PV Solar Inverter Loggers.

The integration communicates directly with the FP4All logger over the local network and makes realtime inverter information available in Home Assistant.

No cloud service and no PVOutput.org connection are required for local realtime monitoring.

---

# 🇳🇱 Nederlands

## FP4All Local

FP4All Local is een lokale Home Assistant-integratie voor FP4All PV Solar Inverter Loggers.

De integratie leest de gegevens rechtstreeks uit de FP4All logger via het lokale netwerk.

### Belangrijk

**Local · Realtime · No PVOutput required**

De realtime gegevens worden rechtstreeks uit de lokale FP4All logger gelezen.

Daarvoor is geen:

* cloudverbinding;
* PVOutput.org;
* externe monitoringdienst

nodig.

Dit maakt het mogelijk om de FP4All logger lokaal binnen Home Assistant te gebruiken.

---

## Belangrijkste functies

FP4All Local 3.1.9 ondersteunt onder andere:

* lokale communicatie via HTTP;
* realtime uitlezing;
* meerdere FP4All loggers;
* automatische updates;
* uitlezen van `status.xml`;
* uitlezen van `status.htm`;
* uitlezen van `index.htm`;
* energieproductie;
* totale energieproductie;
* bedrijfsuren;
* omvormerstatus;
* bedrijfsmodus;
* bedrijfsmodus tekst;
* communicatiestatus;
* inverterinformatie;
* Friendly Names;
* lokale cache;
* communicatie-fallback;
* behoud van sensoren tijdens tijdelijke communicatieproblemen;
* behoud van sensoren na een Home Assistant reload;
* behoud van sensoren na een Home Assistant restart;
* bestaande entity-id's blijven behouden.

---

## Realtime lokale communicatie

De integratie maakt rechtstreeks verbinding met het lokale IP-adres van de FP4All logger.

Bijvoorbeeld:

```text
192.168.178.9
```

De FP4All logger moet bereikbaar zijn vanaf de Home Assistant-installatie.

De gegevens worden lokaal opgehaald en vervolgens via de Home Assistant `DataUpdateCoordinator` aan de sensoren aangeboden.

---

## Meerdere FP4All loggers

Meerdere loggers kunnen tegelijkertijd worden toegevoegd.

Bijvoorbeeld:

```text
192.168.178.8
192.168.178.9
```

Iedere logger heeft zijn eigen dataset en eigen cachebestand.

---

# Cache en communicatie-fallback

Een belangrijke verbetering in versie 3.1.9 is de lokale cache.

Per omvormer wordt één cachebestand gebruikt:

```text
fp4all_cache/
├── 192_168_178_8.json
└── 192_168_178_9.json
```

De cache bevat de laatst geldige gegevens van de omvormer.

Hierdoor kunnen de sensoren blijven bestaan wanneer de FP4All logger tijdelijk niet bereikbaar is.

Dit is bijvoorbeeld belangrijk wanneer:

* de UTP-kabel wordt losgekoppeld;
* de FP4All webpagina tijdelijk niet bereikbaar is;
* de omvormer 's nachts niet bereikbaar is;
* Home Assistant wordt herladen;
* Home Assistant wordt herstart terwijl de logger niet bereikbaar is.

De laatst bekende geldige sensorwaarden kunnen dan vanuit de cache worden gebruikt.

---

## Communicatiestatus

De integratie heeft een afzonderlijke sensor voor de communicatie.

Bij normale communicatie:

```text
Connected
```

Bij verlies van communicatie:

```text
Communication lost
```

De communicatiestatus wordt niet gebruikt om de normale sensorwaarden te verwijderen.

Daardoor blijven de sensoren beschikbaar tijdens een tijdelijke netwerkonderbreking.

Wanneer de communicatie weer beschikbaar is, worden de actuele gegevens opnieuw opgehaald.

---

# Operating Mode bij communicatieverlies

Wanneer de communicatie met de logger verloren gaat, wordt de bedrijfsstatus aangepast naar een waarschuwingstoestand.

Bijvoorbeeld:

```text
Operating Mode
3
```

en:

```text
Operating Mode Text
Warning
```

Wanneer de communicatie wordt hersteld, kan de normale operating mode opnieuw worden gebruikt.

---

# Friendly Names

De integratie gebruikt de informatie van de omvormer om automatisch herkenbare Friendly Names te maken.

Daarbij kan onder andere worden gebruikt:

* het model van de omvormer;
* de laatste vier cijfers van het serienummer;
* het IP-adres van de logger;
* de naam van de sensor.

Voorbeeld:

```text
FP4All 192.168.178.9 PV 2800 (0505) Today's Generated Energy
```

### Entity ID blijft behouden

De Friendly Name verandert **niet** de bestaande entity-id.

Bijvoorbeeld:

```text
sensor.garage_fp4all_192_168_178_9_power
```

blijft dezelfde entity-id.

De zichtbare naam kan bijvoorbeeld zijn:

```text
FP4All 192.168.178.9 PV 2800 (0505) Power
```

Dit is belangrijk voor bestaande:

* dashboards;
* automatiseringen;
* scripts;
* templates;
* andere Home Assistant-configuraties.

Bestaande entity-id's hoeven hierdoor niet opnieuw ingesteld te worden.

---

# Sensoren

De integratie maakt verschillende sensoren beschikbaar.

## Realtime waarden

* Power
* Temperature
* PV Voltage
* AC Voltage
* AC Frequency
* AC Current
* Timestamp
* Operating Mode
* Operating Mode Text
* Communication

## Energie

* Energy Today
* Energy Total
* Today's Generated Energy
* Lifetime Generated Energy
* Operating Hours
* Lifetime Operating Hours
* CO₂ Saved
* Lifetime Earnings

## Extra invertergegevens

* Inverter Capacity
* AC Voltage Min
* AC Voltage Max
* AC Frequency Min
* AC Frequency Max
* PV Start Voltage
* Start Delay
* Energy Total High
* Energy Total Low
* Operating Hours High
* Operating Hours Low

---

# FP4All gegevensbronnen

De integratie gebruikt verschillende lokale bestanden van de FP4All logger.

## status.xml

Wordt gebruikt voor realtime gegevens zoals:

* vermogen;
* temperatuur;
* PV-spanning;
* AC-stroom;
* totale energie;
* bedrijfsuren;
* timestamp.

## status.htm

Wordt gebruikt voor aanvullende omvormerinformatie zoals:

* fabrikant;
* model;
* firmware;
* serienummer;
* capaciteit;
* AC-spanningsgrenzen;
* frequentiegegevens;
* PV startspanning;
* startvertraging;
* operating mode.

## index.htm

Wordt gebruikt voor aanvullende gegevens en berekende waarden.

---

# Installatie

## Handmatige installatie

Kopieer de map:

```text
custom_components/fp4all
```

naar:

```text
/config/custom_components/
```

De structuur moet er bijvoorbeeld zo uitzien:

```text
/config/
└── custom_components/
    └── fp4all/
        ├── __init__.py
        ├── coordinator.py
        ├── sensor.py
        ├── const.py
        ├── status.py
        ├── status_parser.py
        ├── index.py
        ├── index_parser.py
        ├── history.py
        └── helpers/
```

Herstart daarna Home Assistant.

Ga vervolgens naar:

**Instellingen → Apparaten & diensten → Integratie toevoegen**

Zoek naar:

**FP4All Local**

Voer het lokale IP-adres van de FP4All logger in.

Bijvoorbeeld:

```text
192.168.178.9
```

---

# Configuratie

Voor iedere FP4All logger wordt een afzonderlijke configuratie gemaakt.

Voor meerdere loggers kan bijvoorbeeld worden gebruikt:

```text
FP4All logger 1
192.168.178.8

FP4All logger 2
192.168.178.9
```

Iedere logger wordt afzonderlijk door Home Assistant beheerd.

---

# Cachebestanden

De cache wordt automatisch aangemaakt.

De bestanden staan onder:

```text
/config/custom_components/fp4all/fp4all_cache/
```

Bijvoorbeeld:

```text
192_168_178_8.json
192_168_178_9.json
```

Deze bestanden hoeven normaal gesproken niet handmatig te worden aangepast.

De cache is bedoeld als fallback wanneer realtime communicatie tijdelijk niet beschikbaar is.

---

# Herstart en reload van Home Assistant

Een belangrijk doel van versie 3.1.9 is dat de integratie robuuster omgaat met een tijdelijk niet-beschikbare FP4All logger.

Wanneer de logger tijdens een:

* Home Assistant reload;
* Home Assistant restart;

niet bereikbaar is, kunnen de laatst bekende gegevens uit de cache worden gebruikt.

Hierdoor blijven de sensoren beschikbaar.

Wanneer de logger later weer bereikbaar wordt, worden de realtime gegevens automatisch opnieuw opgehaald.

---

# Bestaande entity-id's

Versie 3.1.9 is ontwikkeld met behoud van bestaande entity-id's als uitgangspunt.

De Friendly Name kan worden verbeterd zonder de entity-id te veranderen.

Dit voorkomt onnodige aanpassingen aan bestaande Home Assistant-configuraties.

---

# Voorbeeld

Een logger met:

```text
IP:
192.168.178.9

Manufacturer:
PHOENIXTEC

Model:
PV 2800

Serial:
1101BJ0505
```

kan bijvoorbeeld een Friendly Name krijgen zoals:

```text
FP4All 192.168.178.9 PV 2800 (0505) Power
```

terwijl de entity-id bijvoorbeeld blijft:

```text
sensor.garage_fp4all_192_168_178_9_power
```

---

# Screenshots

Screenshots kunnen worden geplaatst in:

```text
screenshots/
```

Bijvoorbeeld:

```text
screenshots/
├── overview.png
├── sensors.png
├── configuration.png
└── communication.png
```

Screenshots zijn niet noodzakelijk voor de werking van de integratie.

---

# Versie 3.1.9

Versie 3.1.9 is een aanzienlijke verbetering ten opzichte van de oudere Build 2.6-versie.

Belangrijke verbeteringen:

* verbeterde lokale realtime uitlezing;
* communicatie-status;
* communicatie-fallback;
* lokale cache;
* sensoren blijven beschikbaar bij tijdelijk communicatieverlies;
* sensoren blijven beschikbaar na reload/restart;
* operating mode warning bij communicatieverlies;
* operating mode text warning;
* automatische Friendly Names;
* behoud van bestaande entity-id's;
* één cachebestand per omvormer;
* tweede cachebestand per omvormer niet meer nodig.

---

# Belangrijk

**FP4All Local werkt lokaal.**

**Realtime gegevens zijn rechtstreeks beschikbaar in Home Assistant.**

**PVOutput.org is niet nodig.**

**Een cloudverbinding is niet nodig voor de lokale realtime gegevens.**

---

# Changelog

Zie:

```text
CHANGELOG.md
```

voor de versiegeschiedenis.

---

# 🇬🇧 English

# FP4All Local for Home Assistant

**Version 3.1.9**

> **Local · Realtime · No PVOutput required**

FP4All Local is a local Home Assistant integration for FP4All PV Solar Inverter Loggers.

The integration communicates directly with the FP4All logger over the local network and provides realtime inverter information to Home Assistant.

No cloud service and no PVOutput.org connection are required for local realtime monitoring.

---

## Main features

FP4All Local 3.1.9 provides:

* local HTTP communication;
* realtime inverter data;
* support for multiple FP4All loggers;
* automatic updates;
* `status.xml` support;
* `status.htm` support;
* `index.htm` support;
* energy production data;
* total energy data;
* operating hours;
* inverter status;
* operating mode;
* operating mode text;
* communication status;
* inverter information;
* automatic Friendly Names;
* local cache;
* communication fallback;
* sensor preservation during temporary communication loss;
* sensor preservation after a Home Assistant reload;
* sensor preservation after a Home Assistant restart;
* preservation of existing entity IDs.

---

## Local realtime communication

The integration connects directly to the local IP address of the FP4All logger.

Example:

```text
192.168.178.9
```

The logger must be reachable from the Home Assistant installation.

The data is retrieved locally and provided to the sensors through Home Assistant's `DataUpdateCoordinator`.

---

# Local · Realtime · No PVOutput required

The realtime inverter data is read directly from the local FP4All logger.

PVOutput.org is **not required**.

No cloud service is required for the local realtime data.

---

# Multiple FP4All loggers

Multiple FP4All loggers can be configured simultaneously.

Example:

```text
192.168.178.8
192.168.178.9
```

Each logger has its own dataset and cache file.

---

# Cache and communication fallback

Version 3.1.9 introduces an improved local cache mechanism.

One cache file is used per inverter:

```text
fp4all_cache/
├── 192_168_178_8.json
└── 192_168_178_9.json
```

The cache contains the last valid dataset received from the inverter.

If the FP4All logger temporarily becomes unavailable, the integration can use the cached data instead of removing the sensors.

This is useful when:

* the network cable is disconnected;
* the FP4All web page is temporarily unavailable;
* the inverter is unavailable during nighttime;
* Home Assistant is reloaded;
* Home Assistant is restarted while the logger is unavailable.

The communication state is handled separately from the cached sensor values.

---

# Communication status

The integration provides a separate communication sensor.

Normal communication:

```text
Connected
```

Communication failure:

```text
Communication lost
```

The communication failure does not unnecessarily remove the existing sensors or their last known values.

When communication is restored, current realtime data is retrieved again.

---

# Operating mode during communication loss

When communication with the logger is lost, the operating mode can be changed to a warning state.

Example:

```text
Operating Mode
3
```

and:

```text
Operating Mode Text
Warning
```

When communication is restored, the normal inverter operating information can be used again.

---

# Friendly Names

The integration automatically creates recognizable Friendly Names using information from the inverter.

The Friendly Name can include:

* inverter model;
* last four digits of the serial number;
* logger IP address;
* sensor name.

Example:

```text
FP4All 192.168.178.9 PV 2800 (0505) Today's Generated Energy
```

## Existing entity IDs are preserved

The Friendly Name does **not** change the existing entity ID.

For example:

```text
sensor.garage_fp4all_192_168_178_9_power
```

can remain the same entity ID while its visible name becomes:

```text
FP4All 192.168.178.9 PV 2800 (0505) Power
```

This means existing:

* dashboards;
* automations;
* scripts;
* templates;
* other Home Assistant configurations

can continue to use the existing entity IDs.

---

# Sensors

## Realtime values

* Power
* Temperature
* PV Voltage
* AC Voltage
* AC Frequency
* AC Current
* Timestamp
* Operating Mode
* Operating Mode Text
* Communication

## Energy

* Energy Today
* Energy Total
* Today's Generated Energy
* Lifetime Generated Energy
* Operating Hours
* Lifetime Operating Hours
* CO₂ Saved
* Lifetime Earnings

## Additional inverter information

* Inverter Capacity
* AC Voltage Min
* AC Voltage Max
* AC Frequency Min
* AC Frequency Max
* PV Start Voltage
* Start Delay
* Energy Total High
* Energy Total Low
* Operating Hours High
* Operating Hours Low

---

# FP4All data sources

The integration uses several local files provided by the FP4All logger.

## status.xml

Used for realtime information such as:

* power;
* temperature;
* PV voltage;
* AC current;
* total energy;
* operating hours;
* timestamp.

## status.htm

Used for additional inverter information such as:

* manufacturer;
* model;
* firmware;
* serial number;
* capacity;
* AC voltage limits;
* frequency information;
* PV start voltage;
* start delay;
* operating mode.

## index.htm

Used for additional information and calculated values.

---

# Installation

## Manual installation

Copy:

```text
custom_components/fp4all
```

to:

```text
/config/custom_components/
```

The resulting structure should look similar to:

```text
/config/
└── custom_components/
    └── fp4all/
        ├── __init__.py
        ├── coordinator.py
        ├── sensor.py
        ├── const.py
        ├── status.py
        ├── status_parser.py
        ├── index.py
        ├── index_parser.py
        ├── history.py
        └── helpers/
```

Restart Home Assistant.

Then go to:

**Settings → Devices & services → Add Integration**

Search for:

**FP4All Local**

Enter the local IP address of the FP4All logger.

Example:

```text
192.168.178.9
```

---

# Configuration

Each FP4All logger is configured separately.

Example:

```text
FP4All logger 1
192.168.178.8

FP4All logger 2
192.168.178.9
```

---

# Cache files

The cache directory is created automatically:

```text
/config/custom_components/fp4all/fp4all_cache/
```

Example:

```text
192_168_178_8.json
192_168_178_9.json
```

Normally these files do not need to be edited manually.

They are used as a fallback when realtime communication is temporarily unavailable.

---

# Home Assistant restart and reload

A major goal of version 3.1.9 is improved behaviour when the FP4All logger is temporarily unavailable.

If the logger is unavailable during:

* a Home Assistant reload;
* a Home Assistant restart;

the last known valid data can be loaded from the local cache.

The sensors therefore remain available.

When the logger becomes available again, current realtime data is automatically retrieved.

---

# Existing entity IDs

Version 3.1.9 is designed to preserve existing entity IDs.

Friendly Names can be improved without changing the entity IDs.

This avoids unnecessary changes to existing Home Assistant dashboards and automations.

---

# Example

Example inverter:

```text
IP:
192.168.178.9

Manufacturer:
PHOENIXTEC

Model:
PV 2800

Serial:
1101BJ0505
```

Possible Friendly Name:

```text
FP4All 192.168.178.9 PV 2800 (0505) Power
```

Existing entity ID:

```text
sensor.garage_fp4all_192_168_178_9_power
```

The entity ID remains unchanged.

---

# Screenshots

Screenshots can be stored in:

```text
screenshots/
```

Example:

```text
screenshots/
├── overview.png
├── sensors.png
├── configuration.png
└── communication.png
```

---

# Version 3.1.9

Version 3.1.9 is a significant improvement over the previous Build 2.6 release.

Main improvements:

* improved local realtime monitoring;
* communication status;
* communication fallback;
* local cache;
* sensors remain available during temporary communication loss;
* sensors remain available after Home Assistant reload/restart;
* operating mode warning during communication loss;
* operating mode text warning;
* automatic Friendly Names;
* preservation of existing entity IDs;
* one cache file per inverter;
* no second manufacturer/model/serial cache file required.

---

# Important

**FP4All Local is local.**

**Realtime data is available directly in Home Assistant.**

**PVOutput.org is not required.**

**No cloud service is required for local realtime data.**

---

# Changelog

See:

```text
CHANGELOG.md
```

for the version history.

---

## License

See `LICENSE` for license information.
