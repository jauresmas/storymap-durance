/* 50 ans au fil de la Durance — plan annexé (MapLibre GL JS) piloté par le défilement du dossier */
(() => {
  'use strict';

  const reduit = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const petitEcran = matchMedia('(max-width: 820px)');

  // --- Sémiologie : mêmes couleurs que les projets QGIS -----------------------
  const C = {
    plan: '#eef0ec', eau: '#1f5f99', lit: '#a7cde9', lac: '#5d9bd0', affluent: '#7eaed6',
    canal: '#d26a1e', ouvrage: '#1b1d1f', tampon: '#5a3d9a', digue: '#a8281e',
    nature: '#3a8a50', limite: '#7d8589'
  };
  const EAU_TRANSPARENTE = 'rgba(31, 95, 153, 0)';

  const ign = (couche, style, format) =>
    `https://data.geopf.fr/wmts?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=${couche}` +
    `&STYLE=${style}&TILEMATRIXSET=PM&FORMAT=${format}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}`;
  // URL absolue : le GeoJSON est chargé par un worker, qui ne résout pas les chemins relatifs
  const geojson = (nom, options = {}) => ({
    type: 'geojson', data: new URL(`donnees/${nom}.geojson`, location.href).href, ...options
  });

  // Emprises mesurées sur les GeoJSON exportés par scripts/05_exporter_web.py
  const EMPRISE = {
    durance: [[4.739, 43.659], [6.725, 44.928]],
    canal: [[5.03, 43.52], [6.05, 44.45]],
    perimetre: [[4.698, 43.564], [5.813, 43.997]],
    natura: [[4.740, 43.656], [6.272, 44.480]],
    communes: [[4.698, 43.564], [6.568, 44.701]],
    epci: [[4.619, 43.157], [6.969, 44.701]]
  };

  // --- Couches du plan, du fond vers le dessus ------------------------------
  const transition = { duration: 800, delay: 0 };
  const largeur = (...arrets) => ['interpolate', ['linear'], ['zoom'], ...arrets];

  const COUCHES = [
    { id: 'relief', type: 'raster', source: 'relief',
      paint: { 'raster-saturation': -1, 'raster-contrast': -0.05, 'raster-brightness-min': 0.1 } },
    { id: 'ortho', type: 'raster', source: 'ortho', paint: {} },
    { id: 'departements', type: 'line', source: 'departements',
      paint: { 'line-color': C.limite, 'line-width': largeur(6, 0.8, 11, 1.6), 'line-dasharray': [4, 3] } },
    { id: 'epci_surface', type: 'fill', source: 'epci', paint: { 'fill-color': C.tampon } },
    { id: 'epci_ligne', type: 'line', source: 'epci', paint: { 'line-color': C.tampon, 'line-width': 1.2 } },
    { id: 'communes_surface', type: 'fill', source: 'communes_riveraines', paint: { 'fill-color': C.tampon } },
    { id: 'communes_ligne', type: 'line', source: 'communes_riveraines', paint: { 'line-color': C.tampon, 'line-width': 0.6 } },
    { id: 'perimetre_surface', type: 'fill', source: 'perimetre_1976', paint: { 'fill-color': C.tampon } },
    { id: 'perimetre_ligne', type: 'line', source: 'perimetre_1976', paint: { 'line-color': '#ffffff', 'line-width': 0.9 } },
    { id: 'natura_sic', type: 'fill', source: 'natura_sic', paint: { 'fill-color': C.nature } },
    { id: 'natura_zps', type: 'line', source: 'natura_zps',
      paint: { 'line-color': C.nature, 'line-width': largeur(7, 1.2, 12, 2.2), 'line-dasharray': [2, 1.5] } },
    { id: 'lit', type: 'fill', source: 'lit', paint: { 'fill-color': C.lit } },
    { id: 'affluents', type: 'line', source: 'affluents',
      paint: { 'line-color': C.affluent, 'line-width': largeur(6, 0.8, 12, 2.4) }, layout: { 'line-cap': 'round' } },
    { id: 'lac', type: 'fill', source: 'lac', paint: { 'fill-color': C.lac } },
    { id: 'levees', type: 'line', source: 'levees',
      paint: { 'line-color': C.digue, 'line-width': largeur(8, 1, 13, 2.8) }, layout: { 'line-cap': 'round' } },
    { id: 'canal', type: 'line', source: 'canal_edf',
      paint: { 'line-color': C.canal, 'line-width': largeur(7, 1.4, 12, 3), 'line-dasharray': [3, 1.6] } },
    { id: 'trace', type: 'line', source: 'durance',
      paint: { 'line-width': largeur(6, 2, 10, 3.4, 13, 5.5), 'line-gradient': degrade(0) },
      layout: { 'line-cap': 'round', 'line-join': 'round' } },
    { id: 'barrages', type: 'circle', source: 'barrages',
      paint: { 'circle-color': C.ouvrage, 'circle-radius': largeur(7, 3.5, 12, 6),
               'circle-stroke-color': '#ffffff', 'circle-stroke-width': 1.5 } },
    { id: 'stations', type: 'circle', source: 'stations',
      paint: { 'circle-color': '#ffffff', 'circle-radius': largeur(7, 3.5, 12, 6),
               'circle-stroke-color': C.ouvrage, 'circle-stroke-width': 2 } }
  ];

  // Opacité « pleine » de chaque couche ; chaque pièce la module de 0 à 1
  const PLEIN = {
    relief: { 'raster-opacity': 0.55 }, ortho: { 'raster-opacity': 1 },
    departements: { 'line-opacity': 0.85 },
    epci_surface: { 'fill-opacity': 0.14 }, epci_ligne: { 'line-opacity': 0.9 },
    communes_surface: { 'fill-opacity': 0.1 }, communes_ligne: { 'line-opacity': 0.6 },
    perimetre_surface: { 'fill-opacity': 0.42 }, perimetre_ligne: { 'line-opacity': 0.95 },
    natura_sic: { 'fill-opacity': 0.55 }, natura_zps: { 'line-opacity': 1 },
    lit: { 'fill-opacity': 0.95 }, affluents: { 'line-opacity': 1 }, lac: { 'fill-opacity': 0.95 },
    levees: { 'line-opacity': 1 }, canal: { 'line-opacity': 1 }, trace: { 'line-opacity': 1 },
    barrages: { 'circle-opacity': 1, 'circle-stroke-opacity': 1 },
    stations: { 'circle-opacity': 1, 'circle-stroke-opacity': 1 }
  };
  const GROUPES = {
    epci: ['epci_surface', 'epci_ligne'], communes: ['communes_surface', 'communes_ligne'],
    perimetre: ['perimetre_surface', 'perimetre_ligne'], natura: ['natura_sic', 'natura_zps']
  };

  // --- Légende et lieux ---------------------------------------------------------
  const LEGENDE = {
    trace: { forme: 'ligne', couleur: C.eau, epaisseur: 3, texte: 'La Durance' },
    lit: { forme: 'surface', couleur: C.lit, texte: 'Lit en eau (BD TOPO)' },
    lac: { forme: 'surface', couleur: C.lac, texte: 'Lac de Serre-Ponçon' },
    affluents: { forme: 'ligne', couleur: C.affluent, epaisseur: 1.6, texte: 'Affluents et Rhône' },
    canal: { forme: 'tirets', couleur: C.canal, epaisseur: 2.6, texte: 'Canal EDF' },
    barrages: { forme: 'pointPlein', couleur: C.ouvrage, texte: 'Barrage sur la Durance' },
    perimetre: { forme: 'surface', couleur: C.tampon, opacite: 0.42, texte: 'Communes fondatrices (reconstitution)' },
    siege: { forme: 'carre', couleur: C.tampon, texte: 'Siège du SMAVD' },
    departements: { forme: 'tirets', couleur: C.limite, epaisseur: 1.3, texte: 'Limite départementale' },
    levees: { forme: 'ligne', couleur: C.digue, epaisseur: 2.2, texte: 'Levées et digues (BD TOPO)' },
    stations: { forme: 'point', couleur: C.ouvrage, texte: 'Station Vigicrues' },
    natura_sic: { forme: 'surface', couleur: C.nature, opacite: 0.55, texte: 'Natura 2000, directive Habitats' },
    natura_zps: { forme: 'tirets', couleur: C.nature, epaisseur: 1.8, texte: 'Natura 2000, directive Oiseaux' },
    communes: { forme: 'surface', couleur: C.tampon, opacite: 0.14, contour: C.tampon, texte: 'Communes riveraines' },
    epci: { forme: 'surface', couleur: C.tampon, opacite: 0.16, contour: C.tampon, texte: 'Intercommunalités riveraines' },
    photo1950: { forme: 'surface', couleur: '#a7a49a', texte: 'Photos 1950-1965 (à gauche)' },
    photoActuelle: { forme: 'surface', couleur: '#5f7350', texte: 'Photos actuelles (à droite)' }
  };

  // Coordonnées : géocodeur IGN (communes), BD TOPO (ouvrages)
  const LIEUX = [
    { id: 'briancon', nom: 'Briançon', lngLat: [6.6372, 44.8962] },
    { id: 'embrun', nom: 'Embrun', lngLat: [6.4847, 44.568] },
    { id: 'serreponcon', nom: 'Barrage de Serre-Ponçon', lngLat: [6.2674, 44.4703] },
    { id: 'lac', nom: 'Lac de Serre-Ponçon', lngLat: [6.41, 44.535], eau: true },
    { id: 'sisteron', nom: 'Sisteron', lngLat: [5.9356, 44.2037] },
    { id: 'manosque', nom: 'Manosque', lngLat: [5.7902, 43.8265] },
    { id: 'cadarache', nom: 'Cadarache', lngLat: [5.7432, 43.718] },
    { id: 'pertuis', nom: 'Pertuis', lngLat: [5.5011, 43.6908] },
    { id: 'mallemort', nom: 'Mallemort', lngLat: [5.1782, 43.7228] },
    { id: 'siege', nom: 'Siège du SMAVD', lngLat: [5.1824, 43.7292], classe: 'siege' },
    { id: 'cavaillon', nom: 'Cavaillon', lngLat: [5.0362, 43.8488] },
    { id: 'avignon', nom: 'Avignon', lngLat: [4.8489, 43.9363] },
    { id: 'saintchamas', nom: 'Saint-Chamas', lngLat: [5.0571, 43.5426] },
    { id: 'berre', nom: 'Étang de Berre', lngLat: [5.11, 43.46], eau: true },
    { id: 'durance', nom: 'la Durance', lngLat: [5.45, 43.69], eau: true },
    { id: 'rhone', nom: 'le Rhône', lngLat: [4.775, 44.02], eau: true, ancre: 'right' },
    { id: 'verdon', nom: 'le Verdon', lngLat: [5.9, 43.755], eau: true }
  ];

  // --- Les pièces du dossier : ce que montre le plan à chaque étape -------------
  const ETAPES = {
    couverture: {
      num: 'Plan d’ensemble', titre: 'La Durance, de la source au Rhône', annee: '1976',
      vue: { emprise: EMPRISE.durance },
      couches: { relief: 1, trace: 1, affluents: 0.7, lac: 1, departements: 0.5 },
      legende: ['trace', 'affluents', 'departements'], lieux: ['sisteron', 'avignon', 'lac']
    },
    loi1955: {
      num: 'Plan n° 1', titre: 'Serre-Ponçon, la grande retenue', annee: '1955',
      vue: { centre: [6.36, 44.49], zoom: 11, inclinaison: 55, cap: -25 },
      couches: { relief: 1, lac: 1, trace: 1, affluents: 0.7, barrages: 1 },
      legende: ['lac', 'trace'], lieux: ['serreponcon', 'embrun', 'lac']
    },
    canal: {
      num: 'Plan n° 2', titre: 'Le canal EDF, vers l’étang de Berre', annee: '1966',
      vue: { emprise: EMPRISE.canal },
      couches: { relief: 1, canal: 1, trace: 0.45, lac: 0.7, barrages: 1, affluents: 0.3 },
      legende: ['canal', 'trace', 'barrages'], lieux: ['sisteron', 'manosque', 'mallemort', 'saintchamas', 'berre']
    },
    calque: {
      num: 'Plan n° 3', titre: 'Le lit entre Oraison et Manosque', annee: '1950', onglet: null,
      vue: { centre: [5.915, 43.945], zoom: 13.2, inclinaison: 0, cap: 0 },
      couches: { ortho: 1 }, calque: true,
      legende: ['photo1950', 'photoActuelle'], lieux: []
    },
    creation: {
      num: 'Plan n° 4', titre: 'Le périmètre fondateur, 1976', annee: '1976',
      vue: { emprise: EMPRISE.perimetre },
      couches: { relief: 1, perimetre: 1, departements: 1, trace: 1, affluents: 0.5 },
      legende: ['perimetre', 'siege', 'trace', 'departements'], lieux: ['siege', 'avignon', 'cavaillon', 'pertuis', 'rhone']
    },
    digues: {
      num: 'Plan n° 5', titre: 'Levées, digues et mesure des crues', annee: '1982',
      vue: { centre: [5.36, 43.745], zoom: 10.1, inclinaison: 45, cap: -12 },
      couches: { relief: 1, levees: 1, stations: 1, lit: 1, trace: 0.5 },
      legende: ['levees', 'stations', 'lit'], lieux: ['mallemort', 'cadarache', 'pertuis', 'cavaillon']
    },
    nature: {
      num: 'Plan n° 6', titre: 'Les sites Natura 2000 « La Durance »', annee: '1997',
      vue: { emprise: EMPRISE.natura },
      couches: { relief: 1, natura: 1, trace: 0.6, lac: 0.6 },
      legende: ['natura_sic', 'natura_zps', 'trace'], lieux: ['sisteron', 'manosque', 'avignon']
    },
    bassin: {
      num: 'Plan n° 7', titre: 'De Serre-Ponçon au Rhône', annee: '2005',
      vue: { emprise: EMPRISE.communes },
      couches: { relief: 1, communes: 1, trace: 1, lac: 1, affluents: 1 },
      legende: ['communes', 'trace', 'affluents'], lieux: ['lac', 'sisteron', 'avignon', 'verdon', 'rhone']
    },
    gemapi: {
      num: 'Plan n° 8', titre: 'Les intercommunalités riveraines', annee: '2018',
      vue: { emprise: EMPRISE.epci },
      // Plan administratif sans relief : à cette emprise, la limite de l'estompage IGN se verrait
      couches: { epci: 1, departements: 1, trace: 1, lac: 0.6 },
      legende: ['epci', 'departements', 'trace'], lieux: ['avignon', 'sisteron', 'berre']
    },
    demain: {
      num: 'Plan n° 9', titre: 'La Durance, vue depuis le Rhône', annee: '2026',
      vue: { centre: [5.05, 43.84], zoom: 9.4, inclinaison: 65, cap: 75 },
      couches: { relief: 1, trace: 1, levees: 0.9, stations: 1, affluents: 0.6, lac: 1 },
      legende: ['trace', 'levees', 'stations'], lieux: ['avignon', 'cavaillon', 'mallemort', 'durance']
    },
    bordereau: {
      num: 'Plan d’ensemble', titre: 'La Durance, de la source au Rhône', annee: '2026', onglet: 'demain',
      vue: { emprise: EMPRISE.durance },
      couches: { relief: 1, trace: 1, affluents: 0.6, lac: 1 },
      legende: ['trace'], lieux: []
    }
  };

  // --- Éléments de la page -----------------------------------------------------
  const $ = sel => document.querySelector(sel);
  const couverture = $('#couverture');
  const intercalaires = $('.intercalaires');
  const cartouche = $('.cartouche');
  const legendeEl = $('#c-legende');
  const lectureEl = $('#c-lecture');
  const nord = $('#c-nord');
  const barre = $('#c-echelle .c-barre');
  const valeurEchelle = $('#c-echelle .c-valeur');
  const recentrer = $('#c-recentrer');
  const alerteEl = $('#c-alerte');
  const calque = $('#calque');
  const poignee = $('.calque-poignee');

  function alerte(message) {
    alerteEl.textContent = message;
    alerteEl.hidden = false;
  }

  // Ouverture de la chemise et apparition des intercalaires au défilement
  function surDefilement() {
    const h = innerHeight;
    couverture.style.setProperty('--ouverture', Math.min(1, scrollY / (h * 0.9)).toFixed(3));
    const v = Math.min(1, Math.max(0, (scrollY - h * 0.55) / (h * 0.3)));
    document.documentElement.style.setProperty('--intercalaires', v.toFixed(2));
  }
  addEventListener('scroll', () => requestAnimationFrame(surDefilement), { passive: true });
  surDefilement();

  // Sans WebGL, le récit reste lisible : seul le plan manque
  function webglDisponible() {
    try {
      const c = document.createElement('canvas');
      return Boolean(c.getContext('webgl2') || c.getContext('webgl'));
    } catch {
      return false;
    }
  }
  if (!window.maplibregl || !webglDisponible()) {
    alerte('Ce navigateur n’affiche pas la carte interactive. Le récit reste lisible.');
    document.documentElement.style.setProperty('--intercalaires', '1');
    return;
  }
  if (location.protocol === 'file:') {
    alerte('Ouvrez cette page avec un serveur web : les données du plan ne se lisent pas depuis le disque.');
  }

  // --- Carte -------------------------------------------------------------------
  function degrade(p) {
    if (p >= 1) return ['interpolate', ['linear'], ['line-progress'], 0, C.eau, 1, C.eau];
    if (p <= 0) return ['interpolate', ['linear'], ['line-progress'], 0, EAU_TRANSPARENTE, 1, EAU_TRANSPARENTE];
    return ['interpolate', ['linear'], ['line-progress'], 0, C.eau, p, C.eau, Math.min(1, p + 0.002), EAU_TRANSPARENTE];
  }

  const style = {
    version: 8,
    sources: {
      relief: { type: 'raster', tileSize: 256, maxzoom: 15,
        tiles: [ign('ELEVATION.ELEVATIONGRIDCOVERAGE.SHADOW', 'estompage_grayscale', 'image/png')] },
      ortho: { type: 'raster', tileSize: 256, maxzoom: 19,
        tiles: [ign('ORTHOIMAGERY.ORTHOPHOTOS', 'normal', 'image/jpeg')] },
      durance: geojson('durance', { lineMetrics: true }),
      lit: geojson('lit'), lac: geojson('lac'), affluents: geojson('affluents'),
      canal_edf: geojson('canal_edf'), barrages: geojson('barrages'),
      perimetre_1976: geojson('perimetre_1976'), departements: geojson('departements'),
      communes_riveraines: geojson('communes_riveraines'), epci: geojson('epci'),
      levees: geojson('levees'), stations: geojson('stations'),
      natura_sic: geojson('natura_sic'), natura_zps: geojson('natura_zps')
    },
    layers: [
      { id: 'fond', type: 'background', paint: { 'background-color': C.plan } },
      ...COUCHES.map(c => {
        const paint = { ...c.paint };
        for (const prop of Object.keys(PLEIN[c.id])) {
          paint[prop] = 0;
          paint[`${prop}-transition`] = transition;
        }
        return { ...c, paint };
      })
    ]
  };

  const map = new maplibregl.Map({
    container: 'carte',
    style,
    center: [5.73, 44.29],
    zoom: 6.5,
    attributionControl: false,
    // Pas de maxBounds : sur grand écran, une vue de toute la vallée déborde
    // n'importe quelle emprise raisonnable et la caméra se bloquerait au centre
    maxPitch: 70,
    minZoom: 5,
    maxZoom: 17,
    fadeDuration: 200
  });
  // La molette fait défiler le récit ; le plan se manipule à la souris ou à deux doigts
  map.scrollZoom.disable();
  if (petitEcran.matches) map.dragPan.disable();

  let pret = false;
  let etapeCourante = null;
  let enAttente = 'couverture';
  const facteurs = {};

  function marges(id) {
    const w = innerWidth;
    // Sur petit écran, le plan n'occupe que le haut de l'écran
    const h = document.getElementById('carte').clientHeight || innerHeight;
    let m;
    if (petitEcran.matches) {
      if (id === 'couverture') {
        m = { top: 72, bottom: Math.max(16, h - (64 + innerHeight * 0.3) + 8), left: 24, right: 24 };
      } else {
        const haut = cartouche.getBoundingClientRect().bottom || 140;
        m = { top: haut + 12, bottom: 16, left: 20, right: 20 };
      }
    } else if (id === 'couverture') {
      m = { left: w * 0.46 + 28, right: w * 0.05 + 28, top: h * 0.09 + 28, bottom: h * 0.15 + 28 };
    } else {
      const colonne = $('.dossier').getBoundingClientRect().right;
      m = { left: colonne + 36, right: 88, top: 40, bottom: (cartouche.offsetHeight || 240) + 48 };
    }
    // Ne jamais demander plus de marge que la carte n'a de place
    const ex = m.left + m.right - (w - 120);
    if (ex > 0) { m.left -= ex / 2; m.right -= ex / 2; }
    const ey = m.top + m.bottom - (h - 120);
    if (ey > 0) { m.top -= ey / 2; m.bottom -= ey / 2; }
    return m;
  }

  // Cadrage d'une emprise calculé en pseudo-Mercator (tuiles de 512 px) : fitBounds de
  // MapLibre 4 se trompe dès que la carte a déjà des marges ou une inclinaison
  function vuePourEmprise([[ouest, sud], [est, nord]], p) {
    const x = lng => (lng + 180) / 360 * 512;
    const y = lat => {
      const r = lat * Math.PI / 180;
      return (1 - Math.log(Math.tan(r) + 1 / Math.cos(r)) / Math.PI) / 2 * 512;
    };
    const boite = map.getContainer();
    const largeurUtile = boite.clientWidth - p.left - p.right;
    const hauteurUtile = boite.clientHeight - p.top - p.bottom;
    const zoom = Math.log2(Math.min(largeurUtile / (x(est) - x(ouest)), hauteurUtile / (y(sud) - y(nord))));
    const yc = (y(sud) + y(nord)) / 2;
    const lat = Math.atan(Math.sinh(Math.PI * (1 - 2 * yc / 512))) * 180 / Math.PI;
    return { center: [(ouest + est) / 2, lat], zoom: Math.min(zoom, 14), pitch: 0, bearing: 0 };
  }

  function cadrer(id, instantane = false) {
    const vue = ETAPES[id].vue;
    const padding = marges(id);
    const cible = vue.emprise
      ? vuePourEmprise(vue.emprise, padding)
      : { center: vue.centre, zoom: vue.zoom - (petitEcran.matches ? 0.9 : 0), pitch: vue.inclinaison, bearing: vue.cap };
    if (reduit || instantane) {
      map.jumpTo({ ...cible, padding });
    } else {
      map.flyTo({ ...cible, padding, duration: 2600, curve: 1.5, essential: true });
    }
  }

  function appliquerCouches(couches) {
    for (const c of COUCHES) {
      const groupe = Object.keys(GROUPES).find(g => GROUPES[g].includes(c.id)) || c.id;
      const f = couches[groupe] ?? 0;
      facteurs[c.id] = f;
      for (const [prop, plein] of Object.entries(PLEIN[c.id])) {
        // Relief atténué aux petites échelles : la limite de couverture de l'estompage IGN s'y voit moins
        const valeur = c.id === 'relief'
          ? ['interpolate', ['linear'], ['zoom'], 7, 0.3 * plein * f, 9, plein * f]
          : plein * f;
        map.setPaintProperty(c.id, prop, valeur);
      }
    }
  }

  function pastille(d) {
    const op = d.opacite ?? 1;
    const contour = d.contour ? `stroke="${d.contour}" stroke-width="1"` : '';
    const formes = {
      ligne: `<line x1="2" y1="7" x2="26" y2="7" stroke="${d.couleur}" stroke-width="${d.epaisseur}" stroke-linecap="round"/>`,
      tirets: `<line x1="1" y1="7" x2="27" y2="7" stroke="${d.couleur}" stroke-width="${d.epaisseur}" stroke-dasharray="4 2.6"/>`,
      surface: `<rect x="1" y="1.5" width="26" height="11" fill="${d.couleur}" fill-opacity="${op}" ${contour}/>`,
      point: `<circle cx="14" cy="7" r="4.5" fill="#fff" stroke="${d.couleur}" stroke-width="2"/>`,
      pointPlein: `<circle cx="14" cy="7" r="4.5" fill="${d.couleur}" stroke="#fff" stroke-width="1.5"/>`,
      carre: `<rect x="9.5" y="2.5" width="9" height="9" fill="${d.couleur}"/>`
    };
    return `<svg viewBox="0 0 28 14" aria-hidden="true">${formes[d.forme]}</svg>`;
  }

  function ecrireLegende(cles) {
    legendeEl.innerHTML = cles.map(k => `<li>${pastille(LEGENDE[k])}<span>${LEGENDE[k].texte}</span></li>`).join('');
  }

  // L'année se retape case par case, sans que le cartouche ne bouge
  function taperAnnee(annee) {
    const cases = document.querySelectorAll('#c-annee span');
    [...annee].forEach((chiffre, i) => {
      const c = cases[i];
      if (c.textContent === chiffre) return;
      setTimeout(() => {
        c.classList.remove('frappe');
        c.textContent = chiffre;
        void c.offsetWidth;
        c.classList.add('frappe');
      }, reduit ? 0 : i * 70);
    });
    $('#c-annee').setAttribute('aria-label', `Année ${annee}`);
  }

  // Lieux : marqueurs HTML pour garder la typographie du dossier sur le plan
  // (MapLibre impose son opacité au conteneur du marqueur : on anime l'étiquette à l'intérieur)
  const marqueurs = new Map();
  for (const l of LIEUX) {
    const conteneur = document.createElement('div');
    const el = document.createElement('span');
    el.className = ['lieu', l.eau && 'eau', l.classe].filter(Boolean).join(' ');
    el.textContent = l.nom;
    conteneur.appendChild(el);
    new maplibregl.Marker({ element: conteneur, anchor: l.ancre || (l.eau ? 'center' : 'left') })
      .setLngLat(l.lngLat).addTo(map);
    marqueurs.set(l.id, el);
  }

  function activer(id, instantane = false) {
    if (!ETAPES[id]) return;
    if (!pret) { enAttente = id; return; }
    if (id === etapeCourante) return;
    etapeCourante = id;
    const e = ETAPES[id];

    document.querySelectorAll('.piece').forEach(p => p.classList.toggle('active', p.dataset.etape === id));
    document.body.classList.toggle('fin', id === 'bordereau');
    // Une pièce sans intercalaire (le calque) n'en active aucun : rail, cartouche et tampon restent d'accord
    const onglet = 'onglet' in e ? e.onglet : id;
    intercalaires.querySelectorAll('a').forEach(a => {
      if (a.dataset.etape === onglet) a.setAttribute('aria-current', 'step');
      else a.removeAttribute('aria-current');
    });

    $('#c-num').textContent = e.num;
    $('#c-plan').textContent = e.titre;
    ecrireLegende(e.legende);
    taperAnnee(e.annee);
    marqueurs.forEach((el, cle) => el.classList.toggle('visible', e.lieux.includes(cle)));

    appliquerCouches(e.couches);
    if (id === 'canal') preparerCalque();
    activerCalque(Boolean(e.calque));
    recentrer.hidden = true;
    cadrer(id, instantane);
  }

  // --- Lecture en direct : coordonnées, nord, échelle --------------------------
  const nombre = (n, d) => n.toLocaleString('fr-FR', { minimumFractionDigits: d, maximumFractionDigits: d });
  let lectureDemandee = false;
  function lecture() {
    lectureDemandee = false;
    const c = map.getCenter();
    const z = map.getZoom();
    lectureEl.textContent = `${nombre(c.lat, 3)}° N · ${nombre(c.lng, 3)}° E · z ${nombre(z, 1)}`;
    nord.style.transform = `rotate(${-map.getBearing()}deg)`;
    // Échelle au centre du plan (tuiles de 512 px en pseudo-Mercator)
    const mParPx = 40075016.686 * Math.cos(c.lat * Math.PI / 180) / (512 * 2 ** z);
    const cible = mParPx * 90;
    const puissance = 10 ** Math.floor(Math.log10(cible));
    const n = cible / puissance;
    const rond = (n >= 5 ? 5 : n >= 2 ? 2 : 1) * puissance;
    barre.style.width = `${Math.round(rond / mParPx)}px`;
    valeurEchelle.textContent = rond >= 1000 ? `${nombre(rond / 1000, 0)} km` : `${rond} m`;
  }
  map.on('move', () => {
    if (!lectureDemandee) { lectureDemandee = true; requestAnimationFrame(lecture); }
  });

  // Quand le lecteur explore le plan, on lui propose d'y revenir
  map.on('movestart', ev => { if (ev.originalEvent && etapeCourante) recentrer.hidden = false; });
  recentrer.addEventListener('click', () => { recentrer.hidden = true; cadrer(etapeCourante); });

  // --- Infobulles ----------------------------------------------------------------
  const SURVOL = {
    perimetre_surface: 'nom', communes_surface: 'nom_officiel', epci_surface: 'nom',
    natura_sic: 'nom_site', stations: 'lbentcru', barrages: 'toponyme'
  };
  const infobulle = new maplibregl.Popup({ closeButton: false, closeOnClick: false, className: 'infobulle', offset: 12 });
  map.on('mousemove', ev => {
    const actives = Object.keys(SURVOL).filter(id => facteurs[id] > 0);
    const f = actives.length ? map.queryRenderedFeatures(ev.point, { layers: actives })[0] : null;
    if (f) {
      const texte = String(f.properties[SURVOL[f.layer.id]] || '').replace(/\s*\[[^\]]*\]/g, '');
      infobulle.setLngLat(ev.lngLat).setText(texte).addTo(map);
      map.getCanvas().style.cursor = 'help';
    } else {
      infobulle.remove();
      map.getCanvas().style.cursor = '';
    }
  });

  // --- Calque 1950-1965 ------------------------------------------------------------
  let calqueCarte = null;
  let calqueSuit = false;
  let coupe = 0;

  function synchroniser() {
    calqueCarte?.jumpTo({
      center: map.getCenter(), zoom: map.getZoom(), bearing: map.getBearing(),
      pitch: map.getPitch(), padding: map.getPadding()
    });
  }
  map.on('move', () => { if (calqueSuit) synchroniser(); });

  function bornesCoupe() {
    const min = petitEcran.matches ? 16 : $('.dossier').getBoundingClientRect().right + 24;
    return [min, innerWidth - (petitEcran.matches ? 16 : 96)];
  }

  function placerCoupe(x) {
    const [min, max] = bornesCoupe();
    coupe = Math.min(max, Math.max(min, x));
    calque.style.setProperty('--coupe', `${coupe}px`);
    poignee.setAttribute('aria-valuenow', String(Math.round(100 * (coupe - min) / (max - min))));
  }

  // Le calque est créé (invisible) dès la pièce précédente, placé sur la vue de
  // comparaison : les photographies de 1950 sont déjà chargées quand on y arrive
  function preparerCalque() {
    if (!calqueCarte) {
      calqueCarte = new maplibregl.Map({
        container: 'calque-carte',
        interactive: false,
        attributionControl: false,
        center: map.getCenter(), zoom: map.getZoom(),
        style: {
          version: 8,
          sources: {
            histo: { type: 'raster', tileSize: 256, maxzoom: 18,
              tiles: [ign('ORTHOIMAGERY.ORTHOPHOTOS.1950-1965', 'BDORTHOHISTORIQUE', 'image/png')] }
          },
          layers: [
            { id: 'fond', type: 'background', paint: { 'background-color': '#d9d7cf' } },
            { id: 'histo', type: 'raster', source: 'histo' }
          ]
        }
      });
    }
    calqueCarte.resize();
    if (!calqueSuit) {
      const vue = ETAPES.calque.vue;
      calqueCarte.jumpTo({
        center: vue.centre, zoom: vue.zoom - (petitEcran.matches ? 0.9 : 0),
        pitch: 0, bearing: 0, padding: marges('calque')
      });
    }
  }

  function activerCalque(actif) {
    calqueSuit = actif;
    calque.classList.toggle('actif', actif);
    if (!actif) return;
    preparerCalque();
    const [min, max] = bornesCoupe();
    placerCoupe((min + max) / 2);
    synchroniser();
  }

  poignee.addEventListener('pointerdown', ev => {
    poignee.setPointerCapture(ev.pointerId);
    const deplacer = e => placerCoupe(e.clientX);
    const lacher = () => {
      poignee.removeEventListener('pointermove', deplacer);
      poignee.removeEventListener('pointerup', lacher);
      poignee.removeEventListener('pointercancel', lacher);
    };
    poignee.addEventListener('pointermove', deplacer);
    poignee.addEventListener('pointerup', lacher);
    poignee.addEventListener('pointercancel', lacher);
  });
  poignee.addEventListener('keydown', ev => {
    const [min, max] = bornesCoupe();
    const pas = ev.shiftKey ? 80 : 24;
    const cibles = { ArrowLeft: coupe - pas, ArrowRight: coupe + pas, Home: min, End: max };
    if (ev.key in cibles) { ev.preventDefault(); placerCoupe(cibles[ev.key]); }
  });

  // --- Chargement : le tracé de la Durance se dessine de l'amont vers le Rhône ------
  let traceDessine = false;
  function dessinerTrace() {
    if (traceDessine) return;
    traceDessine = true;
    if (reduit) { map.setPaintProperty('trace', 'line-gradient', degrade(1)); return; }
    const debut = performance.now();
    const duree = 4200;
    const pas = t => {
      const p = Math.min(1, (t - debut) / duree);
      map.setPaintProperty('trace', 'line-gradient', degrade(1 - (1 - p) ** 3));
      if (p < 1) requestAnimationFrame(pas);
    };
    requestAnimationFrame(pas);
  }
  map.on('sourcedata', ev => {
    if (ev.sourceId === 'durance' && ev.isSourceLoaded && pret) dessinerTrace();
  });

  map.on('error', ev => {
    console.warn('Plan :', ev.error?.message || ev.error);
    const source = ev.sourceId || ev.source?.id || '';
    if (source && source !== 'relief' && source !== 'ortho') {
      alerte('Une partie des données du plan n’a pas pu être chargée.');
    }
  });

  // Dès que le style est prêt (sans attendre toutes les tuiles du relief) : le récit
  // pilote le plan, et chaque couche apparaît à mesure que ses données arrivent
  map.once('style.load', () => {
    pret = true;
    activer(enAttente, true);
    lecture();
    if (map.isSourceLoaded('durance')) dessinerTrace();
  });

  // --- Pièces et intercalaires ----------------------------------------------------------
  const observateur = new IntersectionObserver(entrees => {
    for (const e of entrees) if (e.isIntersecting) activer(e.target.dataset.etape);
  }, {
    // Ligne de lecture : milieu de l'écran, ou milieu de la zone de texte sous le plan sur mobile
    rootMargin: petitEcran.matches ? '-70% 0px -28% 0px' : '-48% 0px -48% 0px'
  });
  document.querySelectorAll('.couverture, .piece, .dos').forEach(el => observateur.observe(el));

  let attenteRedim = 0;
  addEventListener('resize', () => {
    clearTimeout(attenteRedim);
    attenteRedim = setTimeout(() => {
      if (petitEcran.matches) map.dragPan.disable(); else map.dragPan.enable();
      if (etapeCourante) {
        cadrer(etapeCourante, true);
        if (ETAPES[etapeCourante].calque) activerCalque(true);
      }
    }, 200);
  });
})();
