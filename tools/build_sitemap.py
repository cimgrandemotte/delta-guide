#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_sitemap.py — Génère sitemap.xml et robots.txt à partir des pages existantes."""
import pathlib, datetime
from site_common import ROOT, SITE_URL

TODAY = "2026-11-19"
PRIO = {"index.html": ("1.0", "daily")}
DEFAULT = ("0.8", "weekly")
SPECIAL = {
    "pages/astuces-pro/codes-portes.html": ("0.9", "daily"),
    "pages/news/index.html": ("0.9", "daily"),
    "pages/saison-aurora/index.html": ("1.0", "daily"),
    "pages/operateurs/index.html": ("0.9", "weekly"),
    "pages/armurerie/index.html": ("0.9", "weekly"),
    "pages/cartes/index.html": ("0.9", "weekly"),
    "pages/outils/index.html": ("0.9", "monthly"),
}

# 404.html est une page d'erreur : elle ne doit jamais être soumise à l'indexation.
EXCLUS = {"404.html"}

pages = sorted(p.relative_to(ROOT).as_posix() for p in ROOT.rglob("*.html")
               if "node_modules" not in str(p)
               and p.relative_to(ROOT).as_posix() not in EXCLUS)

urls = []
for rel in pages:
    prio, freq = PRIO.get(rel) or SPECIAL.get(rel) or DEFAULT
    loc = SITE_URL + "/" + ("" if rel == "index.html" else rel)
    urls.append(f"""  <url>
    <loc>{loc}</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>{freq}</changefreq>
    <priority>{prio}</priority>
    <xhtml:link rel="alternate" hreflang="fr" href="{loc}"/>
  </url>""")

xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xhtml="http://www.w3.org/1999/xhtml">
{chr(10).join(urls)}
</urlset>
"""
(ROOT / "sitemap.xml").write_text(xml, encoding="utf-8")

robots = f"""# Delta Force — The Ultimate Operator's Guide (fan-made)
User-agent: *
Allow: /
Disallow: /tools/
Disallow: /research/

Sitemap: {SITE_URL}/sitemap.xml
"""
(ROOT / "robots.txt").write_text(robots, encoding="utf-8")
print(f"sitemap.xml — {len(urls)} URLs")
print("robots.txt — mis à jour")
