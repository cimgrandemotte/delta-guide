#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_factions.py — Brakkesh 2.0 : affrontement de factions."""

from site_common import (head, navbar, footer, scripts, write, esc,
                         load, crumbs, page_hero, audio_briefing)

FA = load("factions")
D = 2
AI = "(illustration générée par IA, pas une capture du jeu)"

IN, CH = FA["insigne"], FA["chasse"]

camps = "".join(f"""<article class="card card-accent-{c['accent']}" data-reveal data-delay="{i*90}">
    <div class="flex-between mb-2">
      <h3 class="card-title" style="font-size:1.1rem;margin:0">{esc(c['nom'])}</h3>
      <span class="badge badge-{'blue' if c['accent']=='blue' else 'gold'}">{esc(c['style'])}</span></div>
    <div class="hud tiny txt-{c['accent']} mb-3">OBJECTIF D'OUVERTURE — {esc(c['role'].upper())}</div>
    <figure class="img-frame mb-3">
      <img src="../../assets/images/{c['image']}" alt="{esc(c['alt'])}" loading="lazy" decoding="async">
      <figcaption>{esc(c['nom'])} {AI}</figcaption>
    </figure>
    <p class="small" style="margin:0">{esc(c['detail'])}</p>
  </article>""" for i, c in enumerate(FA["camps"]))

etapes = "".join(f"""<li class="check-row"><span class="num txt-gold mono">{i+1}</span>
    <span>{esc(e)}</span></li>""" for i, e in enumerate(IN["etapes"]))

cons = "".join(f"<li>{esc(c)}</li>" for c in CH["consequences"])

tips = "".join(f"""<article class="card card-accent-green" data-reveal data-delay="{i*60}">
    <h3 class="card-title" style="font-size:.98rem">{esc(t['titre'])}</h3>
    <p class="small muted" style="margin:0">{esc(t['detail'])}</p>
  </article>""" for i, t in enumerate(FA["conseils"]))

evs = "".join(f"""<tr><td><strong>{esc(e['nom'])}</strong></td>
    <td class="mono small txt-orange">{esc(e['dates'])}</td>
    <td class="small muted">{esc(e['quoi'])}</td></tr>""" for e in FA["evenements"])

body = f"""
{page_hero("Operations · Brakkesh", "Brakkesh 2.0 &amp; <span class='grad-text'>les factions</span>",
           "Babel entièrement retravaillée, deux camps rivaux, et la première progression du jeu "
           "qui survit à votre mort.",
           "assets/images/heroes/brakkesh_factions_hero_01.jpg", D, badge="Jusqu'au 10/12")}

<section class="section-sm"><div class="wrap">
  {crumbs([("Cartes", "index.html"), ("Brakkesh &amp; factions", None)], D)}
  <div class="mb-4" style="max-width:560px">{audio_briefing("factions_briefing_01.mp3", "Factions de Brakkesh", "", D)}</div>
  <div class="alert alert-red" data-reveal><span class="ico" aria-hidden="true">⚠</span>
  <div class="small">{esc(FA['_meta']['avertissement'])}</div></div>
</div></section>

<section class="section"><div class="wrap">
  <div class="grid g-2 gap-6 mb-5">
    <div>
      <div class="section-head" data-reveal><div class="eyebrow">Le principe</div>
        <h2>Une couche d'allégeance sur une partie d'extraction</h2>
        <p class="lead">{esc(FA['principe'])}</p></div>
      <div class="alert alert-blue" data-reveal><span class="ico" aria-hidden="true">i</span>
      <div class="small">{esc(FA['changement_camp'])}</div></div>
    </div>
    <figure class="img-frame" data-reveal>
      <img src="../../assets/images/maps/brakkesh_babel_tour_01.jpg" alt="Intérieur d'une tour de béton inachevée, rampes en spirale et puits de lumière vertical" loading="lazy" decoding="async">
      <figcaption>Babel a été entièrement reconstruite — c'est désormais le point chaud de la carte {AI}</figcaption>
    </figure>
  </div>
  <div class="section-head" data-reveal><div class="eyebrow">Deux camps</div><h2>Haavk ou Ahsarah&nbsp;?</h2></div>
  <div class="grid g-2 gap-4 mb-4">{camps}</div>
  <div class="alert alert-green" data-reveal><span class="ico" aria-hidden="true">★</span>
  <div class="small">{esc(FA['neutralite'])}</div></div>
</div></section>

<section class="section" id="insigne"><div class="wrap">
  <div class="grid g-2 gap-6">
    <div>
      <div class="section-head" data-reveal><div class="eyebrow">Progression</div><h2>{esc(IN['titre'])}</h2></div>
      <ul class="checklist" data-reveal>{etapes}</ul>
      <div class="alert alert-red mt-4" data-reveal><span class="ico" aria-hidden="true">!</span>
      <div class="small"><strong>Piège&nbsp;:</strong> {esc(IN['piege'])}</div></div>
    </div>
    <div>
      <figure class="img-frame" data-reveal>
        <img src="../../assets/images/misc/faction_badge_01.jpg" alt="Cartes d'identité plastifiées et figurines métalliques disposées sur une table en bois sombre" loading="lazy" decoding="async">
        <figcaption>L'insigne progresse même quand la sortie échoue {AI}</figcaption>
      </figure>
      <div class="card card-accent-gold mt-4" data-reveal>
        <div class="hud tiny txt-gold mb-2">NIVEAU 2 — LE PREMIER VRAI PALIER</div>
        <p class="small">{esc(IN['palier2'])}</p>
        <div class="divider" style="margin:.9rem 0"></div>
        <div class="hud tiny txt-green mb-2">NIVEAU MAXIMAL</div>
        <p class="small" style="margin:0">{esc(IN['palier_max'])}</p>
      </div>
    </div>
  </div>
</div></section>

<section class="section" id="chasse"><div class="wrap">
  <div class="grid g-2 gap-6">
    <figure class="img-frame" data-reveal>
      <img src="../../assets/images/misc/faction_hunt_01.jpg" alt="Vue plongeante depuis un parapet sur un dédale de ruelles désertiques à l'heure bleue" loading="lazy" decoding="async">
      <figcaption>Vous n'êtes pas marqué en permanence — vous êtes localisé par à-coups {AI}</figcaption>
    </figure>
    <div>
      <div class="section-head" data-reveal><div class="eyebrow">Mécanique</div><h2>{esc(CH['titre'])}</h2>
        <p class="lead">{esc(CH['contenu'])}</p></div>
      <div class="card card-accent-red" data-reveal><ul class="small">{cons}</ul></div>
    </div>
  </div>
</div></section>

<section class="section"><div class="wrap">
  <div class="section-head" data-reveal><div class="eyebrow">{len(FA['conseils'])} conseils</div>
    <h2>Ne pas se ruiner en jouant les factions</h2></div>
  <div class="grid g-auto-md gap-4">{tips}</div>
</div></section>

<section class="section" id="evenements"><div class="wrap">
  <div class="section-head" data-reveal><div class="eyebrow">{len(FA['evenements'])} événements</div>
    <h2>Le calendrier Brakkesh de la Saison 12</h2></div>
  <div class="alert alert-orange mb-4" data-reveal><span class="ico" aria-hidden="true">⏳</span>
  <div class="small">{esc(FA['urgence'])}</div></div>
  <div class="table-wrap" data-reveal><table class="df">
    <thead><tr><th>Événement</th><th>Dates</th><th>Ce que ça donne</th></tr></thead><tbody>{evs}</tbody></table></div>
  <p class="small muted mt-3">{esc(FA['_meta']['sources'])}</p>
</div></section>

<section class="section-sm"><div class="wrap">
  <div class="grid g-3 gap-4">
    <a class="card card-accent" href="index.html" data-reveal><h3 class="card-title" style="font-size:1rem">Toutes les cartes</h3>
      <p class="small muted">Brakkesh dans le détail, et les 11 autres cartes.</p></a>
    <a class="card card-accent" href="../saison-aurora/index.html" data-reveal data-delay="80"><h3 class="card-title" style="font-size:1rem">Saison Aurora</h3>
      <p class="small muted">Tous les jalons datés de la S12.</p></a>
    <a class="card card-accent" href="../hazard-ops/keycards.html" data-reveal data-delay="160"><h3 class="card-title" style="font-size:1rem">Cartes d'accès</h3>
      <p class="small muted">Lesquelles acheter sur Brakkesh.</p></a>
  </div>
</div></section>
"""

html = (head("Brakkesh 2.0 et les factions — Haavk, Ahsarah, insigne et chasses",
             "Guide complet de l'affrontement de factions de Brakkesh 2.0 dans Delta Force : Haavk Corp contre "
             "Garde Ahsarah, postes de contact, montée de l'insigne, niveau 2, chasses de faction et le calendrier "
             "des huit événements de la Saison Aurora.",
             depth=D, canonical="pages/cartes/brakkesh-factions.html",
             image="assets/images/heroes/brakkesh_factions_hero_01.jpg")
        + navbar(D) + '<main id="main">' + body + "</main>" + footer(D) + scripts(D))
print(write("pages/cartes/brakkesh-factions.html", html))
