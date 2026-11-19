#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_az3.py — AZ3 Centrale nucléaire & mode Supercritical."""

from site_common import (head, navbar, footer, scripts, write, esc,
                         load, crumbs, page_hero, audio_briefing)

AZ = load("az3")
D = 2

SC = AZ["supercritical"]
RA = AZ["radiation"]
EX = AZ["extractions_supercritical"]
MA = AZ["mission_arret"]
PO = AZ["paliers_operations"]

off = "".join(f"""<div class="stat-card" data-reveal data-delay="{i*60}">
    <div class="hud tiny muted">{esc(o['quoi'])}</div>
    <div class="num txt-gold" style="font-size:1.15rem">{esc(o['valeur'])}</div>
    <p class="small muted" style="margin:.4rem 0 0">{esc(o['note'])}</p>
  </div>""" for i, o in enumerate(SC["officiel"]))

prep = "".join(f"""<article class="card card-accent-green" data-reveal data-delay="{i*60}">
    <div class="hud tiny txt-green mb-2">PRÉPARATION {p['n']:02d}</div>
    <h4 class="card-title" style="font-size:.98rem">{esc(p['titre'])}</h4>
    <p class="small muted">{esc(p['detail'])}</p>
  </article>""" for i, p in enumerate(SC["preparation"]))

rad = "".join(f"<li>{esc(x)}</li>" for x in RA["regles"])

_rk = {"Faible": "green", "Moyen": "orange", "Élevé": "red"}
voies = "".join(f"""<article class="card card-accent-{_rk.get(v['risque'],'blue')}" data-reveal data-delay="{i*70}">
    <div class="flex-between mb-2"><h4 class="card-title" style="font-size:1rem;margin:0">{esc(v['nom'])}</h4>
      <span class="badge badge-{'red' if v['risque']=='Élevé' else ('green' if v['risque']=='Faible' else 'gold')}">Risque {esc(v['risque'].lower())}</span></div>
    <p class="small">{esc(v['detail'])}</p>
  </article>""" for i, v in enumerate(EX["voies"]))

etapes = "".join(f"""<li class="mb-2"><strong class="txt-orange num">{i+1}.</strong> {esc(e)}</li>"""
                 for i, e in enumerate(MA["etapes"]))

paliers = "".join(f"""<tr><td class="mono num txt-gold"><strong>{esc(l['niveau'])}</strong></td>
    <td class="small">{esc(l['debloque'])}</td></tr>""" for l in PO["lignes"])

survie = "".join(f"<li>{esc(x)}</li>" for x in AZ["survie"])

body = f"""
{page_hero("Carte Hard", "AZ3 &amp; <span class='grad-text'>Supercritical</span>",
           "La seule carte où l'environnement vous tue indépendamment des autres joueurs. "
           "Et à partir du 18 décembre, une version Hard bâtie autour d'une contamination qui se propage.",
           "assets/images/maps/cartes_az3_supercritical_01.jpg", D, badge="18/12/2026")}

<section class="section-sm"><div class="wrap">
  {crumbs([("Cartes", "index.html"), ("AZ3 &amp; Supercritical", None)], D)}
  <div class="mb-4" style="max-width:560px">{audio_briefing("az3_briefing_01.mp3", "AZ3 Supercritical", "", D)}</div>
  <div class="alert alert-orange" data-reveal><span class="ico" aria-hidden="true">!</span>
  <div class="small"><strong>{esc(AZ['_meta']['statut'])}</strong> {esc(SC['annonce'])}</div></div>
</div></section>

<section class="section" id="officiel"><div class="wrap">
  <div class="section-head" data-reveal>
    <div class="eyebrow">Données officielles</div><h2>{esc(SC['titre'])}</h2>
  </div>
  <div class="grid g-auto-sm gap-4 mb-5">{off}</div>
  <div class="alert alert-red" data-reveal><span class="ico" aria-hidden="true">⚠</span>
  <div class="small">{esc(SC['non_officiel'])}</div></div>
</div></section>

<section class="section" id="preparation"><div class="wrap">
  <div class="section-head" data-reveal>
    <div class="eyebrow">D'ici le 18 décembre</div><h2>Quatre choses à faire maintenant</h2>
    <p class="lead">Un mois, c'est court pour monter un niveau d'Operations et mettre 600 000 Alloys de côté. C'est long
    pour attendre sans rien faire.</p>
  </div>
  <div class="grid g-auto-md gap-4">{prep}</div>
</div></section>

<section class="section" id="radiation"><div class="wrap">
  <div class="grid g-2 gap-6">
    <div>
      <div class="section-head" data-reveal><div class="eyebrow">Mécanique</div><h2>{esc(RA['titre'])}</h2>
        <p class="lead">{esc(RA['principe'])}</p></div>
      <div class="card card-accent-red" data-reveal><ul class="small">{rad}</ul></div>
    </div>
    <div>
      <figure class="img-frame" data-reveal>
        <img src="../../assets/images/maps/cartes_az3_supercritical_01.jpg" alt="Hall de réacteur nucléaire baigné d'une brume lumineuse" loading="lazy" decoding="async">
        <figcaption>Au palier 4, votre santé maximale tombe à 60 points (illustration générée par IA, pas une capture du jeu)</figcaption>
      </figure>
      <div class="card card-accent-blue mt-4" data-reveal>
        <h3 class="card-title" style="font-size:1rem">{esc(EX['titre'])}</h3>
        <p class="small muted mb-3">{esc(EX['avertissement'])}</p>
        <div class="grid gap-3">{voies}</div>
      </div>
    </div>
  </div>
</div></section>

<section class="section" id="arret-urgence"><div class="wrap wrap-narrow">
  <div class="section-head" data-reveal><div class="eyebrow">Chaîne scénarisée</div><h2>{esc(MA['titre'])}</h2>
    <p class="lead">{esc(MA['contenu'])}</p></div>
  <div class="card card-accent-orange" data-reveal>
    <ul class="small" style="list-style:none;padding-left:0">{etapes}</ul>
  </div>
  <div class="alert alert-green mt-4" data-reveal><span class="ico" aria-hidden="true">★</span>
  <div class="small">{esc(MA['conseil'])}</div></div>
</div></section>

<section class="section" id="paliers"><div class="wrap">
  <div class="grid g-2 gap-6">
    <div>
      <div class="section-head" data-reveal><div class="eyebrow">Progression</div><h2>{esc(PO['titre'])}</h2>
        <p class="lead">{esc(PO['note'])}</p></div>
      <div class="table-wrap" data-reveal><table class="df">
        <thead><tr><th>Niveau Ops</th><th>Débloque</th></tr></thead><tbody>{paliers}</tbody></table></div>
      <div class="alert alert-blue mt-3" data-reveal><span class="ico" aria-hidden="true">i</span>
      <div class="small">{esc(PO['s12'])}</div></div>
    </div>
    <div>
      <div class="section-head" data-reveal><div class="eyebrow">{len(AZ['survie'])} règles</div><h2>Survivre à AZ3</h2></div>
      <div class="card card-accent-green" data-reveal><ul class="small">{survie}</ul></div>
      <figure class="img-frame mt-4" data-reveal>
        <img src="../../assets/images/misc/extraction_point_01.jpg" alt="Opérateur observant une zone d'extraction marquée par de la fumée" loading="lazy" decoding="async">
        <figcaption>Partez dès que les deux extractions commencent à se peupler (illustration générée par IA, pas une capture du jeu)</figcaption>
      </figure>
    </div>
  </div>
</div></section>

<section class="section-sm"><div class="wrap">
  <div class="grid g-3 gap-4">
    <a class="card card-accent" href="index.html" data-reveal><h3 class="card-title" style="font-size:1rem">Toutes les cartes</h3>
      <p class="small muted">Les 6 cartes d'Operations et les 6 de Warfare.</p></a>
    <a class="card card-accent" href="../hazard-ops/keycards.html" data-reveal data-delay="80"><h3 class="card-title" style="font-size:1rem">Cartes d'accès</h3>
      <p class="small muted">Lesquelles acheter, et lesquelles sont des paris.</p></a>
    <a class="card card-accent" href="../saison-aurora/index.html" data-reveal data-delay="160"><h3 class="card-title" style="font-size:1rem">Saison Aurora</h3>
      <p class="small muted">Tous les jalons datés de la S12.</p></a>
  </div>
</div></section>
"""

html = (head("AZ3 Supercritical — dates, prérequis, radiation et préparation",
             "Tout sur AZ3 Supercritical de Delta Force : ouverture le 18 décembre 2026, Operations niveau 30, "
             "valeur d'entrée de 600 000 Tekniq Alloys, mécanique de radiation à 4 paliers, trois voies d'extraction "
             "et la mission d'arrêt d'urgence étape par étape.",
             depth=D, canonical="pages/cartes/az3-supercritical.html",
             image="assets/images/maps/cartes_az3_supercritical_01.jpg")
        + navbar(D) + '<main id="main">' + body + "</main>" + footer(D) + scripts(D))
print(write("pages/cartes/az3-supercritical.html", html))
