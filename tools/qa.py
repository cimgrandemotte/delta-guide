#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""qa.py — Contrôle qualité : liens internes, images, ancres, a11y basique, SEO."""
import re, pathlib, sys, html as _html
from urllib.parse import urlparse, unquote

ROOT = pathlib.Path(__file__).resolve().parent.parent
pages = sorted(ROOT.rglob("*.html"))
errors, warns = [], []
total_links = total_imgs = 0

for p in pages:
    if "node_modules" in str(p):
        continue
    rel = p.relative_to(ROOT)
    s = p.read_text(encoding="utf-8")

    # --- liens internes
    for m in re.finditer(r'href="([^"]+)"', s):
        href = m.group(1)
        if href.startswith(("http://", "https://", "mailto:", "data:", "#", "javascript:")):
            continue
        total_links += 1
        path, _, frag = href.partition("#")
        if not path:
            continue
        target = (p.parent / unquote(path)).resolve()
        if not target.exists():
            errors.append(f"[LIEN MORT] {rel} → {href}")

    # --- images
    for m in re.finditer(r'<img[^>]*src="([^"]+)"', s):
        src = m.group(1)
        if src.startswith(("http", "data:")):
            continue
        total_imgs += 1
        t = (p.parent / unquote(src)).resolve()
        if not t.exists():
            errors.append(f"[IMAGE MANQUANTE] {rel} → {src}")

    # --- a11y / SEO
    if '<html lang="fr">' not in s:
        errors.append(f"[A11Y] {rel} : attribut lang manquant")
    if s.count("<h1") != 1:
        warns.append(f"[SEO] {rel} : {s.count('<h1')} balise(s) h1 (1 attendue)")
    if 'name="description"' not in s:
        errors.append(f"[SEO] {rel} : meta description manquante")
    if 'rel="canonical"' not in s:
        warns.append(f"[SEO] {rel} : canonical manquant")
    if 'property="og:image"' not in s:
        warns.append(f"[SEO] {rel} : og:image manquant")
    for m in re.finditer(r'<img(?![^>]*\balt=)[^>]*>', s):
        errors.append(f"[A11Y] {rel} : <img> sans attribut alt → {m.group(0)[:70]}")
    if 'id="main"' not in s:
        warns.append(f"[A11Y] {rel} : repère #main absent")
    if "skip-link" not in s:
        warns.append(f"[A11Y] {rel} : lien d'évitement absent")
    # liens externes sans rel
    for m in re.finditer(r'<a\b[^>]*target="_blank"[^>]*>', s):
        if 'rel=' not in m.group(0):
            warns.append(f"[SÉCU] {rel} : target=_blank sans rel → {m.group(0)[:70]}")
    # texte résiduel de template
    for bad in ("None", "{'", "}}", "KeyError"):
        if bad == "None" and re.search(r'>\s*None\s*<', s):
            warns.append(f"[CONTENU] {rel} : valeur « None » visible")

print("=" * 66)
print(f"  QA — {len(pages)} pages · {total_links} liens internes · {total_imgs} images")
print("=" * 66)
if errors:
    print(f"\n❌ {len(errors)} ERREUR(S)")
    for e in errors[:50]:
        print("   " + e)
else:
    print("\n✅ Aucune erreur bloquante.")
if warns:
    print(f"\n⚠️  {len(warns)} AVERTISSEMENT(S)")
    for w in warns[:50]:
        print("   " + w)
else:
    print("✅ Aucun avertissement.")
print()
sys.exit(1 if errors else 0)
