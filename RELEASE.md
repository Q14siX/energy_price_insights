# Energy Price Insights — Releases

**Aktuelle Version / Current version:** `20261025.001622`  
**Vorherige Version / Previous version:** `20261025.001153`  
**Lizenz / License:** Apache License 2.0

## Aktuelle Änderungen – Deutsch

- **Timeline-Vorschau entspricht dem Dashboard:** Die Modulanordnung aus dem Editor bleibt auf dem Dashboard auch bei etwas größerer Kartenbreite erhalten: aktueller Strompreis und die Tageskennzahlen stehen links untereinander, die Preisphase über die volle Höhe rechts.
- **Einheitliche Diagrammbedienung:** Die Auswahl Heute/Morgen/Heute & morgen und die Zoom-Bedienung stehen im Timeline-Design dauerhaft unter der Diagrammüberschrift. Die Detailwerte der Preisphase behalten eine Spalte bei.
- **Schmale Displays:** Erst bei extrem schmalen Karten wechseln die Spalten aus Platzgründen in eine einspaltige Ansicht. Andere Kartendesigns bleiben unverändert.
- **Home-Assistant-Kompatibilität:** Den veralteten Geräte-Registry-Aufruf `async_get_device` durch `async_get_device_by_identifier` mit passender Config-Entry-ID ersetzt, um die Deprecation-Warnung zu vermeiden und auf Home Assistant 2027.8 vorzubereiten.
- **Kompatibel:** Keine Änderung an Preisberechnung, vorhandenen Entitäts-IDs oder Einrichtung; Logo und Icon bleiben bytegenau erhalten.
- **Prüfung:** JavaScript- und Python-Syntax, JSON-Dateien, Paketintegrität sowie Browsertests bei elf Kartenbreiten; kein horizontaler Überlauf. Kein vollständiger Test auf einer produktiven Home-Assistant-Installation.

## Current changes – English

- **Timeline editor preview matches the dashboard:** The layout chosen in the editor stays the same on the dashboard even with a slightly wider card: current rate and daily metrics are stacked on the left, while the price period spans the full height on the right.
- **Consistent chart toolbar:** Today/tomorrow selection and zoom controls remain below the chart heading in Timeline mode. Price-period detail fields remain in one column.
- **Narrow displays:** Only extremely narrow cards switch to a single-column arrangement. Other card designs remain unchanged.
- **Home Assistant compatibility:** Replaced deprecated device-registry `async_get_device` with config-entry-scoped `async_get_device_by_identifier`, preventing the warning and preparing for Home Assistant 2027.8.
- **Backward compatible:** No pricing logic, entity IDs or setup changes; branding images remain byte-for-byte identical.
- **Verification:** JavaScript/Python syntax, JSON, archive integrity and browser checks at eleven card widths; no horizontal overflow. Not yet fully tested in a production Home Assistant installation.

---

## Vorherige Version / Previous release: `20261025.001153`

### Deutsch

- **Editor-/Dashboard-Darstellung angeglichen:** Im Timeline-Design wird bei ähnlich breiten Karten dieselbe Modulaufteilung verwendet. Die Tageswerte stehen unter dem zweispaltigen Preis-/Phasenbereich, statt beim Öffnen des Editors in die linke Spalte zu wechseln.
- **Schmalansicht gezielter aktiviert:** Der Breakpoint für das besonders schmale Cockpit-Layout wurde von 450 auf 405 Pixel Karteninhaltsbreite abgesenkt.
- **Diagrammbedienung optimiert:** Die Zeitbereichsschalter und Zoomknöpfe bleiben bei typischen Editor-/Dashboard-Kartenbreiten gemeinsam in einer Zeile.
- **Keine Änderungen an Berechnung und Einrichtung:** Preisquellen, Entitäten, Zeitfensterlogik, die vier Kartendesigns und die vereinfachte Einrichtung bleiben erhalten.
- **Layout geprüft:** Browserbasierte Breitentests für alle vier Designs auf neun Kartenbreiten ohne horizontalen Überlauf; Editor-/Dashboard-Vergleich für Timeline erfolgreich.

#### English

- **Consistent editor/dashboard layout:** The Timeline design now uses the same module arrangement at similar card widths. Daily metrics stay underneath the two-column price/period overview rather than moving into its left column in the editor.
- **More deliberate narrow breakpoint:** The extra-narrow cockpit layout switches on at 405 instead of 450 pixels of card content width.
- **Chart controls stay together:** Range-selection and zoom buttons remain on a single row for typical editor and dashboard card widths.
- **No changes to pricing or setup:** Price providers, entities, favorable-period calculations, all four designs, and the streamlined setup remain intact.
- **Layout verification:** Browser-based width checks across all four designs and nine card widths found no horizontal overflow; Timeline editor/dashboard parity was verified.

---

## Vorherige Version / Previous release: `20261025.000817`

### Deutsch

- **Einrichtungsassistent gestrafft:** Die zusätzliche Seite „Name und Raum“ entfällt vollständig.
- **Home-Assistant-Standarddialog verwenden:** Gerätename und Bereich werden ausschließlich im abschließenden Home-Assistant-Dialog „Benennen und zuordnen“ festgelegt.
- **Ablauf unverändert funktionsfähig:** Bei Tibber führt die Anbieterwahl direkt zur Auswahl des Auswertungsverfahrens; bei EPEX Spot, Octopus Energy und universellen Quellen zur Auswahl der Preisdaten.
- **Abwärtskompatibel:** Bestehende Konfigurationen, benutzerdefinierte Namen und Entitäts-IDs bleiben erhalten. Die Karte und deren Designs sind unverändert.
- **Übersetzungen und Dokumentation angepasst:** Der entfallene Schritt wurde aus allen Einrichtungsübersetzungen entfernt.

#### English

- **Streamlined setup:** Removed the redundant “Name and area” wizard page.
- **Native Home Assistant naming:** Device name and area are selected in Home Assistant’s final “Name and assign” dialog.
- **Provider routing retained:** Tibber now goes straight to evaluation method selection; EPEX Spot, Octopus Energy and generic sources proceed to price entity selection.
- **Backwards-compatible:** Existing configurations, legacy custom names and entity IDs remain unchanged. The dashboard card and its designs have not been modified.
- **Updated translations and documentation:** Removed the obsolete setup step from all translation files.

---

## Vorherige Version / Previous release: `20261024.212504`

### Deutsch

#### Erstveröffentlichung

Energy Price Insights erscheint erstmals als eigenständige, kostenlos nutzbare **Home-Assistant-Integration zur Analyse dynamischer Strompreise**, einschließlich einer integrierten, vollständig responsiven Dashboardkarte. Der Code wird als Custom-Integration unter `custom_components/energy_price_insights` bereitgestellt; die Installation ist manuell oder nach Veröffentlichung des GitHub-Repositories über ein benutzerdefiniertes **HACS-Integrationsrepository** möglich.

#### Enthaltene Funktionen

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
- **Installation und Betrieb:** Mehrstufiger Konfigurationsassistent, Gültigkeitsprüfung des Preiscaches, idempotente Dashboard-Ressourcenregistrierung und beibehaltene Entitäts-IDs. (Zum Zeitpunkt dieser Erstveröffentlichung beinhaltete der Assistent noch eine eigene Namens-/Raumseite.)

**Keine Gerätesteuerung:** Die Integration ist ausschließlich zur Preisanalyse bestimmt und sendet keine Lade-, Entlade- oder Schaltbefehle.

#### Installation

1. Repository `https://github.com/Q14siX/energy_price_insights` nach Veröffentlichung in HACS als **benutzerdefiniertes Repository vom Typ Integration** hinzufügen oder `custom_components/energy_price_insights` manuell kopieren.
2. Home Assistant neu starten.
3. Unter **Einstellungen → Geräte & Dienste** die Integration **Energy Price Insights** einrichten.
4. Die gebündelte Karte `custom:energy-price-insights-card` zum Dashboard hinzufügen.

#### Prüfung und Einschränkungen

Syntax, zweisprachige Übersetzungsschlüssel, die Kartenmodule und ihre Schalter, die Paketstruktur sowie gezielte Browser- und Berechnungstests wurden geprüft. Die neue Version wurde **nicht vollständig mit allen Drittanbieter-Datenquellen in einer produktiven Home-Assistant-Instanz Ende-zu-Ende getestet**. Die eigentliche Prognose hängt weiterhin von der Verfügbarkeit und Qualität der Quelldaten ab.

Weitere Anleitungen: [README.md](README.md). Fehler: [GitHub Issues](https://github.com/Q14siX/energy_price_insights/issues).

---

### English

#### Initial public release

Energy Price Insights launches as a standalone, free **Home Assistant integration for dynamic electricity price analysis**, including a fully responsive Lovelace dashboard card. It is distributed as a custom integration under `custom_components/energy_price_insights`, installable manually or, once its GitHub repository is public, through a custom **HACS Integration** repository.

#### Features included

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
- **Deployment:** Multi-step setup wizard, valid forecast caching, idempotent dashboard resource registration and stable existing entity IDs. (This initial release also included a separate name/area page, removed in the subsequent release.)

**Read-only analysis:** The integration does not control appliances, batteries or grid import/export, nor does it send switching or charge/discharge commands.

#### Installation

1. Once public, add `https://github.com/Q14siX/energy_price_insights` to HACS as a custom **Integration** repository, or copy `custom_components/energy_price_insights` manually.
2. Restart Home Assistant.
3. Under **Settings → Devices & services**, configure **Energy Price Insights**.
4. Add the bundled `custom:energy-price-insights-card` to a dashboard.

#### Verification and limitations

Syntax, bilingual translation keys, card modules and toggles, package structure and targeted browser/calculation tests were checked. **A full production end-to-end test with every upstream price-provider account has not been performed.** Forecast availability and quality remain dependent on the upstream price source.

Instructions: [README.md](README.md). Report issues: [GitHub Issues](https://github.com/Q14siX/energy_price_insights/issues).

