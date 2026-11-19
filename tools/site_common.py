#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
site_common.py — Layout partagé du site « Delta Force — The Ultimate Operator's Guide ».
Génère head, navbar, footer et squelette de page. Utilisé par les scripts build_*.py.
"""

import json
import os
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE_NAME = "Delta Force — The Ultimate Operator's Guide"
SLOGAN = "Every Raid. Every Operator. Every Edge."
SITE_URL = "https://delta-guide.duckdns.org"
SEASON = "Saison 12 — Aurora"
BUILD_DATE = "2026-11-19"


def load(name):
    with open(ROOT / "data" / f"{name}.json", encoding="utf-8") as f:
        return json.load(f)


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


# --------------------------------------------------------------------------
# Structure de navigation (titre, href relatif à la racine, enfants)
# --------------------------------------------------------------------------
NAV = [
    ("QG", "index.html", []),
    ("Débutant", "pages/debutant/index.html", []),
    ("Opérateurs", "pages/operateurs/index.html", [
        ("Les 19 opérateurs", "pages/operateurs/index.html"),
        ("Contre-jeu des capacités", "pages/operateurs/contre-jeu.html"),
    ]),
    ("Armurerie", "pages/armurerie/index.html", [
        ("Toutes les armes", "pages/armurerie/index.html"),
        ("Munitions & pénétration", "pages/armurerie/munitions.html"),
        ("Codes de build", "pages/armurerie/builds.html"),
        ("Gunsmith expliqué", "pages/armurerie/gunsmith.html"),
    ]),
    ("Detonation", "pages/detonation/index.html", []),
    ("Hazard Ops", "pages/hazard-ops/index.html", [
        ("Guide du mode", "pages/hazard-ops/index.html"),
        ("Mandel Brick & Classé", "pages/hazard-ops/mandel-brick.html"),
        ("Black Site", "pages/hazard-ops/black-site.html"),
        ("Les 8 boss", "pages/hazard-ops/boss.html"),
        ("Keycards", "pages/hazard-ops/keycards.html"),
        ("Hot Zone 3v3v3", "pages/hazard-ops/hot-zone.html"),
        ("Départements", "pages/hazard-ops/departements.html"),
    ]),
    ("Cartes", "pages/cartes/index.html", [
        ("Les 12 cartes", "pages/cartes/index.html"),
        ("AZ3 & Supercritical", "pages/cartes/az3-supercritical.html"),
        ("Brakkesh & factions", "pages/cartes/brakkesh-factions.html"),
    ]),
    ("Warfare", "pages/havoc-warfare/index.html", []),
    ("BHD", "pages/black-hawk-down/index.html", []),
    ("Aurora", "pages/saison-aurora/index.html", []),
    ("Pro", "pages/astuces-pro/index.html", [
        ("Réglages & astuces", "pages/astuces-pro/index.html"),
        ("Duels & jeu en solo", "pages/astuces-pro/duels.html"),
        ("Codes de portes", "pages/astuces-pro/codes-portes.html"),
    ]),
    ("Encyclopédie", "pages/encyclopedie/index.html", [
        ("Lexique & univers", "pages/encyclopedie/index.html"),
        ("Tier list S12", "pages/encyclopedie/tier-list.html"),
        ("Économie", "pages/encyclopedie/economie.html"),
        ("News", "pages/news/index.html"),
    ]),
    ("Outils", "pages/outils/index.html", [
        ("Calculateurs tactiques", "pages/outils/index.html"),
        ("Artisanat & enchères", "pages/outils/artisanat.html"),
    ]),
]

FOOTER_COLS = [
    ("Modes de jeu", [
        ("Hazard Operations", "pages/hazard-ops/index.html"),
        ("Havoc Warfare", "pages/havoc-warfare/index.html"),
        ("Black Hawk Down", "pages/black-hawk-down/index.html"),
        ("Cartes interactives", "pages/cartes/index.html"),
    ]),
    ("Références", [
        ("Les 19 opérateurs", "pages/operateurs/index.html"),
        ("Armurerie complète", "pages/armurerie/index.html"),
        ("Munitions & pénétration", "pages/armurerie/munitions.html"),
        ("Tier list Saison 12", "pages/encyclopedie/tier-list.html"),
    ]),
    ("Outils & astuces", [
        ("Outils tactiques", "pages/outils/index.html"),
        ("Codes de portes du jour", "pages/astuces-pro/codes-portes.html"),
        ("Black Site Planner", "pages/hazard-ops/black-site.html"),
        ("Réglages pro", "pages/astuces-pro/index.html"),
    ]),
]


def rel(depth):
    return "../" * depth if depth else ""


# --------------------------------------------------------------------------
def head(title, desc, depth=0, canonical="", extra_head="", image="assets/images/heroes/accueil_hero_01.jpg"):
    b = rel(depth)
    full_title = title if title == SITE_NAME else f"{title} | Delta Force Guide"
    canon = f"{SITE_URL}/{canonical}" if canonical else SITE_URL
    schema = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": full_title,
        "description": desc,
        "inLanguage": "fr-FR",
        "isPartOf": {"@type": "WebSite", "name": SITE_NAME, "url": SITE_URL},
        "about": {
            "@type": "VideoGame",
            "name": "Delta Force",
            "publisher": [{"@type": "Organization", "name": "Level Infinite"},
                          {"@type": "Organization", "name": "Garena"}],
            "author": {"@type": "Organization", "name": "Team Jade"},
            "gamePlatform": ["PC", "PlayStation 5", "Xbox Series X|S", "iOS", "Android"],
            "genre": ["Tactical shooter", "Extraction shooter", "FPS"],
        },
    }
    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(full_title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="theme-color" content="#080B0F">
<meta name="author" content="Guide fan-made communautaire">
<link rel="canonical" href="{canon}">
<meta property="og:type" content="website">
<meta property="og:locale" content="fr_FR">
<meta property="og:site_name" content="{esc(SITE_NAME)}">
<meta property="og:title" content="{esc(full_title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{SITE_URL}/{image}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(full_title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{SITE_URL}/{image}">
<link rel="alternate" hreflang="fr" href="{canon}">
<link rel="alternate" hreflang="x-default" href="{canon}">
<link rel="manifest" href="{b}manifest.json">
<link rel="icon" type="image/jpeg" href="{b}assets/images/logos/favicon.jpg"><link rel="apple-touch-icon" href="{b}assets/images/logos/apple-touch-icon.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Exo+2:wght@400;600;700;800;900&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&family=Orbitron:wght@700;900&family=Rajdhani:wght@500;600;700&family=Share+Tech+Mono&display=swap" media="print" onload="this.media='all'">
<noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Exo+2:wght@400;600;700;800;900&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&family=Orbitron:wght@700;900&family=Rajdhani:wght@500;600;700&family=Share+Tech+Mono&display=swap"></noscript>
<link rel="stylesheet" href="{b}assets/css/design-system.css">
<link rel="stylesheet" href="{b}assets/css/animations.css">
<link rel="stylesheet" href="{b}assets/css/components.css">
<link rel="stylesheet" href="{b}assets/css/responsive.css">
<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>
{extra_head}
</head>
<body>
<a class="skip-link" href="#main">Aller au contenu principal</a>
<div class="scanlines" aria-hidden="true"></div>
<div class="noise" aria-hidden="true"></div>
<div class="boot" aria-hidden="true"><div class="boot-inner">
  <div class="hud txt-green" style="font-size:.78rem;letter-spacing:.3em">INITIALISATION DU SYSTÈME</div>
  <div class="boot-bar"><i></i></div>
</div></div>
"""


# --------------------------------------------------------------------------
def navbar(depth=0):
    b = rel(depth)
    items = []
    for label, href, children in NAV:
        if children:
            sub = "".join(f'<a href="{b}{h}">{esc(t)}</a>' for t, h in children)
            items.append(
                f'<div class="nav-group"><a href="{b}{href}">{esc(label)}</a>'
                f'<div class="nav-panel">{sub}</div></div>')
        else:
            items.append(f'<a href="{b}{href}">{esc(label)}</a>')
    links = "".join(items)
    return f"""<nav class="site-nav" aria-label="Navigation principale">
  <div class="wrap nav-inner">
    <a class="brand" href="{b}index.html" aria-label="Accueil — Delta Force Ultimate Operator's Guide">
      <span class="brand-mark" aria-hidden="true">DF</span>
      <span class="brand-txt"><b>Delta Force</b><span>Operator's Guide</span></span>
    </a>
    <div class="nav-links" id="nav-links">{links}</div>
    <div class="nav-actions">
      <button class="search-trigger" aria-label="Ouvrir la recherche globale">
        <span aria-hidden="true">⌕</span><span class="sr-only">Rechercher</span><kbd>Ctrl K</kbd>
      </button>
      <button class="nav-burger" aria-label="Ouvrir le menu" aria-expanded="false" aria-controls="nav-links"><span></span></button>
    </div>
  </div>
</nav>
<div class="search-modal" role="dialog" aria-modal="true" aria-label="Recherche globale">
  <div class="search-box">
    <input type="search" placeholder="Rechercher un opérateur, une arme, une carte, un outil…" aria-label="Champ de recherche" autocomplete="off">
    <div class="search-results"></div>
  </div>
</div>
"""


# --------------------------------------------------------------------------
def footer(depth=0):
    b = rel(depth)
    cols = ""
    for title, links in FOOTER_COLS:
        lis = "".join(f'<li><a href="{b}{h}">{esc(t)}</a></li>' for t, h in links)
        cols += f'<div class="footer-col"><h4>{esc(title)}</h4><ul>{lis}</ul></div>'
    return f"""<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div class="footer-col">
        <a class="brand mb-3" href="{b}index.html">
          <span class="brand-mark" aria-hidden="true">DF</span>
          <span class="brand-txt"><b>Delta Force</b><span>Operator's Guide</span></span>
        </a>
        <p class="small muted">Guide communautaire francophone ultra-complet sur Delta Force.
        Opérateurs, armes, cartes, boss, économie, outils tactiques — mis à jour pour la {esc(SEASON)}.</p>
        <p class="hud tiny txt-green mt-3">{esc(SLOGAN)}</p>
      </div>
      {cols}
    </div>
    <div class="legal-box">
      <strong>Mentions légales &amp; crédits.</strong> Ce site est un <strong>guide fan-made non officiel</strong>,
      réalisé par des joueurs pour des joueurs, à but informatif et sans but lucratif.
      <em>Delta Force</em> est développé par <strong>Team Jade</strong> (<strong>TiMi Studio Group</strong>) et édité par
      <strong>Level Infinite</strong> et <strong>Garena</strong> selon les régions.
      Toutes les marques, noms, logos, images, personnages et éléments de jeu cités appartiennent à leurs propriétaires respectifs.
      Ce site n'est ni affilié, ni approuvé, ni sponsorisé par Team Jade, TiMi Studio Group, Level Infinite, Garena ou Tencent.
      Les illustrations du site sont des <strong>créations originales générées par IA</strong> à usage d'ambiance : elles ne
      représentent pas des captures du jeu. Les données de gameplay proviennent de sources publiques datées, listées dans
      <code>research/sources_log.json</code>. Le jeu évoluant en continu, vérifiez toujours les patch notes officiels sur
      <a href="https://www.playdeltaforce.com/" rel="noopener nofollow" target="_blank">playdeltaforce.com</a>.
    </div>
    <div class="footer-bottom">
      <span>© <span data-year>2026</span> — Guide fan-made. Contenu sous licence MIT (code).</span>
      <span class="hud">BUILD {BUILD_DATE} · {esc(SEASON).upper()}</span>
    </div>
  </div>
</footer>
<script src="{b}assets/js/app.js"></script>
<script src="{b}assets/js/search.js" defer></script>
"""


def scripts(depth=0, extra=""):
    return extra + "\n</body>\n</html>\n"


# --------------------------------------------------------------------------
def crumbs(items, depth=0):
    """items: liste de (label, href_relatif_racine|None)"""
    b = rel(depth)
    out = ['<nav class="crumbs" aria-label="Fil d\'Ariane">']
    out.append(f'<a href="{b}index.html">QG</a>')
    for label, href in items:
        out.append('<span class="sep" aria-hidden="true">›</span>')
        if href:
            out.append(f'<a href="{b}{href}">{esc(label)}</a>')
        else:
            out.append(f'<span aria-current="page">{esc(label)}</span>')
    out.append("</nav>")
    return "".join(out)


def page_hero(eyebrow, title, lead, image, depth=0, badge=""):
    b = rel(depth)
    badge_html = f'<span class="badge badge-new">{esc(badge)}</span>' if badge else ""
    img = f'<div class="hero-bg" aria-hidden="true"><img src="{b}{image}" alt="" loading="eager" decoding="async"></div>' if image else ""
    return f"""<header class="page-hero">
  {img}
  <div class="wrap page-hero-content">
    <div class="eyebrow">{esc(eyebrow)}</div>
    <h1 class="display">{title} {badge_html}</h1>
    <p class="lead mt-3">{lead}</p>
  </div>
</header>"""


def write(path, html):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(html)
    return f"{path}  ({len(html):,} octets)".replace(",", " ")


def audio_briefing(file, title, duree="", depth=0):
    """Lecteur audio de briefing (dégradation gracieuse si le fichier manque)."""
    b = rel(depth)
    return f"""<div class="audio-player" data-reveal>
  <button class="play" aria-label="Lire le briefing audio : {esc(title)}">▶</button>
  <div class="meta">
    <b>Briefing audio — {esc(title)}</b>
    <span>NARRATION FR{' · ' + esc(duree) if duree else ''} · SYNTHÈSE VOCALE</span>
  </div>
  <div class="audio-bars" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i></div>
  <audio preload="none" src="{b}assets/audio/briefings/{file}"></audio>
</div>"""
