// Comportements communs ajoutés à chaque export qgis2web (par scripts/04_integrer_export.py).
// Chargé après le script de qgis2web : la variable globale `map` (Leaflet) existe.
(function () {
  if (typeof map === 'undefined') return;

  map.attributionControl.addAttribution(
    'Données : IGN, INPN, Vigicrues (Etalab 2.0) · SMAVD');

  // Dans la StoryMap, la molette doit faire défiler le récit et non zoomer la carte :
  // le zoom à la molette ne s'active qu'après un clic sur la carte.
  if (window.self !== window.top) {
    map.scrollWheelZoom.disable();
    map.once('click', () => map.scrollWheelZoom.enable());
  }

  // Recentrage demandé par la page StoryMap (boutons .lieu, voir story.js)
  window.addEventListener('message', evt => {
    const d = evt.data || {};
    if (d.type === 'allerA') {
      map.flyTo([d.lat, d.lon], d.zoom, { duration: 1.4 });
    }
  });
})();
