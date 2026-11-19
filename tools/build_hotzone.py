#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_hotzone.py — Hot Zone 3v3v3, le terrain d'entraînement gratuit."""

from site_common import (head, navbar, footer, scripts, write, esc,
                         load, crumbs, page_hero, audio_briefing)

HZ = load("hot_zone")
D = 2

EQ = HZ["equipement"]

regles = "".join(f"""<li class="check-row"><span class="num txt-gold mono">{i+1}</span>
    <span>{esc(r)}</span></li>""" for i, r in enumerate(HZ["regles"]))

pourquoi = "".join(f"<li>{esc(x)}</li>" for x in HZ["pourquoi"])

tac = "".join(f"""<article class="card card-accent-blue" data-reveal data-delay="{i*60}">
    <div class="hud tiny txt-blue mb-2">TACTIQUE {i+1:02d}</div>
    <h3 class="card-title" style="font-size:1rem">{esc(t['titre'])}</h3>
    <p class="small muted">{esc(t['detail'])}</p>
  </article>""" for i, t in enumerate(HZ["tactiques"]))

ops = "".join(f'<span class="chip" data-val="{esc(o)}">{esc(o)}</span>' for o in HZ["operateurs"])

body = f"""
{page_hero("Operations · 3v3v3", "Hot <span class='grad-text'>Zone</span>",
           "Trois équipes, petites cartes, équipement fourni. Votre réserve n'est jamais touchée — "
           "c'est le meilleur entraînement gratuit du jeu.",
           "assets/images/misc/hot_zone_01.jpg", D, badge="Zéro risque")}

<section class="section-sm"><div class="wrap">
  {crumbs([("Hazard Ops", "index.html"), ("Hot Zone", None)], D)}
  <div class="mb-4" style="max-width:560px">{audio_briefing("hotzone_briefing_01.mp3", "Hot Zone", "", D)}</div>
  <div class="alert alert-orange" data-reveal><span class="ico" aria-hidden="true">!</span>
  <div class="small">{esc(HZ['_meta']['avertissement'])}</div></div>
</div></section>

<section class="section"><div class="wrap">
  <div class="grid g-2 gap-6">
    <div>
      <div class="section-head" data-reveal><div class="eyebrow">Le principe</div>
        <h2>Le seul mode d'Operations où vous ne risquez rien</h2>
        <p class="lead">{esc(HZ['principe'])}</p></div>
      <div class="card card-accent-green" data-reveal>
        <h3 class="card-title" style="font-size:1rem">Pourquoi y passer du temps</h3>
        <ul class="small">{pourquoi}</ul>
      </div>
    </div>
    <div>
      <div class="section-head" data-reveal><div class="eyebrow">{len(HZ['regles'])} règles</div><h2>Comment se gagne une manche</h2></div>
      <ul class="checklist" data-reveal>{regles}</ul>
    </div>
  </div>
</div></section>

<section class="section"><div class="wrap wrap-narrow">
  <div class="card card-accent-gold" data-reveal>
    <h2 class="card-title" style="font-size:1.15rem">{esc(EQ['titre'])}</h2>
    <p class="small">{esc(EQ['contenu'])}</p>
    <div class="divider" style="margin:1rem 0"></div>
    <div class="hud tiny txt-gold mb-2">L'ASTUCE QUI FAIT GAGNER DES MANCHES</div>
    <p class="small" style="margin:0">{esc(EQ['astuce'])}</p>
  </div>
</div></section>

<section class="section"><div class="wrap">
  <div class="section-head" data-reveal>
    <div class="eyebrow">{len(HZ['tactiques'])} tactiques</div><h2>Jouer à trois équipes, pas à deux</h2>
    <p class="lead">Le Hot Zone n'est pas un affrontement classique avec un camp en trop. La présence d'une troisième
    escouade change l'intégralité du calcul : celui qui entre le premier dans un échange le perd presque toujours.</p>
  </div>
  <div class="grid g-auto-md gap-4 mb-5">{tac}</div>
  <div class="grid g-2 gap-4">
    <div class="card card-accent-green" data-reveal>
      <h3 class="card-title" style="font-size:1rem">Opérateurs qui ressortent</h3>
      <div class="chips mb-2">{ops}</div>
      <p class="small muted" style="margin:0">{esc(HZ['note_operateurs'])}</p>
    </div>
    <div class="card card-accent-orange" data-reveal data-delay="80">
      <h3 class="card-title" style="font-size:1rem">La limite du mode</h3>
      <p class="small" style="margin:0">{esc(HZ['limite'])}</p>
    </div>
  </div>
</div></section>

<section class="section-sm"><div class="wrap">
  <div class="grid g-3 gap-4">
    <a class="card card-accent" href="../astuces-pro/duels.html" data-reveal>
      <h3 class="card-title" style="font-size:1rem">Duels &amp; angles</h3>
      <p class="small muted">Ce que vous devez travailler pendant vos manches de Hot Zone.</p></a>
    <a class="card card-accent" href="mandel-brick.html" data-reveal data-delay="80">
      <h3 class="card-title" style="font-size:1rem">MandelBrick</h3>
      <p class="small muted">Le décodage, ici comme en Operations.</p></a>
    <a class="card card-accent" href="../debutant/index.html" data-reveal data-delay="160">
      <h3 class="card-title" style="font-size:1rem">Je débute</h3>
      <p class="small muted">Vos sept premières heures, sans perdre d'argent.</p></a>
  </div>
</div></section>
"""

html = (head("Hot Zone 3v3v3 — règles, économie de manches et tactiques",
             "Guide du mode Hot Zone de Delta Force : 3v3v3 sans risque pour votre réserve, décodage du MandelBrick, "
             "économie de points par manche, cinq tactiques à trois équipes et les opérateurs qui y fonctionnent.",
             depth=D, canonical="pages/hazard-ops/hot-zone.html",
             image="assets/images/misc/hot_zone_01.jpg")
        + navbar(D) + '<main id="main">' + body + "</main>" + footer(D) + scripts(D))
print(write("pages/hazard-ops/hot-zone.html", html))
