/* ==========================================================================
   maps.js — Cartes interactives Leaflet.js avec marqueurs filtrables.
   Dégradation gracieuse : si Leaflet n'est pas chargé (preview hors-ligne),
   un plan de secours textuel s'affiche à la place.
   ========================================================================== */
(function () {
  'use strict';

  const CATS = {
    extract:    { label: 'Extractions',       color: '#00FF9D' },
    boss:       { label: 'Boss',              color: '#FF2D2D' },
    keycard:    { label: 'Salles à keycard',  color: '#FFD700' },
    loot:       { label: 'Loot haute valeur', color: '#00C8FF' },
    password:   { label: 'Porte à code',      color: '#FF6B00' },
    secret:     { label: 'Secret',            color: '#9C27B0' },
    spawn:      { label: 'Zone de spawn',     color: '#E8EDF5' }
  };

  /* Marqueurs indicatifs : positions relatives (0–1000) sur un plan schématique.
     Ce ne sont PAS des coordonnées extraites du jeu — ils situent les zones
     décrites dans les guides. Pour les positions exactes, utiliser deltaforce.th.gl. */
  const DATA = {
    'zero-dam': { nom: 'Zero Dam', markers: [
      { x: 500, y: 180, c: 'boss',     t: 'Saeed « Fiery Owl »', d: 'Capitaine de la garde — M249. Boss le plus accessible du jeu.' },
      { x: 330, y: 300, c: 'loot',     t: 'Administrative Center', d: 'Loot le plus dense et PvP le plus intense de la carte.' },
      { x: 660, y: 420, c: 'password', t: 'Porte à code — Major Substation', d: 'Côté droit : ramper dans le pipeline souterrain jusqu\'au bout.' },
      { x: 220, y: 560, c: 'loot',     t: 'Cement Plant', d: 'Route de loot moyenne à l\'abri de la majorité des joueurs.' },
      { x: 770, y: 610, c: 'loot',     t: 'Substation Dormitory', d: 'Rarement pillé par ceux qui y spawnent.' },
      { x: 480, y: 740, c: 'secret',   t: 'Porte secrète CRACKED', d: 'Code reconstitué en morse sur la carte Warfare Cracked (objectifs A1/B1/C1/D1).' },
      { x: 140, y: 150, c: 'extract',  t: 'Extraction nord-ouest', d: 'Sortie classique, souvent surveillée en fin de timer.' },
      { x: 860, y: 820, c: 'extract',  t: 'Extraction sud-est', d: 'Plus éloignée, moins campée.' },
      { x: 500, y: 920, c: 'spawn',    t: 'Zone de spawn sud', d: 'Insertion fréquente côté usine.' }
    ]},
    'layali-grove': { nom: 'Layali Grove', markers: [
      { x: 430, y: 250, c: 'keycard',  t: 'Sparkling Empress Hotel', d: 'Plus gros concentré de keycards de valeur du jeu. King\'s Suite ici.' },
      { x: 620, y: 360, c: 'boss',     t: 'Reis « Abyss Shark »', d: 'Commandant Ahsarah. Drop : Reis Black Card.' },
      { x: 250, y: 470, c: 'loot',     t: 'Haavk WSR Lab', d: 'Radar Station + Lab Building. Électronique de haute valeur.' },
      { x: 780, y: 560, c: 'password', t: 'Porte à code — entrée souterraine', d: 'Coin inférieur droit de la carte.' },
      { x: 370, y: 650, c: 'loot',     t: 'Aminya Village', d: 'Loot moyen, bonne zone de transit.' },
      { x: 560, y: 760, c: 'loot',     t: 'Cargo Havoc', d: 'Conteneurs et caisses militaires.' },
      { x: 150, y: 200, c: 'extract',  t: 'Extraction nord', d: 'Accessible depuis Desert Trails Farm.' },
      { x: 880, y: 880, c: 'extract',  t: 'Underground Dock', d: 'Ajout de la refonte 2.0. Sortie discrète.' }
    ]},
    'space-city': { nom: 'Space City', markers: [
      { x: 500, y: 230, c: 'boss',     t: 'Desmoulins OU Hudson', d: 'Tirage à chances égales. Écoutez l\'audio de boss avant d\'engager.' },
      { x: 300, y: 330, c: 'keycard',  t: 'Bon Lab', d: 'Salles à keycard, technologie haute valeur.' },
      { x: 700, y: 400, c: 'keycard',  t: 'Black Chamber', d: 'Zone rénovée en S11.' },
      { x: 420, y: 500, c: 'password', t: 'Porte à code — Assembly Room 2F', d: 'Industrial Zone, deuxième étage.' },
      { x: 640, y: 620, c: 'loot',     t: 'CEO Office', d: 'Loot administratif de grande valeur.' },
      { x: 250, y: 700, c: 'loot',     t: 'Buoyancy Lab', d: 'Zone technique verticale.' },
      { x: 120, y: 450, c: 'extract',  t: 'Extraction ouest', d: 'Sortie rapide depuis le secteur laboratoire.' },
      { x: 880, y: 760, c: 'extract',  t: 'Extraction sud-est', d: 'Traversée à découvert : attention aux snipers.' }
    ]},
    'brakkesh': { nom: 'Brakkesh 2.0', markers: [
      { x: 500, y: 280, c: 'loot',     t: 'New Tower of Babel', d: 'ENTIÈREMENT RETRAVAILLÉE en S12 : nouveau terrain, nouvelles rotations.' },
      { x: 620, y: 200, c: 'boss',     t: 'Blue Eagle HAAVK-64', d: 'Hélicoptère de patrouille. Rester sous couvert dur.' },
      { x: 360, y: 400, c: 'password', t: 'Porte à code — nord du Hammam', d: 'Old Bath, côté nord.' },
      { x: 720, y: 450, c: 'keycard',  t: 'Museum', d: 'Salles verrouillées à forte valeur.' },
      { x: 240, y: 330, c: 'loot',     t: 'Hotel', d: 'Rue principale, très disputée dès le début de partie.' },
      { x: 810, y: 330, c: 'loot',     t: 'Fortress / Azure Town', d: 'Aussi meurtrier que le côté hôtel.' },
      { x: 300, y: 620, c: 'loot',     t: 'Market → Parking', d: 'Itinéraire nettement moins fréquenté — le plus sûr en solo.' },
      { x: 540, y: 520, c: 'secret',   t: 'Control Room remaniée', d: 'Nouvelles entrées et accès à l\'étage supérieur plus précoce.' },
      { x: 500, y: 740, c: 'keycard',  t: 'Underground Vault', d: 'Master Keycard requise.' },
      { x: 160, y: 820, c: 'extract',  t: 'Dog tag extraction', d: 'Sortie privilégiée des runs budget.' }
    ]},
    'tide-prison': { nom: 'Tide Prison', markers: [
      { x: 500, y: 300, c: 'boss',     t: 'Warden Ghroth', d: 'Administration Block. 3 Elite Guards + 2 Shieldbearers. Points faibles : épaules et dos.' },
      { x: 560, y: 230, c: 'loot',     t: 'Warden\'s Private Vault (2F)', d: 'Deux coffres, fort taux de drop Tier 6.' },
      { x: 300, y: 380, c: 'loot',     t: 'Security Monitoring Suite', d: 'West Wing : trois PC cases, électronique haut de gamme.' },
      { x: 420, y: 470, c: 'password', t: 'Porte à code — hall 1F', d: 'Administrative Area, coin de l\'escalier du hall.' },
      { x: 700, y: 560, c: 'spawn',    t: 'Cellules de départ', d: 'SEULE carte où la partie commence enfermé : s\'évader avant de pouvoir tirer.' },
      { x: 250, y: 680, c: 'loot',     t: 'Sections inondées', d: 'Loot sous-marin. Gérer son souffle.' },
      { x: 820, y: 760, c: 'extract',  t: 'Extraction en plongée', d: 'Au moins une sortie impose de plonger.' },
      { x: 140, y: 250, c: 'extract',  t: 'Extraction nord', d: 'Sortie terrestre classique.' }
    ]},
    'az3': { nom: 'AZ3 Nuclear Plant', markers: [
      { x: 500, y: 350, c: 'boss',     t: 'Neural Device Agent H1000', d: 'Combat en zone irradiée. Gérer le timer autant que le DPS.' },
      { x: 330, y: 280, c: 'loot',     t: 'Cœur technique', d: 'Loot élite, forte irradiation.' },
      { x: 680, y: 480, c: 'password', t: 'Porte à code — Seawater Treatment Area', d: 'Bâtiments situés à proximité.' },
      { x: 420, y: 600, c: 'loot',     t: 'Zone de stockage', d: 'Caisses techniques à haute valeur.' },
      { x: 200, y: 520, c: 'extract',  t: 'Extraction ouest', d: 'Sortie rapide pour run court.' },
      { x: 800, y: 680, c: 'extract',  t: 'Extraction est', d: 'Traversée exposée.' },
      { x: 500, y: 820, c: 'secret',   t: 'Supercritical — 18 décembre 2026', d: 'Difficulté Élite, prérequis Operations niveau 30. Pas encore disponible.' }
    ]}
  };

  function fallback(el, key) {
    const d = DATA[key]; if (!d) return;
    el.innerHTML = '<div class="map-fallback"><strong>' + d.nom + '</strong><br>' +
      'La carte interactive nécessite la bibliothèque Leaflet (connexion réseau).<br>' +
      'Points d\'intérêt référencés :</div><ul class="small muted" style="padding:0 1.5rem 1.5rem 2.5rem">' +
      d.markers.map(m => '<li><strong style="color:' + (CATS[m.c] ? CATS[m.c].color : '#fff') + '">' +
        m.t + '</strong> — ' + m.d + '</li>').join('') + '</ul>';
  }

  function build(el) {
    const key = el.dataset.map;
    const d = DATA[key];
    if (!d) return;
    if (typeof window.L === 'undefined') { fallback(el, key); return; }

    const L = window.L;
    const bounds = [[0, 0], [1000, 1000]];
    const map = L.map(el, {
      crs: L.CRS.Simple, minZoom: -1.2, maxZoom: 2,
      zoomControl: true, attributionControl: false
    });
    map.fitBounds(bounds);
    map.setMaxBounds([[-200, -200], [1200, 1200]]);

    // Fond schématique dessiné en SVG (aucune ressource externe)
    const svg = encodeURIComponent(
      '<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="1000">' +
      '<rect width="1000" height="1000" fill="#0C1117"/>' +
      '<g stroke="#00FF9D" stroke-opacity=".10" stroke-width="1">' +
      Array.from({ length: 20 }, (_, i) => '<line x1="' + i * 50 + '" y1="0" x2="' + i * 50 + '" y2="1000"/>' +
        '<line x1="0" y1="' + i * 50 + '" x2="1000" y2="' + i * 50 + '"/>').join('') +
      '</g><g stroke="#00C8FF" stroke-opacity=".22" stroke-width="2" fill="none">' +
      '<rect x="120" y="120" width="300" height="220" rx="4"/>' +
      '<rect x="560" y="180" width="320" height="260" rx="4"/>' +
      '<rect x="180" y="560" width="280" height="300" rx="4"/>' +
      '<rect x="580" y="600" width="300" height="240" rx="4"/>' +
      '<path d="M420 230 H560 M460 340 V560 M880 440 V600 M460 860 H580"/>' +
      '</g><text x="500" y="520" fill="#2A3A4C" font-family="monospace" font-size="26" text-anchor="middle">PLAN SCHÉMATIQUE</text></svg>');
    L.imageOverlay('data:image/svg+xml,' + svg, bounds).addTo(map);

    const layers = {};
    Object.keys(CATS).forEach(c => { layers[c] = L.layerGroup().addTo(map); });

    d.markers.forEach(m => {
      const col = CATS[m.c] ? CATS[m.c].color : '#fff';
      const icon = L.divIcon({
        className: '',
        html: '<div style="width:16px;height:16px;border-radius:50%;background:' + col +
              ';box-shadow:0 0 12px ' + col + ';border:2px solid #080B0F"></div>',
        iconSize: [16, 16], iconAnchor: [8, 8]
      });
      L.marker([1000 - m.y, m.x], { icon, title: m.t })
        .bindPopup('<strong style="color:' + col + '">' + m.t + '</strong><br><span style="font-size:.84em">' + m.d + '</span>')
        .addTo(layers[m.c] || layers.loot);
    });

    // Légende / filtres
    const legend = el.parentElement.querySelector('.map-legend');
    if (legend) {
      legend.innerHTML = Object.entries(CATS).map(([k, v]) =>
        '<label class="lg"><input type="checkbox" checked data-layer="' + k + '" style="accent-color:' + v.color + '">' +
        '<span class="dot" style="background:' + v.color + '"></span>' + v.label + '</label>').join('');
      legend.addEventListener('change', e => {
        const k = e.target.dataset.layer; if (!k) return;
        if (e.target.checked) map.addLayer(layers[k]); else map.removeLayer(layers[k]);
      });
    }
    setTimeout(() => map.invalidateSize(), 220);
  }

  function init() {
    const els = Array.from(document.querySelectorAll('[data-map]'));
    if (!els.length) return;
    els.forEach(el => {
      // Construire à l'ouverture du panneau pour éviter les cartes invisibles
      const panel = el.closest('.tabpanel');
      if (!panel || panel.classList.contains('active')) build(el);
      else {
        const obs = new MutationObserver(() => {
          if (panel.classList.contains('active') && !el._built) { el._built = true; build(el); obs.disconnect(); }
        });
        obs.observe(panel, { attributes: true, attributeFilter: ['class'] });
      }
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
