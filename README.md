![https://raw.githubusercontent.com/Q14siX/energy_price_insights/master/custom_components/energy_price_insights/brand/logo.png](https://raw.githubusercontent.com/Q14siX/energy_price_insights/master/custom_components/energy_price_insights/brand/logo.png)

# Energy Price Insights

**Dynamische Strompreise verstehen. Günstige Zeitfenster finden. / Understand dynamic electricity prices. Find favorable time windows.**

**[Deutsch](#deutsch) · [English](#english)**

> **Home Assistant custom integration · Read-only price analysis · Four modular Lovelace designs · DE / EN**

---

## Deutsch

### Was ist Energy Price Insights?

**Energy Price Insights** ist eine unabhängige, kostenlos selbst hostbare Custom-Integration für **Home Assistant**. Sie analysiert dynamische Strompreise aus bereits eingebundenen Preisquellen, berechnet zeitgewichtete Tagesdurchschnitte und erkennt günstige, zusammenhängende Zeitfenster. Eine integrierte, kompakte Lovelace-Karte zeigt die Ergebnisse übersichtlich an.

Die Integration **steuert keine Verbraucher, Batteriespeicher oder Wechselrichter**. Sie sendet weder Schalt- noch Lade-/Entladebefehle. Für eigene Automationen stehen Home-Assistant-Sensoren und ein Binärsensor zur Verfügung. Das Projekt basiert konzeptionell auf der Preisauswertung von [Energy Storage Control](https://github.com/Q14siX/energy_storage_control), ist aber eigenständig und benötigt die ursprüngliche Integration nicht.

![https://raw.githubusercontent.com/Q14siX/energy_price_insights/master/examples/Designs.png](https://raw.githubusercontent.com/Q14siX/energy_price_insights/master/examples/Designs.png)

### Funktionen

- **Zwei Auswertungsverfahren:** Günstigschwelle in Prozent oder günstigste vollständig bepreiste Zeitfenster mit Mindestdauer.
- **Zwei Suchbereiche:** Nur zukünftige oder laufende und zukünftige günstige Phasen.
- **Zeitgewichtete Tagesdurchschnitte:** Heute und morgen, inklusive Angaben zur Datenabdeckung.
- **Zusammenhängende Phasen:** Preisgünstige Abschnitte können über Mitternacht fortgesetzt werden, sofern beide Tage ihre jeweilige Günstiggrenze erfüllen; echte Preiswechsel und Datenlücken bleiben berücksichtigt.
- **Mehrere Konfigurationen:** Unabhängige Preisquellen und mehrere Tibber-Zuhause.
- **Direkte Neubewertung:** Änderungen an Methode, Schwelle, Mindestdauer und Suchbereich werden ohne Neustart neu berechnet.
- **Gültiger Preiscache:** Preisprognosen und laufende Phasen bleiben nach kurzen Neustarts verfügbar. Überalterte Daten werden nicht als aktuelle Preise verwendet (Cache höchstens 24 Stunden nach erfolgreichem Abruf).
- **Deutsch und Englisch:** Einrichtungsdialoge, Entitäten, Status, Karte und visueller Editor.

### Unterstützte Preisquellen

| Quelle | Voraussetzung | Hinweis |
|---|---|---|
| **Tibber** | Offizielle Home-Assistant-Tibber-Integration und Aktion `tibber.get_prices` | Unterstützt mehrere Zuhause. |
| **EPEX Spot** | [ha_epex_spot](https://github.com/mampfes/ha_epex_spot) | *Market Price* (Börsenpreis) und *Total Price* (End-/Gesamtpreis) unterscheiden. |
| **Octopus Energy** | [HomeAssistant-OctopusEnergy](https://github.com/BottlecapDave/HomeAssistant-OctopusEnergy) | Die genannte Integration betrifft UK; Bezugs- und Einspeisetarife nicht verwechseln. |
| **Universelle Quelle** | Geeignete Home-Assistant-`sensor`- oder `event`-Entität mit zeitgestempelten Preisen | Z. B. Nord Pool, aWATTar, ENTSO-E oder REST-/Template-Daten. Attribut- und Feldnamen bei Bedarf zuordnen. |

Eine Quelle mit **nur einem aktuellen Preis ohne Prognoseintervalle** reicht nicht aus, um künftige Zeitfenster zu bestimmen. Unterstützte Währungen umfassen EUR, GBP, SEK, NOK, DKK und PLN. Preise werden innerhalb der vorhandenen Währung auf **Währung/kWh** normiert; **keine Währungsumrechnung**. Negative Strompreise und verschiedene Intervalllängen werden verarbeitet.

### Installation

**Über HACS (benutzerdefiniertes Repository):**

1. In HACS das Menü **⋮ → Benutzerdefinierte Repositories** öffnen.
2. `https://github.com/Q14siX/energy_price_insights` hinzufügen und den Typ **Integration** wählen.
3. **Energy Price Insights** herunterladen und **Home Assistant neu starten**.
4. Unter **Einstellungen → Geräte & Dienste → Integration hinzufügen** nach **Energy Price Insights** suchen und den Assistenten starten.

**Manuelle Installation:** Den vollständigen Ordner `custom_components/energy_price_insights` aus dem Repository oder Installations-ZIP in `<config>/custom_components/energy_price_insights` kopieren. Home Assistant neu starten und die Integration unter **Geräte & Dienste** hinzufügen.

Die jeweilige vorgelagerte Anbieterintegration muss bereits funktionsfähig eingerichtet sein. Für die universelle Quelle ist keine Tibber-, EPEX- oder Octopus-Integration zwingend erforderlich.

### Einrichtung und Optionen

Der mehrstufige Assistent führt durch Preisquelle, gegebenenfalls Quellentitäten, Auswertungsverfahren, den passenden Prozent- bzw. Minutenwert und Suchbereich. Bei universellen Quellen können zusätzliche Feldzuordnungen notwendig sein. **Gerätename und Bereich werden anschließend im normalen Home-Assistant-Abschlussdialog „Benennen und zuordnen“ festgelegt.**

**Bestehende Entitäts-IDs bleiben bei Updates stabil.** Die ursprüngliche Einrichtungseite „Name und Raum“ entfällt. Die abschließende Umbenennung eines Geräts in Home Assistant verändert bereits vergebene Entitäts-IDs nicht automatisch; sie können bei Bedarf über die Entitätsverwaltung geändert werden. Der Bereich kann zusätzlich über die Integrationsoptionen angepasst werden. Schwelle, Mindestdauer, Verfahren und Suchbereich sind über die Optionen sowie die vorhandenen `number`-/`select`-Entitäten veränderbar.

### Wie werden günstige Zeiträume bestimmt?

**Günstigschwelle (Standard):** Für **jeden lokalen Kalendertag** wird separat berechnet:

```text
Günstiggrenze = Tagesminimum + (Tagesmaximum − Tagesminimum) × Schwellenwert / 100
```

Beispiel: 0,10–0,30 €/kWh und 20 % Schwelle ergeben eine Günstiggrenze von **0,14 €/kWh**. Einstellbar von **0–100 %** in **0,01-%-Schritten**. Direkt aneinandergrenzende günstige Intervalle werden zu Phasen verbunden, auch über einen Tageswechsel, sofern sie an beiden Tagen als günstig gelten.

**Mindestdauer:** Einstellbar von **1–1.440 Minuten**. Es werden die günstigsten **vollständig bepreisten, lückenlosen, zusammenhängenden** Abschnitte anhand des **zeitgewichteten Durchschnittspreises** verglichen. Alle gleich günstigen Kandidaten werden berücksichtigt. Überlappende oder angrenzende Kandidaten können eine längere Phase bilden: **60 Minuten Mindestdauer bedeuten nicht automatisch 60 Minuten Gesamtdauer.** Teurere Abschnitte oder Preis-Datenlücken werden nicht überbrückt.

**Suchbereiche:** `future` für zukünftig beginnende Fenster beziehungsweise `active_future` für laufende und zukünftige Fenster. Bei bereits laufenden Phasen ist die Restdauer relevant.

Der zeitgewichtete Tagesdurchschnitt ergibt sich aus `Σ(Preis × bepreiste Minuten) / Σ(bepreiste Minuten)`. Unvollständige Tage sind über `covered_minutes`, `day_duration_minutes` und `full_day_coverage` erkennbar. Lokale Kalendertage mit 23 oder 25 Stunden bei einer Zeitumstellung werden berücksichtigt.

### Eigene Lovelace-Dashboardkarte

**Kartentyp:** `custom:energy-price-insights-card`

Die Karte wird mit der Integration installiert. Die JavaScript-Ressource wird nach Möglichkeit **automatisch und ohne doppelte Einträge** registriert; ein separates HACS-Dashboardpaket ist nicht nötig. Nach Installation oder Update einmal das Dashboard im Browser neu laden.

**Vier eigenständige Designs:**

- **Aurora:** Kompaktes Analyse-Cockpit mit hervorgehobenem Preis und separatem Phasen-/Diagrammbereich.
- **Minimal:** Zurückhaltende, horizontale Darstellung mit reduzierten Elementen.
- **Glass:** Leichte, gestaffelte Bereiche mit dezenten Glas-/Kachel-Effekten.
- **Timeline:** Diagrammorientierte Ansicht, in der der Preisverlauf im Vordergrund steht.

Die Layouts passen sich der Kartenbreite an. In allen vier Designs (Aurora, Minimal, Glass, Timeline) bleiben die im Beispielbild dargestellte Modulreihenfolge und die Verteilung von aktuellem Strompreis, Tageskennzahlen und Preisphase in der Editor-Vorschau und im Dashboard gleich. Aurora und Minimal zeigen die Preisübersicht vor dem Diagramm; Glass und Timeline zeigen das Diagramm zuerst. Die Diagrammsteuerung bleibt unter der Diagrammüberschrift. Nur sehr schmale Karten wechseln zu einer einspaltigen Übersicht. Im visuellen Editor können die meisten Module und ihre Bestandteile **separat aktiviert oder deaktiviert** werden: Kopfzeile und Symbole, oberes Akzentband, aktueller Preis und Einheit, Status und Indikator, die beiden Tagesdurchschnitte, Statistikfelder, Phasenüberschrift/-details, Navigation, Countdown, einzelne Einstellfelder, Verfügbarkeitsanzeige sowie Diagrammtitel, -einheit, -achsen, -gitter, Zeitbereich, Markierungen, Legendenbestandteile, Fadenkreuz, Tooltip, Zoomknöpfe, Mausrad-/Pinch-Zoom und Verschieben. Außerdem: Akzentfarbe, Kartentitel, Diagrammtyp/-höhe, Abstände und erweiterte Entitätszuordnung.

**Vier-Stunden-Kurzprognose:** Unter „Inhalte“ lässt sich die kompakte Preisvorschau (`show_price_sparkline`) separat aktivieren. Ihre Beschriftung kann unabhängig davon ausgeblendet werden (`show_price_sparkline_label`). Für den Text stehen im visuellen Editor die Varianten **„4-Stunden-Trend“** (Standard), **„Nächste 4 Stunden“** und **„4-Stunden-Prognose“** bereit. Alternativ gibt es unter **„Eigener Text“** genau ein Eingabefeld für eine individuelle Beschriftung. Dieser Text wird in jeder Home-Assistant-Sprache unverändert angezeigt. Ein leeres Feld verwendet den automatisch übersetzten Standardtext.

```yaml
show_price_sparkline: true
show_price_sparkline_label: true
sparkline_label_style: custom
sparkline_label_text: "Mein 4-Stunden-Trend"
```

Die Akzentfarbe steuert auch das **ausgewählte günstige Preisfenster**; das obere farbige Rahmenband kann separat deaktiviert werden. Das Diagramm besitzt eine zeitgerechte Darstellung, auswählbare Zeiträume (heute/morgen/beide Tage) und eine Navigation zwischen mehreren gleich günstigen Phasen. Datenaktualisierungen verändern die DOM-Kartenstruktur nur gezielt, statt bei jedem neuen Zustand die komplette Karte neu zu erstellen.

Beispiel-YAML:

```yaml
type: custom:energy-price-insights-card
entity: sensor.epi_wohnung_current_price
design: aurora
chart_span: both
accent: "#0ea5a4"
show_accent_border: false
show_chart: true
show_phase: true
show_averages: true
show_controls: false
```

`wohnung` dient nur als **Beispiel**; den tatsächlichen Entitätsnamen aus der eigenen Home-Assistant-Installation einsetzen. Die Entität kann alternativ bequem im visuellen Editor ausgewählt werden.

### Bereitgestellte Entitäten

`<name>` steht für den bei der Einrichtung erzeugten Namens-Slug. Bei mehreren Tibber-Zuhause können zusätzlich angepasste Namen verwendet werden.

| Entitäts-ID | Bedeutung |
|---|---|
| `sensor.epi_<name>_current_price` | Aktueller Strompreis und Preisstatistik |
| `sensor.epi_<name>_forecast_today` | Zeitgewichteter Durchschnittspreis heute und zugehörige Intervalle |
| `sensor.epi_<name>_forecast_tomorrow` | Zeitgewichteter Durchschnittspreis morgen und zugehörige Intervalle |
| `sensor.epi_<name>_favorable_phase` | Gewählte Preisphase und weitere gleich günstige Phasen |
| `binary_sensor.epi_<name>_favorable_now` | Binärsignal für die laufende günstige Phase |
| `sensor.epi_<name>_price_availability` | Diagnose der Verfügbarkeit und Datenabdeckung |
| `number.epi_<name>_favorable_threshold` | Günstigschwelle in % |
| `number.epi_<name>_window_minutes` | Mindestdauer in Minuten |
| `select.epi_<name>_price_evaluation_mode` | Auswertungsverfahren (`threshold`/`window`) |
| `select.epi_<name>_window_search_scope` | Suchbereich (`future`/`active_future`) |

### Grenzen und Unterstützung

- **Nur Auswertung:** Keine direkte Geräte-, Speicher- oder Netzleistungsregelung.
- **Vorhersage begrenzt durch Anbieter:** Fehlende morgige Daten werden nicht geschätzt; ein nicht vollständig bepreistes Zeitfenster wird nicht erfunden.
- **Keine Währungsumrechnung:** Vergleiche nur Preise derselben Währung bzw. korrekt normalisierte Einheiten.
- **Fehlerberichte:** [GitHub Issues](https://github.com/Q14siX/energy_price_insights/issues).
- **Lizenz:** [Apache License 2.0](LICENSE). Entwickler: [Q14siX](https://github.com/Q14siX). Keine offizielle Verbindung zu den erwähnten Stromanbietern.

---

## English

### What is Energy Price Insights?

**Energy Price Insights** is an independent, self-hostable **Home Assistant custom integration** for analysing dynamic electricity prices. It consumes forecasts from existing price integrations, calculates time-weighted daily averages and finds low-cost continuous periods. An integrated, compact Lovelace card visualises the results.

It **does not control appliances, batteries or inverters**, and issues no switching or charge/discharge commands. Home Assistant sensor and binary sensor entities can be used in your own automations. The project builds on the price-analysis concept from [Energy Storage Control](https://github.com/Q14siX/energy_storage_control), but is independent of that integration.

![https://raw.githubusercontent.com/Q14siX/energy_price_insights/master/examples/Designs.png](https://raw.githubusercontent.com/Q14siX/energy_price_insights/master/examples/Designs.png)

### Features

- **Two evaluation methods:** Percentage-based favorable threshold or cheapest fully priced windows with a minimum duration.
- **Two search scopes:** Future-only, or active and future favorable periods.
- **Time-weighted daily averages:** Today and tomorrow, including forecast-coverage details.
- **Continuous periods:** Favorable intervals can span midnight if prices satisfy each calendar day's threshold; real price changes and gaps remain respected.
- **Multiple configurations:** Independent price sources and multiple Tibber homes.
- **Immediate recalculation:** Changes to evaluation method, threshold, minimum duration and scope apply without restarting.
- **Persistent valid cache:** Forecasts and active periods can survive brief restarts. Outdated data is never reused as a current forecast (no more than 24 hours after a successful fetch).
- **German and English:** Setup, entities, statuses, dashboard card and visual editor.

### Supported price sources

| Source | Requirement | Important |
|---|---|---|
| **Tibber** | Official Home Assistant Tibber integration and `tibber.get_prices` action | Multiple homes supported. |
| **EPEX Spot** | [ha_epex_spot](https://github.com/mampfes/ha_epex_spot) | Distinguish *Market Price* (exchange rate) from *Total Price* (configured end-consumer rate). |
| **Octopus Energy** | [HomeAssistant-OctopusEnergy](https://github.com/BottlecapDave/HomeAssistant-OctopusEnergy) | Linked implementation is for the UK; do not confuse import and export rates. |
| **Generic** | Suitable Home Assistant `sensor` or `event` entity with timestamped rates | E.g. Nord Pool, aWATTar, ENTSO-E, REST or template-based entities, with configurable fields. |

A source offering **only the current price without future intervals** is insufficient for time-window planning. Supported currencies include EUR, GBP, SEK, NOK, DKK and PLN. Supported units are normalised to **currency/kWh** within the source currency; **no FX conversion** is performed. Negative prices and variable interval lengths are supported.

### Installation

**HACS (custom repository):**

1. In HACS open **⋮ → Custom repositories**.
2. Add `https://github.com/Q14siX/energy_price_insights` and select type **Integration**.
3. Download **Energy Price Insights**, then **restart Home Assistant**.
4. Go to **Settings → Devices & services → Add integration**, search for **Energy Price Insights**, and follow the wizard.

**Manual installation:** Copy the entire `custom_components/energy_price_insights` directory from the repository or the installation ZIP to `<config>/custom_components/energy_price_insights`. Restart Home Assistant, then add it under **Devices & services**.

Set up the upstream price-provider integration first. The generic adapter does not require Tibber, EPEX or Octopus specifically.

### Setup and options

The multi-step wizard covers the price provider, source entities where applicable, evaluation method, the relevant percentage or minute value, and search scope. Generic sources may require manual field mapping. **Home Assistant’s standard final “Name and assign” dialog handles the device name and area.**

**Existing entity IDs are preserved across updates.** The separate initial “Name and area” step has been removed. Renaming a device in Home Assistant’s final dialog does not automatically rename existing entity IDs; entity IDs can be edited in the entity registry if needed. Areas can also be changed through the integration options. Threshold, window length, method and scope can be changed through their existing `number` and `select` entities.

### Price evaluation

**Threshold (default):** A separate limit is calculated **per local calendar day**:

```text
Favorable limit = Daily minimum + (Daily maximum − Daily minimum) × Threshold / 100
```

For rates of €0.10–€0.30/kWh and a threshold of 20%, the favorable limit is **€0.14/kWh**. Configurable from **0 to 100%**, in **0.01% increments**. Directly adjacent favorable intervals become continuous phases, even across midnight when both days' limits allow it.

**Minimum-duration method:** Configure **1–1,440 minutes**. The integration compares the **time-weighted average rate** of the cheapest **fully priced, gap-free, contiguous** candidate windows and retains all equally favorable candidates. Overlapping or adjacent candidates may form longer periods: **a 60-minute minimum is not necessarily a 60-minute displayed phase**. More expensive intervals and price-data gaps are not bridged.

**Scopes:** `future` considers future-starting periods, while `active_future` also considers periods already in progress. Remaining time matters when planning a new load.

The time-weighted daily average is `Σ(rate × priced minutes) / Σ(priced minutes)`. Incomplete days can be identified through `covered_minutes`, `day_duration_minutes` and `full_day_coverage`. Local 23-hour and 25-hour days caused by DST transitions are handled.

### Integrated Lovelace dashboard card

**Card type:** `custom:energy-price-insights-card`

The card is bundled with the integration. Its JavaScript resource is registered **automatically without duplicate entries** when possible; no separate HACS dashboard add-on is needed. Reload your dashboard once after an install or upgrade.

**Four structurally different designs:**

- **Aurora:** Compact analysis cockpit with an emphasised rate and separate period/chart panel.
- **Minimal:** Understated, horizontal layout with reduced visual weight.
- **Glass:** Light staggered areas and subtle glass/tile effects.
- **Timeline:** Chart-first presentation with the price trend as the focal point.

Layouts respond to card width. All four designs (Aurora, Minimal, Glass and Timeline) now retain the arrangement shown in the reference design image in both the editor preview and the dashboard: current rate and daily metrics on the left, price period on the right. Aurora and Minimal display the overview above the chart; Glass and Timeline display the chart first. Chart controls stay below the chart title. Only very narrow cards switch to a single-column overview. The visual editor lets users **independently show or hide most modules and their subcomponents**, including: heading and icons, accent border, current rate and unit, status and indicator, both daily averages, statistics, phase heading/details, period navigation, countdown, individual evaluation controls, availability, and chart title/unit/axes/grid/range/markers/legend entries/crosshair/tooltip/zoom buttons/wheel-and-pinch zoom/panning. You can also customise accent color, card title, chart style and height, spacing and advanced entity mapping.

**Four-hour mini forecast:** Enable the compact price preview independently under “Visible content” (`show_price_sparkline`). Its caption can be switched off separately (`show_price_sparkline_label`). The visual editor offers **“4-hour trend”** (default), **“Next 4 hours”**, and **“4-hour forecast”**, or **“Custom text”** with a single editable caption field. The custom caption is displayed unchanged regardless of the Home Assistant language; an empty field falls back to the automatically translated default.

```yaml
show_price_sparkline: true
show_price_sparkline_label: true
sparkline_label_style: custom
sparkline_label_text: "Mein 4-Stunden-Trend"
```

The accent color also applies to the **selected favorable window**, and the top colored border can be disabled independently. The graph uses a time-accurate axis, supports today/tomorrow/both days and highlights the chosen period among equally favorable windows. Normal state updates reconcile only changed DOM nodes instead of replacing the entire card.

Example YAML:

```yaml
type: custom:energy-price-insights-card
entity: sensor.epi_wohnung_current_price
design: aurora
chart_span: both
accent: "#0ea5a4"
show_accent_border: false
show_chart: true
show_phase: true
show_averages: true
show_controls: false
```

Replace `wohnung` with your own entity slug, or choose the entity through the visual editor.

### Provided entities

`<name>` refers to the slug assigned at initial setup; multiple Tibber homes may use additional suffixes.

| Entity ID | Purpose |
|---|---|
| `sensor.epi_<name>_current_price` | Current rate and statistics |
| `sensor.epi_<name>_forecast_today` | Time-weighted average today and price intervals |
| `sensor.epi_<name>_forecast_tomorrow` | Time-weighted average tomorrow and price intervals |
| `sensor.epi_<name>_favorable_phase` | Selected favorable period and other equally favorable periods |
| `binary_sensor.epi_<name>_favorable_now` | Binary signal for a favorable period currently in progress |
| `sensor.epi_<name>_price_availability` | Availability and coverage diagnostic |
| `number.epi_<name>_favorable_threshold` | Percentage threshold |
| `number.epi_<name>_window_minutes` | Minimum period duration |
| `select.epi_<name>_price_evaluation_mode` | Evaluation method (`threshold`/`window`) |
| `select.epi_<name>_window_search_scope` | Eligible periods (`future`/`active_future`) |

### Limitations and support

- **Read-only analytics:** No direct switching, battery management or grid-balancing controls.
- **Forecast limited by source:** Missing next-day rates are not guessed; incomplete price windows are never invented.
- **No currency conversion:** Compare only rates in the same currency or correctly normalised units.
- **Issue tracker:** [GitHub Issues](https://github.com/Q14siX/energy_price_insights/issues).
- **License:** [Apache License 2.0](LICENSE). Developed by [Q14siX](https://github.com/Q14siX); not officially affiliated with any named electricity provider.
