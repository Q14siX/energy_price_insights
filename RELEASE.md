# Energy Price Insights — Initial Public Release

**Version:** `20261024.212504`  
**Release:** First public GitHub / HACS-ready package  
**License:** Apache License 2.0

[Deutsch](#deutsch) · [English](#english)

---

## Deutsch

### Erstveröffentlichung

Energy Price Insights erscheint erstmals als eigenständige, kostenlos nutzbare **Home-Assistant-Integration zur Analyse dynamischer Strompreise**, einschließlich einer integrierten, vollständig responsiven Dashboardkarte. Der Code wird als Custom-Integration unter `custom_components/energy_price_insights` bereitgestellt; die Installation ist manuell oder nach Veröffentlichung des GitHub-Repositories über ein benutzerdefiniertes **HACS-Integrationsrepository** möglich.

### Enthaltene Funktionen

- **Vier eigenständige Dashboarddesigns:** Aurora, Minimal, Glass und Timeline; kompakt, mehrspaltig und responsiv.
- **Konfigurierbare Kurzprognose-Beschriftung:** Korrekte Standardtexte („4-Stunden-Trend“, „Nächste 4 Stunden“, „4-Stunden-Prognose“), ein einziges Eingabefeld für einen eigenen Text (sprachunabhängig angezeigt) und separat deaktivierbare Beschriftung.
- **Modularer visueller Editor:** Separat schaltbare Informationsmodule und fein abgestufte Einzelelemente, darunter Kopfzeilen-Symbol/Zusatztext, Preiseinheit, Statuspunkt, Phasen- und Statistikdetails, Einstellfelder sowie Diagrammachsen, Gitter, Hervorhebungen, Legende, Tooltip und Interaktionsfunktionen.
- **Interaktiver Strompreisverlauf:** Zeitgerechte Preisintervalle, Preis-/Zeit-Tooltip, Fadenkreuz, Heute/Morgen-Auswahl, auswählbare Diagrammtypen, Diagrammhöhe, Zoom und Verschieben.
- **Günstige Preisphasen:** Navigation durch alle gleich günstigen Zeitfenster mit ausgewählter Hervorhebung in der individuellen Akzentfarbe; optionales oberes Akzentband und Countdown.
- **Stabile Dashboardaktualisierung:** Gezielte Aktualisierung vorhandener DOM-Elemente statt vollständigem Neuaufbau bei normalen Home-Assistant-Zustandsänderungen.
- **Preisquellen:** Tibber, EPEX Spot, Octopus Energy (UK) und universelle zeitgestempelte Home-Assistant-Sensor-/Eventdaten.
- **Zwei Auswertungsverfahren:** Prozentuale Tages-Günstigschwelle (0–100 %, Schrittweite 0,01 %) und günstigste zusammenhängende Zeitfenster (1–1.440 Minuten Mindestdauer).
- **Zeitlogik:** Lokale Tagesgrenzen, zusammenhängende günstige Phasen über Mitternacht, Zeitumstellung, gemischte Intervalllängen und zeitgewichtete Durchschnitte.
- **Zwei Suchbereiche:** Nur zukünftige oder laufende und zukünftige Phasen; direkte Neubewertung nach Änderungen der Parameter.
- **Home-Assistant-Entitäten:** Aktueller Preis, Tagesdurchschnitte, günstige Phase, Günstig-Status, Preisverfügbarkeit, `number`- und `select`-Optionen.
- **Mehrsprachigkeit:** Durchgängige deutsche und englische Oberfläche für Integration, Entitäten und Dashboardkarte.
- **Installation und Betrieb:** Eigener Konfigurationsassistent mit Name/Raum, Gültigkeitsprüfung des Preiscaches, idempotente Dashboard-Ressourcenregistrierung und beibehaltene Entitäts-IDs.

**Keine Gerätesteuerung:** Die Integration ist ausschließlich zur Preisanalyse bestimmt und sendet keine Lade-, Entlade- oder Schaltbefehle.

### Installation

1. Repository `https://github.com/Q14siX/energy_price_insights` nach Veröffentlichung in HACS als **benutzerdefiniertes Repository vom Typ Integration** hinzufügen oder `custom_components/energy_price_insights` manuell kopieren.
2. Home Assistant neu starten.
3. Unter **Einstellungen → Geräte & Dienste** die Integration **Energy Price Insights** einrichten.
4. Die gebündelte Karte `custom:energy-price-insights-card` zum Dashboard hinzufügen.

### Prüfung und Einschränkungen

Syntax, zweisprachige Übersetzungsschlüssel, die Kartenmodule und ihre Schalter, die Paketstruktur sowie gezielte Browser- und Berechnungstests wurden geprüft. Die neue Version wurde **nicht vollständig mit allen Drittanbieter-Datenquellen in einer produktiven Home-Assistant-Instanz Ende-zu-Ende getestet**. Die eigentliche Prognose hängt weiterhin von der Verfügbarkeit und Qualität der Quelldaten ab.

Weitere Anleitungen: [README.md](README.md). Fehler: [GitHub Issues](https://github.com/Q14siX/energy_price_insights/issues).

---

## English

### Initial public release

Energy Price Insights launches as a standalone, free **Home Assistant integration for dynamic electricity price analysis**, including a fully responsive Lovelace dashboard card. It is distributed as a custom integration under `custom_components/energy_price_insights`, installable manually or, once its GitHub repository is public, through a custom **HACS Integration** repository.

### Features included

- **Four distinct dashboard designs:** Aurora, Minimal, Glass and Timeline; compact, multi-column and responsive.
- **Customisable mini-forecast caption:** Correct localized presets (“4-hour trend”, “Next 4 hours”, “4-hour forecast”), one custom caption field (displayed unchanged in either language), and a separate caption visibility toggle.
- **Modular visual editor:** Individual switches for information modules and many sub-elements, including header icon/subtitle, price unit, status indicator, period/statistic details, evaluation fields, chart axes, grid, highlighting, legend, tooltip and gesture controls.
- **Interactive electricity price timeline:** Time-accurate slots, hover price/time tooltip, crosshair, today/tomorrow selection, chart styles, height, zoom and pan.
- **Favorable periods:** Navigate all equally favorable windows, highlight the selected window using the custom accent color, optionally hide the colored top border and show a countdown.
- **Stable card updates:** Reconciles existing DOM elements instead of rebuilding the entire card on normal Home Assistant state changes.
- **Price sources:** Tibber, EPEX Spot, Octopus Energy (UK), and generic timestamped Home Assistant sensor/event data.
- **Two evaluation methods:** Daily favorable threshold (0–100%, 0.01% increments) and cheapest continuous periods (1–1,440 minutes minimum duration).
- **Accurate time handling:** Local day boundaries, cross-midnight favorable periods, DST changes, variable interval lengths and time-weighted averages.
- **Two search scopes:** Future-only or active-and-future periods, with immediate reevaluation after settings change.
- **Home Assistant entities:** Current rate, daily averages, favorable period, favorable-now status, price availability, `number` and `select` options.
- **Bilingual interface:** Complete German and English presentation across setup, entities and dashboard card.
- **Deployment:** Multi-step wizard with initial name/area, valid forecast caching, idempotent dashboard resource registration and stable existing entity IDs.

**Read-only analysis:** The integration does not control appliances, batteries or grid import/export, nor does it send switching or charge/discharge commands.

### Installation

1. Once public, add `https://github.com/Q14siX/energy_price_insights` to HACS as a custom **Integration** repository, or copy `custom_components/energy_price_insights` manually.
2. Restart Home Assistant.
3. Under **Settings → Devices & services**, configure **Energy Price Insights**.
4. Add the bundled `custom:energy-price-insights-card` to a dashboard.

### Verification and limitations

Syntax, bilingual translation keys, card modules and toggles, package structure and targeted browser/calculation tests were checked. **A full production end-to-end test with every upstream price-provider account has not been performed.** Forecast availability and quality remain dependent on the upstream price source.

Instructions: [README.md](README.md). Report issues: [GitHub Issues](https://github.com/Q14siX/energy_price_insights/issues).
