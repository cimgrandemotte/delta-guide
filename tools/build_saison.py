#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_saison.py — Page Saison 12 Aurora + page News."""

from site_common import (head, navbar, footer, scripts, write, esc,
                         load, crumbs, page_hero, audio_briefing)

s = load("season12")
D = 2

# ------------------------------------------------------------- NOUVEAUTÉS
nouv = "".join(f"""<div class="card card-accent-orange" data-reveal data-delay="{(i%3)*60}">
    <span class="badge badge-new">NOUVEAU S12</span>
    <h3 class="card-title mt-2" style="font-size:1.02rem">{esc(n.get('titre','—'))}</h3>
    <p class="small muted">{esc(n.get('detail',''))}</p>
    {f'<p class="tiny mt-2"><span class="badge badge-grey">{esc(n["confiance"]).upper()}</span></p>' if n.get('confiance') and n['confiance'] != 'confirme' else ''}
  </div>""" for i, n in enumerate(s["nouveautes_majeures"]))

# ------------------------------------------------------------- PATCH 12/11
p12 = s["patch_12_novembre"]
p12_html = "".join(f"<li>{esc(c)}</li>" for c in p12.get("changements", []))

# ------------------------------------------------------------- ÉQUILIBRAGE ARMES
def arme_rows(lst):
    out = ""
    for a in lst:
        sens = a.get("sens", "")
        cls = "badge-green" if "buff" in sens.lower() else ("badge-red" if "nerf" in sens.lower() else "badge-grey")
        out += (f'<tr><td><strong>{esc(a.get("arme","—"))}</strong></td>'
                f'<td class="small">{esc(a.get("changement",""))}</td>'
                f'<td><span class="badge {cls}">{esc(sens or "ajustement").upper()}</span></td></tr>')
    return out

ea = s["equilibrage_armes"]
armes_tabs = ""
armes_panels = ""
for idx, (mode, lst) in enumerate(ea.items()):
    label = {"operations": "Operations", "warfare": "Warfare", "detonation": "Detonation"}.get(mode, mode.title())
    armes_tabs += f'<button class="{"active" if idx==0 else ""}" data-tab="arm-{mode}" role="tab">{label} ({len(lst)})</button>'
    warn = ('<div class="alert alert-red mb-4"><span class="ico">⚠</span><div>Ces changements sont '
            '<strong>exclusifs au mode Detonation</strong> et n\'affectent ni Operations ni Warfare.</div></div>'
            if mode == "detonation" else "")
    armes_panels += f"""<div class="tabpanel {'active' if idx==0 else ''}" data-panel="arm-{mode}">
      {warn}
      <div class="table-wrap"><table class="df">
        <thead><tr><th class="sortable">Arme</th><th>Changement</th><th class="sortable">Sens</th></tr></thead>
        <tbody>{arme_rows(lst)}</tbody></table></div>
    </div>"""

# ------------------------------------------------------------- ÉQUILIBRAGE OPÉRATEURS
ECH = s["echeances"]
_st = {"Dernier jour": "badge-red", "Échéance dépassée": "badge-grey", "En cours": "badge-green", "À préparer": "badge-new"}
ech_rows = "".join(f"""<tr>
    <td class="mono small"><strong>{esc(e['date'])}</strong></td>
    <td class="small">{esc(e['quoi'])}</td>
    <td><span class="badge {_st.get(e['statut'],'badge-grey')}">{esc(e['statut'])}</span></td>
  </tr>""" for e in ECH["items"])
EOD = s["equilibrage_operateurs_detail"]
_op = lambda L: "".join(f'<tr><td><strong>{esc(x["operateur"])}</strong></td><td class="small muted">{esc(x["changement"])}</td></tr>' for x in L)
eod_tm = _op(EOD["tous_modes"]); eod_dt = _op(EOD["detonation_seulement"])
EQC = s["equilibrage_chiffre"]
def _eq_table(items):
    return "".join(f"""<tr>
      <td><strong>{esc(x['arme'])}</strong></td>
      <td class="small">{esc(x['detail'])}</td>
      <td class="num"><span class="badge {'badge-green' if x['sens'].startswith('↑') else 'badge-red' if x['sens'].startswith('↓') else 'badge-grey'}">{esc(x['sens'])}</span></td>
    </tr>""" for x in items)
eqc_tm = _eq_table(EQC["tous_modes"])
eqc_op = _eq_table(EQC["operations"])
eqc_dt = _eq_table(EQC["detonation_seulement"])
VN = EQC["vehicule_neural"]
vn_items = "".join(f"<li class='mono small'>{esc(v)}</li>" for v in VN["valeurs"])

eo = s["equilibrage_operateurs"]
ops_blocks = ""
for mode, val in eo.items():
    if mode.startswith("_") or not isinstance(val, list):
        continue
    label = {"tous_modes": "Tous les modes", "operations": "Operations uniquement",
             "warfare": "Warfare uniquement", "detonation_uniquement": "Detonation UNIQUEMENT"}.get(mode, mode)
    danger = mode == "detonation_uniquement"
    rows = "".join(
        f'<tr><td><strong>{esc(c.get("operateur","—"))}</strong></td>'
        f'<td class="small">{esc(c.get("changement",""))}</td>'
        f'<td><span class="badge {"badge-green" if "buff" in str(c.get("sens","")).lower() else "badge-red" if "nerf" in str(c.get("sens","")).lower() else "badge-grey"}">{esc(c.get("sens","—")).upper()}</span></td></tr>'
        for c in val)
    ops_blocks += f"""<div class="mb-6" data-reveal>
      <h3 class="card-title flex items-center gap-2">
        {esc(label)} <span class="badge {'badge-red' if danger else 'badge-green'}">{len(val)}</span>
      </h3>
      {'<div class="alert alert-red mb-3"><span class="ico">⚠</span><div><strong>Ne transposez pas ces changements aux autres modes.</strong> C\'est l\'erreur de lecture la plus répandue sur les patch notes Aurora.</div></div>' if danger else ''}
      <div class="table-wrap"><table class="df">
        <thead><tr><th>Opérateur</th><th>Changement</th><th>Sens</th></tr></thead>
        <tbody>{rows}</tbody></table></div>
    </div>"""

note_eo = eo.get("_avertissement") or eo.get("avertissement") or ""

# ------------------------------------------------------------- VÉHICULES
veh = "".join(f"<li>{esc(v if isinstance(v,str) else v.get('changement',''))}</li>"
              for v in s["equilibrage_vehicules"])

# ------------------------------------------------------------- EVENTS
def fr(d):
    if not d or not isinstance(d, str) or "-" not in d:
        return esc(str(d or "—"))
    y, m, j = d.split("-")
    mois = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet",
            "août", "septembre", "octobre", "novembre", "décembre"]
    return f"{int(j)} {mois[int(m)-1]} {y}"

TODAY = "2026-11-19"
ev_rows = ""
for e in s["events"]:
    fin = e.get("fin", "")
    termine = bool(fin) and isinstance(fin, str) and fin < TODAY
    statut = ('<span class="badge badge-grey">TERMINÉ</span>' if termine
              else '<span class="badge badge-green">EN COURS</span>' if (e.get("debut", "") or "") <= TODAY
              else '<span class="badge badge-blue">À VENIR</span>')
    ev_rows += (f'<tr style="{"opacity:.5" if termine else ""}">'
                f'<td><strong>{esc(e.get("nom","—"))}</strong></td>'
                f'<td class="small">{esc(e.get("mode","—"))}</td>'
                f'<td class="small mono" data-sort="{esc(e.get("debut",""))}">{fr(e.get("debut"))} → {fr(fin)}</td>'
                f'<td class="small muted">{esc(e.get("recompenses",""))}</td>'
                f'<td>{statut}</td></tr>')

# ------------------------------------------------------------- SEASON PASS
sp = s["season_pass"]
sp_items = "".join(f"<li>{esc(x)}</li>" for x in sp.get("recompenses_majeures", []))
cosm = "".join(f"<li>{esc(x if isinstance(x,str) else x.get('nom',''))}</li>" for x in s.get("autres_cosmetiques", []))

# ------------------------------------------------------------- PRIORITÉS
prio = "".join(f"""<div class="tl-item">
    <div class="tl-date">Priorité {i+1}</div>
    <p>{esc(p if isinstance(p,str) else p.get('action',''))}</p>
  </div>""" for i, p in enumerate(s["priorites_joueur"]))

sa = s["saison"]
infos = "".join(f'<tr><td class="hud tiny muted">{esc(k.replace("_"," ").title())}</td><td>{esc(v) if not isinstance(v,list) else esc(", ".join(map(str,v)))}</td></tr>'
                for k, v in sa.items())

AZ = s.get("az3_supercritical", {})
ZP = s.get("zenith_port", {})
BF = s.get("brakkesh_factions", {})
AT = s.get("attachements_limites", {})

az_rows = "".join(f'<tr><td class="hud tiny muted">{esc(k)}</td><td>{esc(AZ.get(v,""))}</td></tr>' for k, v in [
    ("Fenêtre", "fenetre"), ("Niveau requis", "niveau_requis"),
    ("Coût d'entrée", "cout_entree"), ("Polaris Patrol", "polaris_patrol")])

RT = ZP.get("mecanique_riptide", {})
bf_steps = "".join(f"<li>{esc(x)}</li>" for x in BF.get("fonctionnement", []))
bf_tags = "".join(f'<span class="badge badge-gold">{esc(f)}</span> ' for f in BF.get("factions", []))
at_rows = "".join(f"""<tr>
    <td><strong>{esc(a['nom'])}</strong></td>
    <td class="mono num">{esc(a['controle'])}</td><td class="mono num">{esc(a['stabilite'])}</td>
    <td class="mono num">{esc(a['precision'])}</td><td class="mono num">{esc(a['maniabilite'])}</td>
    <td class="small muted">{esc(a['effet'])}</td>
  </tr>""" for a in AT.get("lignes", []))

body = f"""
{page_hero("Briefing saisonnier", "Saison 12 — <span class='grad-text'>Aurora</span>",
           "Déployée le <strong>10 novembre 2026 à 02:00 UTC</strong> sans interruption de service. "
           "Nouvelle opératrice, nouveau fusil, refonte de Brakkesh, carte Warfare inédite et cinq munitions.",
           "assets/images/season/saison_aurora_01.jpg", D, badge="NOUVEAU S12")}

<section class="section-sm"><div class="wrap">
  {crumbs([("Saison Aurora", None)], D)}
  <div class="grid g-2 gap-4 mb-5">
    <figure class="img-frame" data-reveal><img src="../../assets/images/operators/operateurs_martelo_01.jpg" alt="Martelo, nouvelle opératrice Assaut de la Saison Aurora" loading="lazy" decoding="async"><figcaption>Martelo — Ariete et Smoke Halo, la nouvelle opératrice Assaut (illustration générée par IA, pas une capture du jeu)</figcaption></figure>
    <figure class="img-frame" data-reveal data-delay="80"><img src="../../assets/images/season/saison_martelo_action_01.jpg" alt="Opératrice en pleine charge à travers un nuage de fumée dans une rue urbaine" loading="lazy" decoding="async"><figcaption>La réduction de dégâts de l'Ariete est frontale : son flanc ne bénéficie d'aucun bonus (illustration générée par IA, pas une capture du jeu)</figcaption></figure>
  </div>
  <div class="mb-5" style="max-width:560px">{audio_briefing("saison_briefing_01.mp3", "Saison 12 Aurora", "", D)}</div>
  <div class="grid g-2 gap-5">
    <div class="hud-panel" data-reveal>
      <div class="hud-head">Fiche de saison</div>
      <div class="table-wrap" style="border:0"><table class="df" style="min-width:0"><tbody>{infos}</tbody></table></div>
    </div>
    <div class="hud-panel" data-reveal>
      <div class="hud-head"><span class="pulse-dot orange" aria-hidden="true"></span> À ne pas rater</div>
      <div class="timeline">{prio}</div>
    </div>
  </div>
</div></section>

<section class="section"><div class="wrap">
  <div class="section-head" data-reveal>
    <div class="eyebrow">{len(s['nouveautes_majeures'])} nouveautés majeures</div>
    <h2>Le contenu d'Aurora</h2>
  </div>
  <div class="grid g-auto-md">{nouv}</div>
</div></section>

<section class="section"><div class="wrap">
  <div class="section-head" data-reveal>
    <div class="eyebrow">Mise à jour du {fr(p12.get('date'))}</div>
    <h2>Patch d'équilibrage post-lancement</h2>
  </div>
  <div class="card" data-reveal><ul class="small">{p12_html}</ul></div>
</div></section>

<section class="section"><div class="wrap">
  <div class="section-head" data-reveal>
    <div class="eyebrow">Équilibrage</div>
    <h2>Armes — par mode</h2>
    <p class="lead">Un même fusil peut être buffé en Operations et nerfé en Detonation. Choisissez l'onglet du mode que vous jouez.</p>
  </div>
  <div class="tabs" role="tablist" data-reveal>{armes_tabs}</div>
  {armes_panels}
</div></section>

<section class="section"><div class="wrap">
  <div class="section-head" data-reveal>
    <div class="eyebrow">Équilibrage</div>
    <h2>Opérateurs — par mode</h2>
    {f'<div class="alert alert-red mt-3"><span class="ico">⚠</span><div>{esc(note_eo)}</div></div>' if note_eo else ''}
  </div>
  {ops_blocks}
</div></section>

<section class="section" id="echeances"><div class="wrap">
  <div class="section-head" data-reveal>
    <div class="eyebrow">Ne rien rater</div><h2>{esc(ECH['titre'])}</h2>
    <p class="lead">{esc(ECH['note'])}</p>
  </div>
  <div class="table-wrap" data-reveal><table class="df" style="min-width:620px">
    <thead><tr><th class="sortable">Date</th><th>Contenu</th><th>Statut</th></tr></thead>
    <tbody>{ech_rows}</tbody></table></div>
  <div class="alert alert-orange mt-5" data-reveal><span class="ico" aria-hidden="true">🌍</span>
  <div class="small">{esc(s['note_garena'])}</div></div>
</div></section>

<section class="section" id="operateurs-detail"><div class="wrap">
  <div class="section-head" data-reveal>
    <div class="eyebrow">Opérateurs</div><h2>Équilibrage détaillé</h2>
    <p class="lead">{esc(EOD['avertissement'])}</p>
  </div>
  <h3 class="card-title mb-3">Tous les modes</h3>
  <div class="table-wrap mb-6" data-reveal><table class="df" style="min-width:620px">
    <thead><tr><th>Opérateur</th><th>Changement</th></tr></thead><tbody>{eod_tm}</tbody></table></div>
  <h3 class="card-title mb-3 txt-red">Detonation uniquement — ne pas transposer</h3>
  <div class="table-wrap" data-reveal><table class="df" style="min-width:620px">
    <thead><tr><th>Opérateur</th><th>Changement</th></tr></thead><tbody>{eod_dt}</tbody></table></div>
  <p class="tiny muted mt-4">Guide du mode concerné : <a href="../detonation/index.html">Detonation</a>.</p>
</div></section>

<section class="section" id="chiffres"><div class="wrap">
  <div class="section-head" data-reveal>
    <div class="eyebrow">Notes de patch</div>
    <h2>Équilibrage chiffré</h2>
    <p class="lead">{esc(EQC['note'])}</p>
  </div>

  <h3 class="card-title mb-3">Tous les modes</h3>
  <div class="table-wrap mb-6" data-reveal><table class="df" style="min-width:620px">
    <thead><tr><th>Arme</th><th>Changement</th><th class="num">Sens</th></tr></thead>
    <tbody>{eqc_tm}</tbody></table></div>

  <h3 class="card-title mb-3">Operations</h3>
  <div class="table-wrap mb-6" data-reveal><table class="df" style="min-width:620px">
    <thead><tr><th>Arme</th><th>Changement</th><th class="num">Sens</th></tr></thead>
    <tbody>{eqc_op}</tbody></table></div>

  <h3 class="card-title mb-3">Detonation uniquement</h3>
  <div class="table-wrap mb-5" data-reveal><table class="df" style="min-width:620px">
    <thead><tr><th>Arme</th><th>Changement</th><th class="num">Sens</th></tr></thead>
    <tbody>{eqc_dt}</tbody></table></div>

  <div class="card card-accent-blue" data-reveal>
    <h3 class="card-title" style="font-size:1rem">{esc(VN['libelle'])}</h3>
    <ul class="muted mt-3">{vn_items}</ul>
    <div class="divider"></div>
    <p class="small"><strong class="txt-blue">Lecture :</strong> {esc(VN['lecture'])}</p>
  </div>
</div></section>

<section class="section"><div class="wrap">
  <div class="section-head" data-reveal>
    <div class="eyebrow">Équilibrage</div>
    <h2>Véhicules</h2>
  </div>
  <div class="card card-accent-orange" data-reveal><ul class="small">{veh}</ul></div>
</div></section>

<section class="section" id="events"><div class="wrap">
  <div class="section-head" data-reveal>
    <div class="eyebrow">Calendrier</div>
    <h2>Les {len(s['events'])} events de la saison</h2>
    <p class="lead">Cliquez sur un en-tête pour trier. Statut calculé au 19 novembre 2026.</p>
  </div>
  <div class="table-wrap" data-reveal><table class="df">
    <thead><tr><th class="sortable">Event</th><th class="sortable">Mode</th><th class="sortable">Période</th><th>Récompenses</th><th class="sortable">Statut</th></tr></thead>
    <tbody>{ev_rows}</tbody></table></div>
</div></section>

<section class="section"><div class="wrap">
  <div class="grid g-2 gap-5">
    <div class="card card-accent" data-reveal>
      <h3 class="card-title">Season Pass</h3>
      <p class="small mb-3">{'<strong class="txt-green">Martelo est débloquée gratuitement via le pass.</strong>' if sp.get('martelo_gratuit') else ''}</p>
      <ul class="small muted">{sp_items}</ul>
    </div>
    <div class="card card-accent-blue" data-reveal>
      <h3 class="card-title">Autres cosmétiques</h3>
      <ul class="small muted">{cosm}</ul>
    </div>
  </div>
</div></section>

<section class="section-sm"><div class="wrap">
  <div class="alert alert-blue" data-reveal>
    <span class="ico" aria-hidden="true">ℹ</span>
    <div><strong>Reset des missions.</strong> L'arrivée d'Aurora a réinitialisé l'intégralité des missions de la Saison 11.
    En revanche, <strong>votre stash n'est pas wipé</strong> : Delta Force ne pratique pas de remise à zéro de l'inventaire.</div>
  </div>
</div></section>

<section class="section" id="zenith-port-s12"><div class="wrap">
  <div class="section-head" data-reveal>
    <div class="eyebrow">Warfare</div><h2>{esc(ZP.get('titre',''))}</h2>
    <p class="lead">{esc(ZP.get('pitch',''))}</p>
  </div>
  <div class="grid g-2 gap-6">
    <div>
      <div class="card card-accent-blue" data-reveal>
        <h3 class="card-title" style="font-size:1rem">{esc(RT.get('nom',''))}</h3>
        <p class="small"><strong class="txt-orange">Déclencheur —</strong> {esc(RT.get('declencheur',''))}</p>
        <div class="divider"></div>
        <p class="small"><strong class="txt-blue">Effet —</strong> {esc(RT.get('effet',''))}</p>
        <div class="divider"></div>
        <p class="small"><strong class="txt-green">Physique —</strong> {esc(RT.get('physique',''))}</p>
      </div>
      <div class="alert alert-blue mt-4" data-reveal><span class="ico" aria-hidden="true">i</span>
      <div class="small">{esc(ZP.get('technique',''))}</div></div>
      <div class="alert alert-red mt-3" data-reveal><span class="ico" aria-hidden="true">✕</span>
      <div class="small">{esc(ZP.get('retrait',''))}</div></div>
      <p class="small muted mt-3">{esc(ZP.get('evenement',''))}</p>
    </div>
    <div>
      <figure class="img-frame" data-reveal>
        <img src="../../assets/images/maps/cartes_zenith_riptide_01.jpg" alt="Vague massive déferlant sur un port industriel" loading="lazy" decoding="async">
        <figcaption>Riptide inonde l'objectif bas et ouvre les toits (illustration générée par IA, pas une capture du jeu)</figcaption>
      </figure>
    </div>
  </div>
</div></section>

<section class="section" id="brakkesh-factions"><div class="wrap">
  <div class="section-head" data-reveal>
    <div class="eyebrow">Operations</div><h2>{esc(BF.get('titre',''))}</h2>
    <p class="lead">{esc(BF.get('refonte',''))}</p>
  </div>
  <div class="grid g-2 gap-6">
    <div>
      <figure class="img-frame" data-reveal>
        <img src="../../assets/images/maps/cartes_brakkesh_babel_01.jpg" alt="Tour inachevée de béton brut dominant une ville désertique au couchant" loading="lazy" decoding="async">
        <figcaption>Babel entièrement retravaillée — routes et entrées à réapprendre (illustration générée par IA, pas une capture du jeu)</figcaption>
      </figure>
    </div>
    <div>
      <p class="mb-3">{bf_tags}</p>
      <div class="card card-accent-gold" data-reveal>
        <h3 class="card-title" style="font-size:1rem">Comment ça marche</h3>
        <ol class="small">{bf_steps}</ol>
      </div>
      <div class="card card-accent mt-4" data-reveal>
        <p class="small"><strong>Arsenal Brakkesh —</strong> {esc(BF.get('arsenal_brakkesh',''))}</p>
      </div>
      <p class="small muted mt-3">{esc(BF.get('fenetres',''))}</p>
    </div>
  </div>
</div></section>

<section class="section" id="az3-supercritical"><div class="wrap">
  <div class="section-head" data-reveal>
    <div class="eyebrow">Mode difficile</div><h2>{esc(AZ.get('titre',''))}</h2>
    <p class="lead">{esc(AZ.get('pitch',''))}</p>
  </div>
  <div class="grid g-2 gap-6">
    <div>
      <div class="table-wrap" data-reveal><table class="df" style="min-width:380px"><tbody>{az_rows}</tbody></table></div>
      <div class="alert alert-orange mt-4" data-reveal><span class="ico" aria-hidden="true">⚠</span>
      <div class="small">{esc(AZ.get('conseil',''))}</div></div>
    </div>
    <div>
      <figure class="img-frame" data-reveal>
        <img src="../../assets/images/maps/cartes_az3_supercritical_01.jpg" alt="Hall de centrale nucléaire envahi par une brume de contamination verdâtre" loading="lazy" decoding="async">
        <figcaption>AZ3 Supercritical — la contamination se propage dans la zone (illustration générée par IA, pas une capture du jeu)</figcaption>
      </figure>
    </div>
  </div>
</div></section>

<section class="section" id="kits-haavk"><div class="wrap">
  <div class="section-head" data-reveal>
    <div class="eyebrow">{esc(AT.get('fenetre',''))}</div><h2>{esc(AT.get('titre',''))}</h2>
  </div>
  <div class="table-wrap" data-reveal><table class="df" style="min-width:760px">
    <thead><tr><th>Kit</th><th>Contrôle</th><th>Stabilité</th><th>Précision</th><th>Maniabilité</th><th>Effet</th></tr></thead>
    <tbody>{at_rows}</tbody>
  </table></div>
  <p class="small txt-orange mt-3" data-reveal>{esc(AT.get('note',''))}</p>
</div></section>
"""

html = (head("Saison 12 — Aurora", "Tout sur la Saison 12 Aurora de Delta Force : patch notes complets, "
             "Martelo, AN-94, Brakkesh 2.0, Zenith Port, 5 nouvelles munitions, équilibrage par mode, "
             "17 events datés et season pass.",
             depth=D, canonical="pages/saison-aurora/index.html",
             image="assets/images/season/saison_aurora_01.jpg")
        + navbar(D) + '<main id="main">' + body + "</main>" + footer(D) + scripts(D))
print(write("pages/saison-aurora/index.html", html))

# ============================================================== PAGE NEWS
news_items = []
for e in s["events"]:
    fin = e.get("fin", "")
    if isinstance(fin, str) and fin and fin >= TODAY:
        news_items.append(e)
news_html = "".join(f"""<article class="card card-media" data-reveal>
    <div class="body">
      <div class="flex items-center gap-2 mb-2">
        <span class="badge badge-green">{esc(e.get('mode','Tous'))}</span>
        <span class="tiny muted mono">{fr(e.get('debut'))} → {fr(e.get('fin'))}</span>
      </div>
      <h3 class="card-title">{esc(e.get('nom','—'))}</h3>
      <p class="small muted">{esc(e.get('recompenses',''))}</p>
    </div>
  </article>""" for e in news_items)

news_body = f"""
{page_hero("Fil d'actualité", "News &amp; events <span class='grad-text'>en cours</span>",
           "Ce qui tourne en ce moment dans Delta Force. État au 19 novembre 2026.",
           "assets/images/season/saison_aurora_01.jpg", D)}
<section class="section"><div class="wrap">
  {crumbs([("News", None)], D)}
  <figure class="img-frame mb-5" data-reveal>
    <img src="../../assets/images/misc/news_brief_01.jpg" alt="Salle de briefing militaire vide avant la réunion, écran de projection éclairé et chaises alignées" loading="lazy" decoding="async">
    <figcaption>Chaque patch redistribue les cartes — et la moitié des changements ne se voient qu'à l'usage. (illustration générée par IA, pas une capture du jeu)</figcaption>
  </figure>
  <div class="mb-4" style="max-width:560px">{audio_briefing("news_briefing_01.mp3", "Actualités", "", D)}</div>
  <div class="alert mb-5" data-reveal>
    <span class="ico" aria-hidden="true">⏱</span>
    <div><strong>Page statique mise à jour manuellement.</strong> Les restrictions CORS empêchent un site statique
    d'interroger les serveurs officiels depuis le navigateur. Dernière vérification : <strong>19 novembre 2026</strong>.
    Source de référence : <a href="https://www.playdeltaforce.com/" target="_blank" rel="noopener nofollow">playdeltaforce.com</a>.</div>
  </div>
  <div class="grid g-auto-md">{news_html}</div>
  <div class="text-center mt-6"><a class="btn btn-orange" href="../saison-aurora/index.html">Calendrier complet des 17 events</a></div>
</div></section>
"""

PD = s["patch_detail"]
CO = PD["collab"]
_grp = "".join(f"""<article class="card card-accent-{g['accent']}" data-reveal data-delay="{i*50}">
    <div class="flex-between mb-2"><h3 class="card-title" style="font-size:1rem;margin:0">{esc(g['nom'])}</h3>
      <span class="badge badge-grey">{len(g['items'])}</span></div>
    <ul class="small">{"".join(f"<li>{esc(x)}</li>" for x in g["items"])}</ul>
  </article>""" for i, g in enumerate(PD["groupes"]))
_tot = sum(len(g["items"]) for g in PD["groupes"])

news_patch = f"""
<section class="section" id="patch-detail"><div class="wrap">
  <div class="section-head" data-reveal>
    <div class="eyebrow">{_tot} changements</div><h2>{esc(PD['titre'])}</h2>
    <p class="lead">{esc(PD['intro'])}</p>
  </div>
  <div class="grid g-2 gap-4 mb-5">{_grp}</div>
  <div class="grid g-2 gap-6">
    <div class="card card-accent-gold" data-reveal>
      <div class="hud tiny txt-gold mb-2">{esc(CO['dates'])}</div>
      <h3 class="card-title" style="font-size:1.05rem">{esc(CO['titre'])}</h3>
      <p class="small" style="margin:0">{esc(CO['detail'])}</p>
    </div>
    <figure class="img-frame" data-reveal data-delay="80">
      <img src="../../assets/images/misc/firing_range_cibles_01.jpg" alt="Stand d'entraînement intérieur avec rangée de mannequins blindés sur rails motorisés" loading="lazy" decoding="async">
      <figcaption>Le stand de tir accepte désormais des cibles mobiles et le test des capacités d'opérateur (illustration générée par IA, pas une capture du jeu)</figcaption>
    </figure>
  </div>
  <p class="small muted mt-4">{esc(PD['source'])}</p>
</div></section>
"""
html_news = (head("News & events en cours", "Les events Delta Force actifs en novembre et décembre 2026, "
                  "avec dates, modes et récompenses. Saison 12 Aurora.",
                  depth=D, canonical="pages/news/index.html",
                  image="assets/images/season/saison_aurora_01.jpg")
             + navbar(D) + '<main id="main">' + news_body + news_patch + "</main>" + footer(D) + scripts(D))
print(write("pages/news/index.html", html_news))
