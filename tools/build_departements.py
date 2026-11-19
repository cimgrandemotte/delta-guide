#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_departements.py — Départements, réputation et paliers du Black Site."""

from site_common import (head, navbar, footer, scripts, write, esc,
                         load, crumbs, page_hero, audio_briefing)

DP = load("departements")
D = 2

PR = DP["principe"]
CIK = DP["cash_is_king"]

deps = "".join(f"""<article class="card card-accent{'-' + d['accent'] if d['accent'] else ''}" data-reveal data-delay="{i*60}">
    <div class="flex-between mb-2">
      <h3 class="card-title" style="font-size:1.05rem;margin:0">{esc(d['nom'])}</h3>
      <span class="badge badge-grey">{esc(d['priorite'])}</span>
    </div>
    <div class="hud tiny muted mb-2">{esc(d['nom_en'])}</div>
    <p class="small">{esc(d['role'])}</p>
    <div class="divider"></div>
    <p class="small txt-green"><strong>Pourquoi elle compte :</strong> {esc(d['pourquoi'])}</p>
  </article>""" for i, d in enumerate(DP["departements"]))

regles = "".join(f"<li>{esc(x)}</li>" for x in DP["regles"])

def _station(s, i):
    rows = "".join(f"""<tr><td class="mono small">{esc(p['palier'])}</td>
      <td class="small txt-orange">{esc(p['requis'])}</td>
      <td class="small">{esc(p['gain'])}</td></tr>""" for p in s["paliers"])
    return f"""<article class="card" data-reveal data-delay="{(i % 2)*70}">
    <h3 class="card-title" style="font-size:1.05rem">{esc(s['nom'])}</h3>
    <div class="table-wrap mb-3"><table class="df">
      <thead><tr><th>Palier</th><th>Requis</th><th>Gain</th></tr></thead>
      <tbody>{rows}</tbody></table></div>
    <p class="small txt-green"><strong>Verdict :</strong> {esc(s['verdict'])}</p>
  </article>"""

stations = "".join(_station(s, i) for i, s in enumerate(DP["stations"]))

ordre = "".join(f"""<article class="card card-accent-green" data-reveal data-delay="{i*55}">
    <div class="hud tiny txt-green mb-2">PRIORITÉ {o['n']:02d}</div>
    <h4 class="card-title" style="font-size:.98rem">{esc(o['quoi'])}</h4>
    <p class="small muted">{esc(o['pourquoi'])}</p>
  </article>""" for i, o in enumerate(DP["ordre_recommande"]))

cik_chips = "".join(f'<span class="chip" data-val="{esc(p)}">{esc(p)}</span>' for p in CIK["paliers"])

body = f"""
{page_hero("Operations", "Les <span class='grad-text'>départements</span>",
           "Le quatrième pilier d'Operations, et celui que presque personne ne monte. "
           "Cinq réputations, un plafond au niveau 4, et des verrous croisés qui bloquent "
           "le Black Site tant qu'on les ignore.",
           "assets/images/heroes/departements_hero_01.jpg", D)}

<section class="section-sm"><div class="wrap">
  {crumbs([("Hazard Ops", "index.html"), ("Départements", None)], D)}
  <div class="mb-4" style="max-width:560px">{audio_briefing("departements_briefing_01.mp3", "Départements", "", D)}</div>
  <p class="lead" data-reveal style="max-width:74ch">{esc(PR['contenu'])}</p>
  <div class="alert alert-blue mt-4" data-reveal><span class="ico" aria-hidden="true">i</span>
  <div class="small"><strong>La boucle :</strong> {esc(PR['boucle'])}</div></div>
  <div class="alert alert-orange mt-3" data-reveal><span class="ico" aria-hidden="true">!</span>
  <div class="small">{esc(DP['_meta']['avertissement'])}</div></div>
</div></section>

<section class="section" id="les-cinq"><div class="wrap">
  <div class="section-head" data-reveal>
    <div class="eyebrow">{len(DP['departements'])} départements</div><h2>Qui fait quoi, et dans quel ordre</h2>
  </div>
  <div class="grid g-auto-md gap-4 mb-6">{deps}</div>
  <div class="grid g-2 gap-6">
    <div class="card card-accent-blue" data-reveal><ul class="small">{regles}</ul></div>
    <figure class="img-frame" data-reveal>
      <img src="../../assets/images/misc/departements_medical_01.jpg" alt="Infirmerie de campagne avec chariots d'acier et étagères de fournitures médicales" loading="lazy" decoding="async">
      <figcaption>L'Infirmerie : des marges modestes mais régulières (illustration générée par IA, pas une capture du jeu)</figcaption>
    </figure>
  </div>
</div></section>

<section class="section" id="paliers"><div class="wrap">
  <div class="section-head" data-reveal>
    <div class="eyebrow">{len(DP['stations'])} stations</div><h2>Les paliers du Black Site, station par station</h2>
    <p class="lead">Chaque palier réclame un niveau d'Operations, des matériaux, et parfois une réputation de département.
    Ce sont ces prérequis croisés qui rendent les départements obligatoires plutôt qu'optionnels.</p>
  </div>
  <div class="grid g-2 gap-4">{stations}</div>
</div></section>

<section class="section" id="ordre"><div class="wrap">
  <div class="grid g-2 gap-6 mb-6">
    <figure class="img-frame" data-reveal>
      <img src="../../assets/images/misc/departements_station_01.jpg" alt="Comptoir de ravitaillement militaire, caisses empilées et casiers métalliques" loading="lazy" decoding="async">
      <figcaption>Chaque palier de réputation ouvre des articles permanents à la Supply Station (illustration générée par IA, pas une capture du jeu)</figcaption>
    </figure>
    <div>
      <div class="section-head" data-reveal><div class="eyebrow">Économie</div><h2>{esc(CIK['titre'])}</h2></div>
      <div class="card card-accent-gold" data-reveal>
        <p class="small">{esc(CIK['contenu'])}</p>
        <div class="chips mt-3">{cik_chips}</div>
      </div>
    </div>
  </div>
  <div class="section-head" data-reveal>
    <div class="eyebrow">Feuille de route</div><h2>Dans quel ordre investir</h2>
    <p class="lead">Tous les paliers ne se valent pas. Certains ont un rendement composé, d'autres sont de simples prérequis.</p>
  </div>
  <div class="grid g-auto-md gap-4">{ordre}</div>
</div></section>

<section class="section-sm"><div class="wrap">
  <div class="grid g-3 gap-4">
    <a class="card card-accent" href="black-site.html" data-reveal><h3 class="card-title" style="font-size:1rem">Black Site</h3>
      <p class="small muted">Les 11 stations, l'ordre d'amélioration et le planificateur.</p></a>
    <a class="card card-accent" href="../outils/artisanat.html" data-reveal data-delay="80"><h3 class="card-title" style="font-size:1rem">Artisanat &amp; enchères</h3>
      <p class="small muted">Calculer une marge avant de lancer huit heures de production.</p></a>
    <a class="card card-accent" href="../encyclopedie/economie.html" data-reveal data-delay="160"><h3 class="card-title" style="font-size:1rem">Économie</h3>
      <p class="small muted">La boucle de profit complète.</p></a>
  </div>
</div></section>
"""

html = (head("Départements Operations — réputation, paliers et prérequis du Black Site",
             "Guide des 5 départements de Delta Force Operations : Unité de Guerre Tactique, Bataillon d'Assaut, "
             "Laboratoire T&E, Infirmerie, Soutien de Base. Tous les paliers du Black Site avec niveaux "
             "d'Operations requis, gains et prérequis croisés de réputation.",
             depth=D, canonical="pages/hazard-ops/departements.html",
             image="assets/images/heroes/departements_hero_01.jpg")
        + navbar(D) + '<main id="main">' + body + "</main>" + footer(D) + scripts(D))
print(write("pages/hazard-ops/departements.html", html))
