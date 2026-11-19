#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_armurerie.py — Armurerie (index), Munitions, Codes de build."""

from site_common import (head, navbar, footer, scripts, write, esc,
                         load, crumbs, page_hero, audio_briefing)

W = load("weapons")
A = load("ammo")
B = load("builds")
T = load("tier_list")
D = 2

CATS = W["categories"]


def tierof(w):
    return w.get("tier") or w.get("tier_ops") or w.get("tier_warfare") or ""


# =========================================================== ARMURERIE INDEX
cards = []
for i, w in enumerate(W["armes"]):
    t = tierof(w)
    tb = f'<span class="tier tier-{esc(t)}" style="width:1.6rem;height:1.6rem;font-size:.8rem">{esc(t)}</span>' if t else ""
    new = '<span class="badge badge-new">NOUVEAU S12</span>' if w.get("badge") == "NOUVEAU S12" else ""
    stats = w.get("stats") or w.get("stats_operations") or {}
    stat_rows = ""
    for k, v in stats.items():
        label = k.replace("_", " ").replace("rpm", "RPM").replace("ms", "m/s").title()
        pct = None
        if isinstance(v, (int, float)):
            maxes = {"degats": 110, "portee_m": 200, "controle": 100, "maniabilite": 100,
                     "stabilite": 100, "precision": 100, "penetration_armure": 100,
                     "penetration": 100, "capacite": 150}
            if k in maxes:
                pct = min(100, v / maxes[k] * 100)
        if pct is not None:
            cls = "hi" if pct >= 66 else ("mid" if pct >= 33 else "low")
            stat_rows += (f'<div class="statbar"><span class="lbl">{esc(label)}</span>'
                          f'<span class="track"><span class="fill {cls}" data-pct="{pct:.0f}"></span></span>'
                          f'<span class="val">{esc(v)}</span></div>')
        else:
            stat_rows += (f'<div class="statbar"><span class="lbl">{esc(label)}</span>'
                          f'<span class="small" style="grid-column:2/4">{esc(v)}</span></div>')

    builds = "".join(
        f"""<div class="mb-2">
          <div class="tiny muted mb-1">{esc(b.get('mode','—'))}{' · ' + esc(b['note']) if b.get('note') else ''}</div>
          <div class="codebox"><code>{esc(b['code'])}</code>
          <button class="copy-btn" data-copy="{esc(b['code'])}">COPIER</button></div>
        </div>""" for b in w.get("builds", []))

    acc = "".join(f'<span class="chip">{esc(x)}</span>' for x in w.get("accessoires_recommandes", []))
    extra = ""
    for key, label, cls in [("s12", "Changement S12", "alert-orange"), ("event", "Event", "alert-blue"),
                            ("deblocage", "Déblocage", ""), ("deblocage_warfare", "Déblocage Warfare", ""),
                            ("restriction", "Restriction", "alert-red"),
                            ("particularite", "Particularité", "alert-green"),
                            ("cout_build_complet", "Coût", ""), ("note_degats", "Dégâts", ""),
                            ("cosmetiques_s12", "Cosmétique S12", "")]:
        if w.get(key):
            extra += f'<p class="small mb-2"><strong class="txt-green">{label} :</strong> {esc(w[key])}</p>'

    cards.append(f"""<article class="card" id="{esc(w['id'])}"
      data-tags="{esc(w.get('categorie','').lower().replace(' ','-'))} {'new' if new else ''} tier-{esc(t).lower()}"
      data-search="{esc(w['nom'])} {esc(w.get('categorie',''))} {esc(w.get('calibre',''))} {esc(w.get('resume',''))}"
      data-reveal data-delay="{(i%3)*50}">
      <div class="flex items-start justify-between gap-3 mb-2">
        <div>
          <div class="op-class">{esc(w.get('categorie','—'))}{' · ' + esc(w['calibre']) if w.get('calibre') else ''}</div>
          <h3 class="op-name">{esc(w['nom'])}</h3>
        </div>
        <div class="flex gap-2 items-center">{new}{tb}</div>
      </div>
      {f'<p class="small mb-3">{esc(w["resume"])}</p>' if w.get('resume') else ''}
      {f'<p class="tiny muted mb-3">Taux de sélection : <strong class="txt-blue">{esc(w.get("pick_rate") or w.get("pick_rate_ops"))}</strong></p>' if (w.get('pick_rate') or w.get('pick_rate_ops')) else ''}
      {extra}
      {f'<details class="acc mt-3"><summary>Statistiques</summary><div class="acc-body">{stat_rows}</div></details>' if stat_rows else ''}
      {f'<details class="acc"><summary>Codes de build ({len(w.get("builds",[]))})</summary><div class="acc-body">{builds}</div></details>' if builds else ''}
      {f'<details class="acc"><summary>Accessoires recommandés</summary><div class="acc-body"><div class="chips">{acc}</div></div></details>' if acc else ''}
    </article>""")

cat_chips = "".join(f'<button class="chip" data-val="{c.lower().replace(" ","-")}">{esc(c)}</button>' for c in CATS)

# Accessoires
accs = W["accessoires"]
slots = "".join(f'<span class="chip">{esc(x)}</span>' for x in accs["slots"])
ex = "".join(f"""<tr><td><strong>{esc(a['nom'])}</strong></td><td>{esc(a['slot'])}</td>
    <td class="small muted">{esc(a['effet'])}</td></tr>""" for a in accs["exemples_majeurs"])

body = f"""
{page_hero("Armurerie", "Toutes les <span class='grad-text'>armes</span>",
           "Statistiques, accessoires et codes de build importables en un clic. "
           "Chaque changement d'équilibrage précise son mode d'application.",
           "assets/images/weapons/armurerie_an94_01.jpg", D, badge="AN-94 S12")}

<section class="section-sm"><div class="wrap">
  {crumbs([("Armurerie", None)], D)}
  <div class="grid g-2 gap-4 mb-5">
    <figure class="img-frame" data-reveal><img src="../../assets/images/weapons/armurerie_sniper_01.jpg" alt="Tireur d'élite en position d'observation sur une crête à l'aube" loading="lazy" decoding="async"><figcaption>Longue portée — patience et position</figcaption></figure>
    <figure class="img-frame" data-reveal data-delay="90"><img src="../../assets/images/weapons/armurerie_cqb_01.jpg" alt="Binôme dégageant un couloir étroit à l'arme compacte" loading="lazy" decoding="async"><figcaption>Combat rapproché — la première rafale propre décide</figcaption></figure>
  </div>
  <div class="mb-4" style="max-width:560px">{audio_briefing("armurerie_briefing_01.mp3", "Armurerie", "", D)}</div>
  <div class="flex wrapf gap-3 mb-5">
    <a class="btn btn-ghost btn-sm" href="munitions.html">Munitions &amp; pénétration</a>
    <a class="btn btn-ghost btn-sm" href="builds.html">Tous les codes de build</a>
    <a class="btn btn-ghost btn-sm" href="../outils/index.html#ttk">Calculateur TTK</a>
  </div>
  <div class="hud-panel" data-filter-group data-filter-target="#weapon-grid > article"
       data-filter-input="#w-search" data-filter-count="#w-count" data-reveal>
    <div class="flex wrapf items-center justify-between gap-4">
      <div class="chips">
        <button class="chip active" data-val="all">Toutes</button>
        {cat_chips}
        <button class="chip" data-val="new">Nouveautés S12</button>
      </div>
      <div class="field" style="min-width:230px">
        <label for="w-search">Recherche</label>
        <input class="input" id="w-search" type="search" placeholder="Nom, calibre, catégorie…">
      </div>
    </div>
    <p class="tiny muted mt-3"><span id="w-count">{len(W['armes'])}</span> arme(s) affichée(s) sur {len(W['armes'])}.</p>
  </div>
</div></section>

<section class="section-sm"><div class="wrap">
  <div class="grid g-auto-md" id="weapon-grid">{''.join(cards)}</div>
</div></section>

<section class="section"><div class="wrap">
  <div class="section-head" data-reveal>
    <div class="eyebrow">{esc(accs['note'])}</div>
    <h2>Accessoires</h2>
  </div>
  <div class="card mb-5" data-reveal>
    <h3 class="card-title" style="font-size:1rem">Slots disponibles</h3>
    <div class="chips mt-2">{slots}</div>
    <p class="small muted mt-3">{esc(accs['calibration'])}</p>
  </div>
  <div class="table-wrap" data-reveal><table class="df">
    <thead><tr><th class="sortable">Accessoire</th><th class="sortable">Slot</th><th>Effet</th></tr></thead>
    <tbody>{ex}</tbody></table></div>
</div></section>

<section class="section-sm"><div class="wrap">
  <div class="alert" data-reveal><span class="ico" aria-hidden="true">⚠</span>
  <div><strong>À propos des codes de build.</strong> {esc(W['_meta']['avertissement'])}
  Format : <code class="mono">{esc(W['_meta']['format_code'])}</code></div></div>
</div></section>
"""
html = (head("Armurerie — toutes les armes", "Armurerie complète de Delta Force : statistiques détaillées, "
             "accessoires, codes de build copiables et changements d'équilibrage Saison 12 par mode. AN-94 incluse.",
             depth=D, canonical="pages/armurerie/index.html",
             image="assets/images/weapons/armurerie_an94_01.jpg")
        + navbar(D) + '<main id="main">' + body + "</main>" + footer(D) + scripts(D))
print(write("pages/armurerie/index.html", html))


# =========================================================== MUNITIONS
regles = "".join(f"<li>{esc(r)}</li>" for r in A["regles_fondamentales"])
conv = "".join(f"""<div class="card text-center" data-reveal>
    <div style="height:6px;background:{c['couleur']};margin:-1rem -1rem 1rem"></div>
    <strong class="display" style="font-size:1.3rem;color:{c['couleur']}">{esc(c['tier'])}</strong>
    <p class="small mt-2">{esc(c['libelle'])}</p>
    <p class="tiny muted">{esc(c['usage'])}</p>
  </div>""" for c in A["convention_couleurs"])

cal_blocks = ""
for c in A["calibres"]:
    rows = ""
    for m in c["munitions"]:
        new = '<span class="badge badge-new">S12</span>' if m.get("nouveau_s12") else ""
        pen = m.get("penetration", "—")
        pencol = ["#808080", "#4CAF50", "#2196F3", "#9C27B0", "#FFD700", "#FF4444"][min(5, max(0, int(pen) - 1))] if isinstance(pen, int) else "#7A8FA6"
        rows += (f'<tr><td><strong>{esc(m["nom"])}</strong> {new}</td>'
                 f'<td class="num"><span class="tier" style="background:{pencol};width:1.6rem;height:1.6rem;font-size:.78rem">{esc(pen)}</span></td>'
                 f'<td class="small mono">{esc(m.get("prix_par_balle","—"))}</td>'
                 f'<td class="small muted">{esc(m.get("effet") or m.get("usage",""))}</td>'
                 f'<td class="small mono">{esc(m.get("mult_degats","—"))} / {esc(m.get("mult_penetration","—"))}</td></tr>')
    cal_blocks += f"""<div class="mb-6" data-reveal>
      <h3 class="card-title flex items-center gap-2">{esc(c['calibre'])}
        <span class="badge badge-grey">{len(c['munitions'])} munitions</span></h3>
      {f'<p class="small muted mb-2">{esc(c["note"])}</p>' if c.get('note') else ''}
      <div class="table-wrap"><table class="df">
        <thead><tr><th>Munition</th><th class="num">Pénétration</th><th>Prix / balle</th><th>Effet / usage</th><th>Dmg / Pen ×</th></tr></thead>
        <tbody>{rows}</tbody></table></div>
    </div>"""

s12_rows = "".join(
    f'<tr><td><strong>{esc(m["munition"])}</strong> <span class="badge badge-new">S12</span></td>'
    f'<td>{esc(m["type"])}</td><td class="num">{esc(m["niveau"])}</td>'
    f'<td class="num mono">{esc(m["mult_degats"])}</td><td class="num mono">{esc(m["mult_pen"])}</td></tr>'
    for m in A["nouveautes_s12_resume"])

arm_regles = "".join(f"<li>{esc(r)}</li>" for r in A["armures"]["regles"])

# --- matrice de pénétration (data/ammo.json) ---
MX = A["matrice_penetration"]
_pc = lambda v: ("#FF2D2D" if v >= 100 else "#FF9500" if v >= 75 else "#FFD700" if v >= 50
                 else "#4C8FA8" if v >= 25 else "#3A4454")
mx_head = "".join(f'<th class="num">Armure {n}</th>' for n in MX["niveaux_armure"])
mx_rows = ""
for ln in MX["lignes"]:
    cells = "".join(
        f'<td class="num" style="background:{_pc(v)}22;color:{_pc(v)};font-weight:700;font-family:var(--f-mono)">{v} %</td>'
        for v in ln["taux"])
    mx_rows += (f'<tr><th scope="row" style="text-align:left">'
                f'<span class="tier" style="background:{["#808080","#4CAF50","#2196F3","#9C27B0","#FFD700","#FF4444"][ln["munition"]-1]};'
                f'width:1.6rem;height:1.6rem;font-size:.78rem">{ln["munition"]}</span> Munition niv. {ln["munition"]}'
                f'</th>{cells}</tr>')

# --- prix par calibre ---
prix_blocks = "".join(f"""<div class="card" data-reveal data-delay="{i*60}">
    <h3 class="card-title" style="font-size:1rem">{esc(pc['calibre'])}</h3>
    <div class="table-wrap mt-2"><table class="df" style="min-width:0">
      <thead><tr><th>Munition</th><th class="num">Niv.</th><th class="num">Prix / balle</th><th>Usage</th></tr></thead>
      <tbody>{''.join(f'<tr><td class="mono small">{esc(m["nom"])}</td>'
                      f'<td class="num"><span class="tier" style="background:{["#808080","#4CAF50","#2196F3","#9C27B0","#FFD700","#FF4444"][m["niveau"]-1]};width:1.4rem;height:1.4rem;font-size:.7rem">{m["niveau"]}</span></td>'
                      f'<td class="num mono small">{esc(m["prix"])}</td>'
                      f'<td class="tiny muted">{esc(m["usage"])}</td></tr>' for m in pc['munitions'])}</tbody>
    </table></div>
  </div>""" for i, pc in enumerate(A["prix_par_calibre"]))

# --- casques (data/armures.json) ---
AR = load("armures")
casques = "".join(f"""<tr>
    <td><strong>{esc(c['nom'])}</strong></td>
    <td class="num"><span class="tier" style="background:{["#808080","#4CAF50","#2196F3","#9C27B0","#FFD700","#FF4444"][c['niveau']-1]};width:1.5rem;height:1.5rem;font-size:.74rem">{c['niveau']}</span></td>
    <td class="num mono {'txt-green' if '+' in c['audition'] and c['audition'] != '+20 %' else 'txt-red' if 'réduite' in c['audition'] else ''}">{esc(c['audition'])}</td>
    <td class="small muted">{esc(c['contrepartie'])}</td>
    <td class="small">{esc(c['verdict'])}</td>
  </tr>""" for c in AR["casques"])

mun_body = f"""
{page_hero("Balistique", "Munitions &amp; <span class='grad-text'>pénétration</span>",
           "Le système le plus important de Delta Force — et le plus mal compris. "
           "Six niveaux de pénétration, six niveaux d'armure, et une règle qui décide de tous vos duels.",
           "assets/images/weapons/armurerie_an94_01.jpg", D, badge="5 MUNITIONS S12")}

<section class="section-sm"><div class="wrap">
  {crumbs([("Armurerie", "pages/armurerie/index.html"), ("Munitions", None)], D)}
  <div class="mb-4" style="max-width:560px">{audio_briefing("munitions_briefing_01.mp3", "Balistique", "", D)}</div>
  <div class="alert alert-red" data-reveal><span class="ico" aria-hidden="true">⚠</span>
  <div>{esc(A['_meta']['avertissement'])}</div></div>
</div></section>

<section class="section"><div class="wrap wrap-narrow">
  <div class="section-head" data-reveal>
    <div class="eyebrow">À retenir avant tout</div>
    <h2>Les règles fondamentales</h2>
  </div>
  <div class="card card-accent" data-reveal><ul>{regles}</ul></div>
  <div class="text-center mt-5"><a class="btn btn-primary" href="../outils/index.html#penetration">Tester avec le simulateur de pénétration</a></div>
</div></section>

<section class="section"><div class="wrap">
  <div class="section-head" data-reveal><div class="eyebrow">Convention communautaire</div><h2>Les six tiers</h2></div>
  <div class="grid" style="grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:var(--sp-4)">{conv}</div>
</div></section>

<section class="section"><div class="wrap">
  <div class="section-head" data-reveal>
    <div class="eyebrow">Nouveautés Aurora</div>
    <h2>Les 5 munitions de la Saison 12</h2>
    <p class="lead">Attention : la plupart des guides n'en annoncent que deux. Il y en a bien <strong>cinq</strong>.</p>
  </div>
  <div class="table-wrap" data-reveal><table class="df">
    <thead><tr><th>Munition</th><th>Type</th><th class="num">Niveau</th><th class="num">× Dégâts</th><th class="num">× Pénétration</th></tr></thead>
    <tbody>{s12_rows}</tbody></table></div>
  <div class="alert alert-orange mt-4" data-reveal><span class="ico" aria-hidden="true">💡</span>
  <div><strong>La 9x19 7N30 n'est pas une amélioration gratuite.</strong> Elle atteint le niveau 5 de pénétration
  mais coûte 10 % de dégâts, 15 % de multiplicateur de pénétration d'armure et davantage de recul.</div></div>
</div></section>

<section class="section"><div class="wrap">
  <div class="section-head" data-reveal><div class="eyebrow">Référence complète</div><h2>Tous les calibres</h2></div>
  {cal_blocks}
</div></section>

<section class="section-sm"><div class="wrap">
  <figure class="img-frame mb-5" data-reveal><img src="../../assets/images/weapons/armurerie_etabli_01.jpg" alt="Établi d'armurier vu de dessus avec fusil démonté et accessoires alignés" loading="lazy" decoding="async"><figcaption>Le choix de la munition pèse plus lourd que n'importe quel accessoire (illustration générée par IA, pas une capture du jeu)</figcaption></figure>
</div></section>

<section class="section" id="matrice"><div class="wrap">
  <div class="section-head" data-reveal>
    <div class="eyebrow">La table de référence</div><h2>{esc(MX['titre'])}</h2>
    <p class="lead">{esc(MX['lecture'])}</p>
  </div>
  <div class="table-wrap" data-reveal><table class="df" style="min-width:720px">
    <thead><tr><th style="text-align:left">Munition \\ Armure</th>{mx_head}</tr></thead>
    <tbody>{mx_rows}</tbody>
  </table></div>
  <div class="grid g-2 gap-4 mt-5">
    <div class="alert alert-orange" data-reveal><span class="ico" aria-hidden="true">⚠</span>
    <div class="small">{esc(MX['nuance_niveau_6'])}</div></div>
    <div class="alert alert-blue" data-reveal><span class="ico" aria-hidden="true">∑</span>
    <div class="small">{esc(MX['exemple_chiffre'])}</div></div>
  </div>
</div></section>

<section class="section" id="prix"><div class="wrap">
  <div class="section-head" data-reveal>
    <div class="eyebrow">Budget</div><h2>Prix par calibre</h2>
    <p class="lead">L'écart entre une munition niveau 3 et une niveau 5 est d'un facteur dix. C'est la décision
    économique la plus structurante de chaque raid.</p>
  </div>
  <div class="grid g-2 gap-4">{prix_blocks}</div>
  <figure class="img-frame mt-6" data-reveal>
    <img src="../../assets/images/ammo/munitions_tiers_01.jpg" alt="Cartouches de calibres différents alignées par ordre croissant de pénétration" loading="lazy" decoding="async">
    <figcaption>D'un palier de pénétration à l'autre, le prix est multiplié par dix (illustration générée par IA, pas une capture du jeu)</figcaption>
  </figure>
</div></section>

<section class="section" id="casques"><div class="wrap">
  <div class="section-head" data-reveal>
    <div class="eyebrow">Protection &amp; audition</div><h2>Casques : le vrai arbitrage</h2>
    <p class="lead">{esc(AR['arbitrage'])}</p>
  </div>
  <div class="alert alert-red mb-5" data-reveal><span class="ico" aria-hidden="true">⚠</span>
  <div class="small">{esc(AR['regle_hitbox'])}</div></div>
  <div class="table-wrap" data-reveal><table class="df" style="min-width:820px">
    <thead><tr><th class="sortable">Casque</th><th class="num">Niv.</th><th class="num">Audition</th><th>Contrepartie</th><th>Verdict</th></tr></thead>
    <tbody>{casques}</tbody>
  </table></div>
  <div class="grid g-2 gap-4 mt-5">
    <div class="card card-accent-green" data-reveal><h3 class="card-title" style="font-size:1rem">Boosters de perception</h3>
      <p class="small muted">{esc(AR['note_perception'])}</p></div>
    <div class="card card-accent-blue" data-reveal><h3 class="card-title" style="font-size:1rem">Bourdonnement d'oreilles</h3>
      <p class="small muted">{esc(AR['ear_ringing'])}</p></div>
  </div>
</div></section>

<section class="section"><div class="wrap wrap-narrow">
  <div class="section-head" data-reveal><div class="eyebrow">L'autre moitié de l'équation</div><h2>Armures</h2></div>
  <div class="card" data-reveal>
    <p class="small mb-3"><strong>Types :</strong> {esc(', '.join(A['armures']['types']))} —
    <strong>Niveaux :</strong> {esc(', '.join(map(str, A['armures']['niveaux'])))}</p>
    <ul class="small">{arm_regles}</ul>
  </div>
</div></section>
"""

AI = "(illustration générée par IA, pas une capture du jeu)"
M12 = A["munitions_s12"]
_m12 = "".join(f"""<article class="card card-accent-{m['accent']}" data-reveal data-delay="{i*60}">
    <div class="flex-between mb-2">
      <h3 class="card-title mono" style="font-size:1rem;margin:0">{esc(m['nom'])}</h3>
      <span class="badge badge-{'red' if m['pen']=='Niveau 5' else 'gold'}">{esc(m['pen'])}</span></div>
    <div class="hud tiny muted mb-2">{esc(m['type'])} · dégâts {esc(m['deg'])} · pénétration d'armure {esc(m['ap'])}</div>
    <p class="small">{esc(m['effet'])}</p>
    <p class="small txt-{m['accent'] if m['accent'] in ('green','orange','blue','red') else 'gold'}" style="margin:.5rem 0 0">{esc(m['verdict'])}</p>
  </article>""" for i, m in enumerate(M12["lignes"]))

mun_s12 = f"""
<section class="section" id="munitions-s12"><div class="wrap">
  <div class="section-head" data-reveal>
    <div class="eyebrow">Saison 12 · Aurora</div><h2>{esc(M12['titre'])}</h2>
    <p class="lead">{esc(M12['principe'])}</p>
  </div>
  <div class="grid g-2 gap-4 mb-4">{_m12}</div>
  <div class="grid g-2 gap-4">
    <figure class="img-frame" data-reveal>
      <img src="../../assets/images/ammo/ammo_detonant_01.jpg" alt="Mallette mousse contenant deux rangées de cartouches subsoniques à pointe polymère" loading="lazy" decoding="async">
      <figcaption>Les .300BLK n'explosent pas à chaque impact : il faut enchaîner les touches en moins de trois secondes {AI}</figcaption>
    </figure>
    <figure class="img-frame" data-reveal data-delay="80">
      <img src="../../assets/images/ammo/ammo_cinder_01.jpg" alt="Rangée de cartouches à pointe orange sur un établi en acier sombre" loading="lazy" decoding="async">
      <figcaption>La CINDER brûle la cible plusieurs secondes, au prix d'un recul accru {AI}</figcaption>
    </figure>
  </div>
  <div class="grid g-2 gap-4 mt-4">
    <div class="alert alert-blue" data-reveal><span class="ico" aria-hidden="true">i</span>
    <div class="small">{esc(M12['note_calibre'])}</div></div>
    <div class="alert alert-red" data-reveal><span class="ico" aria-hidden="true">!</span>
    <div class="small"><strong>Nouveau&nbsp;:</strong> {esc(M12['mecanique_nouvelle'])}</div></div>
  </div>
  <figure class="img-frame mt-4" data-reveal>
    <img src="../../assets/images/misc/penetration_gel_01.jpg" alt="Trois blocs de gélatine balistique alignés sur un rail d'essai en acier" loading="lazy" decoding="async">
    <figcaption>Une balle peut désormais traverser plusieurs cibles alignées {AI}</figcaption>
  </figure>
  <p class="small muted mt-3">{esc(M12['source'])}</p>
</div></section>
"""
html_mun = (head("Munitions & pénétration", "Guide complet des munitions de Delta Force : niveaux de pénétration 1 à 6, "
                 "tous les calibres, prix, et les 5 nouvelles munitions de la Saison Aurora (.300BLK TIV/TTV, CINDER, 7N30, SPALL).",
                 depth=D, canonical="pages/armurerie/munitions.html",
                 image="assets/images/weapons/armurerie_an94_01.jpg")
            + navbar(D) + '<main id="main">' + mun_body + mun_s12 + "</main>" + footer(D) + scripts(D))
print(write("pages/armurerie/munitions.html", html_mun))


# =========================================================== BUILDS
rows = "".join(f"""<tr data-tags="{esc(b.get('mode','').lower())}"
    data-search="{esc(b.get('arme',''))} {esc(b.get('role',''))} {esc(b.get('mode',''))}">
    <td><strong>{esc(b.get('arme','—'))}</strong> {'<span class="badge badge-new">S12</span>' if b.get('badge') else ''}</td>
    <td><span class="badge {'badge-green' if b.get('mode')=='Operations' else 'badge-blue'}">{esc(b.get('mode','—'))}</span></td>
    <td class="small">{esc(b.get('role','—'))}</td>
    <td><div class="codebox"><code>{esc(b['code'])}</code>
      <button class="copy-btn" data-copy="{esc(b['code'])}">COPIER</button></div></td>
  </tr>""" for b in B["builds"])

pick = "".join(f'<tr><td><strong>{esc(p["arme"])}</strong></td><td class="num">{esc(p["taux"])}</td>'
               f'<td><span class="tier tier-{esc(p["tier"])}" style="width:1.6rem;height:1.6rem;font-size:.78rem">{esc(p["tier"])}</span></td></tr>'
               for p in B["meta_operations"]["pick_rates"])

loadouts = "".join(f"""<div class="card card-accent-blue" data-reveal>
    <div class="flex items-center justify-between gap-2 mb-2">
      <h3 class="card-title" style="font-size:1rem">{esc(l['nom'])}</h3>
      <span class="badge badge-grey">{esc(l['cout'])}</span>
    </div>
    <ul class="small muted mb-3">{''.join(f'<li>{esc(x)}</li>' for x in l['contenu'])}</ul>
    <p class="small"><strong class="txt-green">Objectif :</strong> {esc(l['objectif'])}</p>
  </div>""" for l in B["loadouts_types"])

b_body = f"""
{page_hero("Import direct", "Codes de <span class='grad-text'>build</span>",
           f"{len(B['builds'])} configurations vérifiées, copiables en un clic et importables directement dans le jeu.",
           "assets/images/weapons/armurerie_an94_01.jpg", D)}

<section class="section-sm"><div class="wrap">
  {crumbs([("Armurerie", "pages/armurerie/index.html"), ("Codes de build", None)], D)}
  <figure class="img-frame mb-5" data-reveal>
    <img src="../../assets/images/weapons/builds_rack_01.jpg" alt="Râtelier mural d'armurerie portant six fusils aux configurations différentes" loading="lazy" decoding="async">
    <figcaption>Un code de build n'est qu'un point de départ : les valeurs diffèrent entre Operations et Warfare. (illustration générée par IA, pas une capture du jeu)</figcaption>
  </figure>
  <div class="mb-4" style="max-width:560px">{audio_briefing("builds_briefing_01.mp3", "Codes de build", "", D)}</div>
  <div class="grid g-2 gap-5">
    <div class="hud-panel" data-reveal>
      <div class="hud-head">Comment importer</div>
      <p class="small">{esc(B['_meta']['comment_importer'])}</p>
    </div>
    <div class="alert" data-reveal><span class="ico" aria-hidden="true">⚠</span>
      <div>{esc(B['_meta']['avertissement'])}</div></div>
  </div>
</div></section>

<section class="section-sm"><div class="wrap">
  <div class="hud-panel mb-4" data-filter-group data-filter-target="#builds-table tbody tr"
       data-filter-input="#b-search" data-filter-count="#b-count" data-reveal>
    <div class="flex wrapf items-center justify-between gap-4">
      <div class="chips">
        <button class="chip active" data-val="all">Tous</button>
        <button class="chip" data-val="operations">Operations</button>
        <button class="chip" data-val="warfare">Warfare</button>
      </div>
      <div class="field" style="min-width:230px">
        <label for="b-search">Recherche</label>
        <input class="input" id="b-search" type="search" placeholder="Arme, rôle…">
      </div>
    </div>
    <p class="tiny muted mt-3"><span id="b-count">{len(B['builds'])}</span> build(s) affiché(s).</p>
  </div>
  <div class="table-wrap"><table class="df" id="builds-table" style="min-width:860px">
    <thead><tr><th class="sortable">Arme</th><th class="sortable">Mode</th><th class="sortable">Rôle</th><th>Code</th></tr></thead>
    <tbody>{rows}</tbody></table></div>
</div></section>

<section class="section"><div class="wrap">
  <div class="grid g-2 gap-6">
    <div>
      <div class="section-head" data-reveal><div class="eyebrow">Méta observé</div><h2>Taux de sélection</h2></div>
      <div class="table-wrap" data-reveal><table class="df" style="min-width:0">
        <thead><tr><th>Arme</th><th class="num">Pick rate</th><th>Tier</th></tr></thead>
        <tbody>{pick}</tbody></table></div>
    </div>
    <div>
      <div class="section-head" data-reveal><div class="eyebrow">Prêt à l'emploi</div><h2>Loadouts types</h2></div>
      <div class="grid gap-3">{loadouts}</div>
    </div>
  </div>
</div></section>
"""
html_b = (head("Codes de build copiables", f"{len(B['builds'])} codes de build Delta Force vérifiés et copiables "
               "en un clic : AUG, AWM, AN-94, M4A1, CI-19, SMG-45 et plus. Operations et Warfare.",
               depth=D, canonical="pages/armurerie/builds.html",
               image="assets/images/weapons/armurerie_an94_01.jpg")
          + navbar(D) + '<main id="main">' + b_body + "</main>" + footer(D) + scripts(D))
print(write("pages/armurerie/builds.html", html_b))


# ====================================================== GUNSMITH
GS = load("gunsmith")

LM = GS["le_malentendu"]
st_rows = "".join(f"""<tr>
    <td><strong class="txt-green">{esc(s['nom'])}</strong></td>
    <td class="small">{esc(s['controle'])}</td>
    <td class="small txt-red">{esc(s['ne_fait_pas'])}</td>
    <td class="small muted">{esc(s['modifie_par'])}</td>
    <td class="small muted">{esc(s['compte_pour'])}</td>
  </tr>""" for s in GS["statistiques"])

CAL = GS["calibration"]
cal_rules = "".join(f"<li>{esc(x)}</li>" for x in CAL["regles"])

etapes = "".join(f"""<article class="card card-accent-orange" data-reveal data-delay="{i*70}">
    <div class="hud tiny txt-orange mb-2">ÉTAPE {e['n']:02d}</div>
    <h3 class="card-title" style="font-size:1rem">{esc(e['titre'])}</h3>
    <p class="small muted">{esc(e['detail'])}</p>
  </article>""" for i, e in enumerate(GS["methode_build"]["etapes"]))

pieges = "".join(f"""<div class="card card-accent-red" data-reveal data-delay="{i*50}">
    <div class="hud tiny txt-red mb-2">PIÈGE {i+1:02d}</div>
    <h4 class="card-title" style="font-size:.95rem">{esc(p['titre'])}</h4>
    <p class="small muted">{esc(p['detail'])}</p>
  </div>""" for i, p in enumerate(GS["pieges"]))

prof_rows = "".join(f"""<tr>
    <td><strong>{esc(p['arme'])}</strong></td>
    <td class="small txt-green mono">{esc(p['priorite'])}</td>
    <td class="small muted">{esc(p['note'])}</td>
  </tr>""" for p in GS["profils"])

AS = GS["astuce_souffle"]

gs_body = f"""
{page_hero("Atelier", "Comprendre le <span class='grad-text'>Gunsmith</span>",
           "Contrôle, Maniabilité, Stabilité, Précision : quatre mots que presque tout le monde "
           "interprète de travers. Voici ce que chaque statistique fait réellement — et comment "
           "construire une arme à partir de son métier plutôt que de ses chiffres.",
           "assets/images/heroes/gunsmith_hero_01.jpg", D)}

<section class="section-sm"><div class="wrap">
  {crumbs([("Armurerie", "index.html"), ("Gunsmith", None)], D)}
  <div class="mb-4" style="max-width:560px">{audio_briefing("gunsmith_briefing_01.mp3", "Gunsmith", "", D)}</div>
  <div class="alert alert-red" data-reveal><span class="ico" aria-hidden="true">⚠</span>
  <div class="small"><strong>{esc(LM['titre'])}</strong><br>{esc(LM['contenu'])}</div></div>
  <div class="alert alert-orange mt-3" data-reveal><span class="ico" aria-hidden="true">!</span>
  <div class="small">{esc(LM['corollaire'])}</div></div>
</div></section>

<section class="section" id="statistiques"><div class="wrap">
  <div class="section-head" data-reveal>
    <div class="eyebrow">Les {len(GS['statistiques'])} statistiques</div><h2>Ce que chaque chiffre fait vraiment</h2>
    <p class="lead">La colonne rouge est la plus utile : elle liste ce que la statistique ne fait PAS, c'est-à-dire l'erreur que tout le monde commet.</p>
  </div>
  <div class="table-wrap" data-reveal><table class="df" style="min-width:980px">
    <thead><tr><th>Statistique</th><th>Ce qu'elle gouverne</th><th>Ce qu'elle ne fait pas</th><th>Modifiée par</th><th>Compte pour</th></tr></thead>
    <tbody>{st_rows}</tbody>
  </table></div>
  <figure class="img-frame mt-6" data-reveal>
    <img src="../../assets/images/weapons/armurerie_recul_01.jpg" alt="Vue en enfilade d'un fusil au stand de tir, départ de coup et douille éjectée" loading="lazy" decoding="async">
    <figcaption>Un chargeur entier sur un mur, sans corriger : la seule mesure fiable de votre recul (illustration générée par IA, pas une capture du jeu)</figcaption>
  </figure>
</div></section>

<section class="section" id="calibration"><div class="wrap">
  <div class="grid g-2 gap-6">
    <div>
      <div class="section-head" data-reveal><div class="eyebrow">{esc(CAL['ou'])}</div><h2>{esc(CAL['titre'])}</h2>
        <p class="lead">{esc(CAL['principe'])}</p></div>
      <div class="card card-accent-gold" data-reveal><ul class="small">{cal_rules}</ul></div>
    </div>
    <div>
      <figure class="img-frame" data-reveal>
        <img src="../../assets/images/weapons/gunsmith_calibration_01.jpg" alt="Gros plan macro sur un tournevis dynamométrique réglant un rail de garde-main" loading="lazy" decoding="async">
        <figcaption>Chaque curseur est un troc, jamais un bonus (illustration générée par IA, pas une capture du jeu)</figcaption>
      </figure>
      <div class="card card-accent-blue mt-4" data-reveal>
        <h3 class="card-title" style="font-size:1rem">{esc(AS['titre'])}</h3>
        <p class="small">{esc(AS['contenu'])}</p>
      </div>
    </div>
  </div>
</div></section>

<section class="section" id="methode"><div class="wrap">
  <div class="section-head" data-reveal><div class="eyebrow">Méthode</div><h2>{esc(GS['methode_build']['titre'])}</h2></div>
  <div class="grid g-auto-md gap-4">{etapes}</div>
</div></section>

<section class="section" id="profils"><div class="wrap">
  <div class="section-head" data-reveal>
    <div class="eyebrow">Par famille</div><h2>Quelle priorité pour quelle arme</h2>
    <p class="lead">Une arme à un coup et une arme d'arrosage ne se construisent pas du tout de la même façon.</p>
  </div>
  <div class="table-wrap" data-reveal><table class="df" style="min-width:780px">
    <thead><tr><th>Famille</th><th>Ordre de priorité</th><th>Note</th></tr></thead>
    <tbody>{prof_rows}</tbody>
  </table></div>
</div></section>

<section class="section" id="pieges"><div class="wrap">
  <div class="section-head" data-reveal><div class="eyebrow">{len(GS['pieges'])} pièges</div><h2>Ce qui fait rater un build</h2></div>
  <div class="grid g-auto-md gap-4">{pieges}</div>
</div></section>

<section class="section-sm"><div class="wrap">
  <div class="grid g-3 gap-4">
    <a class="card card-accent" href="builds.html" data-reveal><h3 class="card-title" style="font-size:1rem">Codes de build</h3>
      <p class="small muted">{len(B['builds'])} configurations prêtes à importer.</p></a>
    <a class="card card-accent" href="munitions.html" data-reveal data-delay="80"><h3 class="card-title" style="font-size:1rem">Munitions &amp; pénétration</h3>
      <p class="small muted">Pourquoi la pénétration d'armure n'est pas le niveau de munition.</p></a>
    <a class="card card-accent" href="../outils/index.html" data-reveal data-delay="160"><h3 class="card-title" style="font-size:1rem">Calculateurs</h3>
      <p class="small muted">Temps d'élimination et pénétration, en direct.</p></a>
  </div>
</div></section>
"""

html_gs = (head("Gunsmith — Contrôle, Stabilité et calibration expliqués",
                "Comprendre le Gunsmith de Delta Force : ce que gouvernent réellement Contrôle, Maniabilité, "
                "Stabilité et Précision, pourquoi le recul n'est pas la Stabilité, comment calibrer gratuitement "
                "et quelle priorité adopter selon la famille d'arme.",
                depth=D, canonical="pages/armurerie/gunsmith.html",
                image="assets/images/heroes/gunsmith_hero_01.jpg")
           + navbar(D) + '<main id="main">' + gs_body + "</main>" + footer(D) + scripts(D))
print(write("pages/armurerie/gunsmith.html", html_gs))
