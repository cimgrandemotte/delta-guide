#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_cartes.py — Cartes interactives (Leaflet) + Havoc Warfare + Black Hawk Down."""

from site_common import (head, navbar, footer, scripts, write, esc,
                         load, crumbs, page_hero, audio_briefing)

MP = load("maps")
TP = [m for m in MP["operations"] if m["id"] == "tide-prison"][0]
TPE, TPC, TPX = TP["evasion_cellule"], TP["cartes_acces"], TP["extractions"]
tp_puz = "".join(f"""<article class="card card-accent-orange" data-reveal data-delay="{i*60}">
    <div class="hud tiny txt-orange mb-2">MÉCANISME {i+1:02d}</div>
    <h4 class="card-title" style="font-size:.98rem">{esc(p['nom'])}</h4>
    <p class="small muted"><strong>Indice :</strong> {esc(p['indice'])}</p>
    <p class="small txt-green">{esc(p['geste'])}</p>
  </article>""" for i, p in enumerate(TPE["puzzles"]))
tp_tips = "".join(f"<li>{esc(x)}</li>" for x in TPE["conseils"])
tp_cards = "".join(f"""<tr><td><strong>{esc(n['niveau'])}</strong></td><td class="small">{esc(n['usage'])}</td>
    <td class="mono small txt-blue">{esc(n['durabilite'])}</td><td class="small muted">{esc(n['ou'])}</td></tr>"""
    for n in TPC["niveaux"])
_rk = {"Faible": "green", "Moyen": "orange", "Élevé": "red"}
tp_ext = "".join(f"""<article class="card card-accent-{_rk.get(x['risque'],'blue')}" data-reveal data-delay="{i*70}">
    <div class="flex-between mb-2"><h4 class="card-title" style="font-size:1rem;margin:0">{esc(x['nom'])}</h4>
      <span class="badge badge-{'red' if x['risque']=='Élevé' else ('green' if x['risque']=='Faible' else 'gold')}">Risque {esc(x['risque'].lower())}</span></div>
    <div class="hud tiny muted mb-2">{esc(x['cout'])}</div>
    <p class="small">{esc(x['detail'])}</p>
    <p class="small txt-green"><strong>Conseil :</strong> {esc(x['conseil'])}</p>
  </article>""" for i, x in enumerate(TPX["sorties"]))

VE = load("vehicles")
BH = load("bhd")
TL = load("tier_list")
D = 2

LEAFLET_HEAD = ("""<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
  integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin="">""")
LEAFLET_JS = ("""<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"
  integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>
<script src="../../assets/js/maps.js"></script>""")

# =========================================================== CARTES
tabs = "".join(f'<button class="{"active" if i==0 else ""}" data-tab="{esc(m["id"])}" role="tab">{esc(m["nom"])}</button>'
               for i, m in enumerate(MP["operations"]))

panels = ""
for i, m in enumerate(MP["operations"]):
    zones = "".join(f'<span class="chip">{esc(z)}</span>' for z in m.get("zones_cles", []))
    routes = "".join(f"""<div class="mb-2"><strong class="txt-green">{esc(r['nom'])}</strong>
        <p class="small muted">{esc(r['desc'])}</p></div>""" for r in m.get("routes", []))
    astuces = "".join(f"<li>{esc(a)}</li>" for a in m.get("astuces", []))

    rework = ""
    if m.get("rework_s12"):
        rw = m["rework_s12"]
        fa = rw.get("factions", {})
        fac = ""
        if fa:
            fac = f"""<div class="card card-accent-orange mt-3">
              <h4 class="card-title" style="font-size:.98rem">Système de factions <span class="badge badge-new">NOUVEAU S12</span></h4>
              <p class="small mb-2">{esc(fa.get('mecanique',''))}</p>
              <div class="grid g-2 gap-3 mb-2">
                <div class="hud-panel"><div class="hud-head">Ahsarah Guard</div><p class="small">{esc(fa.get('ahsarah',''))}</p></div>
                <div class="hud-panel"><div class="hud-head" style="color:var(--df-orange)">HAAVK Corp</div><p class="small">{esc(fa.get('haavk',''))}</p></div>
              </div>
              <p class="small"><strong class="txt-green">Perk haut badge :</strong> {esc(fa.get('perk_haut_badge',''))}</p>
              <div class="alert alert-red mt-2"><span class="ico">⚠</span><div>{esc(fa.get('danger',''))}</div></div>
              <p class="tiny muted mt-2">{esc(fa.get('coordonnees',''))}</p>
            </div>"""
        rework = f"""<div class="card card-accent-orange mb-4">
          <h3 class="card-title" style="font-size:1.05rem">Refonte Saison 12 <span class="badge badge-new">NOUVEAU S12</span></h3>
          <ul class="small muted">
            <li><strong>Babel :</strong> {esc(rw.get('babel',''))}</li>
            <li><strong>Control room :</strong> {esc(rw.get('control_room',''))}</li>
            <li><strong>Passages :</strong> {esc(rw.get('nouveaux_passages',''))}</li>
          </ul>
          {fac}
        </div>"""

    supercrit = ""
    if m.get("supercritical"):
        sc = m["supercritical"]
        supercrit = f"""<div class="alert alert-red mb-4"><span class="ico">🔒</span><div>
          <strong>AZ3 Supercritical — {esc(sc['statut'])}.</strong> Ouverture le <strong>{esc(sc['date'])}</strong>.
          Prérequis : {esc(sc['prerequis'])}. {esc(sc['note'])}</div></div>"""

    img = {"brakkesh": "assets/images/maps/cartes_brakkesh_01.jpg",
           "zero-dam": "assets/images/maps/cartes_zerodam_01.jpg",
           "layali-grove": "assets/images/maps/cartes_layaligrove_01.jpg",
           "space-city": "assets/images/maps/cartes_spacecity_01.jpg",
           "tide-prison": "assets/images/maps/cartes_tideprison_01.jpg",
           "az3": "assets/images/maps/cartes_az3_01.jpg"}.get(m["id"])
    img_html = (f'<figure class="img-frame mb-4"><img src="../../{img}" alt="{esc(m["nom"])}" loading="lazy" decoding="async">'
                f'<figcaption>Illustration d\'ambiance — {esc(m["nom"])} (image générée par IA, pas une capture du jeu)</figcaption></figure>') if img else ""

    panels += f"""<div class="tabpanel {'active' if i==0 else ''}" data-panel="{esc(m['id'])}" id="{esc(m['id'])}">
      <div class="grid" style="grid-template-columns:1.25fr .75fr;gap:var(--sp-5)">
        <div>
          <div class="map-shell">
            <div class="leaflet-map" data-map="{esc(m['id'])}" role="application"
                 aria-label="Carte interactive de {esc(m['nom'])}"></div>
            <div class="map-legend"></div>
          </div>
          <p class="tiny muted mt-2">Plan schématique à visée pédagogique : les marqueurs situent les zones décrites
          dans les guides, ils ne sont pas extraits du jeu. Pour des coordonnées exactes, consultez
          <a href="https://deltaforce.th.gl/" target="_blank" rel="noopener nofollow">deltaforce.th.gl</a>.</p>
        </div>
        <div>
          <div class="flex wrapf gap-2 mb-3">
            <span class="badge badge-red">{esc(m.get('difficulte','—'))}</span>
            {f'<span class="badge badge-new">{esc(m["badge"])}</span>' if m.get('badge') else ''}
            {f'<span class="badge badge-blue">{m["localisations_referencees"]} marqueurs référencés</span>' if m.get('localisations_referencees') else ''}
            {f'<span class="badge badge-gold">{m["keycards"]} keycards</span>' if m.get('keycards') else ''}
          </div>
          <p class="small mb-3">{esc(m.get('resume',''))}</p>
          <div class="hud-panel mb-3">
            <div class="hud-head">Fiche rapide</div>
            <p class="small mb-1"><strong class="txt-red">Boss :</strong> {esc(m.get('boss','Aucun'))}</p>
            <p class="small mb-1"><strong class="txt-orange">Porte à code :</strong> {esc(m.get('porte_a_code','—'))}</p>
            <p class="small mb-1"><strong class="txt-blue">Disponibilité :</strong> {esc(m.get('disponibilite','—'))}</p>
            {f'<p class="small"><strong class="txt-gold">Coût d\'entrée :</strong> {esc(m["cout_entree"])}</p>' if m.get('cout_entree') else ''}
          </div>
          {f'<div class="mb-3"><div class="hud-head">Zones clés</div><div class="chips">{zones}</div></div>' if zones else ''}
        </div>
      </div>
      <div class="mt-5">
        {img_html}
        {supercrit}
        {rework}
        <div class="grid g-2 gap-5">
          {f'<div><div class="hud-head">Routes de loot</div>{routes}</div>' if routes else ''}
          {f'<div><div class="hud-head">Astuces</div><ul class="small muted">{astuces}</ul></div>' if astuces else ''}
        </div>
        {f'<div class="alert alert-blue mt-4"><span class="ico">🔐</span><div><strong>Secret CRACKED.</strong> {esc(m["secret_cracked"])}</div></div>' if m.get('secret_cracked') else ''}
        {f'<div class="alert alert-green mt-4"><span class="ico">☢</span><div><strong>Décontamination.</strong> {esc(m["decontamination"])}</div></div>' if m.get('decontamination') else ''}
        {f'<div class="alert mt-4"><span class="ico">🎯</span><div><strong>Boucle de la carte.</strong> {esc(m["boucle"])}</div></div>' if m.get('boucle') else ''}
      </div>
    </div>"""

cat_leg = "".join(f'<span class="lg"><span class="dot" style="background:{c["couleur"]}"></span>{esc(c["libelle"])}</span>'
                  for c in MP["categories_marqueurs"])

body = f"""
{page_hero("Reconnaissance", "Cartes <span class='grad-text'>interactives</span>",
           f"Les six cartes d'extraction, avec {MP['_meta']['total_localisations_referencees']} localisations référencées "
           "par la communauté. Marqueurs filtrables : extractions, boss, keycards, loot et portes à code.",
           "assets/images/maps/cartes_brakkesh_01.jpg", D, badge="BRAKKESH 2.0")}

<section class="section-sm"><div class="wrap">
  {crumbs([("Cartes", None)], D)}
  <div class="mb-4" style="max-width:560px">{audio_briefing("cartes_briefing_01.mp3", "Reconnaissance", "", D)}</div>
  <figure class="img-frame mb-5" data-reveal>
    <img src="../../assets/images/maps/cartes_brakkesh_factions_01.jpg" alt="Deux points de contrôle de milices rivales dans une vieille ville dense" loading="lazy" decoding="async">
    <figcaption>Brakkesh 2.0 — la verticalité et les factions redéfinissent chaque rotation (illustration générée par IA, pas une capture du jeu)</figcaption>
  </figure>
  <div class="tabs" role="tablist" data-reveal>{tabs}</div>
  {panels}
</div></section>

<section class="section-sm"><div class="wrap">
  <div class="hud-panel" data-reveal>
    <div class="hud-head">Catégories de marqueurs</div>
    <div class="map-legend" style="border:0;padding:0">{cat_leg}</div>
  </div>
</div></section>

<section class="section" id="tide-prison"><div class="wrap">
  <div class="section-head" data-reveal>
    <div class="eyebrow">Dossier carte · difficulté {esc(TP.get("difficulte","Hard"))}</div>
    <h2>Tide Prison — sortir de sa cellule, puis sortir tout court</h2>
    <p class="lead">{esc(TPE["principe"])}</p>
  </div>

  <div class="grid g-2 gap-6 mb-6">
    <figure class="img-frame" data-reveal>
      <img src="../../assets/images/maps/cartes_tideprison_cellule_01.jpg" alt="Intérieur d'une cellule de prison barrée par une grille de faisceaux laser rouges" loading="lazy" decoding="async">
      <figcaption>Cinq mécanismes de sortie possibles, tirés au sort à chaque partie (illustration générée par IA, pas une capture du jeu)</figcaption>
    </figure>
    <figure class="img-frame" data-reveal data-delay="80">
      <img src="../../assets/images/maps/cartes_tideprison_quai_01.jpg" alt="Quai maritime battu par la houle au pied de tours de guet, à l'aube" loading="lazy" decoding="async">
      <figcaption>Le point fixe en mer : aucun prérequis, aucun couvert (illustration générée par IA, pas une capture du jeu)</figcaption>
    </figure>
  </div>

  <h3 class="mb-3">{esc(TPE["titre"])}</h3>
  <div class="grid g-auto-sm gap-4 mb-4">{tp_puz}</div>
  <div class="card card-accent-blue" data-reveal><ul class="small">{tp_tips}</ul></div>

  <div class="divider"></div>

  <div class="grid g-2 gap-6">
    <div>
      <h3 class="mb-2">{esc(TPC["titre"])}</h3>
      <div class="alert alert-orange mb-3" data-reveal><span class="ico" aria-hidden="true">!</span>
      <div class="small">{esc(TPC["avertissement"])}</div></div>
      <div class="table-wrap" data-reveal><table class="df">
        <thead><tr><th>Niveau</th><th>Ouvre</th><th>Durabilité</th><th>Où la trouver</th></tr></thead>
        <tbody>{tp_cards}</tbody></table></div>
      <p class="small muted mt-2">{esc(TPC["regle"])}</p>
    </div>
    <div>
      <h3 class="mb-2">{esc(TPX["titre"])}</h3>
      <div class="alert alert-red mb-3" data-reveal><span class="ico" aria-hidden="true">⚠</span>
      <div class="small">{esc(TPX["avertissement"])}</div></div>
      <div class="grid gap-3">{tp_ext}</div>
      <figure class="img-frame mt-4" data-reveal>
        <img src="../../assets/images/misc/extraction_helico_01.jpg" alt="Hélicoptère d'extraction en vol stationnaire au-dessus d'une zone balisée par de la fumée" loading="lazy" decoding="async">
        <figcaption>Choisir sa sortie avant de remplir son sac, jamais l'inverse (illustration générée par IA, pas une capture du jeu)</figcaption>
      </figure>
    </div>
  </div>

  <div class="alert alert-gold mt-6" data-reveal><span class="ico" aria-hidden="true">★</span>
  <div class="small">{esc(TP["note_boss"])}</div></div>
</div></section>

"""
_ZD = [m for m in MP["operations"] if m["id"] == "zero-dam"][0]
_SC = [m for m in MP["operations"] if m["id"] == "space-city"][0]
_zp, _ze, _sa = _ZD["priorite_butin"], _ZD["extractions_detail"], _SC["apparitions"]

_ordre = "".join(f"""<li class="check-row"><span class="num txt-gold mono">{i+1}</span>
    <span>{esc(x)}</span></li>""" for i, x in enumerate(_zp["ordre"]))
_exf = "".join(f"""<tr><td><strong>{esc(l['nom'])}</strong></td><td class="small txt-orange">{esc(l['condition'])}</td>
    <td class="small muted">{esc(l['note'])}</td></tr>""" for l in _ze["lignes"])
_vmap = {"Excellente": "green", "Bonne mais risquée": "gold", "Correcte": "blue", "Faible": "grey",
         "Faible sans carte": "grey", "Mauvaise": "red"}
_spw = "".join(f"""<article class="card" data-reveal data-delay="{i*50}">
    <div class="flex-between mb-2"><h4 class="card-title" style="font-size:.98rem;margin:0">{esc(s['lieu'])}</h4>
      <span class="badge badge-{_vmap.get(s['valeur'],'grey')}">{esc(s['valeur'])}</span></div>
    <p class="small muted" style="margin:0">{esc(s['detail'])}</p>
  </article>""" for i, s in enumerate(_sa["lignes"]))

routes_body = f"""
<section class="section" id="routes-butin"><div class="wrap">
  <div class="section-head" data-reveal>
    <div class="eyebrow">Zero Dam</div><h2>{esc(_zp['titre'])}</h2>
    <p class="lead">{esc(_zp['note'])}</p>
  </div>
  <div class="grid g-2 gap-6 mb-5">
    <div><ul class="checklist" data-reveal>{_ordre}</ul>
      <div class="alert alert-gold mt-3" data-reveal><span class="ico" aria-hidden="true">★</span>
      <div class="small">{esc(_zp['salles_premium'])}</div></div></div>
    <div>
      <h3 style="font-size:1.05rem">{esc(_ze['titre'])}</h3>
      <p class="small muted">{esc(_ze['avertissement'])}</p>
      <div class="table-wrap" data-reveal><table class="df">
        <thead><tr><th>Sortie</th><th>Condition</th><th>Remarque</th></tr></thead><tbody>{_exf}</tbody></table></div>
    </div>
  </div>
  <div class="divider"></div>
  <div class="section-head mt-5" data-reveal>
    <div class="eyebrow">Space City</div><h2>{esc(_sa['titre'])}</h2>
    <p class="lead">{esc(_sa['contenu'])}</p>
  </div>
  <div class="grid g-auto-md gap-4">{_spw}</div>
  <div class="alert alert-blue mt-4" data-reveal><span class="ico" aria-hidden="true">i</span>
  <div class="small">{esc(_sa['coeur'])}</div></div>
</div></section>
"""

html = (head("Cartes interactives", "Les 6 cartes d'extraction de Delta Force en interactif : Zero Dam, Layali Grove, "
             "Space City, Brakkesh 2.0, Tide Prison et AZ3. Extractions, boss, keycards, loot et portes à code.",
             depth=D, canonical="pages/cartes/index.html",
             image="assets/images/maps/cartes_brakkesh_01.jpg", extra_head=LEAFLET_HEAD)

        + navbar(D) + '<main id="main">' + body + routes_body + "</main>" + footer(D) + scripts(D, LEAFLET_JS))
print(write("pages/cartes/index.html", html))


# =========================================================== HAVOC WARFARE
eq = "".join(f"<li>{esc(x)}</li>" for x in VE["equilibrage_s12"])

veh_cards = "".join(f"""<article class="card" data-tags="tier-{esc(str(v.get('tier','')).lower())}"
    data-search="{esc(v['nom'])} {esc(v.get('categorie',''))} {esc(v.get('roles',''))}" data-reveal>
    <div class="flex items-start justify-between gap-2 mb-2">
      <div><div class="op-class">{esc(v.get('categorie','—'))}</div>
        <h3 class="op-name" style="font-size:1rem">{esc(v['nom'])}</h3></div>
      <span class="tier tier-{esc(str(v.get('tier','D'))[0])}">{esc(v.get('tier','—'))}</span>
    </div>
    <p class="tiny muted mb-2">{esc(v.get('places',''))}</p>
    <p class="small mb-2"><strong class="txt-green">Rôle :</strong> {esc(v.get('roles',''))}</p>
    {f'<ul class="small muted mb-2">{"".join(f"<li>+ {esc(x)}</li>" for x in v.get("forces",[]))}</ul>' if v.get('forces') else ''}
    {f'<ul class="small muted mb-2" style="color:var(--df-red)">{"".join(f"<li>− {esc(x)}</li>" for x in v.get("faiblesses",[]))}</ul>' if v.get('faiblesses') else ''}
    {f'<div class="alert alert-blue"><span class="ico">💡</span><div class="small">{"".join(f"<div>{esc(x)}</div>" for x in v.get("conseils",[]))}</div></div>' if v.get('conseils') else ''}
    {f'<p class="tiny txt-orange mt-2">⚑ {esc(v["note_s12"])}</p>' if v.get('note_s12') else ''}
  </article>""" for v in VE["vehicules"])

contre = "".join(f"<li>{esc(c)}</li>" for c in VE["contre_vehicules"])

warfare_maps = "".join(f"""<div class="card {'card-accent-orange' if w.get('badge') else 'card-accent-blue' if w.get('statut') != 'RETIRÉE EN S12' else 'card-accent-red'}" data-reveal>
    <div class="flex items-center justify-between gap-2 mb-2">
      <h3 class="card-title" style="font-size:1rem">{esc(w['nom'])}</h3>
      {f'<span class="badge badge-new">{esc(w["badge"])}</span>' if w.get('badge') else
       f'<span class="badge badge-red">{esc(w["statut"])}</span>' if w.get('statut') else
       f'<span class="badge badge-grey">{esc(w.get("type","—"))}</span>'}
    </div>
    <p class="small muted">{esc(w.get('resume',''))}</p>
    {f'<p class="small mt-2"><strong class="txt-blue">Événement Riptide :</strong> {esc(w["evenement_riptide"])}</p>' if w.get('evenement_riptide') else ''}
    {f'<ul class="small muted mt-2">{"".join(f"<li>{esc(x)}</li>" for x in w.get("specificites",[]))}</ul>' if w.get('specificites') else ''}
    {f'<p class="tiny txt-orange mt-2">⚑ Patch 12/11 : {esc("; ".join(w["patch_12_11"]))}</p>' if w.get('patch_12_11') else ''}
    {f'<p class="tiny muted mt-2">{esc(w["event"])}</p>' if w.get('event') else ''}
    {f'<p class="tiny muted mt-2">{esc(w["s12"])}</p>' if w.get('s12') else ''}
  </div>""" for w in MP["warfare"])

vt = TL["vehicules"]
vt_rows = "".join(f"""<div class="tier-row">
    <div class="tier-label" style="background:var(--tier-{k.lower()})">{k}</div>
    <div class="tier-drop">{''.join(f'<span class="tier-item">{esc(n)}</span>' for n in v)}</div>
  </div>""" for k, v in vt.items())

TA = VE.get("tactiques_avancees", {})
def _tacblock(key, cls, lab):
    return "".join(f"""<div class="card {cls}" data-reveal data-delay="{i*45}">
      <div class="hud tiny mb-2">{lab} {i+1:02d}</div>
      <h4 class="card-title" style="font-size:.95rem">{esc(t['nom'])}</h4>
      <p class="small muted">{esc(t['detail'])}</p></div>""" for i, t in enumerate(TA.get(key, [])))
tac_bl = _tacblock("blindes", "card-accent-orange", "BLINDÉ")
tac_av = _tacblock("antivehicule", "card-accent-red", "ANTI-VÉH.")
tac_sc = _tacblock("score_et_streaks", "card-accent-gold", "SCORE")
tac_if = _tacblock("infanterie", "card-accent-blue", "INFANTERIE")

w_body = f"""
{page_hero("Combat interarmes", "Havoc <span class='grad-text'>Warfare</span>",
           "32 contre 32, chars, hélicoptères et objectifs à prendre. Un mode où la coordination d'escouade "
           "pèse plus lourd que le gunskill individuel.",
           "assets/images/vehicles/warfare_tank_01.jpg", D, badge="ZENITH PORT S12")}

<section class="section-sm"><div class="wrap">
  {crumbs([("Havoc Warfare", None)], D)}
  <div class="mb-4" style="max-width:560px">{audio_briefing("warfare_briefing_01.mp3", "Havoc Warfare", "", D)}</div>
  <div class="alert alert-orange" data-reveal><span class="ico" aria-hidden="true">⚙</span>
  <div><strong>Équilibrage Saison 12 :</strong><ul class="small mt-2">{eq}</ul></div></div>
</div></section>

<section class="section" id="zenith-port"><div class="wrap">
  <div class="section-head" data-reveal><div class="eyebrow">Théâtres d'opération</div><h2>Les cartes Warfare</h2></div>
  <figure class="img-frame mb-5" data-reveal>
    <img src="../../assets/images/maps/cartes_zenithport_01.jpg" alt="Zenith Port sous assaut naval" loading="lazy" decoding="async">
    <figcaption>Zenith Port — nouvelle carte de la Saison Aurora (illustration générée par IA, pas une capture du jeu)</figcaption>
  </figure>
  <div class="grid g-auto-md">{warfare_maps}</div>
</div></section>

<section class="section" id="riptide"><div class="wrap">
  <figure class="img-frame mb-5" data-reveal><img src="../../assets/images/maps/cartes_zenith_riptide_01.jpg" alt="Vague Riptide submergeant les quais de Zenith Port" loading="lazy" decoding="async"><figcaption>Riptide — le barrage intercepté par la DCA génère les vagues qui noient les objectifs bas (illustration générée par IA, pas une capture du jeu)</figcaption></figure>
</div></section>

<section class="section" id="vehicules"><div class="wrap">
  <div class="section-head" data-reveal>
    <div class="eyebrow">{len(VE['vehicules'])} engins</div><h2>Véhicules</h2>
    <p class="lead">Un bon équipage de char vaut dix fantassins. Un mauvais pilote d'hélicoptère offre un kill streak à l'adversaire.</p>
  </div>
  <div class="hud-panel mb-5" data-filter-group data-filter-target="#veh-grid > article" data-filter-count="#v-count" data-reveal>
    <div class="chips">
      <button class="chip active" data-val="all">Tous</button>
      <button class="chip" data-val="tier-s">Tier S</button>
      <button class="chip" data-val="tier-a">Tier A</button>
      <button class="chip" data-val="tier-b">Tier B</button>
    </div>
    <p class="tiny muted mt-3"><span id="v-count">{len(VE['vehicules'])}</span> véhicule(s) affiché(s).</p>
  </div>
  <figure class="img-frame mb-5" data-reveal><img src="../../assets/images/vehicles/warfare_helico_01.jpg" alt="Hélicoptère d'attaque en virage serré" loading="lazy" decoding="async"><figcaption>Le pilote d'hélicoptère de transport touche désormais 120 points d'assistance (illustration générée par IA, pas une capture du jeu)</figcaption></figure>
  <div class="grid g-auto-md" id="veh-grid">{veh_cards}</div>
</div></section>

<section class="section"><div class="wrap">
  <div class="grid g-2 gap-6">
    <div>
      <div class="section-head" data-reveal><div class="eyebrow">Classement</div><h2>Tier list véhicules</h2></div>
      <div class="tierlist" data-reveal>{vt_rows}</div>
    </div>
    <div>
      <div class="section-head" data-reveal><div class="eyebrow">Riposte</div><h2>Contre-jeu anti-véhicule</h2></div>
      <div class="card card-accent-red" data-reveal><ul class="small">{contre}</ul></div>
    </div>
  </div>
</div></section>
<section class="section" id="tactiques-avancees"><div class="wrap">
  <div class="section-head" data-reveal>
    <div class="eyebrow">Niveau supérieur</div><h2>{esc(TA.get('titre',''))}</h2>
    <p class="lead">Vingt-quatre réflexes tirés des retours de joueurs expérimentés, classés par rôle.</p>
  </div>

  <h3 class="card-title mb-3" style="font-size:1.05rem">Piloter un blindé</h3>
  <div class="grid g-auto-sm gap-4 mb-5">{tac_bl}</div>

  <figure class="img-frame mb-6" data-reveal>
    <img src="../../assets/images/vehicles/warfare_hulldown_01.jpg" alt="Char en position défilement de coque, seule la tourelle dépasse d'un talus" loading="lazy" decoding="async">
    <figcaption>Position coque enterrée : seule la tourelle dépasse, la surface touchable est minimale (illustration générée par IA, pas une capture du jeu)</figcaption>
  </figure>

  <h3 class="card-title mb-3" style="font-size:1.05rem">Détruire un véhicule</h3>
  <div class="grid g-auto-sm gap-4 mb-5">{tac_av}</div>

  <h3 class="card-title mb-3" style="font-size:1.05rem">Score, frappes et rentabilité</h3>
  <div class="grid g-auto-sm gap-4 mb-5">{tac_sc}</div>

  <h3 class="card-title mb-3" style="font-size:1.05rem">À pied</h3>
  <div class="grid g-auto-sm gap-4">{tac_if}</div>
</div></section>
"""
html_w = (head("Havoc Warfare — véhicules & cartes", "Guide du mode Havoc Warfare 32v32 de Delta Force : "
               "tous les véhicules avec tier list, contre-jeu anti-blindé, cartes dont la nouvelle Zenith Port "
               "et son événement Riptide.",
               depth=D, canonical="pages/havoc-warfare/index.html",
               image="assets/images/vehicles/warfare_tank_01.jpg")
          + navbar(D) + '<main id="main">' + w_body + "</main>" + footer(D) + scripts(D))
print(write("pages/havoc-warfare/index.html", html_w))


# =========================================================== BLACK HAWK DOWN
pres = BH["presentation"]
pres_rows = "".join(f'<tr><td class="hud tiny muted">{esc(k.replace("_"," ").title())}</td><td>{esc(v)}</td></tr>'
                    for k, v in pres.items())
chaps = "".join(f"""<article class="card" data-reveal data-delay="{(i%3)*60}">
    <div class="flex items-center gap-3 mb-2">
      <span class="tier" style="background:var(--df-orange)">{c['numero']}</span>
      <h3 class="card-title" style="font-size:1.05rem;margin:0">{esc(c['titre'])}</h3>
    </div>
    <p class="small muted">{esc(c['resume'])}</p>
  </article>""" for i, c in enumerate(BH["chapitres"]))
conseils = "".join(f"<li>{esc(c)}</li>" for c in BH["conseils"])
liens = "".join(f"<li>{esc(l)}</li>" for l in BH["liens_univers"])

bh_body = f"""
{page_hero("Campagne coopérative", "Black Hawk <span class='grad-text'>Down</span>",
           "Sept chapitres, Mogadiscio 1993, Operation Gothic Serpent. "
           "Gratuite pour tous les joueurs depuis sa sortie — et la meilleure école de gunplay du jeu.",
           "assets/images/bhd/bhd_mogadiscio_01.jpg", D)}

<section class="section-sm"><div class="wrap">
  {crumbs([("Black Hawk Down", None)], D)}
  <figure class="img-frame mb-5" data-reveal>
    <img src="../../assets/images/misc/bhd_helico_ville_01.jpg" alt="Hélicoptère de transport militaire virant au-dessus d'une ville basse et poussiéreuse" loading="lazy" decoding="async">
    <figcaption>Black Hawk Down : une campagne coopérative, pas un mode compétitif. (illustration générée par IA, pas une capture du jeu)</figcaption>
  </figure>
  <figure class="img-frame mb-5" data-reveal><img src="../../assets/images/bhd/bhd_convoi_01.jpg" alt="Convoi blindé bloqué par des barricades en feu dans une rue étroite" loading="lazy" decoding="async"><figcaption>Le convoi immobilisé — la situation qui définit toute la campagne (illustration générée par IA, pas une capture du jeu)</figcaption></figure>
  <div class="mb-4" style="max-width:560px">{audio_briefing("bhd_briefing_01.mp3", "Black Hawk Down", "", D)}</div>
  <div class="grid g-2 gap-5">
    <div class="hud-panel" data-reveal>
      <div class="hud-head">Fiche</div>
      <div class="table-wrap" style="border:0"><table class="df" style="min-width:0"><tbody>{pres_rows}</tbody></table></div>
    </div>
    <div class="hud-panel" data-reveal>
      <div class="hud-head">Conseils de jeu</div>
      <ul class="small muted">{conseils}</ul>
    </div>
  </div>
</div></section>

<section class="section"><div class="wrap">
  <div class="section-head" data-reveal><div class="eyebrow">Déroulé</div><h2>Les 7 chapitres</h2></div>
  <div class="grid g-auto-md">{chaps}</div>
</div></section>

<section class="section"><div class="wrap wrap-narrow">
  <div class="card card-accent-blue" data-reveal>
    <h3 class="card-title">Liens avec l'univers</h3>
    <ul class="small muted">{liens}</ul>
  </div>
  <div class="alert mt-4" data-reveal><span class="ico" aria-hidden="true">🕊</span>
  <div>{esc(BH['disclaimer'])}</div></div>
</div></section>
"""
html_bh = (head("Black Hawk Down — la campagne", "Guide de la campagne coopérative Black Hawk Down de Delta Force : "
                "les 7 chapitres, conseils de jeu et contexte historique de la bataille de Mogadiscio (1993).",
                depth=D, canonical="pages/black-hawk-down/index.html",
                image="assets/images/bhd/bhd_mogadiscio_01.jpg")
           + navbar(D) + '<main id="main">' + bh_body + "</main>" + footer(D) + scripts(D))
print(write("pages/black-hawk-down/index.html", html_bh))
