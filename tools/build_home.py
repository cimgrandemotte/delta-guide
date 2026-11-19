#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_home.py — Génère index.html (le Quartier Général)."""

from site_common import (head, navbar, footer, scripts, write, esc,
                         load, SITE_NAME, SLOGAN, SEASON, audio_briefing)

s12 = load("season12")
ops = load("operators")
tiers = load("tier_list")
codes = load("daily_codes")

D = 0  # profondeur racine

# ---------------------------------------------------------------- HERO
hero = f"""<header class="hero">
  <div class="hero-bg" aria-hidden="true">
    <img src="assets/images/heroes/accueil_hero_01.jpg" alt="" fetchpriority="high" decoding="async">
  </div>
  <div class="wrap hero-content">
    <div class="eyebrow"><span class="pulse-dot" aria-hidden="true"></span> Saison 12 · Aurora · Live depuis le 10 novembre 2026</div>
    <h1 class="display">DELTA FORCE<br><span class="grad-text">THE ULTIMATE<br>OPERATOR'S GUIDE</span></h1>
    <p class="slogan">{esc(SLOGAN)}</p>
    <p class="lead">Le guide francophone le plus complet sur <strong>Delta Force</strong> : 19 opérateurs décortiqués,
    armurerie intégrale, 6 cartes d'extraction, 8 boss, 101 keycards, Black Site, Havoc Warfare, campagne Black Hawk Down
    et une batterie d'outils tactiques. Données vérifiées et sourcées, à jour de la <strong class="txt-orange">Saison Aurora</strong>.</p>
    <div class="mt-6" style="max-width:520px">{audio_briefing("accueil_briefing_01.mp3", "Quartier Général", "", 0)}</div>
    <div class="flex wrapf gap-3 mt-5">
      <a class="btn btn-primary btn-lg" href="pages/saison-aurora/index.html">Briefing Saison 12 <span aria-hidden="true">→</span></a>
      <a class="btn btn-ghost btn-lg" href="pages/operateurs/index.html">Les 19 opérateurs</a>
      <a class="btn btn-blue btn-lg" href="pages/outils/index.html">Outils tactiques</a>
    </div>
    <div class="mt-7 stat-grid" style="max-width:860px">
      <div class="stat-cell"><span class="n" data-count="19">0</span><span class="l">Opérateurs</span></div>
      <div class="stat-cell"><span class="n" data-count="101">0</span><span class="l">Keycards</span></div>
      <div class="stat-cell"><span class="n" data-count="1326">0</span><span class="l">Marqueurs cartes</span></div>
      <div class="stat-cell"><span class="n" data-count="8">0</span><span class="l">Boss</span></div>
      <div class="stat-cell"><span class="n" data-count="15">0</span><span class="l">Outils</span></div>
    </div>
  </div>
</header>"""

# ---------------------------------------------------------------- ALERTE S12
nouveautes = s12.get("nouveautes_majeures", [])[:6]
nouv_html = "".join(
    f"""<div class="card card-accent-orange" data-reveal data-delay="{i*60}">
      <div class="flex items-center justify-between gap-2 mb-2">
        <span class="badge badge-new">NOUVEAU S12</span>
      </div>
      <h3 class="card-title">{esc(n.get('titre', n.get('nom', '—')))}</h3>
      <p class="small muted">{esc(n.get('description', n.get('detail', '')))[:260]}</p>
    </div>""" for i, n in enumerate(nouveautes))

alerte = f"""<section class="section-sm">
  <div class="wrap">
    <div class="alert alert-red" data-reveal>
      <span class="ico" aria-hidden="true">⚠</span>
      <div><strong>PIÈGE DE LECTURE DES PATCH NOTES AURORA.</strong>
      Une grande partie des changements d'opérateurs annoncés le 7 novembre ne s'appliquent
      <em>qu'au mode Detonation</em> (Toxik, Raptor, Morse, Uluru, Gizmo, Stinger, Hackclaw, Vlinder, Desmoulins,
      ainsi que les GE2 de Luna et Shepherd). Ne les transposez pas à Operations ou Warfare.
      Sur ce guide, chaque changement précise <strong>son mode d'application</strong>.</div>
    </div>
  </div>
</section>"""

# ---------------------------------------------------------------- NOUVEAUTÉS
sec_nouv = f"""<section class="section" id="nouveautes">
  <div class="wrap">
    <div class="section-head" data-reveal>
      <div class="eyebrow">Mise à jour majeure</div>
      <h2>Ce qui change avec <span class="txt-orange">Aurora</span></h2>
      <p class="lead">Déployée le <strong>10 novembre 2026 à 02:00 UTC sans interruption de service</strong>,
      la Saison 12 apporte une nouvelle opératrice, un nouveau fusil d'assaut, la refonte de Brakkesh,
      une carte Warfare inédite et cinq munitions.</p>
    </div>
    <div class="grid g-auto-md">{nouv_html}</div>
    <div class="text-center mt-6" data-reveal>
      <a class="btn btn-orange" href="pages/saison-aurora/index.html">Tous les détails de la saison <span aria-hidden="true">→</span></a>
    </div>
  </div>
</section>"""

# ---------------------------------------------------------------- SECTIONS DU GUIDE
sections = [
    ("Les 19 opérateurs", "pages/operateurs/index.html", "assets/images/operators/operateurs_martelo_01.jpg",
     "Fiches complètes : capacités, forces, faiblesses, counters, synergies d'escouade et ordre de déblocage recommandé.",
     "19 fiches", "NOUVEAU S12"),
    ("Armurerie", "pages/armurerie/index.html", "assets/images/weapons/armurerie_an94_01.jpg",
     "Toutes les armes avec statistiques, accessoires et codes de build importables en un clic. AN-94 incluse.",
     "40+ armes", "NOUVEAU S12"),
    ("Hazard Operations", "pages/hazard-ops/index.html", "assets/images/heroes/hazardops_extraction_01.jpg",
     "Le mode extraction de A à Z : boucle de jeu, économie, Black Site, boss, keycards et survie.",
     "Mode PvPvE", ""),
    ("Cartes interactives", "pages/cartes/index.html", "assets/images/maps/cartes_brakkesh_01.jpg",
     "Six cartes d'extraction avec marqueurs filtrables : extractions, boss, keycards, loot et portes à code.",
     "1 326 marqueurs", "NOUVEAU S12"),
    ("Havoc Warfare", "pages/havoc-warfare/index.html", "assets/images/vehicles/warfare_tank_01.jpg",
     "Combat interarmes 32v32 : véhicules, tier list, contre-jeu anti-blindé et la nouvelle carte Zenith Port.",
     "32v32", "NOUVEAU S12"),
    ("Black Hawk Down", "pages/black-hawk-down/index.html", "assets/images/bhd/bhd_mogadiscio_01.jpg",
     "Les sept chapitres de la campagne coopérative gratuite, inspirée de la bataille de Mogadiscio.",
     "7 chapitres", ""),
    ("Les 8 boss", "pages/hazard-ops/boss.html", "assets/images/bosses/boss_ghroth_01.jpg",
     "Saeed, Reis, Blue Eagle, Desmoulins, Hudson, Warden Ghroth, Raven et H1000 : phases, points faibles et butin.",
     "8 boss", ""),
    ("Saison Aurora", "pages/saison-aurora/index.html", "assets/images/season/saison_aurora_01.jpg",
     "Patch notes complets, calendrier des 17 events datés, season pass et priorités à ne pas rater.",
     "17 events", "NOUVEAU S12"),
]

cards = ""
for i, (t, u, img, d, meta, badge) in enumerate(sections):
    b = f'<span class="badge badge-new">{badge}</span>' if badge else ""
    cards += f"""<a class="card card-media" href="{u}" data-reveal data-delay="{(i%4)*70}">
      <div class="thumb">
        <img src="{img}" alt="{esc(t)}" loading="lazy" decoding="async" width="800" height="500">
        <div class="ontop">{b}</div>
      </div>
      <div class="body">
        <h3 class="card-title">{esc(t)}</h3>
        <p class="small muted">{esc(d)}</p>
      </div>
      <div class="foot"><span>{esc(meta)}</span><span class="txt-green" aria-hidden="true">CONSULTER →</span></div>
    </a>"""

sec_sections = f"""<section class="section" id="guide">
  <div class="wrap">
    <div class="section-head" data-reveal>
      <div class="eyebrow">Centre de commandement</div>
      <h2>Explorer le guide</h2>
    </div>
    <div class="grid g-auto-md">{cards}</div>
  </div>
</section>"""

# ---------------------------------------------------------------- TIER LIST APERÇU
def tier_row(label, names, cls):
    chips = "".join(f'<span class="tier-item">{esc(n)}</span>' for n in names)
    return f"""<div class="tier-row">
      <div class="tier-label tier-{cls}" style="background:var(--tier-{cls.lower()})">{label}</div>
      <div class="tier-drop">{chips}</div>
    </div>"""

ops_t = tiers["operations"]["tiers"]
war_t = tiers["warfare"]["tiers"]
tl_ops = "".join(tier_row(k, v, k) for k, v in ops_t.items())
tl_war = "".join(tier_row(k, v, k) for k, v in war_t.items())

sec_tier = f"""<section class="section" id="tier-list">
  <div class="wrap">
    <div class="section-head" data-reveal>
      <div class="eyebrow">Méta · instantané du 15 novembre 2026</div>
      <h2>Tier list des opérateurs</h2>
      <p class="lead">La tier list de Delta Force <strong>n'est pas unique</strong> : un opérateur excellent en extraction
      peut être médiocre à 64 joueurs. Voici les deux classements qui comptent.</p>
    </div>
    <div class="tabs" role="tablist" data-reveal>
      <button class="active" data-tab="ops" role="tab" aria-selected="true">Hazard Operations</button>
      <button data-tab="war" role="tab" aria-selected="false">Havoc Warfare</button>
    </div>
    <div class="tabpanel active" data-panel="ops">
      <div class="tierlist">{tl_ops}</div>
    </div>
    <div class="tabpanel" data-panel="war">
      <div class="tierlist">{tl_war}</div>
    </div>
    <div class="alert alert-blue mt-5" data-reveal>
      <span class="ico" aria-hidden="true">ℹ</span>
      <div><strong>Snapshot daté.</strong> Ce classement reflète le méta au 15/11/2026, après la mise à jour d'équilibrage
      du 12 novembre. <a href="pages/encyclopedie/tier-list.html">Créer votre propre tier list</a> avec l'éditeur drag &amp; drop.</div>
    </div>
  </div>
</section>"""

# ---------------------------------------------------------------- CODES DU JOUR
codes_rows = "".join(
    f"""<tr><td><strong>{esc(c['carte'])}</strong></td>
      <td><span class="mono txt-green" style="font-size:1.1rem;letter-spacing:.2em">{esc(c['code'])}</span></td>
      <td class="small muted">{esc(c['emplacement'])}</td></tr>"""
    for c in codes["codes"])

sec_codes = f"""<section class="section" id="codes">
  <div class="wrap">
    <div class="grid" style="grid-template-columns:1.15fr .85fr;gap:var(--sp-6)" data-reveal>
      <div>
        <div class="section-head">
          <div class="eyebrow">Renseignement terrain</div>
          <h2>Codes de portes</h2>
        </div>
        <div class="alert mb-4">
          <span class="ico" aria-hidden="true">⏱</span>
          <div><strong>Ces codes changent tous les jours.</strong> Relevé du
          <strong>{esc(codes['_meta']['date_releve'])}</strong> — ils servent surtout à montrer le format et
          <strong>les emplacements des portes</strong>, eux permanents.
          Vérifiez toujours <a href="https://www.playdeltaforce.com/events/hq/" target="_blank" rel="noopener nofollow">la page officielle</a> avant un raid.</div>
        </div>
        <div class="table-wrap">
          <table class="df">
            <thead><tr><th>Carte</th><th>Code</th><th>Emplacement de la porte</th></tr></thead>
            <tbody>{codes_rows}</tbody>
          </table>
        </div>
        <a class="btn btn-ghost btn-sm mt-4" href="pages/astuces-pro/codes-portes.html">Page complète + secret CRACKED</a>
      </div>
      <div>
        <div class="hud-panel">
          <div class="hud-head"><span class="pulse-dot" aria-hidden="true"></span> Transmission prioritaire</div>
          <p class="mono small" data-typewriter data-speed="16">OPÉRATEUR. Saison Aurora active. Brakkesh reconfigurée : les factions Ahsarah et Haavk recrutent sur le terrain. Zenith Port sous le feu — attendez-vous à des vagues. Cinq nouvelles munitions en circulation, dont deux détonantes. Vérifiez votre niveau de pénétration avant de partir. Terminé.</p>
          <div class="radar mt-5" style="max-width:190px;margin-inline:auto" aria-hidden="true"></div>
        </div>
      </div>
    </div>
  </div>
</section>"""

# ---------------------------------------------------------------- OUTILS
outils = [
    ("Calculateur TTK / STK / DPS", "pages/outils/index.html#ttk", "Combien de balles, en combien de temps, contre quelle armure."),
    ("Simulateur de pénétration", "pages/outils/index.html#penetration", "Munition niveau 1→6 contre armure niveau 1→6, verdict immédiat."),
    ("Black Site Planner", "pages/hazard-ops/black-site.html#planner", "Ordre d'amélioration optimal et coûts en Tekniq Alloys."),
    ("Codes de build copiables", "pages/armurerie/builds.html", "40+ codes vérifiés, import en un clic dans le jeu."),
    ("Calculateur eDPI", "pages/outils/index.html#edpi", "Convertissez votre sensibilité sans perdre vos repères."),
    ("Générateur de loadout", "pages/outils/index.html#loadout", "Un défi aléatoire : opérateur, arme, munitions, carte."),
    ("Tier list drag & drop", "pages/encyclopedie/tier-list.html", "Composez et partagez votre propre classement."),
    ("Quiz tactique Aurora", "pages/outils/index.html#quiz", "12 questions sur la saison. Score honnête garanti."),
]
outils_html = "".join(
    f"""<a class="card card-accent" href="{u}" data-reveal data-delay="{(i%4)*60}">
      <h3 class="card-title" style="font-size:1rem">{esc(t)}</h3>
      <p class="small muted">{esc(d)}</p>
    </a>""" for i, (t, u, d) in enumerate(outils))

sec_outils = f"""<section class="section" id="outils">
  <div class="wrap">
    <div class="section-head" data-reveal>
      <div class="eyebrow">Boîte à outils</div>
      <h2>Outils tactiques</h2>
      <p class="lead">Quinze outils interactifs qui tournent entièrement dans votre navigateur, sans compte ni installation.</p>
    </div>
    <div class="grid g-auto-sm">{outils_html}</div>
  </div>
</section>"""

# ---------------------------------------------------------------- MÉTHODO
sec_methodo = f"""<section class="section" id="methodo">
  <div class="wrap wrap-narrow">
    <div class="hud-panel" data-reveal>
      <div class="hud-head">Méthodologie &amp; fiabilité</div>
      <div class="grid g-2 gap-5">
        <div>
          <h3 class="card-title">Données sourcées et datées</h3>
          <p class="small muted">Chaque chiffre de ce guide provient de sources publiques identifiées : patch notes,
          bases de données communautaires, guides spécialisés et retours de joueurs. Toutes les sources sont
          horodatées dans le journal de recherche du projet.</p>
        </div>
        <div>
          <h3 class="card-title">Écarts assumés</h3>
          <p class="small muted">Quand les sources contredisent une idée reçue, nous suivons les sources :
          <strong>19 opérateurs</strong> et non 18, <strong>5 nouvelles munitions</strong> et non 2,
          AZ3 Supercritical au <strong>18 décembre</strong> et pas au lancement. Les points incertains
          sont marqués « À CONFIRMER ».</p>
        </div>
      </div>
      <div class="divider"></div>
      <p class="tiny muted">Jeu en service continu : un guide est toujours un instantané. Dernière vérification complète
      des données le <strong>19 novembre 2026</strong>.</p>
    </div>
  </div>
</section>"""

html = (
    head(SITE_NAME,
         "Guide fan-made francophone ultra-complet sur Delta Force : 19 opérateurs, armurerie, 6 cartes interactives, "
         "8 boss, 101 keycards, Black Site, Havoc Warfare, campagne Black Hawk Down et 15 outils tactiques. "
         "À jour de la Saison 12 Aurora.",
         depth=D, canonical="")
    + navbar(D)
    + '<main id="main">'
    + hero + alerte + sec_nouv + sec_sections + sec_tier + sec_codes + sec_outils + sec_methodo
    + "</main>"
    + footer(D) + scripts(D)
)

print(write("index.html", html))
