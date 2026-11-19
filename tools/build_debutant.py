#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_debutant.py — Parcours débutant : premières heures, erreurs, kit budget."""

from site_common import (head, navbar, footer, scripts, write, esc,
                         load, crumbs, page_hero, audio_briefing)

DB = load("debutant")
D = 2

QM = DB["quel_mode_dabord"]
qm_rows = "".join(f"""<tr>
    <td><strong>{esc(c['question'])}</strong></td>
    <td class="small">{esc(c['warfare'])}</td>
    <td class="small">{esc(c['operations'])}</td>
  </tr>""" for c in QM["comparaison"])

heures = "".join(f"""<article class="card card-accent-orange" data-reveal data-delay="{i*80}">
    <div class="flex items-center justify-between gap-2 mb-2">
      <span class="badge badge-new">{esc(h['tranche'])}</span>
    </div>
    <h3 class="card-title" style="font-size:1.05rem">{esc(h['titre'])}</h3>
    <p class="small txt-orange mb-2"><strong>Objectif —</strong> {esc(h['objectif'])}</p>
    <ul class="small muted">{"".join(f"<li>{esc(a)}</li>" for a in h["actions"])}</ul>
  </article>""" for i, h in enumerate(DB["dix_premieres_heures"]))

road = "".join(f"""<div class="card card-accent-blue" data-reveal data-delay="{i*70}">
    <div class="hud tiny txt-blue mb-2">{esc(r['semaine'])}</div>
    <p class="small"><strong>{esc(r['focus'])}</strong></p>
    <div class="divider"></div>
    <p class="small muted">{esc(r['objectif'])}</p>
  </div>""" for i, r in enumerate(DB["roadmap_30j"]))

LB = DB["loadout_budget"]
lb_rows = "".join(f"""<tr>
    <td><strong>{esc(l['poste'])}</strong></td>
    <td class="small">{esc(l['choix'])}</td>
    <td class="mono num small txt-green">{esc(l['cout'])}</td>
    <td class="small muted">{esc(l['pourquoi'])}</td>
  </tr>""" for l in LB["lignes"])

DS = DB["distances_sonores"]
ds_rows = "".join(f"""<tr>
    <td><strong>{esc(d['mouvement'])}</strong></td>
    <td class="mono num small">{esc(d['releve_a'])}</td>
    <td class="mono num small">{esc(d['releve_b'])}</td>
    <td class="small muted">{esc(d['verdict'])}</td>
  </tr>""" for d in DS["lignes"])

err = "".join(f"""<article class="card card-accent-red" data-reveal data-delay="{i*50}">
    <div class="hud tiny txt-red mb-2">ERREUR {i+1:02d}</div>
    <h3 class="card-title" style="font-size:1rem">{esc(e['titre'])}</h3>
    <p class="small muted mb-2"><em>{esc(e['symptome'])}</em></p>
    <p class="small"><strong class="txt-orange">Cause —</strong> {esc(e['cause'])}</p>
    <p class="small"><strong class="txt-green">Correctif —</strong> {esc(e['correctif'])}</p>
  </article>""" for i, e in enumerate(DB["erreurs"]))

VS = DB["valeur_par_slot"]
vs_items = "".join(f"<li>{esc(x)}</li>" for x in VS["consequences"])

ops = "".join(f"""<article class="card card-accent-green" data-reveal data-delay="{i*70}">
    <div class="flex items-center justify-between gap-2 mb-2">
      <h3 class="card-title" style="font-size:1.05rem">{esc(o['nom'])}</h3>
      <span class="badge badge-grey">{esc(o['role'])}</span>
    </div>
    <p class="small"><span class="hud tiny muted">DIFFICULTÉ</span> {esc(o['difficulte'])}</p>
    <div class="divider"></div>
    <p class="small">{esc(o['verdict'])}</p>
    <p class="small txt-orange">⚠ {esc(o['attention'])}</p>
  </article>""" for i, o in enumerate(DB["operateurs_demarrage"]))

nope = "".join(f"<li>{esc(x)}</li>" for x in DB["a_ne_pas_faire_au_demarrage"])

body = f"""
{page_hero("Prise en main", "Guide du <span class='grad-text'>débutant</span>",
           "De la première heure au premier million d'Alloys. Un parcours chiffré, les huit erreurs "
           "qui ruinent un démarrage, et le kit qui rapporte dès le premier raid.",
           "assets/images/heroes/debutant_hero_01.jpg", D, badge="S12")}

<section class="section-sm"><div class="wrap">
  {crumbs([("Débutant", None)], D)}
  <figure class="img-frame mb-5" data-reveal>
    <img src="../../assets/images/misc/debutant_premiere_sortie_01.jpg" alt="Opérateur légèrement équipé à la rampe arrière d'un avion, face à une vallée brumeuse à l'aube" loading="lazy" decoding="async">
    <figcaption>Votre première sortie ne doit rien rapporter : elle doit vous apprendre la carte. (illustration générée par IA, pas une capture du jeu)</figcaption>
  </figure>
  <div class="mb-4" style="max-width:560px">{audio_briefing("debutant_briefing_01.mp3", "Guide du débutant", "", D)}</div>
  <div class="alert alert-green" data-reveal><span class="ico" aria-hidden="true">★</span>
  <div class="small"><strong>La règle d'or.</strong> {esc(DB['regle_d_or'])}</div></div>
</div></section>

<section class="section" id="quel-mode"><div class="wrap">
  <div class="section-head" data-reveal>
    <div class="eyebrow">Première décision</div><h2>{esc(QM['titre'])}</h2>
    <p class="lead">Verdict : <strong class="txt-green">{esc(QM['verdict'])}</strong></p>
  </div>
  <div class="table-wrap" data-reveal><table class="df" style="min-width:760px">
    <thead><tr><th>Question</th><th>Havoc Warfare</th><th>Hazard Operations</th></tr></thead>
    <tbody>{qm_rows}</tbody>
  </table></div>
</div></section>

<section class="section" id="dix-heures"><div class="wrap">
  <div class="section-head" data-reveal>
    <div class="eyebrow">Parcours guidé</div><h2>Vos dix premières heures</h2>
    <p class="lead">Quatre paliers, un objectif unique par palier. Ne passez au suivant qu'une fois celui-ci tenu.</p>
  </div>
  <div class="grid g-2 gap-4 mb-6">{heures}</div>

  <figure class="img-frame" data-reveal>
    <img src="../../assets/images/misc/knife_run_01.jpg" alt="Opérateur léger progressant accroupi dans un entrepôt sombre, couteau en main" loading="lazy" decoding="async">
    <figcaption>Le run au couteau : zéro investissement, zéro perte possible (illustration générée par IA, pas une capture du jeu)</figcaption>
  </figure>
</div></section>

<section class="section" id="roadmap"><div class="wrap">
  <div class="section-head" data-reveal><div class="eyebrow">30 jours</div><h2>Feuille de route du premier mois</h2></div>
  <div class="grid g-auto-md gap-4">{road}</div>
</div></section>

<section class="section" id="kit"><div class="wrap">
  <div class="section-head" data-reveal>
    <div class="eyebrow">Économie</div><h2>{esc(LB['titre'])}</h2>
    <p class="lead">{esc(LB['principe'])}</p>
  </div>
  <div class="table-wrap" data-reveal><table class="df" style="min-width:820px">
    <thead><tr><th>Poste</th><th>Choix</th><th>Coût</th><th>Pourquoi</th></tr></thead>
    <tbody>{lb_rows}</tbody>
  </table></div>
  <p class="small txt-green mt-3" data-reveal><strong>Total — {esc(LB['total'])}</strong></p>
</div></section>

<section class="section" id="son"><div class="wrap">
  <div class="section-head" data-reveal>
    <div class="eyebrow">Discrétion</div><h2>{esc(DS['titre'])}</h2>
  </div>
  <div class="alert alert-orange mb-4" data-reveal><span class="ico" aria-hidden="true">⚠</span>
  <div class="small">{esc(DS['avertissement'])}</div></div>
  <div class="table-wrap" data-reveal><table class="df" style="min-width:700px">
    <thead><tr><th>Déplacement</th><th>Relevé A</th><th>Relevé B</th><th>Conséquence</th></tr></thead>
    <tbody>{ds_rows}</tbody>
  </table></div>
  <div class="card card-accent-green mt-4" data-reveal><p class="small">{esc(DS['regle'])}</p></div>
</div></section>

<section class="section" id="erreurs"><div class="wrap">
  <div class="section-head" data-reveal>
    <div class="eyebrow">{len(DB['erreurs'])} pièges</div><h2>Les erreurs qui coûtent cher</h2>
    <p class="lead">Chacune est décrite par son symptôme — c'est ainsi qu'on la reconnaît dans sa propre partie.</p>
  </div>
  <div class="grid g-auto-md gap-4">{err}</div>
</div></section>

<section class="section" id="valeur-slot"><div class="wrap wrap-narrow">
  <div class="section-head" data-reveal><div class="eyebrow">Arithmétique</div><h2>{esc(VS['titre'])}</h2>
    <p class="lead">{esc(VS['regle'])}</p></div>
  <div class="card card-accent-gold" data-reveal>
    <p class="small txt-gold mb-2"><strong>{esc(VS['cible'])}</strong></p>
    <ul class="small">{vs_items}</ul>
  </div>
</div></section>

<section class="section" id="operateurs"><div class="wrap">
  <div class="section-head" data-reveal><div class="eyebrow">Roster</div><h2>Par qui commencer</h2></div>
  <div class="grid g-auto-md gap-4 mb-6">{ops}</div>

  <div class="card card-accent-red" data-reveal>
    <h3 class="card-title" style="font-size:1rem">À ne surtout pas faire au démarrage</h3>
    <ul class="small">{nope}</ul>
  </div>
</div></section>

<section class="section-sm"><div class="wrap">
  <div class="grid g-3 gap-4">
    <a class="card card-accent" href="../armurerie/munitions.html" data-reveal><h3 class="card-title" style="font-size:1rem">Munitions &amp; pénétration</h3>
      <p class="small muted">La matrice qui explique vos duels perdus.</p></a>
    <a class="card card-accent" href="../astuces-pro/index.html" data-reveal data-delay="80"><h3 class="card-title" style="font-size:1rem">Réglages &amp; astuces pro</h3>
      <p class="small muted">Audio, graphismes, sensibilité : la config qui fait gagner.</p></a>
    <a class="card card-accent" href="../encyclopedie/economie.html" data-reveal data-delay="160"><h3 class="card-title" style="font-size:1rem">Économie</h3>
      <p class="small muted">Craft, hôtel des ventes et boucle de profit.</p></a>
  </div>
</div></section>
"""

html = (head("Guide du débutant Delta Force — vos 10 premières heures",
             "Parcours débutant complet pour Delta Force : Warfare ou Operations en premier, les dix "
             "premières heures heure par heure, kit budget rentable, distances sonores, les huit erreurs "
             "les plus coûteuses et la feuille de route du premier mois.",
             depth=D, canonical="pages/debutant/index.html",
             image="assets/images/heroes/debutant_hero_01.jpg")
        + navbar(D) + '<main id="main">' + body + "</main>" + footer(D) + scripts(D))
print(write("pages/debutant/index.html", html))
