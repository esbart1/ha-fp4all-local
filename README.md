# FP4All Local for Home Assistant

![FP4All Logo](screenshots/fp4all_logo.png)

Een lokale Home Assistant integratie voor FP4All PV Solar Inverter Loggers.

Deze integratie leest de gegevens rechtstreeks uit de lokale FP4All logger via het netwerk en maakt de waarden beschikbaar als Home Assistant sensoren.

Geen cloudverbinding nodig.

---

## Functies

* Lokale uitlezing via HTTP
* Ondersteuning voor meerdere FP4All loggers
* Realtime inverter waarden
* Energie productie gegevens
* Statusinformatie van de omvormer
* Index pagina uitlezing
* Historie ondersteuning
* Automatische updates via Home Assistant DataUpdateCoordinator

---

## Ondersteunde waarden

### Actuele waarden

* Vermogen (PAC)
* PV spanning (VPV)
* AC spanning (VAC)
* AC stroom (IAC)
* Netfrequentie (FAC)
* Temperatuur
* Bedrijfsmodus

### Energie

* Dagproductie
* Totale productie
* Levensduur energie
* Bedrijfsuren

---

## Ondersteunde FP4All pagina's

De integratie gebruikt:

### status.xml

Voor snelle realtime waarden:

* vermogen
* temperatuur
* spanning
* stroom

### status.htm

Voor uitgebreide inverter informatie:

* fabrikant
* model
* firmware
* capaciteit
* limieten
* bedrijfsmodus

### index.htm

Voor aanvullende gegevens:

* dagopbrengst
* totale opbrengst
* CO₂ besparing
* opbrengst indicatie

---

## Installatie

### Handmatig

Kopieer de map:

```
custom_components/fp4all
```

naar:

```
config/custom_components/
```

Herstart Home Assistant.

Daarna:

```
Instellingen
→ Apparaten & diensten
→ Integratie toevoegen
→ FP4All Local
```

---

## Configuratie

Benodigd:

* IP-adres van de FP4All logger
* Bereikbaarheid via het lokale netwerk

Voorbeeld:

```
192.168.178.8
```

---

## Build informatie

### Build 2.6

Nieuwe onderdelen:

* High/Low counter helper toegevoegd
* Teststructuur toegevoegd
* GitHub release voorbereiding
* Parser verbeteringen
* Betere scheiding tussen download en parsing

---

## Ontwikkeling

Projectstructuur:

```
fp4all
│
├── coordinator.py
├── sensor.py
│
├── helpers
│   └── combine_high_low.py
│
├── tests
│   └── test_combine_high_low.py
│
├── status_parser.py
└── index_parser.py
```

---

## Screenshots

Worden toegevoegd:

```
screenshots/
├── overview.png
├── sensors.png
└── configuration.png
```

---

## Testomgeving

Getest met:

* Home Assistant
* FP4All logger
* Lokale netwerkverbinding

---

## Versie historie

| Versie | Beschrijving                               |
| ------ | ------------------------------------------ |
| 2.6    | GitHub voorbereiding en helper uitbreiding |
| 2.5    | Parser uitbreidingen                       |
| 2.4    | Basis integratie                           |

---

## Licentie

Dit project is bedoeld voor persoonlijk gebruik en ontwikkeling binnen Home Assistant.
