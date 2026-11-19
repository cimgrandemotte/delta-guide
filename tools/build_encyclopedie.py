#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_encyclopedie.py — Encyclopédie : lexique, factions, chronologie, méthodologie."""

from site_common import (head, navbar, footer, scripts, write, esc,
                         load, crumbs, page_hero, audio_briefing)

ST = load("settings")
D = 2

LEXIQUE = [
    ("ADS", "Aim Down Sights — viser avec l'optique de l'arme. Le coefficient ADS règle la sensibilité dans ce mode."),
    ("Black Site", "Base personnelle du mode Operations. Onze stations à améliorer, uniquement en Tekniq Alloys."),
    ("CQB / CQC", "Close Quarters Battle / Combat — combat rapproché, typiquement en intérieur et en couloir."),
    ("Detonation", "Mode de jeu compétitif à manches. Attention : beaucoup de changements d'équilibrage lui sont exclusifs."),
    ("eDPI", "DPI × sensibilité en jeu. L'unité de comparaison réelle entre deux joueurs."),
    ("Extraction", "Point de sortie d'un raid. Sortir vivant valide tout le butin transporté."),
    ("Falloff", "Chute de dégâts avec la distance. Exprimée en paliers : par exemple 27 m / 40 m."),
    ("Hazard Operations", "Mode extraction PvPvE : on entre avec un kit, on pille, on ressort — ou on perd tout."),
    ("Havoc Warfare", "Mode de combat interarmes 32 contre 32, avec véhicules et objectifs."),
    ("Hot drop", "Atterrir volontairement dans une zone très disputée pour du loot rapide et du PvP immédiat."),
    ("Keycard", "Carte d'accès ouvrant une salle verrouillée. 0,05 kg, slot 1×1, nombre d'usages limité."),
    ("Loadout", "Configuration complète d'une arme ou d'un équipement. Partageable via un code d'import."),
    ("Operator / Opérateur", "Personnage jouable avec des capacités propres. 19 au total en Saison 12."),
    ("Pénétration", "Niveau de perforation d'une munition (1 à 6), à comparer au niveau d'armure adverse."),
    ("Pick rate", "Taux de sélection d'une arme ou d'un opérateur par la communauté. Indicateur de méta."),
    ("Safe Box", "Conteneur spécial dont le contenu survit à la mort. À réserver aux objets de mission critiques."),
    ("Stash", "Stockage permanent du joueur. Première station à améliorer au Black Site."),
    ("STK / TTK", "Shots To Kill / Time To Kill — nombre de balles et temps nécessaires pour mettre à terre."),
    ("Tekniq Alloys", "Monnaie de jeu principale. Tout le contenu de gameplay s'achète avec."),
    ("Third party", "Intervenir sur un combat déjà engagé entre deux autres escouades. La stratégie la plus rentable en Hard."),
    ("Tier list", "Classement de puissance relative. Dans Delta Force, il doit être séparé par mode."),
    ("Wipe", "Remise à zéro du stash entre saisons. Delta Force n'en pratique pas."),
]

FACTIONS = [
    ("G.T.I.", "Global Tactical Initiative — la force d'intervention jouée par les opérateurs. Structure de commandement du joueur.",
     "green"),
    ("Haavk Corporation", "Conglomérat militaro-industriel privé. Présent sur toutes les cartes via ses laboratoires, "
     "ses gardes d'élite et ses directeurs (Desmoulins, Hudson). À Brakkesh, Haavk veut protéger une livraison de cargo.",
     "orange"),
    ("Ahsarah Guard", "Faction armée locale contrôlant une partie de Brakkesh et de Layali Grove. "
     "Son commandant Reis est l'un des huit boss. À Brakkesh, Ahsarah veut reprendre la tour.",
     "red"),
    ("Administration de Tide Prison", "Corps pénitentiaire du complexe offshore, dirigé par Warden Ghroth, "
     "escorté de gardes d'élite et de porteurs de boucliers.",
     "blue"),
]

SAISONS = [
    ("Saison 12", "Aurora", "10 novembre 2026", "Martelo, AN-94, Brakkesh 2.0 et son système de factions, "
     "Zenith Port et l'événement Riptide, 5 nouvelles munitions, Loading Plans, tier Chroma, Firing Range 2.0, "
     "collaboration Phantom Blade Zero.", True),
    ("Saison 11", "—", "2026", "Carte Warfare The Mog inspirée de Black Hawk Down. Refonte de Layali Grove "
     "(Fisher's Hut, Rock Cavern, Underground Dock) et de Space City (Bon Lab, Black Chamber, Test Range). "
     "Grand gagnant : la K437.", False),
    ("Mise à jour", "Propriété du butin", "Septembre 2025", "Le butin des boss appartient désormais au joueur "
     "qui porte le coup fatal ou contribue le plus de dégâts.", False),
    ("Contenu", "Black Hawk Down", "21 février 2025", "Campagne solo et coopérative à 4 joueurs, gratuite pour tous. "
     "Sept chapitres sur la bataille de Mogadiscio (1993).", False),
]

lex = "".join(f"""<div class="card" data-search="{esc(t)} {esc(d)}" data-reveal>
    <h3 class="card-title" style="font-size:1rem">{esc(t)}</h3>
    <p class="small muted">{esc(d)}</p>
  </div>""" for t, d in LEXIQUE)

fac = "".join(f"""<div class="card card-accent{'' if c=='green' else '-'+c}" data-reveal>
    <h3 class="card-title">{esc(n)}</h3>
    <p class="small muted">{esc(d)}</p>
  </div>""" for n, d, c in FACTIONS)

chrono = "".join(f"""<div class="tl-item {'' if cur else 'done'}">
    <div class="tl-date">{esc(date)}</div>
    <h4 style="font-size:1.05rem">{esc(s)}{f' — {esc(nom)}' if nom != '—' else ''}
      {'<span class="badge badge-new">ACTUELLE</span>' if cur else ''}</h4>
    <p class="small muted">{esc(d)}</p>
  </div>""" for s, nom, date, d, cur in SAISONS)

plat = "".join(f'<tr><td class="hud tiny muted">{esc(k.title())}</td><td>{esc(v)}</td></tr>'
               for k, v in ST["plateformes"].items())

body = f"""
{page_hero("Référence", "<span class='grad-text'>Encyclopédie</span>",
           "Lexique, factions, chronologie des saisons et plateformes. "
           "Tout ce qu'il faut pour comprendre le reste du guide.",
           "assets/images/season/saison_aurora_01.jpg", D)}

<section class="section-sm"><div class="wrap">
  {crumbs([("Encyclopédie", None)], D)}
  <figure class="img-frame mb-5" data-reveal>
    <img src="../../assets/images/misc/encyclopedie_lore_01.jpg" alt="Vaste complexe industriel abandonné à l'heure dorée, tuyauterie rouillée et tours de refroidissement" loading="lazy" decoding="async">
    <figcaption>L'univers du jeu tient autant dans ses décors que dans ses dialogues. (illustration générée par IA, pas une capture du jeu)</figcaption>
  </figure>
  <div class="mb-4" style="max-width:560px">{audio_briefing("encyclopedie_briefing_01.mp3", "Encyclopédie", "", D)}</div>
  <div class="flex wrapf gap-3">
    <a class="btn btn-ghost btn-sm" href="tier-list.html">Tier list Saison 12</a>
    <a class="btn btn-ghost btn-sm" href="economie.html">Économie</a>
    <a class="btn btn-ghost btn-sm" href="../news/index.html">News</a>
  </div>
</div></section>

<section class="section"><div class="wrap">
  <div class="section-head" data-reveal>
    <div class="eyebrow">{len(LEXIQUE)} entrées</div><h2>Lexique</h2>
    <p class="lead">Les termes anglais sont conservés : ce sont ceux que vous verrez en jeu et sur les serveurs vocaux.</p>
  </div>
  <div class="hud-panel mb-5" data-filter-group data-filter-target="#lex-grid > div"
       data-filter-input="#lex-search" data-filter-count="#lex-count" data-reveal>
    <div class="field" style="max-width:340px">
      <label for="lex-search">Rechercher un terme</label>
      <input class="input" id="lex-search" type="search" placeholder="TTK, Safe Box, falloff…">
    </div>
    <p class="tiny muted mt-3"><span id="lex-count">{len(LEXIQUE)}</span> terme(s) affiché(s).</p>
  </div>
  <div class="grid g-auto-sm" id="lex-grid">{lex}</div>
</div></section>

<section class="section"><div class="wrap">
  <div class="section-head" data-reveal><div class="eyebrow">Univers</div><h2>Factions</h2></div>
  <div class="grid g-auto-md">{fac}</div>
</div></section>

<section class="section"><div class="wrap wrap-narrow">
  <div class="section-head" data-reveal><div class="eyebrow">Historique</div><h2>Chronologie</h2></div>
  <div class="timeline" data-reveal>{chrono}</div>
</div></section>

<section class="section"><div class="wrap">
  <div class="grid g-2 gap-6">
    <div>
      <div class="section-head" data-reveal><div class="eyebrow">Supports</div><h2>Plateformes</h2></div>
      <div class="table-wrap" data-reveal><table class="df" style="min-width:0"><tbody>{plat}</tbody></table></div>
    </div>
    <div>
      <div class="section-head" data-reveal><div class="eyebrow">Transparence</div><h2>Méthodologie</h2></div>
      <div class="card card-accent" data-reveal>
        <ul class="small">
          <li>Toutes les données proviennent de sources publiques identifiées et datées.</li>
          <li>Les sources sont listées avec leur date de publication et un niveau de confiance
          (officiel, élevé, moyen, communautaire) dans le fichier <code>research/sources_log.json</code> du projet.</li>
          <li>Quand les sources contredisent une idée reçue, nous suivons les sources et le signalons explicitement.</li>
          <li>Les faits non confirmés portent la mention <strong>« À CONFIRMER »</strong>.</li>
          <li>Chaque changement d'équilibrage précise <strong>son mode d'application</strong>
          (Operations, Warfare ou Detonation).</li>
          <li>Dernière vérification complète : <strong>19 novembre 2026</strong>.</li>
        </ul>
      </div>
      <div class="alert alert-blue mt-4" data-reveal><span class="ico" aria-hidden="true">🖼</span>
      <div>Toutes les illustrations de ce site sont des <strong>créations originales générées par IA</strong>
      à usage d'ambiance. Ce ne sont pas des captures du jeu et elles ne représentent pas fidèlement ses assets.</div></div>
    </div>
  </div>
</div></section>
"""
html = (head("Encyclopédie — lexique & univers", "Encyclopédie Delta Force : lexique de 22 termes, factions "
             "(G.T.I., Haavk, Ahsarah), chronologie des saisons, plateformes et méthodologie du guide.",
             depth=D, canonical="pages/encyclopedie/index.html",
             image="assets/images/season/saison_aurora_01.jpg")
        + navbar(D) + '<main id="main">' + body + "</main>" + footer(D) + scripts(D))
print(write("pages/encyclopedie/index.html", html))
