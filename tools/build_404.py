#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_404.py — page 404 (référencée par netlify.toml et vercel.json)."""

from site_common import head, navbar, footer, scripts, write

D = 0

body = """
<section class="section" style="min-height:62vh;display:flex;align-items:center">
  <div class="wrap wrap-narrow" style="text-align:center">
    <div class="hud tiny txt-red" data-reveal>ERREUR 404 · LIAISON PERDUE</div>
    <h1 class="display" style="font-size:clamp(3rem,12vw,7rem);margin:.4rem 0 .8rem">
      <span class="grad-text">HORS ZONE</span></h1>
    <p class="lead" data-reveal>Cette page n'existe pas, ou elle a été déplacée lors d'une mise à jour du guide.
    Rien n'est perdu : tout le contenu reste accessible depuis le QG.</p>
    <div class="grid g-3 gap-4 mt-5" style="text-align:left">
      <a class="card card-accent-green" href="index.html" data-reveal>
        <h2 class="card-title" style="font-size:1rem">Retour au QG</h2>
        <p class="small muted">La synthèse de la Saison 12 et l'accès à l'ensemble du guide.</p></a>
      <a class="card card-accent-blue" href="pages/debutant/index.html" data-reveal data-delay="80">
        <h2 class="card-title" style="font-size:1rem">Je débute</h2>
        <p class="small muted">Vos sept premières heures, sans perdre d'argent inutilement.</p></a>
      <a class="card card-accent-orange" href="pages/astuces-pro/codes-portes.html" data-reveal data-delay="160">
        <h2 class="card-title" style="font-size:1rem">Codes du jour</h2>
        <p class="small muted">Les codes de portes quotidiens des six cartes d'Operations.</p></a>
    </div>
    <p class="small muted mt-5" data-reveal>Vous pouvez aussi ouvrir la recherche avec la touche
      <kbd class="mono">/</kbd> depuis n'importe quelle page.</p>
  </div>
</section>
"""

html = (head("Page introuvable — Delta Force Ultimate Guide",
             "Cette page n'existe pas ou a été déplacée. Retournez au QG du guide Delta Force.",
             depth=D, canonical="404.html")
        + navbar(D) + '<main id="main">' + body + "</main>" + footer(D) + scripts(D))
print(write("404.html", html))
