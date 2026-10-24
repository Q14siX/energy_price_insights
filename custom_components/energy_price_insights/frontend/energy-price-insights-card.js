/* Energy Price Insights Lovelace card — self-contained and bilingual. */
const CARD_TYPE = 'energy-price-insights-card';
const DEFAULTS = Object.freeze({
  type: `custom:${CARD_TYPE}`, design: 'aurora', chart_span: 'both',
  show_accent_border: true, show_title: true, show_header_icon: true, show_header_subtitle: true,
  show_price: true, show_price_label: true, show_price_unit: true, show_price_sparkline: false,
  show_price_sparkline_label: true, sparkline_label_style: 'trend', sparkline_label_text: '',
  show_status: true, show_status_indicator: true, show_averages: true,
  show_chart: true, show_phase: true, show_phase_title: true, show_statistics: false, show_controls: false,
  show_control_method: true, show_control_scope: true, show_control_threshold: true, show_control_minutes: true,
  show_availability: false, show_legend: true, show_legend_price: true, show_legend_selected: true,
  show_chart_title: true, show_chart_unit: true, show_navigation: true, show_zoom: false,
  show_countdown: true, show_phase_start: true, show_phase_end: true,
  show_phase_average: true, show_phase_duration: true, show_phase_minimum: false,
  show_average_today: true, show_average_tomorrow: true,
  show_minimum: true, show_maximum: true, show_chart_axes: true,
  show_chart_crosshair: true, show_chart_tooltip: true, show_chart_hint: false,
  show_chart_range: true, show_chart_highlight: true, show_chart_selected_phase: true, show_chart_other_phases: true,
  show_chart_now: true, show_chart_grid: true, show_chart_gesture_zoom: true, show_chart_pan: true,
  density: 'compact', chart_style: 'auto', chart_height: 'compact', title: '', accent: '#0ea5a4',
});
const I18N = {
  de: {
    name: 'Energy Price Insights', configure: 'Strompreis-Entität auswählen',
    current: 'Aktueller Strompreis', today: 'Ø heute', tomorrow: 'Ø morgen',
    favorable: 'Jetzt günstig', notFavorable: 'Derzeit nicht günstig',
    start: 'Beginn', end: 'Ende', nextWindow: 'Günstige Preisphase',
    phase: 'Günstige Preisphase', noWindow: 'Noch kein geeignetes Zeitfenster verfügbar',
    windowAverage: 'Ø im Zeitfenster', remaining: 'Verbleibend', minutes: 'Minuten',
    minimum: 'Minimum', maximum: 'Maximum', average: 'Durchschnitt',
    forecast: 'Strompreisprognose', price: 'Strompreis', marked: 'Ausgewähltes günstiges Fenster',
    now: 'Jetzt', todayOnly: 'Heute', tomorrowOnly: 'Morgen', twoDays: 'Heute & morgen',
    controls: 'Auswertung einstellen', method: 'Verfahren', scope: 'Suchbereich',
    threshold: 'Günstigschwelle', duration: 'Dauer', availability: 'Preisverfügbarkeit',
    ready: 'Preise verfügbar', no_forecast: 'Keine Preisdaten',
    no_current_price: 'Aktueller Preis fehlt', no_complete_window: 'Kein vollständiges Zeitfenster',
    unknown: 'Noch keine Daten', noPrice: 'Keine Preisdaten für diese Darstellung',
    design: 'Design', chartSpan: 'Zeitraum des Diagramms',
    title: 'Kartentitel (optional)', accent: 'Akzentfarbe (#RRGGBB)', accentBorder: 'Farbiges oberes Rahmenband',
    sections: 'Module ein- und ausblenden', advanced: 'Erweiterte Entitätszuordnung',
    entity: 'Aktueller Preis (erforderlich)', phaseEntity: 'Preisphase',
    todayEntity: 'Tagesdurchschnitt heute', tomorrowEntity: 'Tagesdurchschnitt morgen',
    favorableEntity: 'Gerade günstig (Binärsensor)', availabilityEntity: 'Preisverfügbarkeit',
    thresholdEntity: 'Günstigschwelle (%)', minutesEntity: 'Zeitfensterdauer (Minuten)',
    methodEntity: 'Auswertungsverfahren', scopeEntity: 'Berücksichtigte Zeitfenster',
    header: 'Überschrift', headerIcon: 'Symbol in der Kopfzeile', headerSubtitle: 'Zusatztext in der Kopfzeile', headerSubtitleText: 'Strompreisanalyse', priceLabel: 'Beschriftung des aktuellen Preises', priceUnit: 'Preiseinheit beim aktuellen Preis', statusIndicator: 'Statuspunkt', phaseTitle: 'Titel der Preisphase', priceSparkline:'Kurzprognose (4 Stunden)', priceSparklineLabel:'Beschriftung der Kurzprognose', currentPrice: 'Aktueller Preis', status: 'Günstig-Status',
    dailyAverages: 'Tagesdurchschnitte', graph: 'Preisverlauf', phaseModule: 'Günstige Phase',
    statistics: 'Min/Max/Ø', controlsModule: 'Einstellbare Steuerungen', controlMethod: 'Auswertungsverfahren ändern', controlScope: 'Suchbereich ändern', controlThreshold: 'Günstigschwelle ändern', controlMinutes: 'Mindestdauer ändern',
    availabilityModule: 'Datenverfügbarkeit', legend: 'Diagrammlegende', legendPrice: 'Legende: Preis', legendSelected: 'Legende: Gewähltes Fenster', chartTitle: 'Diagrammtitel', chartUnit: 'Preiseinheit im Diagramm', chartSelectedPhase: 'Gewähltes Fenster hervorheben', chartOtherPhases: 'Weitere günstige Fenster markieren',
    aurora: 'Aurora', minimal: 'Minimal', glass: 'Glass', timeline: 'Timeline',
    incomplete: 'Tagespreise noch unvollständig', covered: 'Abgedeckt',
    unavailable: 'Nicht verfügbar', invalid: 'Wähle eine gültige Strompreis-Entität.',
    adjust: 'Konfiguration', fieldUnits: 'Währung je kWh',
    periodDuration:'Gesamtdauer', minimumDuration:'Mindestdauer', previousPhase:'Vorherige Preisphase', nextPhase:'Nächste Preisphase', of:'von', zoomIn:'Vergrößern', zoomOut:'Verkleinern', resetZoom:'Zurücksetzen', chartHint:'Mausrad oder Zwei-Finger-Geste zum Zoomen · Ziehen zum Verschieben', navigationModule:'Navigation zwischen Preisphasen', zoomModule:'Diagramm-Zoom',
    countdownModule:'Countdown bis zum Start', startsIn:'Start in', running:'Preisphase läuft', activeNow:'Bereits aktiv',
    dayShort:'T',hourShort:'Std.',minuteShort:'Min.', phaseStartModule:'Beginn der Preisphase',
    phaseEndModule:'Ende der Preisphase', phaseAverageModule:'Durchschnitt in der Phase',
    phaseDurationModule:'Dauer der Preisphase', phaseMinimumModule:'Mindestdauer',
    todayModule:'Tagesdurchschnitt heute', tomorrowModule:'Tagesdurchschnitt morgen',
    minModule:'Tagesminimum', maxModule:'Tagesmaximum', chartAxesModule:'Diagrammachsen',
    chartCrosshairModule:'Fadenkreuz', chartTooltipModule:'Preis-Tooltip', chartHintModule:'Bedienhinweis unter dem Diagramm',
    chartGestureZoom:'Zoomen mit Mausrad oder Pinch-Geste', chartPan:'Diagramm durch Ziehen verschieben', chartRangeModule:'Zeitraumauswahl im Diagramm', chartHighlightModule:'Günstige Phasen markieren', chartNowModule:'Jetzt-Markierung', chartGridModule:'Diagramm-Hilfslinien',
    evaluationThreshold:'Günstigschwelle (%)', evaluationWindow:'Günstigstes Zeitfenster (Minuten)', scopeFuture:'Nur zukünftige Zeitfenster', scopeActiveFuture:'Laufende und zukünftige Zeitfenster', nextFourHours:'Nächste 4 Stunden', sparklineTrend:'4-Stunden-Trend', sparklineForecast:'4-Stunden-Prognose', sparklineLabelStyle:'Beschriftung der Kurzprognose', sparklineCustom:'Eigener Text', sparklineText:'Eigene Beschriftung', sparklineTextPlaceholder:'Leer lassen für den Standardtext', editorSubtitle:'Gestaltung und Inhalte individuell anpassen', editorSource:'Datenquelle', editorAppearance:'Darstellung', editorDesignHint:'Vier eigenständige Layouts für unterschiedliche Dashboards', editorContent:'Inhalte', editorPhase:'Preisphase & Countdown', editorChart:'Diagramm & Interaktion', editorAdvanced:'Entitäten & Erweiterte Zuordnung', editorChartHeight:'Diagrammhöhe', editorChartStyle:'Diagrammtyp', editorDensity:'Abstände', compact:'Kompakt', comfortable:'Großzügig', balanced:'Ausgewogen', expanded:'Groß', auto:'Zum Design passend', line:'Linie', area:'Fläche', bars:'Balken', editorOptional:'Optional', editorSourceHint:'Preis-Entität auswählen; weitere Entitäten werden automatisch erkannt.', editorLayout:'Layout', phaseCompact:'Preisphase',
  },
  en: {
    name: 'Energy Price Insights', configure: 'Choose a price entity',
    current: 'Current electricity price', today: 'Avg today', tomorrow: 'Avg tomorrow',
    favorable: 'Favorable now', notFavorable: 'Not currently favorable',
    start: 'Start', end: 'End', nextWindow: 'Favorable price period',
    phase: 'Favorable price period', noWindow: 'No suitable time window available yet',
    windowAverage: 'Window average', remaining: 'Remaining', minutes: 'minutes',
    minimum: 'Minimum', maximum: 'Maximum', average: 'Average',
    forecast: 'Price forecast', price: 'Electricity price', marked: 'Selected favorable window',
    now: 'Now', todayOnly: 'Today', tomorrowOnly: 'Tomorrow', twoDays: 'Today & tomorrow',
    controls: 'Adjust price evaluation', method: 'Evaluation mode', scope: 'Search scope',
    threshold: 'Favorable threshold', duration: 'Duration', availability: 'Price availability',
    ready: 'Prices available', no_forecast: 'No price forecast',
    no_current_price: 'Current price missing', no_complete_window: 'No complete time window',
    unknown: 'No data yet', noPrice: 'No price data for this view',
    design: 'Design', chartSpan: 'Chart range',
    title: 'Card title (optional)', accent: 'Accent color (#RRGGBB)', accentBorder: 'Colored top border',
    sections: 'Show or hide modules', advanced: 'Advanced entity mapping',
    entity: 'Current price (required)', phaseEntity: 'Price period',
    todayEntity: 'Average today', tomorrowEntity: 'Average tomorrow',
    favorableEntity: 'Favorable now (binary sensor)', availabilityEntity: 'Price availability',
    thresholdEntity: 'Favorable threshold (%)', minutesEntity: 'Window duration (minutes)',
    methodEntity: 'Evaluation mode', scopeEntity: 'Eligible time windows',
    header: 'Header', headerIcon: 'Header icon', headerSubtitle: 'Header subtitle', headerSubtitleText: 'Price insights', priceLabel: 'Current price label', priceUnit: 'Current price unit', statusIndicator: 'Status indicator', phaseTitle: 'Price period heading', priceSparkline:'Short forecast (4 hours)', priceSparklineLabel:'Short forecast label', currentPrice: 'Current price', status: 'Favorable status',
    dailyAverages: 'Daily averages', graph: 'Price chart', phaseModule: 'Favorable period',
    statistics: 'Min/Max/Avg', controlsModule: 'Editable controls', controlMethod: 'Evaluation mode control', controlScope: 'Search scope control', controlThreshold: 'Favorable threshold control', controlMinutes: 'Minimum duration control',
    availabilityModule: 'Data availability', legend: 'Chart legend', legendPrice: 'Legend: Price', legendSelected: 'Legend: Selected window', chartTitle: 'Chart title', chartUnit: 'Price unit in chart', chartSelectedPhase: 'Highlight selected window', chartOtherPhases: 'Mark other favorable windows',
    aurora: 'Aurora', minimal: 'Minimal', glass: 'Glass', timeline: 'Timeline',
    incomplete: 'Daily forecast incomplete', covered: 'Covered',
    unavailable: 'Unavailable', invalid: 'Select a valid electricity price entity.',
    adjust: 'Configuration', fieldUnits: 'Currency per kWh',
    periodDuration:'Total duration', minimumDuration:'Minimum duration', previousPhase:'Previous price period', nextPhase:'Next price period', of:'of', zoomIn:'Zoom in', zoomOut:'Zoom out', resetZoom:'Reset', chartHint:'Scroll or pinch to zoom · Drag to pan', navigationModule:'Price period navigation', zoomModule:'Chart zoom',
    countdownModule:'Countdown until start', startsIn:'Starts in', running:'Price period in progress', activeNow:'Already active',
    dayShort:'d',hourShort:'h',minuteShort:'min', phaseStartModule:'Period start',
    phaseEndModule:'Period end', phaseAverageModule:'Period average',
    phaseDurationModule:'Period duration', phaseMinimumModule:'Minimum duration',
    todayModule:'Today average', tomorrowModule:'Tomorrow average',
    minModule:'Day minimum', maxModule:'Day maximum', chartAxesModule:'Chart axes',
    chartCrosshairModule:'Crosshair', chartTooltipModule:'Price tooltip', chartHintModule:'Chart interaction hint',
    chartGestureZoom:'Mousewheel and pinch zoom', chartPan:'Drag to pan chart', chartRangeModule:'Chart range switcher', chartHighlightModule:'Highlight favorable periods', chartNowModule:'Current time marker', chartGridModule:'Chart grid lines',
    evaluationThreshold:'Favorable threshold (%)', evaluationWindow:'Cheapest continuous window (minutes)', scopeFuture:'Future windows only', scopeActiveFuture:'Active and future windows', nextFourHours:'Next 4 hours', sparklineTrend:'4-hour trend', sparklineForecast:'4-hour forecast', sparklineLabelStyle:'Short forecast caption', sparklineCustom:'Custom text', sparklineText:'Custom caption', sparklineTextPlaceholder:'Leave blank to use the default', editorSubtitle:'Customize every part of the card', editorSource:'Data source', editorAppearance:'Appearance', editorDesignHint:'Four distinct layouts for different dashboards', editorContent:'Visible content', editorPhase:'Price period & countdown', editorChart:'Chart & interaction', editorAdvanced:'Entities & advanced mapping', editorChartHeight:'Chart height', editorChartStyle:'Chart style', editorDensity:'Spacing', compact:'Compact', comfortable:'Comfortable', balanced:'Balanced', expanded:'Large', auto:'Match design', line:'Line', area:'Area', bars:'Bars', editorOptional:'Optional', editorSourceHint:'Choose the rate entity; related entities are discovered automatically.', editorLayout:'Layout', phaseCompact:'Period',
  },
};
const MODULES = {
  show_accent_border: 'accentBorder',
  show_title: 'header', show_header_icon: 'headerIcon', show_header_subtitle: 'headerSubtitle',
  show_price: 'currentPrice', show_price_label: 'priceLabel', show_price_unit: 'priceUnit',
  show_price_sparkline:'priceSparkline',show_price_sparkline_label:'priceSparklineLabel',show_status: 'status',show_status_indicator:'statusIndicator',
  show_averages: 'dailyAverages', show_chart: 'graph', show_phase: 'phaseModule', show_phase_title: 'phaseTitle',
  show_statistics: 'statistics', show_controls: 'controlsModule', show_control_method:'controlMethod', show_control_scope:'controlScope', show_control_threshold:'controlThreshold', show_control_minutes:'controlMinutes',
  show_availability: 'availabilityModule', show_legend: 'legend', show_legend_price: 'legendPrice', show_legend_selected: 'legendSelected', show_chart_title: 'chartTitle', show_chart_unit:'chartUnit',
  show_navigation:'navigationModule', show_zoom:'zoomModule', show_countdown:'countdownModule',
  show_phase_start:'phaseStartModule', show_phase_end:'phaseEndModule',
  show_phase_average:'phaseAverageModule', show_phase_duration:'phaseDurationModule',
  show_phase_minimum:'phaseMinimumModule', show_average_today:'todayModule',
  show_average_tomorrow:'tomorrowModule', show_minimum:'minModule',
  show_maximum:'maxModule', show_chart_axes:'chartAxesModule',
  show_chart_crosshair:'chartCrosshairModule', show_chart_tooltip:'chartTooltipModule',
  show_chart_hint:'chartHintModule',show_chart_range:'chartRangeModule',
  show_chart_gesture_zoom:'chartGestureZoom',show_chart_pan:'chartPan',show_chart_highlight:'chartHighlightModule',show_chart_selected_phase:'chartSelectedPhase',show_chart_other_phases:'chartOtherPhases',show_chart_now:'chartNowModule',show_chart_grid:'chartGridModule',
};
const RELATED = {
  phase_entity: ['sensor.', '_favorable_phase'], today_entity: ['sensor.', '_forecast_today'],
  tomorrow_entity: ['sensor.', '_forecast_tomorrow'],
  favorable_entity: ['binary_sensor.', '_favorable_now'],
  availability_entity: ['sensor.', '_price_availability'],
  threshold_entity: ['number.', '_favorable_threshold'],
  minutes_entity: ['number.', '_window_minutes'],
  method_entity: ['select.', '_price_evaluation_mode'],
  scope_entity: ['select.', '_window_search_scope'],
};
const EDITOR_FIELDS = {
  phase_entity: 'phaseEntity', today_entity: 'todayEntity', tomorrow_entity: 'tomorrowEntity',
  favorable_entity: 'favorableEntity', availability_entity: 'availabilityEntity',
  threshold_entity: 'thresholdEntity', minutes_entity: 'minutesEntity',
  method_entity: 'methodEntity', scope_entity: 'scopeEntity',
};
const esc = v => String(v ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const isOn = val => String(val ?? '').toLowerCase() === 'on';
const isValid = state => !!state && !['unknown', 'unavailable'].includes(state.state);
const finite = val => {const n = Number(val); return val === null || val === undefined || val === '' || !Number.isFinite(n) ? null : n;};
const lang = hass => String(hass?.locale?.language || hass?.language || 'en').toLowerCase().startsWith('de') ? 'de' : 'en';
function tr(hass, key) {return (I18N[lang(hass)] || I18N.en)[key] || key;}
function money(val, currency, hass) {
  const n = finite(val);
  if (n === null) return '—';
  const code = String(currency || 'EUR').toUpperCase();
  const symbol = {EUR:'€',GBP:'£',SEK:'kr',NOK:'kr',DKK:'kr',PLN:'zł'}[code] || code;
  return `${new Intl.NumberFormat(lang(hass),{minimumFractionDigits:2, maximumFractionDigits:4}).format(n)} ${symbol}/kWh`;
}
function formatTime(date, hass, withDay=false) {
  const time = new Date(date);
  if (Number.isNaN(time.getTime())) return '—';
  const locale = lang(hass);
  try {
    const opts = {timeZone:hass?.config?.time_zone || undefined, hour:'2-digit',minute:'2-digit',hourCycle:'h23'};
    const clock=new Intl.DateTimeFormat(locale,opts).format(time);
    if (!withDay) return locale==='de' ? `${clock} Uhr` : clock;
    const dateText=new Intl.DateTimeFormat(locale,{timeZone:opts.timeZone,day:'2-digit',month:'2-digit'}).format(time);
    return locale==='de' ? `${dateText} · ${clock} Uhr` : `${dateText} · ${clock}`;
  } catch {return '—';}
}
function countdownText(ms,hass) {
  const minutes=Math.max(0,Math.ceil(ms/60000));
  const days=Math.floor(minutes/1440), hours=Math.floor((minutes%1440)/60), mins=minutes%60;
  const units=[];
  if(days)units.push(`${days} ${tr(hass,'dayShort')}`);
  if(hours)units.push(`${hours} ${tr(hass,'hourShort')}`);
  if(mins || !units.length)units.push(`${mins} ${tr(hass,'minuteShort')}`);
  return units.join(' ');
}
function discover(hass, selected) {
  if (selected && hass?.states?.[selected]) return selected;
  const ids = Object.keys(hass?.states || {}).filter(id => /^sensor\.epi_.*_current_price$/.test(id));
  return ids.length === 1 ? ids[0] : selected;
}
function related(base, key, config) {
  if (config[key]) return config[key];
  if (!base || !base.startsWith('sensor.') || !base.endsWith('_current_price')) return '';
  const suffix = RELATED[key];
  return suffix ? suffix[0] + base.slice('sensor.'.length, -'_current_price'.length) + suffix[1] : '';
}
function loadModel(hass, config) {
  const base = discover(hass, config.entity);
  const get = key => hass?.states?.[related(base, key, config)];
  return {base, current:hass?.states?.[base], phase:get('phase_entity'),
    today:get('today_entity'), tomorrow:get('tomorrow_entity'), favorable:get('favorable_entity'),
    availability:get('availability_entity'), threshold:get('threshold_entity'),
    minutes:get('minutes_entity'), method:get('method_entity'), scope:get('scope_entity')};
}
function extractSeries(model, config, hass) {
  const selected = config.chart_span || 'both';
  const candidates = selected === 'today' ? [model.today] : selected === 'tomorrow' ? [model.tomorrow] : [model.today, model.tomorrow];
  const rows = candidates.flatMap(st => Array.isArray(st?.attributes?.data) ? st.attributes.data : []);
  if (!rows.length && selected === 'both') rows.push(...(Array.isArray(model.current?.attributes?.data) ? model.current.attributes.data : []));
  const slots=[];
  for (const row of rows) {
    const a = Date.parse(row.start_time || row.start || '');
    const b = Date.parse(row.end_time || row.end || '');
    const price = finite(row.price_per_kwh ?? row.price ?? row.value_inc_vat);
    if (!Number.isFinite(a) || price === null) continue;
    slots.push({a,b:Number.isFinite(b)&&b>a?b:null,price});
  }
  slots.sort((x,y) => x.a-y.a);
  const gaps=slots.slice(1).map((s,i)=>s.a-slots[i].a).filter(v=>v>0&&v<=3600000);
  const interval=gaps.length?Math.min(...gaps):900000;
  const out=[];
  slots.forEach((slot,i)=>{
    const end = Math.min(slot.b ?? slot.a+interval, slots[i+1]?.a ?? Infinity);
    if(end>slot.a && !(out.length && out[out.length-1].a === slot.a))out.push({...slot,b:end});
  });
  return out;
}
function sparklineLabel(config,hass){
  const style=config?.sparkline_label_style||'trend';
  if(style==='custom'){
    const custom=typeof config?.sparkline_label_text==='string'?config.sparkline_label_text.trim():'';
    return custom||tr(hass,'sparklineTrend');
  }
  return tr(hass,style==='next'?'nextFourHours':style==='forecast'?'sparklineForecast':'sparklineTrend');
}
function sparkline(model,hass,config){
  const data=extractSeries(model,{chart_span:'both'},hass);
  const now=Date.now(),end=now+4*3600000;
  const rows=data.filter(s=>s.b>now&&s.a<end);
  if(!rows.length)return '';
  // This is a time-proportional, interval-accurate four-hour forecast.
  // Missing data stays empty instead of being connected by a fake trend line.
  const min=Math.min(...rows.map(r=>r.price)),max=Math.max(...rows.map(r=>r.price));
  const W=180,H=38,pad=3;
  const x=t=>pad+(Math.max(now,Math.min(end,t))-now)/(end-now)*(W-2*pad);
  const y=p=>pad+(1-(p-min)/(max-min||1))*(H-2*pad);
  const lines=rows.map(r=>{
    const a=Math.max(now,r.a),b=Math.min(end,r.b);
    return b>a?`<path d="M${x(a).toFixed(1)} ${y(r.price).toFixed(1)} H${x(b).toFixed(1)}" fill="none" stroke="var(--epi-accent)" stroke-width="2.5" stroke-linecap="round" vector-effect="non-scaling-stroke"/>`:'';
  }).join('');
  const connections=rows.slice(1).map((r,i)=>{
    const prev=rows[i];
    return Math.abs(r.a-prev.b)<=1000 && r.a>now && r.a<end
      ? `<path d="M${x(r.a).toFixed(1)} ${y(prev.price).toFixed(1)} V${y(r.price).toFixed(1)}" fill="none" stroke="var(--epi-accent)" stroke-width="2.5" vector-effect="non-scaling-stroke"/>`:'';
  }).join('');
  const minLabel=money(min,model.current?.attributes?.currency||'EUR',hass);
  const maxLabel=money(max,model.current?.attributes?.currency||'EUR',hass);
  const label=sparklineLabel(config,hass);
  return `<div class="epi-hero-trend" title="${esc(label)} · ${esc(minLabel)} – ${esc(maxLabel)}">${config?.show_price_sparkline_label===false?'':`<span class="epi-trend-caption">${esc(label)}</span>`}<svg viewBox="0 0 ${W} ${H}" preserveAspectRatio="none" role="img" aria-label="${esc(label)} · ${esc(minLabel)} – ${esc(maxLabel)}">${lines}${connections}</svg></div>`;
}
function chartSvg(data, phase, allPhases, config, hass, view, width=760) {
  if (!data.length) return `<div class="epi-empty">${esc(tr(hass,'noPrice'))}</div>`;
  const W=Math.max(260,Math.floor(width||620));
  const H={compact:170,balanced:210,expanded:255}[config.chart_height]||210;
  const L=61,R=11,T=16,B=31;
  const minX=Math.min(...data.map(v=>v.a)),maxX=Math.max(...data.map(v=>v.b));
  let from=Math.max(minX,view?.from??minX),to=Math.min(maxX,view?.to??maxX);
  if(to-from<60000){from=minX;to=maxX;}
  const visible=data.filter(s=>s.a<to&&s.b>from), costs=(visible.length?visible:data).map(s=>s.price);
  const vmin=Math.min(...costs),vmax=Math.max(...costs);
  const pad=Math.max((vmax-vmin)*.13,.002),lo=vmin-pad,hi=vmax+pad;
  const X=t=>L+(t-from)/(to-from||1)*(W-L-R);
  const Y=p=>T+(hi-p)/(hi-lo||1)*(H-T-B);
  const formatter=new Intl.NumberFormat(lang(hass),{minimumFractionDigits:3,maximumFractionDigits:4});
  const showAxes=config.show_chart_axes!==false,showGrid=config.show_chart_grid!==false;
  const tickY=showAxes||showGrid?Array.from({length:4},(_,i)=>{
    const f=i/3,y=T+f*(H-T-B);
    return `${showGrid?`<line x1="${L}" y1="${y}" x2="${W-R}" y2="${y}" class="epi-grid-line"/>`:''}${showAxes?`<text class="epi-axis-text" x="${L-9}" y="${y+4.2}" text-anchor="end">${esc(formatter.format(hi-f*(hi-lo)))}</text>`:''}`;
  }).join(''):'';
  const span=to-from,tickCount=W<405?(span>26*3600000?1:2):Math.max(2,Math.min(6,Math.floor((W-L-R)/120)));
  const tickX=showAxes?Array.from({length:tickCount+1},(_,i)=>{
    const time=from+span*i/tickCount,x=X(time), tz=hass?.config?.time_zone||undefined;
    const clock=new Intl.DateTimeFormat(lang(hass),{timeZone:tz,hour:'2-digit',minute:'2-digit',hourCycle:'h23'}).format(new Date(time));
    const day=span>26*3600000?new Intl.DateTimeFormat(lang(hass),{timeZone:tz,day:'2-digit',month:'2-digit'}).format(new Date(time)):'';
    return `<line x1="${x}" y1="${H-B}" x2="${x}" y2="${H-B+4}" class="epi-tick"/><text class="epi-axis-text" x="${x}" y="${H-8}" text-anchor="${i===0?'start':i===tickCount?'end':'middle'}">${esc(day?`${day} ${clock}`:clock)}</text>`;
  }).join(''):'';
  const style=['line','area','bars'].includes(config.chart_style)?config.chart_style:({minimal:'line',timeline:'bars',aurora:'area',glass:'area'}[config.design]||'area');
  const areas=visible.map(s=>{const x1=X(Math.max(from,s.a)),x2=X(Math.min(to,s.b)),y=Y(s.price),base=H-B;
    return `<path class="epi-area" d="M${x1.toFixed(2)} ${base} V${y.toFixed(2)} H${x2.toFixed(2)} V${base} Z"/>`;
  }).join('');
  const bars=visible.map(s=>{const x1=X(Math.max(from,s.a)),x2=X(Math.min(to,s.b)),y=Y(s.price),base=H-B;
    return `<rect class="epi-bar" x="${(x1+1).toFixed(2)}" y="${y.toFixed(2)}" width="${Math.max(1.5,x2-x1-2).toFixed(2)}" height="${Math.max(0,base-y).toFixed(2)}" rx="1.5"/>`;
  }).join('');
  const segments=visible.map(s=>{const x1=X(Math.max(from,s.a)),x2=X(Math.min(to,s.b)),y=Y(s.price);
    return `<path class="epi-plot-line" d="M${x1.toFixed(2)} ${y.toFixed(2)} H${x2.toFixed(2)}"/>`;
  }).join('');
  const connectors=visible.slice(1).map((s,i)=>{const prev=visible[i];if(Math.abs(prev.b-s.a)>1000||s.a<from||s.a>to)return '';
    return `<path class="epi-plot-line" d="M${X(s.a).toFixed(2)} ${Y(prev.price).toFixed(2)} V${Y(s.price).toFixed(2)}"/>`;
  }).join('');
  const selectedKey=(phase?.favorable_from||'')+'|'+(phase?.favorable_until||'');
  const bands=config.show_chart_highlight!==false?allPhases.map(p=>{
    const a=Date.parse(p.favorable_from),b=Date.parse(p.favorable_until);
    if(!Number.isFinite(a)||!Number.isFinite(b)||b<=from||a>=to)return '';
    const left=X(Math.max(a,from)),right=X(Math.min(b,to));
    const selected=p.favorable_from+'|'+p.favorable_until===selectedKey;
    if(selected&&config.show_chart_selected_phase===false)return '';
    if(!selected&&config.show_chart_other_phases===false)return '';
    return `<rect x="${left.toFixed(2)}" y="${T}" width="${Math.max(0,right-left).toFixed(2)}" height="${H-B-T}" rx="3" class="${selected?'epi-band-selected':'epi-band-other'}"/>`;
  }).join(''):'';
  const now=Date.now(),nowLine=config.show_chart_now!==false&&now>=from&&now<=to?`<line x1="${X(now)}" y1="${T}" x2="${X(now)}" y2="${H-B}" class="epi-now-line"/>`:'';
  const cross=config.show_chart_crosshair!==false?`<line class="epi-crosshair" x1="${L}" x2="${L}" y1="${T}" y2="${H-B}" visibility="hidden"/><circle class="epi-cursor-dot" cx="${L}" cy="${T}" r="4.5" visibility="hidden"/>`:'';
  return `<div class="epi-chart-wrap epi-chart-${style}"><svg width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" data-w="${W}" data-h="${H}" data-left="${L}" data-right="${R}" data-top="${T}" data-bottom="${B}" role="img" aria-label="${esc(tr(hass,'forecast'))}">
    ${tickY}${bands}${style==='bars'?bars:style==='area'?areas:''}${style==='bars'?'':segments+connectors}${nowLine}${tickX}${cross}
  </svg>${config.show_chart_tooltip!==false?'<div class="epi-tooltip" hidden></div>':''}</div>`;
}
const STYLE=`
:host{display:block;min-width:0;color:var(--primary-text-color,#1c2939);font-family:var(--primary-font-family,Inter,system-ui,sans-serif)}
ha-card{--epi-bg:var(--ha-card-background,var(--card-background-color,#fff));--epi-fg:var(--primary-text-color,#202b37);--epi-muted:var(--secondary-text-color,#68798b);--epi-line:var(--divider-color,rgba(115,135,155,.2));--epi-soft:color-mix(in srgb,var(--epi-accent) 7%,var(--epi-bg));display:block;container-type:inline-size;box-sizing:border-box;overflow:hidden;position:relative;padding:16px;border-radius:20px;color:var(--epi-fg);background:var(--epi-bg);border:1px solid var(--epi-line);box-shadow:0 10px 30px rgba(13,34,59,.045)}
.epi-layout{display:grid;gap:12px;position:relative;z-index:1;min-width:0}.epi-heading{display:flex;align-items:center;justify-content:space-between;min-width:0;gap:8px}.epi-heading h2{font-size:15px;font-weight:750;letter-spacing:-.025em;margin:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.epi-heading-mark{display:flex;align-items:center;gap:8px;min-width:0}.epi-logo-dot{width:24px;height:24px;flex:0 0 24px;border-radius:9px;background:var(--epi-soft);color:var(--epi-accent);display:grid;place-items:center;font-size:14px;font-weight:800}.epi-heading-meta{font-size:10px;color:var(--epi-muted);font-weight:650;letter-spacing:.075em;text-transform:uppercase;white-space:nowrap}
.epi-stage,.epi-overview,.epi-hero,.epi-phase,.epi-metrics,.epi-chart-section,.epi-controls{min-width:0}.epi-stage{display:grid;gap:11px;align-items:stretch}.epi-overview{display:grid;gap:10px;align-content:start;min-width:0}.epi-hero{display:flex;align-items:flex-start;justify-content:flex-start;gap:7px 12px;padding:15px;border-radius:15px;background:var(--epi-soft);position:relative;min-width:0;flex-direction:column}.epi-eyebrow{display:block;color:var(--epi-muted);font-weight:650;font-size:11px;line-height:1.35;white-space:nowrap}.epi-price{display:flex;align-items:baseline;gap:6px;white-space:nowrap;min-width:0;font-variant-numeric:tabular-nums}.epi-price b{font-size:clamp(21px,3.3cqw,35px);line-height:1.08;letter-spacing:-.052em;font-weight:780}.epi-price small{font-size:11px;letter-spacing:-.01em;font-weight:660;color:var(--epi-muted)}.epi-hero-trend{width:100%;min-height:30px;margin-block:auto;display:flex;align-items:center;padding:8px 0}.epi-hero-trend svg{display:block;width:100%;height:36px;overflow:visible;opacity:.9}.epi-trend-caption{font-size:10px;color:var(--epi-muted);white-space:nowrap;font-weight:650;max-width:100%;overflow:hidden;text-overflow:ellipsis}.epi-hero-trend{flex-direction:column;align-items:stretch;gap:5px}.epi-price-null{font-size:25px;font-weight:700}.epi-status{display:inline-flex;gap:6px;align-items:center;font-size:10.5px;font-weight:700;border-radius:99px;padding:5px 9px;white-space:nowrap;color:var(--epi-muted);background:color-mix(in srgb,var(--epi-fg) 5%,var(--epi-bg));max-width:100%;box-sizing:border-box}.epi-status.good{color:#087f60;background:color-mix(in srgb,#10b981 13%,var(--epi-bg))}.epi-status i{display:inline-block;width:6px;height:6px;flex:0 0 6px;border-radius:50%;background:currentColor}
.epi-phase{display:grid;gap:9px;align-content:start;background:color-mix(in srgb,var(--epi-fg) 2.1%,var(--epi-bg));border:1px solid var(--epi-line);border-radius:15px;padding:12px 14px}.epi-phase-head{display:flex;justify-content:space-between;align-items:center;gap:7px;min-width:0}.epi-phase-head h3{font-size:12px;font-weight:770;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;margin:0}.epi-phase-title-short{display:none}.epi-nav{display:flex;align-items:center;gap:4px;flex:0 0 auto;white-space:nowrap}.epi-nav small{font-size:10px;color:var(--epi-muted);font-weight:650;font-variant-numeric:tabular-nums}.epi-nav button,.epi-zoom button,.epi-range button{display:inline-flex;align-items:center;justify-content:center;border:1px solid var(--epi-line);background:var(--epi-bg);color:var(--epi-fg);font:inherit;min-width:25px;height:25px;border-radius:8px;cursor:pointer;transition:background .15s,box-shadow .15s}.epi-nav button{font-size:18px;line-height:1}.epi-nav button:disabled{opacity:.35;cursor:default}.epi-nav button:focus-visible,.epi-zoom button:focus-visible,.epi-range button:focus-visible{outline:2px solid var(--epi-accent);outline-offset:2px}.epi-phase-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:9px 12px;min-width:0}.epi-phase-field{min-width:0}.epi-phase-field small{display:block;font-size:10px;color:var(--epi-muted);font-weight:580;white-space:nowrap;margin-bottom:3px;overflow:hidden;text-overflow:ellipsis}.epi-phase-field strong{display:block;font-size:clamp(11px,1.4cqw,13px);font-weight:740;letter-spacing:-.025em;white-space:nowrap;font-variant-numeric:tabular-nums}.epi-phase-empty{font-size:11px;color:var(--epi-muted);line-height:1.5}.epi-countdown{display:inline-flex;align-items:center;gap:6px 8px;flex-wrap:wrap;font-size:10.5px;padding:7px 9px;border-radius:9px;background:color-mix(in srgb,var(--epi-accent) 7%,var(--epi-bg));width:fit-content;max-width:100%;box-sizing:border-box}.epi-countdown span{color:var(--epi-muted);white-space:nowrap}.epi-countdown strong{font-weight:730;white-space:nowrap;font-variant-numeric:tabular-nums}
.epi-metrics{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px}.epi-stat{padding:10px 11px;border-radius:12px;border:1px solid var(--epi-line);min-width:0;overflow:hidden}.epi-stat small{display:block;font-size:10px;color:var(--epi-muted);font-weight:650;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.epi-stat strong{display:block;font-size:clamp(11px,1.35cqw,14px);font-weight:750;letter-spacing:-.035em;line-height:1.5;white-space:nowrap;font-variant-numeric:tabular-nums}.epi-stat em{display:block;font-style:normal;font-size:9px;color:var(--epi-muted);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.epi-chart-section{position:relative;display:flex;flex-direction:column;min-width:0;border:1px solid var(--epi-line);border-radius:15px;background:var(--epi-bg);padding:10px 12px 8px}.epi-chart-head{display:flex;justify-content:space-between;align-items:center;gap:6px;min-width:0;min-height:27px;margin-bottom:4px;flex-wrap:wrap}.epi-chart-title{display:flex;align-items:center;gap:8px;min-width:0}.epi-chart-title h3{font-size:12px;font-weight:770;white-space:nowrap;margin:0}.epi-chart-unit{font-size:10px;font-weight:600;color:var(--epi-muted);white-space:nowrap}.epi-chart-actions{display:flex;gap:6px;align-items:center;flex-wrap:wrap}.epi-range,.epi-zoom{display:inline-flex;align-items:center;gap:3px;white-space:nowrap}.epi-range{padding:2px;background:color-mix(in srgb,var(--epi-fg) 5%,var(--epi-bg));border-radius:8px}.epi-range button{border:0;background:transparent;font-size:10px;font-weight:680;min-width:27px;height:24px;padding:0 7px;color:var(--epi-muted)}.epi-range button.active{color:var(--epi-fg);background:var(--epi-bg);box-shadow:0 1px 4px rgba(0,0,0,.1)}.epi-zoom button{font-size:13px;min-width:24px;height:24px;border-radius:7px}.epi-zoom button[data-zoom=reset]{font-size:12px}.epi-chart-root{position:relative;width:100%;min-width:0;overflow:hidden;touch-action:none;user-select:none;cursor:crosshair;overscroll-behavior-x:contain}.epi-chart-root:active{cursor:grabbing;touch-action:none}.epi-chart-wrap{position:relative;width:100%}.epi-chart-wrap svg{display:block;width:100%;height:auto;max-width:100%;overflow:hidden}.epi-chart-wrap svg text{font-family:system-ui,sans-serif}.epi-axis-text{font-size:11px;fill:var(--epi-muted);font-weight:600;paint-order:stroke;stroke:var(--epi-bg);stroke-width:2px;stroke-linejoin:round}.epi-grid-line{stroke:var(--epi-muted);opacity:.14;stroke-width:1}.epi-tick{stroke:var(--epi-muted);opacity:.36}.epi-area{fill:var(--epi-accent);opacity:.09}.epi-plot-line{fill:none;stroke:var(--epi-accent);stroke-width:2.6;stroke-linecap:round;stroke-linejoin:round}.epi-chart-bars .epi-bar{fill:var(--epi-accent);opacity:.55}.epi-chart-bars .epi-plot-line,.epi-chart-bars .epi-area{display:none}.epi-chart-line .epi-area{display:none}.epi-band-selected{fill:var(--epi-accent);opacity:.23}.epi-band-other{fill:var(--epi-accent);opacity:.075}.epi-now-line{stroke:var(--epi-fg);opacity:.7;stroke-width:1.1;stroke-dasharray:3 4}.epi-crosshair{stroke:var(--epi-fg);stroke-width:1.2;stroke-dasharray:3 4}.epi-cursor-dot{fill:var(--epi-accent);stroke:var(--epi-bg);stroke-width:2}.epi-tooltip{position:absolute;z-index:9;left:5px;top:8px;pointer-events:none;max-width:calc(100% - 8px);box-sizing:border-box;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;background:var(--epi-fg);color:var(--epi-bg);border-radius:8px;padding:8px 10px;font-size:11px;font-weight:650;box-shadow:0 6px 20px rgba(0,0,0,.18);font-variant-numeric:tabular-nums}.epi-legend{display:flex;gap:13px;flex-wrap:wrap;color:var(--epi-muted);font-size:10px;margin-top:5px}.epi-legend span{display:flex;align-items:center;gap:5px;white-space:nowrap}.epi-legend i{display:inline-block;width:9px;height:9px;background:var(--epi-accent);border-radius:3px}.epi-legend .selected{background:var(--epi-accent)}.epi-chart-hint{font-size:10px;color:var(--epi-muted);margin-top:5px}.epi-empty{font-size:12px;color:var(--epi-muted);padding:20px 5px;text-align:center}
.epi-controls{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,160px),1fr));gap:9px;background:color-mix(in srgb,var(--epi-fg) 3%,var(--epi-bg));border-radius:13px;padding:10px}.epi-controls label{display:grid;grid-template-columns:minmax(0,1fr);gap:4px;min-width:0;font-size:11px;font-weight:650}.epi-controls select,.epi-controls input{width:100%;max-width:100%;min-width:0;text-overflow:ellipsis;overflow:hidden;white-space:nowrap;box-sizing:border-box;background:var(--epi-bg);border:1px solid var(--epi-line);border-radius:8px;min-height:32px;color:var(--epi-fg);font:inherit;padding:6px}.epi-foot{color:var(--epi-muted);font-size:10px;padding-top:7px;border-top:1px solid var(--epi-line)}
/* Aurora: split trading cockpit */
.design-aurora{background:linear-gradient(125deg,color-mix(in srgb,var(--epi-accent) 6%,var(--epi-bg)),var(--epi-bg) 48%)}
.design-aurora .epi-stage:has(.epi-chart-section){grid-template-columns:minmax(0,5fr) minmax(0,7fr)}
.design-aurora .epi-overview{grid-column:1;grid-row:1}.design-aurora .epi-chart-section{grid-column:2;grid-row:1;align-self:stretch;justify-content:center;box-shadow:0 2px 12px rgba(15,23,42,.02)}
.design-aurora .epi-hero{background:linear-gradient(105deg,color-mix(in srgb,var(--epi-accent) 16%,var(--epi-bg)),color-mix(in srgb,var(--epi-accent) 3%,var(--epi-bg)))}
/* Minimal: editorial wide horizontal summary */
.design-minimal{border-radius:9px;box-shadow:none;padding:15px 16px}.design-minimal .epi-logo-dot{background:transparent;border:1px solid var(--epi-line)}
.design-minimal .epi-stage{grid-template-columns:minmax(0,1fr)}.design-minimal .epi-overview{display:flex;align-items:stretch;gap:0;border-block:1px solid var(--epi-line)}
.design-minimal .epi-hero,.design-minimal .epi-phase,.design-minimal .epi-metrics{background:transparent;border:0;border-radius:0;padding:12px 14px}
.design-minimal .epi-hero{flex:1 1 24%;padding-left:0}.design-minimal .epi-phase{flex:2 1 42%;border-left:1px solid var(--epi-line)}.design-minimal .epi-metrics{flex:1.4 1 34%;border-left:1px solid var(--epi-line);align-self:stretch}.design-minimal .epi-stat{border:0;padding:2px 4px}.design-minimal .epi-chart-section{border:0;border-radius:0;padding:5px 0 0}
/* Glass: visual-first luminous cards */
.design-glass{border-radius:25px;background:radial-gradient(ellipse 80% 90% at 0% 0%,color-mix(in srgb,var(--epi-accent) 20%,transparent),transparent),radial-gradient(ellipse 65% 100% at 100% 85%,color-mix(in srgb,#5b80cf 12%,transparent),transparent),var(--epi-bg);box-shadow:0 13px 37px rgba(12,39,66,.09)}
.design-glass .epi-stage:has(.epi-chart-section){grid-template-columns:minmax(0,7fr) minmax(0,5fr)}
.design-glass .epi-chart-section{grid-column:1;grid-row:1;background:color-mix(in srgb,var(--epi-bg) 82%,transparent);backdrop-filter:blur(9px);box-shadow:0 6px 20px rgba(15,30,65,.06);padding:15px}.design-glass .epi-overview{grid-column:2;grid-row:1;grid-template-columns:1fr 1fr;align-content:start}.design-glass .epi-hero{grid-column:1/-1;background:color-mix(in srgb,var(--epi-bg) 82%,transparent);backdrop-filter:blur(12px);border:1px solid color-mix(in srgb,var(--epi-accent) 24%,var(--epi-line))}
.epi-no-accent-border.design-glass .epi-hero{border-color:var(--epi-line)}.design-glass .epi-phase{grid-column:1/-1;background:color-mix(in srgb,var(--epi-bg) 79%,transparent);backdrop-filter:blur(12px);box-shadow:0 5px 15px rgba(15,30,65,.04)}.design-glass .epi-metrics{grid-column:1/-1}.design-glass .epi-stat{background:color-mix(in srgb,var(--epi-bg) 81%,transparent);backdrop-filter:blur(12px)}
/* Timeline: full-width chronological view followed by a horizontal information rail */
.design-timeline{border-radius:15px;border-top:3px solid var(--epi-accent)}
.epi-no-accent-border.design-timeline{border-top:1px solid var(--epi-line)}
.design-timeline .epi-stage{display:flex;flex-direction:column}.design-timeline .epi-chart-section{order:0;border-radius:11px;border:0;background:color-mix(in srgb,var(--epi-fg) 2%,var(--epi-bg));padding:13px 13px 6px}.design-timeline .epi-overview{order:1;grid-template-columns:minmax(0,2fr) minmax(0,4fr) minmax(0,3fr);gap:0;border-top:1px solid var(--epi-line);padding-top:11px}.design-timeline .epi-hero{grid-column:1;padding:9px 14px 8px 0;background:transparent}.design-timeline .epi-phase{grid-column:2;padding:8px 13px;background:transparent;border:0;border-left:2px solid var(--epi-accent);border-radius:0}.design-timeline .epi-metrics{grid-column:3;border-left:1px solid var(--epi-line);padding-left:11px;align-self:stretch}.design-timeline .epi-stat{border:0;padding:3px 6px;border-radius:0}
.epi-density-comfortable .epi-hero{padding:19px}.epi-density-comfortable .epi-phase{padding:17px}.epi-density-comfortable .epi-stat{padding:13px}
@container (max-width:790px){.design-minimal .epi-overview{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:0}.design-minimal .epi-hero{grid-column:1;border-bottom:1px solid var(--epi-line)}.design-minimal .epi-phase{grid-column:2;border-bottom:1px solid var(--epi-line)}.design-minimal .epi-metrics{grid-column:1/-1;border-left:0;padding-left:0}.design-aurora .epi-stage:has(.epi-chart-section),.design-glass .epi-stage:has(.epi-chart-section){grid-template-columns:1fr}.design-aurora .epi-overview,.design-glass .epi-overview{grid-column:1;grid-row:auto}.design-aurora .epi-chart-section,.design-glass .epi-chart-section{grid-column:1;grid-row:auto}.design-glass .epi-chart-section{grid-row:1}.design-glass .epi-overview{grid-row:2;grid-template-columns:repeat(2,minmax(0,1fr))}.design-glass .epi-hero{grid-column:1}.design-glass .epi-phase{grid-column:2}.design-glass .epi-metrics{grid-column:1/-1}.design-aurora .epi-overview{grid-template-columns:repeat(2,minmax(0,1fr))}.design-aurora .epi-hero{grid-column:1}.design-aurora .epi-phase{grid-column:2}.design-aurora .epi-metrics{grid-column:1/-1}.design-timeline .epi-overview{grid-template-columns:repeat(2,minmax(0,1fr))}.design-timeline .epi-hero{grid-column:1}.design-timeline .epi-phase{grid-column:2}.design-timeline .epi-metrics{grid-column:1/-1;border:0;border-top:1px solid var(--epi-line);padding:9px 0 0}}
@container (max-width:540px){.epi-phase-title-full{display:none}.epi-phase-title-short{display:inline}.epi-phase-head{flex-wrap:nowrap}.epi-nav{gap:2px}.epi-nav button{min-width:21px;height:21px}.epi-nav small{font-size:9.5px}ha-card{padding:11px;border-radius:16px}.epi-layout{gap:9px}.epi-stage,.epi-overview{gap:8px}.epi-logo-dot{width:22px;height:22px;flex-basis:22px}.epi-heading h2{font-size:14px}.epi-heading-meta{display:none}.epi-hero{padding:11px}.epi-price{gap:3px}.epi-price b{font-size:clamp(18px,5cqw,23px)}.epi-price small{font-size:10px}.epi-status{font-size:9.5px;padding:4px 6px}.epi-phase{padding:10px}.epi-phase-head h3{font-size:11px}.epi-phase-grid{grid-template-columns:minmax(0,1fr);gap:7px}.epi-phase-field small{font-size:9.5px;margin-bottom:1px}.epi-phase-field strong{font-size:11px}.epi-countdown{padding:6px;font-size:9.5px;gap:4px}.epi-stat{padding:8px 9px}.epi-stat strong{font-size:12px}.epi-chart-section{padding:8px 9px 6px}.epi-chart-actions{gap:4px}.epi-range button{padding:0 6px}.epi-zoom button{min-width:22px;height:22px}.epi-chart-title h3{font-size:11px}.design-minimal{padding:11px}.design-minimal .epi-hero,.design-minimal .epi-phase{padding:10px}.design-minimal .epi-hero{padding-left:0}.design-timeline .epi-hero{padding:9px 6px 9px 0}.design-timeline .epi-phase{padding:8px}.design-glass .epi-chart-section{padding:10px}}
@container (max-width:365px){.epi-range button{padding:0 4px;min-width:20px}.epi-chart-actions{flex-wrap:wrap}.epi-phase-grid{gap:5px}.epi-chart-head{align-items:flex-start}.epi-chart-actions{width:auto;justify-content:flex-end}.epi-chart-title{width:100%}.epi-chart-section{padding:9px 8px}.epi-chart-wrap{margin-top:1px}.design-aurora .epi-overview,.design-glass .epi-overview,.design-minimal .epi-overview,.design-timeline .epi-overview{grid-template-columns:minmax(0,1fr) minmax(0,1.12fr)}.epi-phase{padding:8px}.epi-phase-head{align-items:flex-start;flex-wrap:wrap}.epi-nav{margin-left:auto}.epi-price b{font-size:18px}.epi-price small{font-size:9.5px}.epi-hero{padding:9px}.epi-eyebrow{font-size:10px}.epi-stat{padding:8px 6px}.epi-stat strong{font-size:11px}}
@container (max-width:310px){.epi-phase-title-full{display:inline}.epi-phase-title-short{display:none}.design-aurora .epi-overview,.design-glass .epi-overview,.design-minimal .epi-overview,.design-timeline .epi-overview{grid-template-columns:1fr}.design-aurora .epi-hero,.design-aurora .epi-phase,.design-glass .epi-hero,.design-glass .epi-phase,.design-minimal .epi-hero,.design-minimal .epi-phase,.design-timeline .epi-hero,.design-timeline .epi-phase{grid-column:1}.epi-phase-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.epi-chart-head{gap:3px}}
/* Timeline: preserve the editor cockpit arrangement on the dashboard, regardless
   of ordinary card width differences. Only genuinely tiny cards stack columns. */
@container (min-width:311px){
.design-timeline .epi-overview:has(> .epi-hero):has(> .epi-phase):has(> .epi-metrics){display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.2fr);grid-template-rows:auto minmax(0,1fr);gap:6px 8px;align-content:stretch}
.design-timeline .epi-overview:has(> .epi-hero):has(> .epi-phase):has(> .epi-metrics) > .epi-hero{grid-column:1;grid-row:1;align-self:start;min-height:0;padding:9px}
.design-timeline .epi-overview:has(> .epi-hero):has(> .epi-phase):has(> .epi-metrics) > .epi-phase{grid-column:2;grid-row:1/span 2;align-self:stretch}
.design-timeline .epi-overview:has(> .epi-hero):has(> .epi-phase):has(> .epi-metrics) > .epi-metrics{grid-column:1;grid-row:2;display:grid;grid-template-columns:minmax(0,1fr);gap:5px;align-self:stretch;border:0;padding:0}
.design-timeline .epi-overview:has(> .epi-hero):has(> .epi-phase):has(> .epi-metrics) > .epi-metrics .epi-stat{padding:5px 7px}
.design-timeline .epi-phase-grid{grid-template-columns:minmax(0,1fr)}
.design-timeline .epi-chart-head{flex-direction:column;align-items:flex-start;flex-wrap:nowrap;gap:6px}
.design-timeline .epi-chart-actions{max-width:100%;justify-content:flex-start;flex-wrap:wrap}
}
/* Visual editor: designed panels, design previews, grouped switches. */
.epi-editor{--epi-bg:var(--ha-card-background,var(--card-background-color,#fff));--epi-fg:var(--primary-text-color,#202b37);--epi-muted:var(--secondary-text-color,#68798b);--epi-line:var(--divider-color,rgba(100,123,150,.2));--epi-accent:var(--primary-color,#0ea5a4);display:grid;gap:13px;color:var(--epi-fg);font-family:var(--primary-font-family,system-ui,sans-serif);font-size:12px;padding:4px 0 14px;min-width:0}.epi-editor *{box-sizing:border-box}.epi-editor [hidden]{display:none!important}.epi-editor-head{display:flex;align-items:center;gap:11px;padding:7px 3px 4px}.epi-editor-symbol{display:grid;place-items:center;width:38px;height:38px;border-radius:13px;color:var(--epi-accent);font-size:22px;background:color-mix(in srgb,var(--epi-accent) 10%,var(--epi-bg))}.epi-editor-head h3{font-size:16px;margin:0;font-weight:780;letter-spacing:-.025em}.epi-editor-head p{font-size:11px;color:var(--epi-muted);margin:3px 0 0}.epi-editor-panel{display:grid;gap:12px;padding:14px;border:1px solid var(--epi-line);border-radius:16px;background:var(--epi-bg)}.epi-editor-panel h4{margin:0;font-weight:760;font-size:13px}.epi-editor-panel p{margin:-6px 0 0;color:var(--epi-muted);line-height:1.4;font-size:11px}.epi-editor-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,185px),1fr));gap:11px}.epi-editor label.epi-field{display:grid;gap:6px;min-width:0;font-size:11px;color:var(--epi-muted);font-weight:680}.epi-editor .epi-field ha-entity-picker{width:100%;display:block;min-width:0}.epi-editor input[type=text],.epi-editor input[type=color],.epi-editor select{font:inherit;min-width:0;width:100%;min-height:37px;background:var(--epi-bg);color:var(--epi-fg);border:1px solid var(--epi-line);border-radius:10px;padding:7px}.epi-editor input[type=color]{padding:3px;cursor:pointer}.epi-design-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:9px}.epi-design-choice{border:1.5px solid var(--epi-line);border-radius:12px;background:var(--epi-bg);color:var(--epi-fg);padding:9px;min-width:0;cursor:pointer;text-align:left;display:grid;gap:8px;font:inherit}.epi-design-choice[aria-pressed=true]{border-color:var(--epi-accent);background:color-mix(in srgb,var(--epi-accent) 5%,var(--epi-bg));box-shadow:inset 0 0 0 1px var(--epi-accent)}.epi-design-choice:hover{border-color:var(--epi-accent)}.epi-design-choice>span{display:flex;gap:5px;align-items:center;font-size:11px;font-weight:720}.epi-design-choice>span i{display:inline-block;border-radius:50%;width:6px;height:6px;background:var(--epi-accent)}.epi-mini{height:51px;border-radius:7px;background:color-mix(in srgb,var(--epi-fg) 4%,var(--epi-bg));display:grid;gap:3px;padding:6px;overflow:hidden}.epi-mini b,.epi-mini em,.epi-mini i{display:block;border-radius:3px;background:color-mix(in srgb,var(--epi-accent) 35%,var(--epi-bg));min-width:0;min-height:0}.epi-mini em{background:color-mix(in srgb,var(--epi-fg) 12%,var(--epi-bg))}.epi-mini.aurora{grid-template-columns:42% 1fr;grid-template-rows:1fr 1fr 1fr}.epi-mini.aurora b{grid-row:1/3}.epi-mini.aurora i{grid-column:2;grid-row:1/-1}.epi-mini.minimal{grid-template-columns:repeat(3,1fr);grid-template-rows:14px 1fr}.epi-mini.minimal i{grid-column:1/-1;grid-row:2}.epi-mini.glass{grid-template-columns:1.5fr 1fr;grid-template-rows:1fr 1fr;background:linear-gradient(120deg,color-mix(in srgb,var(--epi-accent) 15%,var(--epi-bg)),color-mix(in srgb,#587cc6 8%,var(--epi-bg)))}.epi-mini.glass i{grid-row:1/3}.epi-mini.timeline{grid-template-columns:repeat(3,1fr);grid-template-rows:1.7fr 1fr}.epi-mini.timeline i{grid-column:1/-1;grid-row:1}.epi-editor details.epi-group{border:1px solid var(--epi-line);background:var(--epi-bg);border-radius:13px;overflow:hidden}.epi-editor details.epi-group summary{list-style:none;display:flex;align-items:center;justify-content:space-between;cursor:pointer;padding:13px 14px;font-size:12px;font-weight:740;gap:8px}.epi-editor details.epi-group summary::-webkit-details-marker{display:none}.epi-editor details.epi-group summary:after{content:'⌄';font-size:17px;color:var(--epi-muted);line-height:1}.epi-editor details.epi-group[open] summary:after{transform:rotate(180deg)}.epi-editor details.epi-group[open] summary{border-bottom:1px solid var(--epi-line)}.epi-editor .epi-group-content{padding:11px 13px 14px;display:grid;gap:11px}.epi-editor .epi-toggle-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,178px),1fr));gap:8px}.epi-editor label.epi-switch{display:flex;align-items:center;justify-content:space-between;gap:8px;cursor:pointer;min-height:36px;background:color-mix(in srgb,var(--epi-fg) 2%,var(--epi-bg));border:1px solid var(--epi-line);border-radius:9px;padding:7px 9px;font-size:11px;font-weight:600}.epi-editor .epi-switch input{appearance:none;flex:0 0 30px;width:30px;height:17px;background:color-mix(in srgb,var(--epi-muted) 25%,var(--epi-bg));border-radius:99px;position:relative;cursor:pointer;margin:0;transition:background .15s}.epi-editor .epi-switch input:before{content:'';position:absolute;left:2px;top:2px;width:13px;height:13px;border-radius:50%;background:var(--epi-bg);box-shadow:0 1px 3px #0003;transition:transform .15s}.epi-editor .epi-switch input:checked{background:var(--epi-accent)}.epi-editor .epi-switch input:checked:before{transform:translateX(13px)}.epi-editor .epi-switch input:focus-visible{outline:2px solid var(--epi-accent);outline-offset:2px}.epi-editor .epi-advanced{display:grid;gap:9px}.epi-editor .epi-info-pill{display:inline-block;color:var(--epi-muted);font-size:10px;font-weight:500;padding-left:5px}.epi-editor .epi-color-field{display:flex;gap:8px;align-items:center}.epi-editor .epi-color-field input{max-width:55px;flex:0 0 55px}.epi-editor .epi-color-field span{font-family:monospace;color:var(--epi-muted)}
@media(max-width:380px){.epi-design-grid{grid-template-columns:1fr 1fr}.epi-editor-panel{padding:11px}.epi-editor .epi-toggle-grid{grid-template-columns:1fr}}
`;
// Update existing elements instead of reconstructing the entire card on every
// Home Assistant state event. Keeping ha-card mounted prevents Lovelace layout
// churn, scroll anchoring issues, lost focus and repeated chart listeners.
function epiReconcile(current, desired) {
  if(current.nodeType!==desired.nodeType || current.nodeName!==desired.nodeName || current.namespaceURI!==desired.namespaceURI){
    current.replaceWith(desired.cloneNode(true));return;
  }
  if(current.nodeType===Node.TEXT_NODE){if(current.nodeValue!==desired.nodeValue)current.nodeValue=desired.nodeValue;return;}
  if(current.nodeType!==Node.ELEMENT_NODE)return;
  for(const attr of [...current.attributes])if(!desired.hasAttribute(attr.name))current.removeAttribute(attr.name);
  for(const attr of [...desired.attributes])if(current.getAttribute(attr.name)!==attr.value && !(attr.name==='value' && current.getRootNode().activeElement===current))current.setAttribute(attr.name,attr.value);
  if(current.matches('.epi-chart-root'))return; // Redraw SVG in place, not its event container.
  // Preserve an actively edited number or dropdown while HA updates other data.
  if((current.localName==='input'||current.localName==='select') && current!==current.getRootNode().activeElement){
    if(current.value!==desired.value)current.value=desired.value;
  }
  const next=[...desired.childNodes];
  for(let i=0;i<next.length;i++){
    if(i>=current.childNodes.length)current.appendChild(next[i].cloneNode(true));
    else epiReconcile(current.childNodes[i],next[i]);
  }
  while(current.childNodes.length>next.length)current.lastChild.remove();
}
class EnergyPriceInsightsCard extends HTMLElement {
  constructor(){super();this.attachShadow({mode:'open'});this._config={...DEFAULTS};this._hass=null;this._lastSig='';this._selectedPhaseKey=null;this._chartView=null;this._pointerPositions=new Map();this._dragStart=null;this._resizeObserver=null;this._countdownTimer=null;this._observedChartRoot=null;}
  static getConfigElement(){return document.createElement('energy-price-insights-card-editor');}
  static getStubConfig(hass){return {...DEFAULTS,entity:discover(hass)};}
  getCardSize(){return this._config.show_chart?5:3;}
  getGridOptions(){return {columns:12,rows:this._config.show_chart?5:3,min_columns:4,min_rows:2};}
  setConfig(config){if(!config || config.type && config.type!==`custom:${CARD_TYPE}`)throw Error('Invalid card configuration');this._config={...DEFAULTS,...config};this._lastSig='';this._chartView=null;this.render();}
  set hass(hass){this._hass=hass;const m=loadModel(hass,this._config),states=[m.current,m.phase,m.today,m.tomorrow,m.favorable,m.availability,m.threshold,m.minutes,m.method,m.scope];
    const sig=[lang(hass),...states.map(s=>`${s?.entity_id||''}:${s?.last_updated||''}:${s?.state||''}`)].join('|');if(sig!==this._lastSig){this._lastSig=sig;this.render();}}
  connectedCallback(){this.render();if(!this._countdownTimer)this._countdownTimer=setInterval(()=>this._updateCountdown(),15000);}
  disconnectedCallback(){if(this._countdownTimer){clearInterval(this._countdownTimer);this._countdownTimer=null;}this._resizeObserver?.disconnect();this._resizeObserver=null;this._observedChartRoot=null;}
  _phaseList(phase){const blocks=Array.isArray(phase.all_favorable_blocks)?phase.all_favorable_blocks.filter(p=>p&&p.favorable_from&&p.favorable_until):[];
    if(blocks.length)return blocks;
    return phase.favorable_from&&phase.favorable_until?[{favorable_from:phase.favorable_from,favorable_until:phase.favorable_until,avg_price:phase.avg_favorable_phase_price,min_price:phase.min_favorable_phase_price,max_price:phase.max_favorable_phase_price}]:[];
  }
  _chosenPhase(phase,blocks){const primary=phase.favorable_from+'|'+phase.favorable_until;
    const selectKey=this._selectedPhaseKey&&blocks.some(p=>p.favorable_from+'|'+p.favorable_until===this._selectedPhaseKey)?this._selectedPhaseKey:primary;
    let index=blocks.findIndex(p=>p.favorable_from+'|'+p.favorable_until===selectKey);
    if(index<0)index=0;
    return {selected:blocks[index]||null,index};
  }
  _extents(raw){if(!raw.length)return null;return {min:raw[0].a,max:Math.max(...raw.map(r=>r.b))};}
  _viewport(raw){const full=this._extents(raw);if(!full)return null;const span=full.max-full.min;
    if(!this._chartView)return {from:full.min,to:full.max};
    let width=Math.min(span,Math.max(600000,this._chartView.to-this._chartView.from));
    let from=Math.max(full.min,Math.min(full.max-width,this._chartView.from));
    this._chartView={from,to:from+width};return this._chartView;
  }
  _zoom(factor,centerFraction=.5){const range=this._viewport(this._raw||[]),full=this._extents(this._raw||[]);if(!range||!full)return;
    const total=full.max-full.min,span=Math.max(600000,Math.min(total,(range.to-range.from)*factor));
    const center=range.from+(range.to-range.from)*centerFraction;
    let from=Math.max(full.min,Math.min(full.max-span,center-span*centerFraction));
    this._chartView={from,to:from+span};this._refreshPlot();
  }
  _pan(delta){const range=this._viewport(this._raw||[]),full=this._extents(this._raw||[]);if(!range||!full)return;
    const width=range.to-range.from;let from=Math.min(full.max-width,Math.max(full.min,range.from+delta));
    this._chartView={from,to:from+width};this._refreshPlot();
  }
  _refreshPlot(){const root=this.shadowRoot?.querySelector('.epi-chart-root');if(!root||!this._raw)return;
    const oldScroll=root.scrollLeft;root.innerHTML=chartSvg(this._raw,this._displayPhase,this._allPhases,this._config,this._hass,this._viewport(this._raw),Math.max(260,root.clientWidth||620));root.scrollLeft=oldScroll;
  }
  _position(event){const svg=this.shadowRoot?.querySelector('.epi-chart-wrap svg');if(!svg)return null;
    const r=svg.getBoundingClientRect(),px=(event.clientX-r.left)/r.width;
    const width=Number(svg.dataset.w)||620,left=Number(svg.dataset.left)||61,right=Number(svg.dataset.right)||11;const frac=Math.max(0,Math.min(1,(px*width-left)/(width-left-right)));
    return {frac,r};
  }
  _hover(event){const pos=this._position(event),wrap=this.shadowRoot.querySelector('.epi-chart-wrap');if(!pos||!wrap)return;
    const view=this._viewport(this._raw),time=view.from+(view.to-view.from)*pos.frac;
    const period=this._raw.find(p=>p.a<=time&&time<p.b);
    const line=wrap.querySelector('.epi-crosshair'),dot=wrap.querySelector('.epi-cursor-dot'),tip=wrap.querySelector('.epi-tooltip');
    if(!period){if(tip)tip.hidden=true;if(line)line.setAttribute('visibility','hidden');if(dot)dot.setAttribute('visibility','hidden');return;}
    const svg=wrap.querySelector('svg'),width=Number(svg?.dataset.w)||620,left=Number(svg?.dataset.left)||61,right=Number(svg?.dataset.right)||11,H=Number(svg?.dataset.h)||210,T=Number(svg?.dataset.top)||16,B=Number(svg?.dataset.bottom)||31;
    const x=left+pos.frac*(width-left-right),prices=this._raw.filter(p=>p.a<view.to&&p.b>view.from).map(p=>p.price);
    const pad=Math.max((Math.max(...prices)-Math.min(...prices))*.13,.002),low=Math.min(...prices)-pad,high=Math.max(...prices)+pad;
    const y=T+(high-period.price)/(high-low||1)*(H-T-B);
    if(line){line.setAttribute('x1',x);line.setAttribute('x2',x);line.setAttribute('visibility','visible');}
    if(dot){dot.setAttribute('cx',x);dot.setAttribute('cy',y);dot.setAttribute('visibility','visible');}
    if(tip){tip.hidden=false;tip.textContent=`${formatTime(time,this._hass,true)} · ${money(period.price,this._currency,this._hass)}`;
    tip.style.left=`${Math.max(4,Math.min(pos.r.width-tip.offsetWidth-4,event.clientX-pos.r.left+13))}px`;}
  }
  _wireChart(){const root=this.shadowRoot.querySelector('.epi-chart-root');if(!root)return;
    if(root._epiWired)return;root._epiWired=true;
    root.addEventListener('wheel',e=>{if(!this._raw?.length||this._config.show_chart_gesture_zoom===false)return;e.preventDefault();const p=this._position(e);this._zoom(Math.exp(Math.max(-90,Math.min(90,e.deltaY))*.012),p?.frac??.5);},{passive:false});
    root.addEventListener('pointerdown',e=>{if(!this._raw?.length||(this._config.show_chart_pan===false&&this._config.show_chart_gesture_zoom===false))return;root.setPointerCapture(e.pointerId);this._pointerPositions.set(e.pointerId,{x:e.clientX,y:e.clientY});this._dragStart={x:e.clientX,view:this._viewport(this._raw)};});
    root.addEventListener('pointermove',e=>{
      if(this._pointerPositions.has(e.pointerId)){
        const prev=new Map(this._pointerPositions);this._pointerPositions.set(e.pointerId,{x:e.clientX,y:e.clientY});
        if(this._config.show_chart_gesture_zoom!==false && this._pointerPositions.size===2 && prev.size===2){
          const a=[...prev.values()],b=[...this._pointerPositions.values()];
          const oldD=Math.abs(a[0].x-a[1].x),newD=Math.abs(b[0].x-b[1].x);
          const rect=root.querySelector('svg')?.getBoundingClientRect()||root.getBoundingClientRect(),fraction=Math.max(0,Math.min(1,((b[0].x+b[1].x)/2-rect.left)/rect.width));
          if(oldD>12&&newD>12)this._zoom(oldD/newD,fraction);
        }else if(this._config.show_chart_pan!==false && this._pointerPositions.size===1 && this._dragStart){
          const rect=root.querySelector('svg')?.getBoundingClientRect()||root.getBoundingClientRect(),width=this._viewport(this._raw).to-this._viewport(this._raw).from;
          const shift=-(e.clientX-this._dragStart.x)/Math.max(1,rect.width)*width;
          // Relative change from the previous sample to avoid cumulative drift.
          const prevX=prev.get(e.pointerId)?.x??e.clientX;
          if(this._viewport(this._raw).to-this._viewport(this._raw).from>=this._extents(this._raw).max-this._extents(this._raw).min-1000){root.scrollLeft-=e.clientX-prevX;}
          else this._pan(-(e.clientX-prevX)/Math.max(1,rect.width)*width);
        }
      }
      this._hover(e);
    });
    for(const name of ['pointerup','pointercancel'])root.addEventListener(name,e=>{this._pointerPositions.delete(e.pointerId);if(!this._pointerPositions.size)this._dragStart=null;});
    root.addEventListener('pointerleave',()=>{if(this._pointerPositions.size)return;const wrap=this.shadowRoot.querySelector('.epi-chart-wrap');if(!wrap)return;const tooltip=wrap.querySelector('.epi-tooltip'),line=wrap.querySelector('.epi-crosshair'),dot=wrap.querySelector('.epi-cursor-dot');if(tooltip)tooltip.hidden=true;if(line)line.setAttribute('visibility','hidden');if(dot)dot.setAttribute('visibility','hidden');});
  }
  _updateCountdown(){
    const node=this.shadowRoot?.querySelector('[data-countdown]');
    const remain=this.shadowRoot?.querySelector('[data-phase-remaining]');
    if(remain&&Number.isFinite(this._countdownEnd)){const minutes=Math.max(0,Math.ceil((this._countdownEnd-Date.now())/60000));const next=`${minutes} ${tr(this._hass,'minutes')}`;if(remain.textContent!==next)remain.textContent=next;}
    if(!node)return;
    const start=this._countdownStart,end=this._countdownEnd,now=Date.now();
    const label=this.shadowRoot.querySelector('[data-countdown-label]');
    if(!Number.isFinite(start)||!Number.isFinite(end)||now>=end){node.textContent='—';return;}
    if(start<=now){if(label)label.textContent=tr(this._hass,'running');node.textContent=tr(this._hass,'activeNow');return;}
    if(label)label.textContent=tr(this._hass,'startsIn');node.textContent=countdownText(start-now,this._hass);
  }
  render(){if(!this.isConnected||!this.shadowRoot)return;
    const h=this._hass,c=this._config,m=loadModel(h,c),accent=/^#[0-9a-fA-F]{6}$/.test(c.accent)?c.accent:'#0ea5a4';
    if(!h||!m.current){this.shadowRoot.innerHTML=`<style>${STYLE}</style><ha-card style="--epi-accent:${accent}"><div class="epi-empty">${esc(tr(h,'configure'))}</div></ha-card>`;return;}
    const curr=m.current,currency=curr.attributes?.currency||'EUR',good=isOn(m.favorable?.state),phase=m.phase?.attributes||{},blocks=this._phaseList(phase);
    this._currency=currency;
    const {selected,index}=this._chosenPhase(phase,blocks),p=selected||null;
    this._displayPhase=p;this._allPhases=blocks;
    const label=(title,val,sub='')=>`<div class="epi-stat"><small>${esc(title)}</small><strong>${esc(val)}</strong>${sub?`<em title="${esc(sub)}">${esc(sub)}</em>`:''}</div>`;
    const selectedStart=p?.favorable_from,selectedEnd=p?.favorable_until;
    const startMillis=Date.parse(selectedStart||''),endMillis=Date.parse(selectedEnd||'');
    const activePeriod=Number.isFinite(startMillis)&&startMillis<=Date.now()&&Date.now()<endMillis;
    const duration=Number.isFinite(startMillis)&&Number.isFinite(endMillis)?Math.round((endMillis-startMillis)/60000):null;
    const remaining=activePeriod?Math.max(0,Math.ceil((endMillis-Date.now())/60000)):null;
    const minDuration=c.show_phase_minimum!==false&&phase.evaluation_mode==='window'?{key:'minimumDuration',value:`${phase.window_minimum_minutes??phase.window_minutes??'—'} ${tr(h,'minutes')}`} : null;
    const field=(key,value)=>`<div class="epi-phase-field"><small>${esc(tr(h,key))}</small><strong title="${esc(value)}"${key==='remaining'?' data-phase-remaining':''}>${esc(value)}</strong></div>`;
    const phaseItems=p?[c.show_phase_start!==false?field('start',formatTime(selectedStart,h,true)):'',
      c.show_phase_end!==false?field('end',formatTime(selectedEnd,h,true)):'',
      c.show_phase_average!==false?field('windowAverage',money(p.avg_price??phase.avg_favorable_phase_price,currency,h)):'',
      c.show_phase_duration!==false?field(activePeriod?'remaining':'periodDuration',`${activePeriod?remaining:duration??'—'} ${tr(h,'minutes')}`):'',
      minDuration?field(minDuration.key,minDuration.value):''].filter(Boolean):[];
    const phaseCards=p?(phaseItems.length?`<div class="epi-phase-grid">${phaseItems.join('')}</div>`:''):`<div class="epi-phase-empty">${esc(tr(h,'noWindow'))}</div>`;
    const nav=c.show_navigation!==false&&blocks.length>1?`<nav class="epi-nav"><button type="button" data-nav="-1" aria-label="${esc(tr(h,'previousPhase'))}" title="${esc(tr(h,'previousPhase'))}">‹</button><small>${index+1} ${esc(tr(h,'of'))} ${blocks.length}</small><button type="button" data-nav="1" aria-label="${esc(tr(h,'nextPhase'))}" title="${esc(tr(h,'nextPhase'))}">›</button></nav>`:'';
    this._countdownStart=startMillis;this._countdownEnd=endMillis;
    const countdown=c.show_countdown&&p?`<div class="epi-countdown"><span data-countdown-label></span><strong data-countdown>—</strong></div>`:'';
    const phaseBlock=c.show_phase?`<section class="epi-phase">${c.show_phase_title!==false||nav?`<div class="epi-phase-head">${c.show_phase_title!==false?`<h3 title="${esc(tr(h,'phase'))}"><span class="epi-phase-title-full">${esc(tr(h,'phase'))}</span><span class="epi-phase-title-short">${esc(tr(h,'phaseCompact'))}</span></h3>`:''}${nav}</div>`:''}${phaseCards}${countdown}</section>`:'';
    const sym={EUR:'€',GBP:'£',SEK:'kr',NOK:'kr',DKK:'kr',PLN:'zł'}[currency.toUpperCase()]||currency;
    const numeric=finite(curr.state),formatted=numeric===null?'—':new Intl.NumberFormat(lang(h),{minimumFractionDigits:2,maximumFractionDigits:4}).format(numeric);
    const status=c.show_status?`<div class="epi-status ${good?'good':''}">${c.show_status_indicator!==false?'<i></i>':''}${esc(tr(h,good?'favorable':'notFavorable'))}</div>`:'';
    const hero=c.show_price||c.show_status?`<section class="epi-hero">${c.show_price?`${c.show_price_label!==false?`<span class="epi-eyebrow">${esc(tr(h,'current'))}</span>`:''}<div class="epi-price"><b>${esc(formatted)}</b>${numeric===null||c.show_price_unit===false?'':`<small>${esc(sym)}/kWh</small>`}</div>`:''}${c.show_price&&c.show_price_sparkline?sparkline(m,h,c):''}${status}</section>`:'';
    const subToday=m.today?.attributes?.full_day_coverage===false?tr(h,'incomplete'):'';
    const subTomorrow=m.tomorrow?.attributes?.full_day_coverage===false?tr(h,'incomplete'):'';
    const averages=[c.show_average_today!==false?label(tr(h,'today'),money(m.today?.state,currency,h),subToday):'',c.show_average_tomorrow!==false?label(tr(h,'tomorrow'),money(m.tomorrow?.state,currency,h),subTomorrow):''].filter(Boolean);
    const stats=m.today?.attributes||curr.attributes||{};
    const statsCards=[c.show_minimum!==false?label(tr(h,'minimum'),money(stats.min_today_price??stats.min_day_price,currency,h)):'',c.show_maximum!==false?label(tr(h,'maximum'),money(stats.max_today_price??stats.max_day_price,currency,h)):''].filter(Boolean);
    const metricItems=[...(c.show_averages?averages:[]),...(c.show_statistics?statsCards:[])];
    const metrics=metricItems.length?`<section class="epi-metrics">${metricItems.join('')}</section>`:'';
    const effectiveSpan=this._localChartSpan||c.chart_span;
    this._raw=extractSeries(m,{...c,chart_span:effectiveSpan},h);
    const spanButton=(key,text)=>`<button type="button" data-span="${key}" class="${effectiveSpan===key?'active':''}" aria-pressed="${effectiveSpan===key}" title="${esc(text)}">${esc(text)}</button>`;
    const range=c.show_chart_range!==false?`<nav class="epi-range" aria-label="${esc(tr(h,'chartSpan'))}">${spanButton('today',tr(h,'todayOnly'))}${spanButton('tomorrow',tr(h,'tomorrowOnly'))}${spanButton('both',tr(h,'twoDays'))}</nav>`:'';
    const zoom=c.show_zoom!==false?`<div class="epi-zoom"><button type="button" data-zoom="in" aria-label="${esc(tr(h,'zoomIn'))}" title="${esc(tr(h,'zoomIn'))}">+</button><button type="button" data-zoom="out" aria-label="${esc(tr(h,'zoomOut'))}" title="${esc(tr(h,'zoomOut'))}">−</button><button type="button" data-zoom="reset" aria-label="${esc(tr(h,'resetZoom'))}" title="${esc(tr(h,'resetZoom'))}">↺</button></div>`:'';
    const legendItems=[c.show_legend_price!==false?`<span class="epi-legend-price"><i></i>${esc(tr(h,'price'))}</span>`:'',blocks.length&&c.show_chart_highlight!==false&&c.show_chart_selected_phase!==false&&c.show_legend_selected!==false?`<span><i class="selected"></i>${esc(tr(h,'marked'))}</span>`:''].filter(Boolean);
    const chartHeading=[c.show_chart_title!==false?`<h3>${esc(tr(h,'forecast'))}</h3>`:'',c.show_chart_unit!==false?`<small class="epi-chart-unit">${esc(sym)}/kWh</small>`:''].join('');
    const chart=c.show_chart?`<section class="epi-chart-section">${chartHeading||range||zoom?`<div class="epi-chart-head">${chartHeading?`<div class="epi-chart-title">${chartHeading}</div>`:''}<div class="epi-chart-actions">${range}${zoom}</div></div>`:''}<div class="epi-chart-root"${c.show_chart_gesture_zoom===false&&c.show_chart_pan===false?' style="touch-action:auto;cursor:default"':''}>${chartSvg(this._raw,p,blocks,c,h,this._viewport(this._raw))}</div>${c.show_legend&&legendItems.length?`<div class="epi-legend">${legendItems.join('')}</div>`:''}${c.show_chart_hint?`<div class="epi-chart-hint">${esc(tr(h,'chartHint'))}</div>`:''}</section>`:'';
    const ctl=(ent,key)=>ent?`<label>${esc(tr(h,key))}<select data-ctl="${esc(ent.entity_id)}">${(ent.attributes.options||[]).map(v=>{const trans=ent.entity_id.endsWith('_window_search_scope')?{future:'scopeFuture',active_future:'scopeActiveFuture'}:{threshold:'evaluationThreshold',window:'evaluationWindow'};return `<option value="${esc(v)}" ${v===ent.state?'selected':''}>${esc(tr(h,trans[v]||v))}</option>`;}).join('')}</select></label>`:'';
    const nctl=(ent,key)=>ent?`<label>${esc(tr(h,key))}<input type="number" data-num="${esc(ent.entity_id)}" min="${esc(ent.attributes.min??0)}" max="${esc(ent.attributes.max??1440)}" step="${esc(ent.attributes.step||1)}" value="${esc(ent.state)}"></label>`:'';
    const controlItems=[c.show_control_method!==false?ctl(m.method,'method'):'',c.show_control_scope!==false?ctl(m.scope,'scope'):'',phase.evaluation_mode==='window'?(c.show_control_minutes!==false?nctl(m.minutes,'minimumDuration'):''):(c.show_control_threshold!==false?nctl(m.threshold,'threshold'):'')].filter(Boolean);
    const controls=c.show_controls&&controlItems.length?`<section class="epi-controls">${controlItems.join('')}</section>`:'';
    const foot=c.show_availability?`<footer class="epi-foot">${esc(tr(h,'availability'))}: ${esc(tr(h,m.availability?.state)||tr(h,'unknown'))}</footer>`:'';
    const title=c.show_title?`<header class="epi-heading"><div class="epi-heading-mark">${c.show_header_icon!==false?'<span class="epi-logo-dot" aria-hidden="true">↗</span>':''}<h2>${esc(c.title||curr.attributes?.friendly_name?.replace(/ (Aktueller Strompreis|Current electricity price)$/i,'')||tr(h,'name'))}</h2></div>${c.show_header_subtitle!==false?`<span class="epi-heading-meta">${esc(tr(h,'headerSubtitleText'))}</span>`:''}</header>`:'';
    const standaloneCountdown=!c.show_phase?countdown:'';
    const overview=hero||phaseBlock||metrics||standaloneCountdown?`<div class="epi-overview">${hero}${phaseBlock}${metrics}${standaloneCountdown}</div>`:'';
    const stage=overview||chart?`<div class="epi-stage">${overview}${chart}</div>`:'';
    const design=['aurora','minimal','glass','timeline'].includes(c.design)?c.design:'aurora';
    const density=c.density==='comfortable'?'epi-density-comfortable':'epi-density-compact';
    const border=c.show_accent_border===false?' epi-no-accent-border':'';
    const markup=`<ha-card style="--epi-accent:${accent}" class="design-${design} ${density}${border}"><div class="epi-layout">${title}${stage}${controls}${foot}</div></ha-card>`;
    const existing=this.shadowRoot.querySelector('ha-card');
    if(existing){const template=document.createElement('template');template.innerHTML=markup;epiReconcile(existing,template.content.firstElementChild);}
    else this.shadowRoot.innerHTML=`<style>${STYLE}</style>${markup}`;
    this.shadowRoot.querySelectorAll('[data-nav]').forEach(b=>b.onclick=()=>{
      const next=(index+Number(b.dataset.nav)+blocks.length)%blocks.length;
      this._selectedPhaseKey=blocks[next].favorable_from+'|'+blocks[next].favorable_until;this.render();
    });
    this.shadowRoot.querySelectorAll('[data-span]').forEach(b=>b.onclick=()=>{
      this._localChartSpan=b.dataset.span;this._chartView=null;this.render();
    });
    this.shadowRoot.querySelectorAll('[data-zoom]').forEach(b=>b.onclick=()=>{
      if(b.dataset.zoom==='reset'){this._chartView=null;this._refreshPlot();}
      else this._zoom(b.dataset.zoom==='in'?.7:1.4);
    });
    this.shadowRoot.querySelectorAll('[data-ctl]').forEach(el=>el.onchange=async()=>{el.disabled=true;try{await this._hass.callService('select','select_option',{entity_id:el.dataset.ctl,option:el.value});}catch(e){console.warn('Energy Price Insights',e);}finally{el.disabled=false;}});
    this.shadowRoot.querySelectorAll('[data-num]').forEach(el=>el.onchange=async()=>{const val=Number(el.value);if(!Number.isFinite(val))return;el.disabled=true;try{await this._hass.callService('number','set_value',{entity_id:el.dataset.num,value:val});}catch(e){console.warn('Energy Price Insights',e);}finally{el.disabled=false;}});
    this._updateCountdown();this._wireChart();
    const chartRoot=this.shadowRoot.querySelector('.epi-chart-root');
    if(chartRoot!==this._observedChartRoot){
      this._resizeObserver?.disconnect();this._resizeObserver=null;this._observedChartRoot=chartRoot;this._lastChartWidth=0;
      if(chartRoot&&typeof ResizeObserver==='function'){this._resizeObserver=new ResizeObserver(()=>{const w=chartRoot.clientWidth||0;if(w&&w!==this._lastChartWidth){this._lastChartWidth=w;this._refreshPlot();}});this._resizeObserver.observe(chartRoot);}
    }
    if(chartRoot)this._refreshPlot();
  }}

class EnergyPriceInsightsCardEditor extends HTMLElement {
  constructor(){super();this.attachShadow({mode:'open'});this._config={...DEFAULTS};this._hass=null;this._openGroups=new Set(['content']);}
  set hass(value){const previous=this._hass;this._hass=value;
    if(!previous||lang(previous)!==lang(value)||!this.shadowRoot?.querySelector('.epi-editor'))this.render();
    else this.shadowRoot.querySelectorAll('ha-entity-picker').forEach(p=>p.hass=value);}
  setConfig(config){this._config={...DEFAULTS,...config};this.render();}
  _change(key,value){this._config={...this._config,[key]:value};this._syncSparklineSettings();this.dispatchEvent(new CustomEvent('config-changed',{detail:{config:this._config},bubbles:true,composed:true}));}
  _syncSparklineSettings(){
    this.shadowRoot.querySelectorAll('[data-sparkline-settings]').forEach(el=>{el.hidden=this._config.show_price_sparkline!==true;});
    this.shadowRoot.querySelectorAll('[data-sparkline-custom]').forEach(el=>{el.hidden=this._config.show_price_sparkline!==true||this._config.sparkline_label_style!=='custom';});
  }
  render(){if(!this.isConnected||!this._hass)return;
    const h=this._hass,c=this._config,l=key=>esc(tr(h,key));
    const pick=(key,label)=>`<label class="epi-field">${l(label)}<ha-entity-picker data-entity="${key}" allow-custom-entity></ha-entity-picker></label>`;
    const option=(v,key,current)=>`<option value="${v}" ${current===v?'selected':''}>${l(key)}</option>`;
    const toggle=(key)=>`<label class="epi-switch"><span>${l(MODULES[key])}</span><input type="checkbox" data-check="${key}" ${c[key]?'checked':''} aria-label="${l(MODULES[key])}"></label>`;
    const group=(id,label,keys,extra='')=>`<details class="epi-group" data-group="${id}" ${this._openGroups.has(id)?'open':''}><summary>${l(label)}</summary><div class="epi-group-content"><div class="epi-toggle-grid">${keys.map(toggle).join('')}</div>${extra}</div></details>`;
    const sparklineSettings=`<div class="epi-editor-grid" data-sparkline-settings ${!c.show_price_sparkline?'hidden':''}><label class="epi-field">${l('sparklineLabelStyle')}<select data-field="sparkline_label_style">${option('trend','sparklineTrend',c.sparkline_label_style)}${option('next','nextFourHours',c.sparkline_label_style)}${option('forecast','sparklineForecast',c.sparkline_label_style)}${option('custom','sparklineCustom',c.sparkline_label_style)}</select></label></div>
      <div class="epi-editor-grid" data-sparkline-custom ${!c.show_price_sparkline||c.sparkline_label_style!=='custom'?'hidden':''}><label class="epi-field">${l('sparklineText')}<input type="text" data-field="sparkline_label_text" maxlength="80" placeholder="${l('sparklineTextPlaceholder')}" value="${esc(c.sparkline_label_text)}"></label></div>`;
    const design=Object.keys({aurora:1,minimal:1,glass:1,timeline:1}).map(d=>`<button type="button" class="epi-design-choice" data-design="${d}" aria-pressed="${c.design===d}"><div class="epi-mini ${d}" aria-hidden="true"><b></b><em></em><i></i></div><span><i></i>${l(d)}</span></button>`).join('');
    this.shadowRoot.innerHTML=`<style>${STYLE}</style><div class="epi-editor">
      <header class="epi-editor-head"><div class="epi-editor-symbol" aria-hidden="true">↗</div><div><h3>Energy Price Insights</h3><p>${l('editorSubtitle')}</p></div></header>
      <section class="epi-editor-panel"><h4>${l('editorSource')}</h4><p>${l('editorSourceHint')}</p>${pick('entity','entity')}</section>
      <section class="epi-editor-panel"><h4>${l('editorAppearance')}</h4><p>${l('editorDesignHint')}</p><div class="epi-design-grid">${design}</div>
        <div class="epi-editor-grid"><label class="epi-field">${l('title')}<input type="text" data-field="title" value="${esc(c.title)}"></label>
        <label class="epi-field">${l('accent')}<span class="epi-color-field"><input type="color" data-field="accent" value="${/^#[0-9a-fA-F]{6}$/.test(c.accent)?c.accent:'#0ea5a4'}"><span>${esc(c.accent)}</span></span></label>
        <label class="epi-field">${l('editorDensity')}<select data-field="density">${option('compact','compact',c.density)}${option('comfortable','comfortable',c.density)}</select></label></div>
        <div class="epi-toggle-grid">${toggle('show_accent_border')}${toggle('show_header_icon')}${toggle('show_header_subtitle')}</div></section>
      ${group('content','editorContent',['show_title','show_price','show_price_label','show_price_unit','show_price_sparkline','show_price_sparkline_label','show_status','show_status_indicator','show_averages','show_average_today','show_average_tomorrow','show_statistics','show_minimum','show_maximum','show_controls','show_control_method','show_control_scope','show_control_threshold','show_control_minutes','show_availability'],sparklineSettings)}
      ${group('phase','editorPhase',['show_phase','show_phase_title','show_navigation','show_countdown','show_phase_start','show_phase_end','show_phase_average','show_phase_duration','show_phase_minimum'])}
      <details class="epi-group" data-group="chart" ${this._openGroups.has('chart')?'open':''}><summary>${l('editorChart')}</summary><div class="epi-group-content"><div class="epi-toggle-grid">${['show_chart','show_chart_title','show_chart_unit','show_chart_range','show_chart_axes','show_chart_grid','show_chart_highlight','show_chart_selected_phase','show_chart_other_phases','show_chart_now','show_zoom','show_chart_gesture_zoom','show_chart_pan','show_chart_crosshair','show_chart_tooltip','show_legend','show_legend_price','show_legend_selected','show_chart_hint'].map(toggle).join('')}</div>
        <div class="epi-editor-grid"><label class="epi-field">${l('chartSpan')}<select data-field="chart_span">${option('today','todayOnly',c.chart_span)}${option('tomorrow','tomorrowOnly',c.chart_span)}${option('both','twoDays',c.chart_span)}</select></label>
        <label class="epi-field">${l('editorChartHeight')}<select data-field="chart_height">${option('compact','compact',c.chart_height)}${option('balanced','balanced',c.chart_height)}${option('expanded','expanded',c.chart_height)}</select></label>
        <label class="epi-field">${l('editorChartStyle')}<select data-field="chart_style">${option('auto','auto',c.chart_style)}${option('line','line',c.chart_style)}${option('area','area',c.chart_style)}${option('bars','bars',c.chart_style)}</select></label></div></div></details>
      <details class="epi-group" data-group="advanced" ${this._openGroups.has('advanced')?'open':''}><summary>${l('editorAdvanced')} <span class="epi-info-pill">${l('editorOptional')}</span></summary><div class="epi-group-content epi-advanced">${Object.entries(EDITOR_FIELDS).map(([k,v])=>pick(k,v)).join('')}</div></details>
    </div>`;
    this.shadowRoot.querySelectorAll('details[data-group]').forEach(el=>el.addEventListener('toggle',()=>{if(el.open)this._openGroups.add(el.dataset.group);else this._openGroups.delete(el.dataset.group);}));
    this.shadowRoot.querySelectorAll('ha-entity-picker').forEach(el=>{
      const key=el.dataset.entity;el.hass=h;el.value=c[key]||'';
      el.addEventListener('value-changed',ev=>{const v=ev.detail?.value||'';if(v!==this._config[key])this._change(key,v);});
    });
    this.shadowRoot.querySelectorAll('[data-field]').forEach(el=>el.addEventListener('change',()=>this._change(el.dataset.field,el.value)));
    this._syncSparklineSettings();
    this.shadowRoot.querySelectorAll('[data-design]').forEach(el=>el.addEventListener('click',()=>this._change('design',el.dataset.design)));
    this.shadowRoot.querySelectorAll('[data-check]').forEach(el=>el.addEventListener('change',()=>this._change(el.dataset.check,el.checked)));
  }
  connectedCallback(){this.render();}
}
if(!customElements.get(CARD_TYPE)){customElements.define(CARD_TYPE,EnergyPriceInsightsCard);}
if(!customElements.get(`${CARD_TYPE}-editor`)){customElements.define(`${CARD_TYPE}-editor`,EnergyPriceInsightsCardEditor);}
window.customCards=window.customCards||[];
if(!window.customCards.some(c=>c.type===CARD_TYPE))window.customCards.push({type:CARD_TYPE,name:'Energy Price Insights',description:'Strompreis-Analyse / Electricity price insights · DE/EN · 4 Designs',preview:true});
