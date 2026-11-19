#!/usr/bin/env python3
"""build_all.py — Régénère tout le site."""
import subprocess, sys, pathlib
HERE = pathlib.Path(__file__).resolve().parent
MODULES = ["build_home",
    "build_404", "build_debutant", "build_operateurs", "build_saison", "build_armurerie",
           "build_hazard", "build_meta",
    "build_departements", "build_detonation", "build_cartes",
    "build_az3",
    "build_factions",
    "build_hotzone", "build_outils", "build_encyclopedie"]
for m in MODULES:
    print(f"\n── {m} " + "─" * (46 - len(m)))
    r = subprocess.run([sys.executable, str(HERE / f"{m}.py")], cwd=HERE)
    if r.returncode != 0:
        sys.exit(f"ÉCHEC : {m}")
print("\n✅ Site régénéré.")
