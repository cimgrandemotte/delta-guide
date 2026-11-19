/* ==========================================================================
   tools.js — Outils tactiques interactifs
   TTK/STK/DPS · Simulateur de pénétration · eDPI · Loadout aléatoire
   Calculateur de raid · Quiz tactique · Tier list drag & drop
   ========================================================================== */
(function () {
  'use strict';
  const $ = (s, c) => (c || document).querySelector(s);
  const $$ = (s, c) => Array.from((c || document).querySelectorAll(s));
  const fmt = n => Number(n).toLocaleString('fr-FR');

  /* ==================================================== 1. TTK / STK / DPS */
  const WEAPONS = [
    { n: 'AN-94',    d: 34, rpm: 600,  pen: 42, burst: 1800 },
    { n: 'M4A1',     d: 27, rpm: 800,  pen: 32 },
    { n: 'CI-19',    d: 35, rpm: 706,  pen: 38 },
    { n: 'K416',     d: 32, rpm: 880,  pen: 32 },
    { n: 'SMG-45',   d: 35, rpm: 605,  pen: 40 },
    { n: 'MP7',      d: 24, rpm: 950,  pen: 28 },
    { n: 'MK4',      d: 34, rpm: 793,  pen: 34 },
    { n: 'M250',     d: 55, rpm: 550,  pen: 53 },
    { n: 'AWM',      d: 100, rpm: 45,  pen: 70 },
    { n: 'SR-25',    d: 35, rpm: 300,  pen: 48 },
    { n: 'ASh-12',   d: 62, rpm: 450,  pen: 60 },
    { n: 'RM277',    d: 42, rpm: 550,  pen: 55 },
    { n: 'AUG',      d: 30, rpm: 700,  pen: 36 },
    { n: 'AS Val',   d: 30, rpm: 900,  pen: 34 },
    { n: 'MK47',     d: 48, rpm: 500,  pen: 44 }
  ];
  const ZONES = { tete: 2.0, torse: 1.0, abdomen: 0.95, bras: 0.55, jambes: 0.8 };

  function initTTK() {
    const root = $('#ttk'); if (!root) return;
    const wSel = $('#ttk-weapon', root), aSel = $('#ttk-armor', root),
          zSel = $('#ttk-zone', root), pSel = $('#ttk-ammo', root), out = $('#ttk-out', root);
    if (!wSel) return;
    wSel.innerHTML = WEAPONS.map(w => `<option value="${w.n}">${w.n}</option>`).join('');

    function calc() {
      const w = WEAPONS.find(x => x.n === wSel.value) || WEAPONS[0];
      const armor = +aSel.value, ammo = +pSel.value, mult = ZONES[zSel.value] || 1;
      const HP = 100;

      // Modèle pédagogique : la mitigation dépend de l'écart munition / armure.
      let mitig;
      if (ammo > armor) mitig = 0.92;              // surpénétration : quasi plein dégât
      else if (ammo === armor) mitig = 0.62;       // partage armure / santé
      else mitig = Math.max(0.10, 0.45 - (armor - ammo) * 0.11); // sous-pénétration

      const perShot = w.d * mult * mitig;
      const stk = Math.max(1, Math.ceil(HP / perShot));
      const rps = w.rpm / 60;
      const ttk = (stk - 1) / rps;
      const dps = w.d * mult * mitig * rps;

      let verdict, cls;
      if (ammo < armor - 1) { verdict = 'MUNITION INADAPTÉE — vous ne percez pas cette armure'; cls = 'alert-red'; }
      else if (ammo < armor) { verdict = 'Sous-calibré : l\'armure encaisse l\'essentiel'; cls = 'alert-red'; }
      else if (ammo === armor) { verdict = 'Échange équilibré : dégâts partagés armure / santé'; cls = 'alert'; }
      else { verdict = 'Surpénétration : vous traversez l\'armure'; cls = 'alert-green'; }

      const burst = w.burst ? `<p class="tiny txt-orange mt-2">⚑ Les deux premières balles partent à ${w.burst} RPM : en rafale courte le TTK réel est plus bas que l'estimation.</p>` : '';

      out.innerHTML = `
        <div class="stat-grid mb-4">
          <div class="stat-cell"><span class="n">${stk}</span><span class="l">Balles (STK)</span></div>
          <div class="stat-cell"><span class="n">${(ttk * 1000).toFixed(0)}</span><span class="l">TTK en ms</span></div>
          <div class="stat-cell"><span class="n">${dps.toFixed(0)}</span><span class="l">DPS effectif</span></div>
          <div class="stat-cell"><span class="n">${perShot.toFixed(1)}</span><span class="l">Dégâts / balle</span></div>
        </div>
        <div class="alert ${cls}"><span class="ico">${cls === 'alert-green' ? '✓' : cls === 'alert-red' ? '⚠' : '≈'}</span>
        <div><strong>${verdict}.</strong> Munition niveau ${ammo} contre armure niveau ${armor}, impact ${zSel.options[zSel.selectedIndex].text.toLowerCase()}.</div></div>
        ${burst}
        <p class="tiny muted mt-3">Modèle pédagogique calibré sur les règles publiées (répartition armure/santé,
        multiplicateurs de zone). Il donne des ordres de grandeur comparatifs, pas les valeurs exactes du moteur de jeu.</p>`;
    }
    [wSel, aSel, zSel, pSel].forEach(e => e && e.addEventListener('change', calc));
    calc();
  }

  /* ==================================================== 2. PÉNÉTRATION */
  function initPen() {
    const root = $('#penetration'); if (!root) return;
    const grid = $('#pen-grid', root); if (!grid) return;
    const COL = ['#808080', '#4CAF50', '#2196F3', '#9C27B0', '#FFD700', '#FF4444'];
    let html = '<div class="table-wrap"><table class="df" style="min-width:560px"><thead><tr><th>Munition \\ Armure</th>';
    for (let a = 1; a <= 6; a++) html += `<th class="num">Niv. ${a}</th>`;
    html += '</tr></thead><tbody>';
    for (let m = 1; m <= 6; m++) {
      html += `<tr><td><span class="tier" style="background:${COL[m - 1]};width:1.7rem;height:1.7rem;font-size:.78rem">${m}</span> <strong>Niveau ${m}</strong></td>`;
      for (let a = 1; a <= 6; a++) {
        let txt, bg, fg;
        if (m > a) { txt = 'PERCE'; bg = 'rgba(0,255,157,.18)'; fg = '#00FF9D'; }
        else if (m === a) { txt = 'PARTAGE'; bg = 'rgba(255,107,0,.16)'; fg = '#FF6B00'; }
        else if (a - m === 1) { txt = 'FAIBLE'; bg = 'rgba(255,45,45,.12)'; fg = '#FF8A8A'; }
        else { txt = 'BLOQUÉ'; bg = 'rgba(255,45,45,.22)'; fg = '#FF2D2D'; }
        if (m === 5 && a === 6) { txt = 'BLOQUÉ'; bg = 'rgba(255,45,45,.22)'; fg = '#FF2D2D'; }
        html += `<td class="num" style="background:${bg};color:${fg};font-family:var(--f-hud);font-size:.68rem;letter-spacing:.08em">${txt}</td>`;
      }
      html += '</tr>';
    }
    html += '</tbody></table></div>';
    grid.innerHTML = html;

    const mSel = $('#pen-ammo', root), aSel = $('#pen-armor', root), out = $('#pen-out', root);
    function verdict() {
      if (!mSel || !out) return;
      const m = +mSel.value, a = +aSel.value;
      let msg, cls, detail;
      if (m === 5 && a === 6) {
        cls = 'alert-red'; msg = 'BLOQUÉ';
        detail = 'Les munitions dorées (niveau 5) pénètrent les armures de niveau 1 à 5 mais <strong>pas le niveau 6</strong>. C\'est la règle la plus souvent oubliée.';
      } else if (m > a) {
        cls = 'alert-green'; msg = 'PÉNÉTRATION COMPLÈTE';
        detail = 'Votre munition dépasse le niveau d\'armure : les dégâts passent presque intégralement à la santé.';
      } else if (m === a) {
        cls = 'alert'; msg = 'ÉCHANGE ÉQUILIBRÉ';
        detail = 'À niveau égal, les dégâts se répartissent entre la durabilité de l\'armure et la santé. Le duel se joue sur la cadence et la précision.';
      } else {
        cls = 'alert-red'; msg = 'SOUS-CALIBRÉ';
        detail = `Votre munition est ${a - m} niveau(x) en dessous. Seule l'armure encaisse : <strong>aucun dégât de santé</strong> tant qu'elle n'est pas rompue. Visez la tête ou changez de munition.`;
      }
      out.innerHTML = `<div class="alert ${cls}"><span class="ico">${cls === 'alert-green' ? '✓' : cls === 'alert' ? '≈' : '⚠'}</span>
        <div><strong>${msg}</strong> — munition niveau ${m} contre armure niveau ${a}.<br>${detail}</div></div>`;
    }
    [mSel, aSel].forEach(e => e && e.addEventListener('change', verdict));
    verdict();
  }

  /* ==================================================== 3. eDPI */
  function initEdpi() {
    const root = $('#edpi'); if (!root) return;
    const dpi = $('#ed-dpi', root), sens = $('#ed-sens', root), nd = $('#ed-newdpi', root), out = $('#ed-out', root);
    if (!dpi) return;
    function calc() {
      const e = (+dpi.value) * (+sens.value);
      const conv = (+nd.value) > 0 ? e / (+nd.value) : 0;
      let prof, note;
      if (e < 2400) { prof = 'Très bas — sniper longue portée'; note = 'Précision maximale, rotations lentes. Demande un grand tapis.'; }
      else if (e < 4000) { prof = 'Sniper / longue portée'; note = 'Recommandé pour AWM, SR-25 et jeu posé en Operations.'; }
      else if (e < 6400) { prof = 'Polyvalent'; note = 'La zone de confort de la majorité des joueurs. Bon compromis.'; }
      else if (e < 9600) { prof = 'Agressif / CQB'; note = 'Adapté au jeu SMG et aux duels rapprochés. Visée fine plus difficile.'; }
      else { prof = 'Très élevé'; note = 'Rotations instantanées mais contrôle du recul très exigeant.'; }
      out.innerHTML = `
        <div class="stat-grid mb-4">
          <div class="stat-cell"><span class="n">${fmt(Math.round(e))}</span><span class="l">eDPI</span></div>
          <div class="stat-cell"><span class="n">${conv ? conv.toFixed(2) : '—'}</span><span class="l">Sens. à ${fmt(+nd.value)} DPI</span></div>
          <div class="stat-cell"><span class="n">${(e / 800).toFixed(2)}</span><span class="l">Équiv. à 800 DPI</span></div>
        </div>
        <div class="alert alert-blue"><span class="ico">🎯</span><div><strong>${prof}.</strong> ${note}</div></div>
        <p class="tiny muted mt-3">Formule : eDPI = DPI × sensibilité en jeu. Pour conserver le même ressenti en changeant
        de DPI : nouvelle sensibilité = eDPI cible ÷ nouveau DPI. Référence compétitive : 800 DPI, sensibilité 5 à 8, coefficient ADS 1.33.</p>`;
    }
    [dpi, sens, nd].forEach(e => e && e.addEventListener('input', calc));
    calc();
  }

  /* ==================================================== 4. LOADOUT ALÉATOIRE */
  const OPS = ['Martelo', 'D-Wolf', 'Vyron', 'Nox', 'Tempest', 'Stinger', 'Toxik', 'Vlinder', 'Rover',
               'Shepherd', 'Uluru', 'Sineva', 'Gizmo', 'N-Two', 'Luna', 'Hackclaw', 'Raptor', 'Morse'];
  const MAPS = ['Zero Dam', 'Layali Grove', 'Space City', 'Brakkesh 2.0', 'Tide Prison', 'AZ3 Nuclear Plant'];
  const AMMO = ['RRLP (niv. 1)', 'M855 (niv. 3)', 'M855A1 (niv. 4)', 'M995 (niv. 5)', 'CINDER (niv. 4, incendiaire)',
                '.300BLK TIV (niv. 4, détonante)', '.300BLK TTV (niv. 5, détonante)', '5.45 SPALL (niv. 4)',
                '9x19 7N30 (niv. 5)', 'BP 7.62x39 (niv. 4)', 'BS 5.45 (niv. 5)'];
  const DEFIS = ['Aucun secondaire', 'Pas de soin au-delà du premier kit', 'Extraction obligatoire en moins de 10 min',
                 'Interdiction de tirer avant d\'avoir pillé 5 conteneurs', 'Un seul chargeur de rechange',
                 'Pas de visée ADS sous 15 m', 'Ramasser et extraire une keycard', 'Tuer le boss de la carte',
                 'Jouer entièrement accroupi en intérieur', 'Extraire avec plus de 300 000 Alloys de butin'];

  function initLoadout() {
    const root = $('#loadout'); if (!root) return;
    const btn = $('#lo-roll', root), out = $('#lo-out', root);
    if (!btn) return;
    const pick = a => a[Math.floor(Math.random() * a.length)];
    function roll() {
      const w = pick(WEAPONS), o = pick(OPS), m = pick(MAPS), a = pick(AMMO), d = pick(DEFIS);
      out.innerHTML = `
        <div class="grid g-auto-sm">
          <div class="card card-accent"><div class="hud tiny muted mb-1">OPÉRATEUR</div><strong class="display" style="font-size:1.25rem">${o}</strong></div>
          <div class="card card-accent-orange"><div class="hud tiny muted mb-1">ARME PRINCIPALE</div><strong class="display" style="font-size:1.25rem">${w.n}</strong></div>
          <div class="card card-accent-blue"><div class="hud tiny muted mb-1">MUNITIONS</div><strong style="font-size:1rem">${a}</strong></div>
          <div class="card card-accent-red"><div class="hud tiny muted mb-1">CARTE</div><strong style="font-size:1.05rem">${m}</strong></div>
        </div>
        <div class="alert alert-orange mt-4"><span class="ico">⚔</span><div><strong>Défi imposé :</strong> ${d}</div></div>`;
      if (window.SFX) SFX.success();
    }
    btn.addEventListener('click', roll);
    roll();
  }

  /* ==================================================== 5. CALCULATEUR DE RAID */
  function initRaid() {
    const root = $('#raid'); if (!root) return;
    const kit = $('#rd-kit', root), loot = $('#rd-loot', root), runs = $('#rd-runs', root),
          surv = $('#rd-surv', root), survOut = $('#rd-surv-val', root), out = $('#rd-out', root);
    if (!kit) return;
    function calc() {
      const k = +kit.value, l = +loot.value, n = +runs.value, s = (+surv.value) / 100;
      if (survOut) survOut.textContent = (+surv.value) + ' %';
      const gainBrut = l * n * s;
      const coutTotal = k * n;
      const net = gainBrut - coutTotal;
      const parRun = n ? net / n : 0;
      const seuil = l > 0 ? (k / l * 100) : 0;
      out.innerHTML = `
        <div class="stat-grid mb-4">
          <div class="stat-cell"><span class="n" style="color:${net >= 0 ? 'var(--df-green)' : 'var(--df-red)'}">${fmt(Math.round(net))}</span><span class="l">Résultat net</span></div>
          <div class="stat-cell"><span class="n">${fmt(Math.round(parRun))}</span><span class="l">Net par run</span></div>
          <div class="stat-cell"><span class="n">${fmt(Math.round(coutTotal))}</span><span class="l">Investi</span></div>
          <div class="stat-cell"><span class="n">${seuil.toFixed(0)}%</span><span class="l">Survie minimale</span></div>
        </div>
        <div class="alert ${net >= 0 ? 'alert-green' : 'alert-red'}"><span class="ico">${net >= 0 ? '✓' : '⚠'}</span>
        <div>${net >= 0
          ? `Votre kit est <strong>rentable</strong> à ce taux de survie. Vous pouvez monter en gamme tant que vous restez au-dessus de <strong>${seuil.toFixed(0)}%</strong> d'extractions réussies.`
          : `Vous <strong>perdez des Alloys</strong>. Il vous faudrait soit extraire dans <strong>${seuil.toFixed(0)}%</strong> des cas, soit descendre votre kit à <strong>${fmt(Math.round(l * s))} Alloys</strong> maximum.`}
        </div></div>
        <p class="tiny muted mt-3">Rappel : la Safe Box survit à la mort — y placer l'objet de mission critique
        améliore mécaniquement votre rentabilité réelle.</p>`;
    }
    [kit, loot, runs, surv].forEach(e => e && e.addEventListener('input', calc));
    calc();
  }

  /* ==================================================== 6. QUIZ */
  const QUIZ = [
    { q: "Quand la Saison 12 Aurora est-elle passée en live ?", o: ["7 novembre 2026", "10 novembre 2026 à 02:00 UTC", "12 novembre 2026", "1er décembre 2026"], a: 1,
      e: "Déploiement le 10 novembre 2026 à 02:00 UTC, sans interruption de service." },
    { q: "Combien de nouvelles munitions la Saison Aurora introduit-elle ?", o: ["2", "3", "5", "6"], a: 2,
      e: ".300BLK TIV, .300BLK TTV, 5.56 CINDER, 9x19 7N30 et 5.45 SPALL — cinq, pas deux." },
    { q: "Une munition dorée de niveau 5 perce-t-elle une armure de niveau 6 ?", o: ["Oui, toujours", "Non, jamais", "Seulement à bout portant", "Seulement en headshot"], a: 1,
      e: "Les munitions niveau 5 pénètrent les armures 1 à 5, mais pas le niveau 6." },
    { q: "Quelle est la capacité signature de Martelo ?", o: ["Smoke Halo", "Ariete", "Guerreira", "Cryo-Flask"], a: 1,
      e: "Ariete : charge frontale au bélier-bouclier, 30 % de réduction des dégâts de face après l'ajustement pré-saison." },
    { q: "Quelle monnaie faut-il pour améliorer le Black Site ?", o: ["Delta Coins", "Tekniq Alloys", "Warfare Credits", "Les deux au choix"], a: 1,
      e: "Uniquement des Tekniq Alloys. Ne dépensez jamais de Delta Coins pour une amélioration." },
    { q: "Quelle station du Black Site faut-il améliorer en priorité absolue ?", o: ["Workbench", "Pharmacy", "Stash", "Decontamination Chamber"], a: 2,
      e: "Le Stash : sans place de stockage, tout le reste de l'économie est bloqué." },
    { q: "Quel calibre utilise l'AN-94 ?", o: ["5.56x45mm", "7.62x39mm", "5.45x39mm", "6.8x51mm"], a: 2,
      e: "5.45x39mm. Les deux premières balles partent à 1800 RPM avant de retomber à 600." },
    { q: "Sur quelle carte la partie commence-t-elle enfermé en cellule ?", o: ["AZ3", "Tide Prison", "Brakkesh", "Space City"], a: 1,
      e: "Tide Prison : il faut s'évader avant même de pouvoir tirer." },
    { q: "La Ghroth Judgement Card est-elle extractible ?", o: ["Oui, elle se revend très cher", "Non, elle n'est valable que pour le match en cours", "Oui mais une seule par compte", "Elle n'existe pas"], a: 1,
      e: "Elle ouvre une des trois salles de haute valeur, uniquement pendant le match. Elle n'est pas extractible." },
    { q: "Quand AZ3 Supercritical ouvre-t-il ?", o: ["Au lancement de la saison", "18 décembre 2026", "1er janvier 2027", "26 janvier 2027"], a: 1,
      e: "Le 18 décembre 2026, avec un prérequis de niveau Operations 30." },
    { q: "Quelle carte Warfare a été retirée en Saison 12 ?", o: ["The Mog", "Cracked", "Akh Canal", "Threshold"], a: 2,
      e: "Akh Canal a été retirée de la rotation Warfare, sans raison communiquée dans les patch notes." },
    { q: "Que se passe-t-il avec votre stash entre deux saisons ?", o: ["Il est entièrement wipé", "Seuls les consommables sont wipés", "Rien, il est conservé", "Il est converti en Alloys"], a: 2,
      e: "Delta Force ne pratique pas de wipe de stash. Seules les missions de la saison précédente sont réinitialisées." }
  ];

  function initQuiz() {
    const root = $('#quiz'); if (!root) return;
    const box = $('#qz-box', root), prog = $('#qz-prog', root), restart = $('#qz-restart', root);
    if (!box) return;
    let i = 0, score = 0, order = [];

    function start() {
      order = QUIZ.map((_, k) => k).sort(() => Math.random() - 0.5);
      i = 0; score = 0; if (restart) restart.classList.add('hidden'); render();
    }
    function render() {
      if (i >= order.length) return finish();
      const q = QUIZ[order[i]];
      if (prog) prog.innerHTML = `<span class="hud tiny">QUESTION ${i + 1} / ${order.length}</span>
        <span class="hud tiny txt-green">SCORE ${score}</span>`;
      box.innerHTML = `<h3 class="card-title mb-4">${q.q}</h3>` +
        q.o.map((o, k) => `<button class="quiz-opt" data-k="${k}">${o}</button>`).join('');
      $$('.quiz-opt', box).forEach(b => b.addEventListener('click', () => answer(+b.dataset.k, q)));
    }
    function answer(k, q) {
      $$('.quiz-opt', box).forEach((b, idx) => {
        b.disabled = true;
        if (idx === q.a) b.classList.add('good');
        else if (idx === k) b.classList.add('bad');
      });
      if (k === q.a) { score++; if (window.SFX) SFX.success(); } else if (window.SFX) SFX.error();
      const d = document.createElement('div');
      d.className = 'alert ' + (k === q.a ? 'alert-green' : 'alert-red');
      d.style.marginTop = '1rem';
      d.innerHTML = `<span class="ico">${k === q.a ? '✓' : '✗'}</span><div>${q.e}</div>`;
      box.appendChild(d);
      const next = document.createElement('button');
      next.className = 'btn btn-primary mt-4';
      next.textContent = i + 1 >= order.length ? 'Voir le résultat' : 'Question suivante';
      next.addEventListener('click', () => { i++; render(); });
      box.appendChild(next);
      next.focus();
    }
    function finish() {
      const pct = Math.round(score / order.length * 100);
      let grade, msg;
      if (pct >= 90) { grade = 'OPÉRATEUR D\'ÉLITE'; msg = 'Vous lisez les patch notes avant de jouer. Respect.'; }
      else if (pct >= 70) { grade = 'VÉTÉRAN'; msg = 'Solide. Quelques détails de la saison vous échappent encore.'; }
      else if (pct >= 50) { grade = 'OPÉRATEUR CONFIRMÉ'; msg = 'Les bases sont là. Repassez par la page Saison Aurora.'; }
      else { grade = 'RECRUE'; msg = 'Bienvenue. Commencez par la page Munitions : c\'est ce qui tue le plus de joueurs.'; }
      if (prog) prog.innerHTML = '<span class="hud tiny">TERMINÉ</span>';
      box.innerHTML = `<div class="text-center">
        <div class="display grad-text" style="font-size:3rem">${pct}%</div>
        <div class="hud txt-orange mb-3" style="letter-spacing:.2em">${grade}</div>
        <p class="lead" style="margin-inline:auto">${msg}</p>
        <p class="small muted mt-3">${score} bonne(s) réponse(s) sur ${order.length}.</p>
      </div>`;
      if (restart) restart.classList.remove('hidden');
    }
    if (restart) restart.addEventListener('click', start);
    start();
  }

  /* ==================================================== 7. TIER LIST DRAG & DROP */
  function initTierList() {
    const root = $('#tier-editor'); if (!root) return;
    let dragged = null;

    function bindItem(el) {
      el.setAttribute('draggable', 'true');
      el.setAttribute('tabindex', '0');
      el.addEventListener('dragstart', e => { dragged = el; el.classList.add('dragging'); e.dataTransfer.effectAllowed = 'move'; });
      el.addEventListener('dragend', () => { el.classList.remove('dragging'); dragged = null; save(); });
      // Accessibilité clavier : flèches haut/bas pour changer de rang
      el.addEventListener('keydown', e => {
        if (e.key !== 'ArrowUp' && e.key !== 'ArrowDown') return;
        e.preventDefault();
        const zones = $$('.tier-drop', root);
        const cur = zones.indexOf(el.parentElement);
        const next = e.key === 'ArrowUp' ? cur - 1 : cur + 1;
        if (next >= 0 && next < zones.length) { zones[next].appendChild(el); el.focus(); save(); }
      });
    }
    $$('.tier-item', root).forEach(bindItem);

    $$('.tier-drop', root).forEach(z => {
      z.addEventListener('dragover', e => { e.preventDefault(); z.classList.add('over'); });
      z.addEventListener('dragleave', () => z.classList.remove('over'));
      z.addEventListener('drop', e => {
        e.preventDefault(); z.classList.remove('over');
        if (dragged) { z.appendChild(dragged); save(); if (window.SFX) SFX.click(); }
      });
    });

    function state() {
      const o = {};
      $$('.tier-row', root).forEach(r => {
        const k = r.querySelector('.tier-label').textContent.trim();
        o[k] = $$('.tier-item', r).map(x => x.textContent.trim());
      });
      return o;
    }
    function save() { try { localStorage.setItem('df-tierlist', JSON.stringify(state())); } catch (e) {} }
    function load() {
      try {
        const raw = localStorage.getItem('df-tierlist'); if (!raw) return;
        const o = JSON.parse(raw);
        const all = {}; $$('.tier-item', root).forEach(x => { all[x.textContent.trim()] = x; });
        Object.entries(o).forEach(([k, names]) => {
          const row = $$('.tier-row', root).find(r => r.querySelector('.tier-label').textContent.trim() === k);
          if (!row) return;
          const zone = row.querySelector('.tier-drop');
          names.forEach(n => { if (all[n]) zone.appendChild(all[n]); });
        });
      } catch (e) {}
    }
    load();

    const reset = $('#tl-reset'); if (reset) reset.addEventListener('click', () => {
      localStorage.removeItem('df-tierlist'); location.reload();
    });
    const exp = $('#tl-export'); if (exp) exp.addEventListener('click', () => {
      const o = state();
      const txt = Object.entries(o).map(([k, v]) => `${k} : ${v.join(', ') || '—'}`).join('\n');
      const full = `MA TIER LIST DELTA FORCE — Saison 12 Aurora\n${'='.repeat(44)}\n${txt}\n\nCréée avec le Delta Force Ultimate Operator's Guide`;
      navigator.clipboard?.writeText(full).then(
        () => { if (window.toast) toast('Tier list copiée dans le presse-papiers'); if (window.SFX) SFX.success(); },
        () => { if (window.toast) toast('Copie impossible'); });
    });
  }


  /* ==================================================== T06 — CALCULATEUR D'ARTISANAT */
  function initCraft() {
    var cout = document.getElementById('cc-cout');
    if (!cout) return;
    var vente = document.getElementById('cc-vente'),
        duree = document.getElementById('cc-duree'),
        frais = document.getElementById('cc-frais'),
        oNet = document.getElementById('cc-net'),
        oH = document.getElementById('cc-heure'),
        oM = document.getElementById('cc-marge'),
        oV = document.getElementById('cc-verdict');

    function fmt(n) {
      var sign = n < 0 ? '-' : '';
      return sign + Math.round(Math.abs(n)).toLocaleString('fr-FR');
    }
    function calc() {
      var c = +cout.value || 0, v = +vente.value || 0,
          d = Math.max(+duree.value || 0, 0.01), f = (+frais.value || 0) / 100;
      var brut = v * (1 - f);
      var net = brut - c;
      var parH = net / d;
      var marge = c > 0 ? (net / c) * 100 : 0;

      oNet.textContent = fmt(net);
      oH.textContent = fmt(parH) + ' /h';
      oM.textContent = (marge >= 0 ? '+' : '') + marge.toFixed(0) + ' %';
      oNet.className = 'num ' + (net > 0 ? 'txt-green' : 'txt-red');

      var msg;
      if (net <= 0) {
        msg = '<strong class="txt-red">Production à perte.</strong> La commission mange tout. Vendez les matériaux plutôt que de les transformer.';
      } else if (marge < 20) {
        msg = '<strong class="txt-orange">Marge trop mince.</strong> Moins de 20 % après commission : vous immobilisez un atelier pour presque rien. Cherchez mieux.';
      } else if (parH < 2000) {
        msg = '<strong class="txt-orange">Rentable mais lent.</strong> Le profit horaire est faible : acceptable pour un cycle de nuit, pas pour une session active.';
      } else if (parH < 10000) {
        msg = '<strong class="txt-green">Bonne production.</strong> Rendement solide. Lancez-la et vérifiez le marché au prochain cycle.';
      } else {
        msg = '<strong class="txt-gold">Excellente production.</strong> Ce rendement horaire est dans le haut du panier — occupez tous vos ateliers avec ça tant que le prix tient.';
      }
      oV.innerHTML = msg;
    }
    [cout, vente, duree, frais].forEach(function (el) {
      el.addEventListener('input', calc);
    });
    calc();
  }

  /* ==================================================== T08 — ENCHÈRES OU MARCHAND */
  function initMarket() {
    var ah = document.getElementById('mc-ah');
    if (!ah) return;
    var vd = document.getElementById('mc-vendor'),
        frais = document.getElementById('mc-frais'),
        slots = document.getElementById('mc-slots'),
        oNet = document.getElementById('mc-net'),
        oE = document.getElementById('mc-ecart'),
        oC = document.getElementById('mc-case'),
        oV = document.getElementById('mc-verdict');

    function fmt(n) {
      var sign = n < 0 ? '-' : '';
      return sign + Math.round(Math.abs(n)).toLocaleString('fr-FR');
    }
    function calc() {
      var a = +ah.value || 0, v = +vd.value || 0,
          f = (+frais.value || 0) / 100, s = Math.max(+slots.value || 1, 1);
      var net = a * (1 - f);
      var ecart = net - v;
      var best = Math.max(net, v);
      var parCase = best / s;

      oNet.textContent = fmt(net);
      oE.textContent = (ecart >= 0 ? '+' : '') + fmt(ecart);
      oE.className = 'num ' + (ecart > 0 ? 'txt-green' : 'txt-red');
      oC.textContent = fmt(parCase);

      var msg;
      if (ecart <= 0) {
        msg = '<strong class="txt-orange">Vendez au marchand.</strong> Après commission, l\'hôtel des ventes rapporte moins — et vous auriez bloqué un emplacement pour rien.';
      } else if (ecart < 2000) {
        msg = '<strong class="txt-orange">Vendez au marchand.</strong> La règle des cinq secondes : ' + fmt(ecart) + ' Alloys d\'écart ne justifient pas d\'immobiliser un emplacement de vente.';
      } else if (parCase < 10000) {
        msg = '<strong class="txt-green">Listez aux enchères.</strong> L\'écart est réel. Notez que ' + fmt(parCase) + ' Alloys par case reste sous le repère du butin bleu : à emporter seulement si votre sac n\'est pas plein.';
      } else {
        msg = '<strong class="txt-gold">Listez aux enchères sans hésiter.</strong> ' + fmt(parCase) + ' Alloys par case : c\'est exactement ce que vous devez prioriser dans votre sac.';
      }
      oV.innerHTML = msg;
    }
    [ah, vd, frais, slots].forEach(function (el) {
      el.addEventListener('input', calc);
    });
    calc();
  }

  /* ==================================================== T15 — CHECKLIST DE PROGRESSION */
  function initChecklist() {
    var list = document.getElementById('ck-list');
    if (!list) return;
    var boxes = list.querySelectorAll('input[data-check]'),
        count = document.getElementById('ck-count'),
        fill = document.getElementById('ck-fill'),
        reset = document.getElementById('ck-reset'),
        KEY = 'df-checklist';

    function today() {
      var d = new Date();
      return d.getFullYear() + '-' + (d.getMonth() + 1) + '-' + d.getDate();
    }
    function read() {
      try {
        var raw = JSON.parse(localStorage.getItem(KEY) || '{}');
        if (raw.day !== today()) return {};
        return raw.done || {};
      } catch (e) { return {}; }
    }
    function save(done) {
      try {
        localStorage.setItem(KEY, JSON.stringify({ day: today(), done: done }));
      } catch (e) { /* stockage indisponible : la page reste utilisable */ }
    }
    function refresh() {
      var n = 0;
      boxes.forEach(function (b) { if (b.checked) n++; });
      var pct = boxes.length ? Math.round((n / boxes.length) * 100) : 0;
      if (count) count.textContent = n + ' / ' + boxes.length;
      if (fill) { fill.style.width = pct + '%'; fill.setAttribute('data-pct', pct); }
    }

    var done = read();
    boxes.forEach(function (b) {
      var id = b.getAttribute('data-check');
      if (done[id]) b.checked = true;
      b.addEventListener('change', function () {
        var cur = read();
        if (b.checked) cur[id] = 1; else delete cur[id];
        save(cur);
        refresh();
      });
    });
    if (reset) {
      reset.addEventListener('click', function () {
        boxes.forEach(function (b) { b.checked = false; });
        save({});
        refresh();
      });
    }
    refresh();
  }

  /* ==================================================== INIT */
  function init() {
    initTTK(); initPen(); initEdpi(); initLoadout(); initRaid(); initQuiz(); initTierList();
    initCraft(); initMarket(); initChecklist();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
