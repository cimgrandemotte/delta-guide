/* ==========================================================================
   search.js — Recherche globale (Ctrl/Cmd+K). Fuse.js si disponible,
   repli sur un moteur de correspondance interne sinon.
   ========================================================================== */
(function () {
  'use strict';
  const B = window.DF_BASE || './';

  /* Index statique du site : titre, catégorie, description, URL relative à la racine */
  const INDEX = [
    { t: 'Quartier Général', c: 'Navigation', d: "Page d'accueil du guide, synthèse Saison 12 Aurora", u: 'index.html' },
    { t: 'Saison 12 — Aurora', c: 'Saison', d: 'Patch notes, nouveautés, events, season pass, calendrier', u: 'pages/saison-aurora/index.html' },
    { t: 'Martelo', c: 'Opérateur', d: 'Nouvelle opératrice Assault S12 — Ariete, Smoke Halo, Guerreira', u: 'pages/operateurs/index.html#martelo' },
    { t: 'Les 19 opérateurs', c: 'Opérateurs', d: 'Fiches complètes, capacités, tier list, synergies, ordre de déblocage', u: 'pages/operateurs/index.html' },
    { t: 'Armurerie', c: 'Armes', d: 'Toutes les armes, statistiques, accessoires, codes de build', u: 'pages/armurerie/index.html' },
    { t: 'AN-94', c: 'Arme', d: 'Nouveau fusil d\'assaut 5.45x39 de la Saison Aurora, 1800 RPM en burst', u: 'pages/armurerie/index.html#an-94' },
    { t: 'Munitions & pénétration', c: 'Armes', d: 'Niveaux 1 à 6, calibres, .300BLK TIV/TTV, CINDER, 7N30, SPALL', u: 'pages/armurerie/munitions.html' },
    { t: 'Hazard Operations', c: 'Mode', d: 'Mode extraction PvPvE : boucle, économie, survie, extraction', u: 'pages/hazard-ops/index.html' },
    { t: 'Black Site', c: 'Progression', d: '11 stations, ordre d\'amélioration, planificateur de coûts', u: 'pages/hazard-ops/black-site.html' },
    { t: 'Boss', c: 'PvE', d: 'Les 8 boss : Saeed, Reis, Blue Eagle, Desmoulins, Hudson, Ghroth, Raven, H1000', u: 'pages/hazard-ops/boss.html' },
    { t: 'Keycards', c: 'Loot', d: '101 keycards, raretés, prix, salles ouvertes', u: 'pages/hazard-ops/keycards.html' },
    { t: 'Cartes interactives', c: 'Cartes', d: '6 cartes Operations avec marqueurs : extractions, boss, keycards, loot', u: 'pages/cartes/index.html' },
    { t: 'Brakkesh 2.0', c: 'Carte', d: 'Refonte S12, système de factions Ahsarah vs Haavk, Babel retravaillée', u: 'pages/cartes/index.html#brakkesh' },
    { t: 'Tide Prison', c: 'Carte', d: 'Carte Hard, évasion de cellule, Warden Ghroth, zones inondées', u: 'pages/cartes/index.html#tide-prison' },
    { t: 'AZ3 Nuclear Plant', c: 'Carte', d: 'Carte Élite, radiation, Supercritical le 18 décembre 2026', u: 'pages/cartes/index.html#az3' },
    { t: 'Zero Dam', c: 'Carte', d: 'Carte débutant, 457 marqueurs, secret CRACKED', u: 'pages/cartes/index.html#zero-dam' },
    { t: 'Layali Grove', c: 'Carte', d: '22 keycards, Sparkling Empress Hotel, King\'s Suite', u: 'pages/cartes/index.html#layali-grove' },
    { t: 'Space City', c: 'Carte', d: '409 marqueurs, Desmoulins ou Hudson, Bon Lab', u: 'pages/cartes/index.html#space-city' },
    { t: 'Havoc Warfare', c: 'Mode', d: 'Combat interarmes 32v32, véhicules, Zenith Port', u: 'pages/havoc-warfare/index.html' },
    { t: 'Véhicules', c: 'Warfare', d: 'Chars, IFV, hélicoptères, embarcations — tier list et contre-jeu', u: 'pages/havoc-warfare/index.html#vehicules' },
    { t: 'Zenith Port', c: 'Carte Warfare', d: 'Nouvelle carte S12, événement Riptide, physique amphibie', u: 'pages/havoc-warfare/index.html#zenith-port' },
    { t: 'Black Hawk Down', c: 'Campagne', d: 'Les 7 chapitres de la campagne coopérative, Mogadiscio 1993', u: 'pages/black-hawk-down/index.html' },
    { t: 'Tier list S12', c: 'Méta', d: 'Opérateurs Operations et Warfare, armes, véhicules + éditeur drag & drop', u: 'pages/encyclopedie/tier-list.html' },
    { t: 'Astuces pro', c: 'Guides', d: 'Réglages PC/console/mobile, audio, eDPI, erreurs à éviter', u: 'pages/astuces-pro/index.html' },
    { t: 'Codes de portes quotidiens', c: 'Astuces', d: 'Codes du jour par carte et emplacements des portes', u: 'pages/astuces-pro/codes-portes.html' },
    { t: 'Outils tactiques', c: 'Outils', d: 'Calculateur TTK, simulateur de pénétration, eDPI, loadout aléatoire, quiz', u: 'pages/outils/index.html' },
    { t: 'Calculateur TTK / DPS', c: 'Outil', d: 'Time To Kill, Shots To Kill et DPS selon arme, armure et munition', u: 'pages/outils/index.html#ttk' },
    { t: 'Simulateur de pénétration', c: 'Outil', d: 'Munition T1 à T6 contre armure niveau 1 à 6', u: 'pages/outils/index.html#penetration' },
    { t: 'Calculateur eDPI', c: 'Outil', d: 'Convertir DPI et sensibilité, profils sniper / polyvalent / agressif', u: 'pages/outils/index.html#edpi' },
    { t: 'Générateur de loadout', c: 'Outil', d: 'Loadout aléatoire : opérateur, arme, munitions, carte', u: 'pages/outils/index.html#loadout' },
    { t: 'Quiz tactique', c: 'Outil', d: 'Testez vos connaissances sur la Saison Aurora', u: 'pages/outils/index.html#quiz' },
    { t: 'Encyclopédie', c: 'Référence', d: 'Lexique, factions, chronologie des saisons, plateformes', u: 'pages/encyclopedie/index.html' },
    { t: 'Économie & Hôtel des Ventes', c: 'Progression', d: 'Tekniq Alloys, Delta Coins, marché joueurs, paliers de niveau', u: 'pages/encyclopedie/economie.html' },
    { t: 'News', c: 'Actualité', d: 'Dernières informations et calendrier des events Aurora', u: 'pages/news/index.html' }
  ];

  function render(list, q) {
    const box = document.querySelector('.search-results'); if (!box) return;
    if (!list.length) { box.innerHTML = '<div class="search-empty">AUCUN RÉSULTAT POUR « ' + (window.DF ? DF.esc(q) : q) + ' »</div>'; return; }
    box.innerHTML = list.slice(0, 12).map((r, i) =>
      `<a href="${B}${r.u}" ${i === 0 ? 'class="sel"' : ''}>
         <div class="r-cat">${r.c}</div>
         <div class="r-title">${r.t}</div>
         <div class="r-desc">${r.d}</div>
       </a>`).join('');
  }

  function basicSearch(q) {
    const n = q.toLowerCase().trim();
    if (!n) return INDEX.slice(0, 8);
    const terms = n.split(/\s+/);
    return INDEX.map(r => {
      const hay = (r.t + ' ' + r.c + ' ' + r.d).toLowerCase();
      let score = 0;
      terms.forEach(t => {
        if (r.t.toLowerCase().startsWith(t)) score += 10;
        else if (r.t.toLowerCase().includes(t)) score += 6;
        if (r.c.toLowerCase().includes(t)) score += 3;
        if (hay.includes(t)) score += 2;
      });
      return { r, score };
    }).filter(x => x.score > 0).sort((a, b) => b.score - a.score).map(x => x.r);
  }

  let fuse = null;
  function search(q) {
    if (window.Fuse) {
      if (!fuse) fuse = new window.Fuse(INDEX, { keys: [{ name: 't', weight: 3 }, { name: 'c', weight: 1 }, { name: 'd', weight: 1 }], threshold: 0.38, ignoreLocation: true });
      if (!q.trim()) return INDEX.slice(0, 8);
      return fuse.search(q).map(x => x.item);
    }
    return basicSearch(q);
  }

  function init() {
    const modal = document.querySelector('.search-modal');
    const input = modal && modal.querySelector('input');
    if (!modal || !input) return;

    const open = () => {
      modal.classList.add('open'); input.value = ''; render(search(''), '');
      setTimeout(() => input.focus(), 40);
      if (window.SFX) SFX.open();
    };
    const close = () => { modal.classList.remove('open'); if (window.SFX) SFX.close(); };

    document.querySelectorAll('.search-trigger').forEach(b => b.addEventListener('click', open));
    modal.addEventListener('click', e => { if (e.target === modal) close(); });
    input.addEventListener('input', () => render(search(input.value), input.value));

    document.addEventListener('keydown', e => {
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') { e.preventDefault(); modal.classList.contains('open') ? close() : open(); }
      if (e.key === '/' && !/^(INPUT|TEXTAREA|SELECT)$/.test(document.activeElement.tagName)) { e.preventDefault(); open(); }
      if (e.key === 'Escape' && modal.classList.contains('open')) close();
      if (!modal.classList.contains('open')) return;
      if (e.key === 'Enter') { const s = modal.querySelector('.search-results a.sel'); if (s) { e.preventDefault(); location.href = s.href; } }
      if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
        e.preventDefault();
        const items = Array.from(modal.querySelectorAll('.search-results a'));
        if (!items.length) return;
        let i = items.findIndex(x => x.classList.contains('sel'));
        items.forEach(x => x.classList.remove('sel'));
        i = e.key === 'ArrowDown' ? (i + 1) % items.length : (i - 1 + items.length) % items.length;
        items[i].classList.add('sel'); items[i].scrollIntoView({ block: 'nearest' });
      }
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
