#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_outils.py — Page Outils tactiques, Astuces pro, Codes de portes,
   Encyclopédie, Tier list éditable, Économie."""

from site_common import (head, navbar, footer, scripts, write, esc,
                         load, crumbs, page_hero, audio_briefing)

ST = load("settings")
CD = load("daily_codes")
TL = load("tier_list")
EC = load("economy")
OP = load("operators")
D = 2
TOOLS_JS = '<script src="../../assets/js/tools.js"></script>'

opt_lvl = "".join(f'<option value="{i}">Niveau {i}</option>' for i in range(1, 7))

# =========================================================== OUTILS
body = f"""
{page_hero("Boîte à outils", "Outils <span class='grad-text'>tactiques</span>",
           "Des calculateurs qui tournent entièrement dans votre navigateur. Aucun compte, aucune installation, "
           "aucune donnée envoyée nulle part.",
           "assets/images/weapons/armurerie_an94_01.jpg", D)}

<section class="section-sm"><div class="wrap">
  {crumbs([("Outils", None)], D)}
  <figure class="img-frame mb-5" data-reveal>
    <img src="../../assets/images/misc/outils_calcul_01.jpg" alt="Bureau d'analyse de campagne avec calculatrice mécanique, pied à coulisse et papier millimétré" loading="lazy" decoding="async">
    <figcaption>Calculer avant d'acheter coûte trente secondes et évite des millions d'Alloys. (illustration générée par IA, pas une capture du jeu)</figcaption>
  </figure>
  <div class="mb-4" style="max-width:560px">{audio_briefing("outils_briefing_01.mp3", "Outils", "", D)}</div>
  <figure class="img-frame mb-5" data-reveal><img src="../../assets/images/heroes/outils_hero_01.jpg" alt="Salle d'opérations tactique avec écrans de données et maquette holographique" loading="lazy" decoding="async"><figcaption>Six calculateurs pour arrêter de jouer à l'instinct (illustration générée par IA, pas une capture du jeu)</figcaption></figure>
  <div class="chips" data-reveal>
    <a class="chip" href="#ttk">TTK / STK / DPS</a>
    <a class="chip" href="#penetration">Pénétration</a>
    <a class="chip" href="#raid">Rentabilité de raid</a>
    <a class="chip" href="#edpi">eDPI</a>
    <a class="chip" href="#loadout">Loadout aléatoire</a>
    <a class="chip" href="#quiz">Quiz tactique</a>
    <a class="chip" href="../encyclopedie/tier-list.html">Tier list éditable</a>
    <a class="chip" href="../hazard-ops/black-site.html#planner">Black Site Planner</a>
    <a class="chip" href="../armurerie/builds.html">Codes de build</a>
    <a class="chip" href="../astuces-pro/codes-portes.html">Codes de portes</a>
    <a class="chip" href="../cartes/index.html">Cartes interactives</a>
  </div>
</div></section>

<section class="section" id="ttk"><div class="wrap">
  <div class="section-head" data-reveal>
    <div class="eyebrow">Outil 01</div><h2>Calculateur TTK / STK / DPS</h2>
    <p class="lead">Combien de balles pour mettre à terre, en combien de temps, contre quelle armure.</p>
  </div>
  <div class="hud-panel" data-reveal>
    <div class="grid g-4 gap-4 mb-5">
      <div class="field"><label for="ttk-weapon">Arme</label><select class="input" id="ttk-weapon"></select></div>
      <div class="field"><label for="ttk-ammo">Niveau de munition</label>
        <select class="input" id="ttk-ammo">{opt_lvl}</select></div>
      <div class="field"><label for="ttk-armor">Niveau d'armure cible</label>
        <select class="input" id="ttk-armor">{opt_lvl}</select></div>
      <div class="field"><label for="ttk-zone">Zone d'impact</label>
        <select class="input" id="ttk-zone">
          <option value="torse" selected>Torse</option><option value="tete">Tête</option>
          <option value="abdomen">Abdomen</option><option value="bras">Bras</option><option value="jambes">Jambes</option>
        </select></div>
    </div>
    <div id="ttk-out"></div>
  </div>
</div></section>

<section class="section" id="penetration"><div class="wrap">
  <div class="section-head" data-reveal>
    <div class="eyebrow">Outil 02</div><h2>Simulateur de pénétration T1 → T6</h2>
    <p class="lead">La mécanique qui décide de la majorité des duels. Croisez votre munition et l'armure adverse.</p>
  </div>
  <div class="hud-panel mb-5" data-reveal>
    <div class="grid g-2 gap-4 mb-4">
      <div class="field"><label for="pen-ammo">Votre munition</label><select class="input" id="pen-ammo">{opt_lvl}</select></div>
      <div class="field"><label for="pen-armor">Armure adverse</label><select class="input" id="pen-armor">{opt_lvl}</select></div>
    </div>
    <div id="pen-out"></div>
  </div>
  <div id="pen-grid" data-reveal></div>
  <p class="tiny muted mt-3">Rappel : en-dessous du niveau 3 (munition ET armure), l'équipement n'a pratiquement
  aucune valeur en PvP. <a href="../armurerie/munitions.html">Tableau complet des calibres</a>.</p>
</div></section>

<section class="section" id="raid"><div class="wrap">
  <div class="section-head" data-reveal>
    <div class="eyebrow">Outil 03</div><h2>Rentabilité de raid</h2>
    <p class="lead">Votre kit est-il trop cher pour votre taux de survie réel ? Réponse chiffrée.</p>
  </div>
  <div class="hud-panel" data-reveal>
    <div class="grid g-4 gap-4 mb-5">
      <div class="field"><label for="rd-kit">Coût du kit (Alloys)</label>
        <input class="input" id="rd-kit" type="number" min="0" step="5000" value="120000"></div>
      <div class="field"><label for="rd-loot">Butin moyen extrait (Alloys)</label>
        <input class="input" id="rd-loot" type="number" min="0" step="10000" value="400000"></div>
      <div class="field"><label for="rd-runs">Nombre de runs</label>
        <input class="input" id="rd-runs" type="number" min="1" step="1" value="10"></div>
      <div class="field"><label for="rd-surv">Taux d'extraction — <span id="rd-surv-val">45 %</span></label>
        <input class="input" id="rd-surv" type="range" min="5" max="95" step="5" value="45"></div>
    </div>
    <div id="rd-out"></div>
  </div>
</div></section>

<section class="section" id="edpi"><div class="wrap">
  <div class="section-head" data-reveal>
    <div class="eyebrow">Outil 04</div><h2>Calculateur eDPI</h2>
    <p class="lead">Changez de souris sans perdre vos repères musculaires.</p>
  </div>
  <div class="hud-panel" data-reveal>
    <div class="grid g-3 gap-4 mb-5">
      <div class="field"><label for="ed-dpi">DPI actuel</label>
        <input class="input" id="ed-dpi" type="number" min="100" step="50" value="800"></div>
      <div class="field"><label for="ed-sens">Sensibilité en jeu</label>
        <input class="input" id="ed-sens" type="number" min="0.1" step="0.1" value="6"></div>
      <div class="field"><label for="ed-newdpi">Nouveau DPI visé</label>
        <input class="input" id="ed-newdpi" type="number" min="100" step="50" value="1600"></div>
    </div>
    <div id="ed-out"></div>
  </div>
</div></section>

<section class="section" id="loadout"><div class="wrap">
  <div class="section-head" data-reveal>
    <div class="eyebrow">Outil 05</div><h2>Générateur de loadout</h2>
    <p class="lead">Sortez de votre zone de confort. Opérateur, arme, munitions, carte et un défi imposé.</p>
  </div>
  <div class="hud-panel" data-reveal>
    <div id="lo-out" class="mb-4"></div>
    <button class="btn btn-primary" id="lo-roll">Générer un nouveau loadout</button>
  </div>
</div></section>

<section class="section" id="quiz"><div class="wrap wrap-narrow">
  <div class="section-head" data-reveal>
    <div class="eyebrow">Outil 06</div><h2>Quiz tactique Aurora</h2>
    <p class="lead">Douze questions sur la Saison 12. Les réponses sont expliquées.</p>
  </div>
  <div class="hud-panel" data-reveal>
    <div class="flex justify-between items-center mb-4" id="qz-prog"></div>
    <div id="qz-box"></div>
    <button class="btn btn-ghost mt-4 hidden" id="qz-restart">Recommencer</button>
  </div>
</div></section>
"""
html = (head("Outils tactiques", "Outils interactifs pour Delta Force : calculateur TTK/STK/DPS, simulateur de "
             "pénétration des munitions, rentabilité de raid, calculateur eDPI, générateur de loadout et quiz tactique.",
             depth=D, canonical="pages/outils/index.html")
        + navbar(D) + '<main id="main">' + body + "</main>" + footer(D) + scripts(D, TOOLS_JS))
print(write("pages/outils/index.html", html))


# =========================================================== ASTUCES PRO
pc = ST["pc"]
gfx = "".join(f"""<tr><td><strong>{esc(g['parametre'])}</strong></td>
    <td><span class="badge badge-green">{esc(g['valeur'])}</span></td>
    <td class="num small mono">{esc(g.get('gain','—'))}</td>
    <td class="small muted">{esc(g.get('note',''))}</td></tr>""" for g in pc["graphismes"])

cons = "".join(f"<li>{esc(c)}</li>" for c in ST["console"]["conseils"])
mob = "".join(f"<li>{esc(c)}</li>" for c in ST["mobile"]["conseils"])
aud = "".join(f"<li>{esc(c)}</li>" for c in ST["audio"]["conseils"])
ed = ST["edpi"]
ed_rows = "".join(f'<tr><td>{esc(f["profil"])}</td><td class="num mono">{esc(f["edpi"])}</td></tr>' for f in ed["fourchettes"])
plat = "".join(f'<tr><td class="hud tiny muted">{esc(k.title())}</td><td>{esc(v)}</td></tr>'
               for k, v in ST["plateformes"].items())

# --- savoir communautaire (data/communaute.json) ---
CM = load("communaute")
_imp = {"Fort": "card-accent-green", "Moyen": "card-accent-blue"}
terrain = "".join(f"""<article class="card {_imp.get(c['impact'],'card-accent')}" data-reveal data-delay="{i*70}"
     data-tags="impact-{esc(c['impact'].lower())}" data-search="{esc(c['titre'])}">
    <div class="flex items-center justify-between gap-2 mb-2">
      <h3 class="card-title" style="font-size:1rem">{esc(c['titre'])}</h3>
      <span class="badge {'badge-green' if c['impact']=='Fort' else 'badge-grey'}">Impact {esc(c['impact'].lower())}</span>
    </div>
    <p class="small muted">{esc(c['detail'])}</p>
  </article>""" for i, c in enumerate(CM["conseils_terrain"]))

IT = CM["itineraire_3x3"]
etapes_3x3 = "".join(f'<li>{esc(e)}</li>' for e in IT["etapes"])
FC = IT["fate_contract"]

MK = "".join(f"""<article class="card card-accent-green" data-reveal data-delay="{i*55}">
    <div class="hud tiny txt-green mb-2">{i+1:02d}</div>
    <h3 class="card-title" style="font-size:.98rem">{esc(m['titre'])}</h3>
    <p class="small muted mt-2">{esc(m['detail'])}</p>
  </article>""" for i, m in enumerate(CM["mecaniques_cachees"]))

DE = CM["discipline_extraction"]
de_rules = "".join(f"<li>{esc(x)}</li>" for x in DE["regles"])
TX = "".join(f"""<tr><td><strong>{esc(t['type'])}</strong></td>
    <td class="small muted">{esc(t['detail'])}</td></tr>""" for t in CM["types_extraction"])

OT = CM["outils_tiers"]
outils_rows = "".join(f"""<tr>
    <td><span class="mono small">{esc(o['nom'])}</span></td>
    <td class="small">{esc(o['role'])}</td>
    <td class="tiny muted">{esc(o['nature'])}</td>
  </tr>""" for o in OT["legitimes"])
SA = OT["signaux_d_alerte"]
sa_items = "".join(f"<li>{esc(x)}</li>" for x in SA["signaux"])
sa_bad = "".join(f'<span class="chip" style="border-color:var(--df-red);color:var(--df-red)">{esc(x)}</span>' for x in SA["exemples_a_eviter"])
ep = OT["endpoint_observe"]
ep_params = "".join(f"<li class='mono tiny'>{esc(p)}</li>" for p in ep["parametres"])

EQ = ST.get("eq_pas_a_pas", {})
PE = ST.get("portee_d_ecoute", {})
CC = ST.get("config_competitive", {})
eq_rows = "".join(f"""<tr><td><strong>{esc(b['bande'])}</strong></td>
  <td class="mono num txt-green">{esc(b['reglage'])}</td>
  <td class="small muted">{esc(b['effet'])}</td></tr>""" for b in EQ.get("bandes", []))
pe_rows = "".join(f"""<tr><td><strong>{esc(l['mode'])}</strong></td>
  <td class="mono num txt-orange">{esc(l['portee'])}</td>
  <td class="small muted">{esc(l['commentaire'])}</td></tr>""" for l in PE.get("lignes", []))
cc_rows = "".join(f"""<tr><td><strong>{esc(l['reglage'])}</strong></td>
  <td class="txt-green small">{esc(l['valeur'])}</td>
  <td class="small muted">{esc(l['raison'])}</td></tr>""" for l in CC.get("lignes", []))
CON = ST.get("console", {}).get("competitif", {})

BP = EC.get("boucle_profit", {})
bp_steps = "".join(f"<li>{esc(x)}</li>" for x in BP.get("routine", []))
VE2 = EC.get("vendeur_ou_encheres", {})
ve_rows = "".join(f"""<tr><td><strong>{esc(r['rarete'])}</strong></td>
  <td class="small txt-green">{esc(r['action'])}</td>
  <td class="small muted">{esc(r['note'])}</td></tr>""" for r in VE2.get("par_rarete", []))
ve_sav = "".join(f"<li>{esc(x)}</li>" for x in VE2.get("a_savoir", []))
TK = EC.get("tickets_equipement", {})
tk_pts = "".join(f"<li>{esc(x)}</li>" for x in TK.get("points", []))

pro_body = f"""
{page_hero("Optimisation", "Astuces <span class='grad-text'>pro</span>",
           "Réglages PC, console et mobile, audio, sensibilité et les pièges qui coûtent des parties. "
           "Tous les gains de performance cités proviennent de bancs d'essai publiés.",
           "assets/images/heroes/reglages_hero_01.jpg", D)}

<section class="section-sm"><div class="wrap">
  {crumbs([("Astuces pro", None)], D)}
  <div class="mb-4" style="max-width:560px">{audio_briefing("astucespro_briefing_01.mp3", "Astuces pro", "", D)}</div>
  <div class="alert alert-green" data-reveal><span class="ico" aria-hidden="true">💡</span>
  <div><strong>Le réglage contre-intuitif à connaître.</strong> Global Illumination en <strong>Ultra</strong>
  tourne mieux que Medium et High — un quirk du moteur. Si votre machine le supporte, Ultra est à la fois
  plus beau et plus fluide. Sinon, descendez directement à Low : jusqu'à <strong>+75 % de FPS</strong>.</div></div>
</div></section>

<section class="section"><div class="wrap">
  <div class="section-head" data-reveal><div class="eyebrow">PC</div><h2>Réglages graphiques</h2></div>
  <div class="table-wrap" data-reveal><table class="df" style="min-width:720px">
    <thead><tr><th class="sortable">Paramètre</th><th>Valeur</th><th class="num">Gain</th><th>Note</th></tr></thead>
    <tbody>{gfx}</tbody></table></div>
  <div class="grid g-3 gap-4 mt-5">
    <div class="card card-accent" data-reveal><h3 class="card-title" style="font-size:1rem">FOV</h3>
      <p class="small">{esc(pc['fov']['recommande'])}</p>
      <p class="tiny muted mt-2">{esc(pc['fov']['note'])}</p></div>
    <div class="card card-accent" data-reveal><h3 class="card-title" style="font-size:1rem">Souris</h3>
      <p class="small">{esc(pc['souris']['dpi'])} DPI · sensibilité {esc(pc['souris']['sensibilite'])} ·
      coefficient ADS {esc(pc['souris']['coefficient_ads'])} · {esc(pc['souris']['mode_visee'])}</p>
      <p class="tiny muted mt-2">{esc(pc['souris']['note'])}</p></div>
    <div class="card card-accent" data-reveal><h3 class="card-title" style="font-size:1rem">Latence</h3>
      <p class="small">{esc(pc['latence_de_reference'])}</p>
      <p class="tiny muted mt-2">Contre {esc(ST['console']['latence_de_reference'])} sur console.</p></div>
  </div>
</div></section>

<section class="section"><div class="wrap">
  <div class="grid g-3 gap-5">
    <div><div class="section-head" data-reveal><div class="eyebrow">Console</div><h2>PS5 / Xbox</h2></div>
      <div class="card" data-reveal><p class="small mb-2"><strong>FOV :</strong> {esc(ST['console']['fov']['recommande'])}</p>
      <ul class="small muted">{cons}</ul></div></div>
    <div><div class="section-head" data-reveal><div class="eyebrow">Mobile</div><h2>iOS / Android</h2></div>
      <div class="card" data-reveal>
        <p class="small mb-2"><strong>Hipfire :</strong> H {ST['mobile']['sensibilites']['hipfire']['horizontal']} /
        V {ST['mobile']['sensibilites']['hipfire']['vertical']} — <strong>ADS :</strong>
        H {ST['mobile']['sensibilites']['ads']['horizontal']} / V {ST['mobile']['sensibilites']['ads']['vertical']} —
        <strong>Deadzone :</strong> {ST['mobile']['sensibilites']['deadzone']}</p>
        <ul class="small muted">{mob}</ul></div></div>
    <div><div class="section-head" data-reveal><div class="eyebrow">Audio</div><h2>Entendre avant de voir</h2></div>
      <div class="card card-accent-blue" data-reveal><ul class="small muted">{aud}</ul></div></div>
  </div>
</div></section>

<section class="section"><div class="wrap">
  <div class="grid g-2 gap-6">
    <div>
      <div class="section-head" data-reveal><div class="eyebrow">Sensibilité</div><h2>Profils eDPI</h2></div>
      <div class="table-wrap" data-reveal><table class="df" style="min-width:0">
        <thead><tr><th>Profil</th><th class="num">eDPI</th></tr></thead><tbody>{ed_rows}</tbody></table></div>
      <p class="small muted mt-2 mono">{esc(ed['formule'])} — exemple : {esc(ed['exemple'])}</p>
      <a class="btn btn-ghost btn-sm mt-3" href="../outils/index.html#edpi">Ouvrir le calculateur eDPI</a>
    </div>
    <div>
      <div class="section-head" data-reveal><div class="eyebrow">Supports</div><h2>Plateformes</h2></div>
      <div class="table-wrap" data-reveal><table class="df" style="min-width:0"><tbody>{plat}</tbody></table></div>
    </div>
  </div>
</div></section>

<section class="section" id="terrain"><div class="wrap">
  <div class="section-head" data-reveal>
    <div class="eyebrow">Savoir communautaire</div><h2>Conseils de terrain</h2>
    <p class="lead">Remontées de joueurs expérimentés, recoupées quand c'était possible. Ce ne sont pas des
    chiffres officiels — ce sont des habitudes qui font gagner des raids.</p>
  </div>
  <div class="grid g-auto-md">{terrain}</div>
</div></section>

<section class="section-sm"><div class="wrap">
  <figure class="img-frame mb-5" data-reveal><img src="../../assets/images/misc/firing_range_01.jpg" alt="Stand de tir intérieur avec mannequins blindés à différentes distances" loading="lazy" decoding="async"><figcaption>Le stand de tir du Black Site est gratuit : testez-y la pénétration avant de payer vos munitions (illustration générée par IA, pas une capture du jeu)</figcaption></figure>
</div></section>

<section class="section" id="mecaniques"><div class="wrap">
  <div class="section-head" data-reveal>
    <div class="eyebrow">Systèmes méconnus</div><h2>Mécaniques cachées</h2>
    <p class="lead">Huit comportements du jeu que l'interface n'explique jamais, et que la plupart des joueurs
    ignorent après des centaines d'heures.</p>
  </div>
  <div class="grid g-auto-sm">{MK}</div>
</div></section>

<section class="section" id="discipline"><div class="wrap">
  <div class="section-head" data-reveal>
    <div class="eyebrow">Chiffres</div><h2>{esc(DE['titre'])}</h2>
    <p class="lead">La survie en extraction n'est pas une affaire d'instinct : c'est une affaire de seuils.</p>
  </div>
  <div class="grid g-2 gap-6">
    <div class="card card-accent-red" data-reveal><ul class="small">{de_rules}</ul></div>
    <div>
      <div class="card card-accent-gold mb-4" data-reveal>
        <h3 class="card-title" style="font-size:1rem">Valeur par emplacement</h3>
        <p class="small mt-2">{esc(DE['formule_valeur'])}</p>
        <div class="divider"></div>
        <p class="tiny muted">{esc(DE['note_munitions'])}</p>
      </div>
      <div class="table-wrap" data-reveal><table class="df" style="min-width:0">
        <thead><tr><th>Type d'extraction</th><th>Comportement</th></tr></thead>
        <tbody>{TX}</tbody></table></div>
    </div>
  </div>
</div></section>

<section class="section" id="faible-pvp"><div class="wrap">
  <div class="grid g-2 gap-6">
    <div>
      <div class="section-head" data-reveal><div class="eyebrow">Parcours</div><h2>{esc(IT['titre'])}</h2></div>
      <div class="card card-accent-blue" data-reveal>
        <p class="tiny muted mb-3">{esc(IT['contexte'])}</p>
        <ul class="small">{etapes_3x3}</ul>
      </div>
    </div>
    <div>
      <div class="section-head" data-reveal><div class="eyebrow">Contrat du Destin</div><h2>« {esc(FC['nom'])} »</h2></div>
      <div class="card card-accent-orange" data-reveal>
        <p class="small mb-3"><strong class="txt-orange">Exigence :</strong> {esc(FC['exigence'])}</p>
        <div class="divider"></div>
        <p class="small"><strong class="txt-red">Piège :</strong> {esc(FC['piege'])}</p>
      </div>
    </div>
  </div>
</div></section>

<section class="section-sm"><div class="wrap">
  <figure class="img-frame mb-5" data-reveal><img src="../../assets/images/misc/safebox_stash_01.jpg" alt="Safe Box ouverte contenant lingots, liquidités et munitions de valeur" loading="lazy" decoding="async"><figcaption>La Safe Box protège la valeur en cas de mort — mais ne valide jamais un objectif d'extraction (illustration générée par IA, pas une capture du jeu)</figcaption></figure>
</div></section>


<section class="section" id="audio"><div class="wrap">
  <div class="section-head" data-reveal>
    <div class="eyebrow">Le réglage le plus rentable</div><h2>{esc(EQ.get('titre',''))}</h2>
    <p class="lead">{esc(EQ.get('principe',''))}</p>
  </div>
  <div class="grid g-2 gap-6">
    <div>
      <div class="table-wrap" data-reveal><table class="df" style="min-width:420px">
        <thead><tr><th>Bande</th><th>Réglage</th><th>Effet</th></tr></thead>
        <tbody>{eq_rows}</tbody></table></div>
      <div class="alert alert-red mt-4" data-reveal><span class="ico" aria-hidden="true">⚠</span>
      <div class="small">{esc(EQ.get('avertissement',''))}</div></div>
    </div>
    <div>
      <figure class="img-frame" data-reveal>
        <img src="../../assets/images/misc/audio_casque_01.jpg" alt="Casque audio circum-auriculaire posé sur du béton sombre" loading="lazy" decoding="async">
        <figcaption>Circum-auriculaire fermé : les intra-auriculaires enterrent les pas sous le grave (illustration générée par IA, pas une capture du jeu)</figcaption>
      </figure>
      <h3 class="card-title mt-5 mb-3" style="font-size:1rem">{esc(PE.get('titre',''))}</h3>
      <div class="table-wrap" data-reveal><table class="df" style="min-width:380px">
        <thead><tr><th>Mode</th><th>Portée</th><th>Commentaire</th></tr></thead>
        <tbody>{pe_rows}</tbody></table></div>
      <p class="small muted mt-3">{esc(PE.get('materiel',''))}</p>
    </div>
  </div>
</div></section>

<section class="section" id="config"><div class="wrap">
  <div class="section-head" data-reveal>
    <div class="eyebrow">PC</div><h2>{esc(CC.get('titre',''))}</h2>
    <p class="lead">Quinze lignes, chacune justifiée. La lisibilité prime toujours sur le spectacle.</p>
  </div>
  <div class="table-wrap" data-reveal><table class="df" style="min-width:820px">
    <thead><tr><th>Réglage</th><th>Valeur</th><th>Pourquoi</th></tr></thead>
    <tbody>{cc_rows}</tbody>
  </table></div>
  <div class="grid g-3 gap-4 mt-5">
    <div class="card card-accent-blue" data-reveal><h3 class="card-title" style="font-size:.95rem">Console — mode</h3>
      <p class="small muted">{esc(CON.get('mode',''))}</p></div>
    <div class="card card-accent-blue" data-reveal data-delay="80"><h3 class="card-title" style="font-size:.95rem">Console — sensibilité</h3>
      <p class="small muted">{esc(CON.get('sensibilite_pro',''))}</p></div>
    <div class="card card-accent-blue" data-reveal data-delay="160"><h3 class="card-title" style="font-size:.95rem">Console — haptique</h3>
      <p class="small muted">{esc(CON.get('haptique',''))}</p></div>
  </div>
</div></section>

<section class="section" id="outils-tiers"><div class="wrap">
  <div class="section-head" data-reveal>
    <div class="eyebrow">Écosystème</div><h2>Outils communautaires</h2>
  </div>
  <div class="alert alert-red mb-5" data-reveal><span class="ico" aria-hidden="true">⚠</span>
  <div class="small">{esc(OT['avertissement'])}</div></div>
  <div class="table-wrap" data-reveal><table class="df" style="min-width:680px">
    <thead><tr><th>Projet</th><th>Rôle</th><th>Nature technique</th></tr></thead>
    <tbody>{outils_rows}</tbody></table></div>

  <div class="section-head mt-6" data-reveal><div class="eyebrow">Sécurité</div><h3 style="font-size:1.3rem">{esc(SA['titre'])}</h3>
    <p class="small muted mt-2">{esc(SA['intro'])}</p></div>
  <div class="card card-accent-red" data-reveal>
    <ul class="small">{sa_items}</ul>
    <div class="divider"></div>
    <p class="small"><strong class="txt-red">Conséquence :</strong> {esc(SA['consequence'])}</p>
    <div class="hud-head mt-4">Noms à éviter</div>
    <div class="chips mt-2">{sa_bad}</div>
  </div>
  <p class="tiny muted mt-4">{esc(OT['note_automatisation'])}</p>
  <div class="card card-accent mt-5" data-reveal>
    <h3 class="card-title" style="font-size:1rem">Point d'accès observé</h3>
    <p class="mono small txt-blue">{esc(ep['base'])}</p>
    <p class="tiny muted mt-2">{esc(ep['statut'])}</p>
    <ul class="muted mt-3">{ep_params}</ul>
  </div>
</div></section>
"""

OS = CM["outils_open_source"]
_lg = "".join(f"""<article class="card card-accent-green" data-reveal data-delay="{i*80}">
    <div class="flex-between mb-2"><h3 class="card-title" style="font-size:1rem;margin:0">{esc(o['nom'])}</h3>
      <span class="badge badge-green">{esc(o['licence'])}</span></div>
    <div class="hud tiny muted mb-2">par {esc(o['auteur'])}</div>
    <p class="small">{esc(o['quoi'])}</p>
    <p class="small muted mono" style="margin:.5rem 0 .3rem">{esc(o['stack'])}</p>
    <p class="small txt-green" style="margin:0">{esc(o['pourquoi'])}</p>
  </article>""" for i, o in enumerate(OS["legitimes"]))

pro_os = f"""
<section class="section" id="outils-communautaires"><div class="wrap wrap-narrow">
  <div class="section-head" data-reveal>
    <div class="eyebrow">Hors du jeu</div><h2>{esc(OS['titre'])}</h2>
  </div>
  <div class="alert alert-red mb-4" data-reveal><span class="ico" aria-hidden="true">⚠</span>
  <div class="small">{esc(OS['avertissement'])}</div></div>
  <div class="grid gap-4 mb-4">{_lg}</div>
  <div class="card card-accent-blue" data-reveal><p class="small" style="margin:0">{esc(OS['critere'])}</p></div>
</div></section>
"""
html_pro = (head("Astuces pro — réglages PC, console & mobile", "Les meilleurs réglages Delta Force : graphismes PC "
                 "(le quirk Global Illumination), FOV, sensibilité souris, réglages console et mobile, audio et eDPI.",
                 depth=D, canonical="pages/astuces-pro/index.html")
            + navbar(D) + '<main id="main">' + pro_body + pro_os + "</main>" + footer(D) + scripts(D))
print(write("pages/astuces-pro/index.html", html_pro))


# =========================================================== CODES DE PORTES
rows = "".join(f"""<tr>
    <td><strong>{esc(c['carte'])}</strong></td>
    <td><div class="codebox"><code style="font-size:1.1rem;letter-spacing:.25em">{esc(c['code'])}</code>
      <button class="copy-btn" data-copy="{esc(c['code'])}">COPIER</button></div></td>
    <td class="small muted">{esc(c['emplacement'])}</td>
  </tr>""" for c in CD["codes"])
cr = CD["secret_cracked"]
conseils = "".join(f"<li>{esc(c)}</li>" for c in CD["conseils"])

cp_body = f"""
{page_hero("Renseignement", "Codes de <span class='grad-text'>portes</span>",
           f"Relevé du {esc(CD['_meta']['date_releve'])}. Les codes changent chaque jour — "
           "mais les <strong>emplacements des portes</strong>, eux, sont permanents.",
           "assets/images/maps/cartes_brakkesh_01.jpg", D)}

<section class="section-sm"><div class="wrap">
  {crumbs([("Astuces pro", "pages/astuces-pro/index.html"), ("Codes de portes", None)], D)}
  <figure class="img-frame mb-5" data-reveal>
    <img src="../../assets/images/misc/codes_portes_clavier_01.jpg" alt="Clavier à code industriel encrassé sur une porte blindée, touches effacées par l'usure" loading="lazy" decoding="async">
    <figcaption>Les codes changent chaque jour — la porte, elle, ne bouge pas. (illustration générée par IA, pas une capture du jeu)</figcaption>
  </figure>
  <div class="mb-4" style="max-width:560px">{audio_briefing("codesportes_briefing_01.mp3", "Codes de portes", "", D)}</div>
  <div class="alert alert-red" data-reveal><span class="ico" aria-hidden="true">⏱</span>
  <div><strong>{esc(CD['_meta']['avertissement_majeur'])}</strong></div></div>
  <div class="alert alert-blue mt-3" data-reveal><span class="ico" aria-hidden="true">🔧</span>
  <div>{esc(CD['_meta']['note_technique'])} Sources de référence :
  <a href="https://www.playdeltaforce.com/events/hq/" target="_blank" rel="noopener nofollow">playdeltaforce.com/events/hq</a>,
  <a href="https://deltaforceitems.com/" target="_blank" rel="noopener nofollow">deltaforceitems.com</a>.</div></div>
</div></section>

<section class="section-sm"><div class="wrap">
  <div class="table-wrap" data-reveal><table class="df" style="min-width:680px">
    <thead><tr><th>Carte</th><th>Code du {esc(CD['_meta']['date_releve'])}</th><th>Emplacement de la porte</th></tr></thead>
    <tbody>{rows}</tbody></table></div>
</div></section>

<section class="section"><div class="wrap wrap-narrow">
  <div class="section-head" data-reveal><div class="eyebrow">Énigme cross-mode</div><h2>Le secret CRACKED</h2></div>
  <div class="card card-accent-purple" data-reveal style="border-left:2px solid var(--df-purple)">
    <p class="small mb-3"><strong class="txt-green">Carte :</strong> {esc(cr['carte'])}</p>
    <p class="small mb-3">{esc(cr['description'])}</p>
    <p class="small mb-3"><strong class="txt-orange">Méthode :</strong> {esc(cr['methode'])}</p>
    <div class="alert alert-red"><span class="ico" aria-hidden="true">⚠</span>
    <div><ul class="small">{''.join(f'<li>{esc(p)}</li>' for p in cr['pieges'])}</ul></div></div>
  </div>
</div></section>

<section class="section-sm"><div class="wrap wrap-narrow">
  <div class="card card-accent" data-reveal><h3 class="card-title">Conseils</h3><ul class="small">{conseils}</ul></div>
</div></section>
"""
html_cp = (head("Codes de portes quotidiens", "Les codes de portes du jour pour Zero Dam, Layali Grove, Brakkesh, "
                "Space City, Tide Prison et AZ3, avec l'emplacement exact de chaque porte et le secret CRACKED.",
                depth=D, canonical="pages/astuces-pro/codes-portes.html",
                image="assets/images/maps/cartes_brakkesh_01.jpg")
           + navbar(D) + '<main id="main">' + cp_body + "</main>" + footer(D) + scripts(D))
print(write("pages/astuces-pro/codes-portes.html", html_cp))


# =========================================================== TIER LIST ÉDITABLE
all_ops = [o["nom"] for o in OP["operateurs"]]
rows_tl = ""
for k in ["S", "A", "B", "C", "D"]:
    rows_tl += f"""<div class="tier-row">
      <div class="tier-label" style="background:var(--tier-{k.lower()})">{k}</div>
      <div class="tier-drop" data-tier="{k}"></div>
    </div>"""
pool = "".join(f'<span class="tier-item">{esc(n)}</span>' for n in all_ops)

def static_tl(block):
    return "".join(f"""<div class="tier-row">
      <div class="tier-label" style="background:var(--tier-{k.lower()})">{k}</div>
      <div class="tier-drop">{''.join(f'<span class="tier-item" style="cursor:default">{esc(n)}</span>' for n in v)}</div>
    </div>""" for k, v in block.items())

tl_body = f"""
{page_hero("Méta Saison 12", "Tier <span class='grad-text'>list</span>",
           f"Instantané du {esc(TL['_meta']['snapshot'])}, après la mise à jour d'équilibrage du 12 novembre. "
           "Et un éditeur pour composer la vôtre.",
           "assets/images/season/saison_aurora_01.jpg", D)}

<section class="section-sm"><div class="wrap">
  {crumbs([("Encyclopédie", "pages/encyclopedie/index.html"), ("Tier list", None)], D)}
  <figure class="img-frame mb-5" data-reveal>
    <img src="../../assets/images/misc/tierlist_podium_01.jpg" alt="Cinq opérateurs en contre-jour dans un hangar sombre, silhouettes découpées par une lumière orange" loading="lazy" decoding="async">
    <figcaption>Un classement n'est jamais une vérité : c'est un instantané de la méta, scindé par mode. (illustration générée par IA, pas une capture du jeu)</figcaption>
  </figure>
  <div class="mb-4" style="max-width:560px">{audio_briefing("tierlist_briefing_01.mp3", "Tier list", "", D)}</div>
  <div class="alert alert-red" data-reveal><span class="ico" aria-hidden="true">⚠</span>
  <div><strong>Correction importante.</strong> {esc(TL['_meta']['correction_importante'])}</div></div>
  <div class="alert mt-3" data-reveal><span class="ico" aria-hidden="true">ℹ</span>
  <div>{esc(TL['_meta']['avertissement'])}</div></div>
</div></section>

<section class="section"><div class="wrap">
  <div class="section-head" data-reveal><div class="eyebrow">Opérateurs</div><h2>Classement par mode</h2></div>
  <div class="tabs" role="tablist" data-reveal>
    <button class="active" data-tab="t-ops" role="tab">Operations</button>
    <button data-tab="t-war" role="tab">Warfare</button>
    <button data-tab="t-arm-ops" role="tab">Armes Operations</button>
    <button data-tab="t-arm-war" role="tab">Armes Warfare</button>
  </div>
  <div class="tabpanel active" data-panel="t-ops">
    <p class="small muted mb-3">{esc(TL['operations']['libelle'])}</p>
    <div class="tierlist">{static_tl(TL['operations']['tiers'])}</div>
    <div class="grid g-auto-sm mt-5">
      {''.join(f'<div class="card"><strong class="txt-green">{esc(k)}</strong><p class="small muted mt-1">{esc(v)}</p></div>' for k, v in TL['operations']['justifications'].items())}
    </div>
  </div>
  <div class="tabpanel" data-panel="t-war">
    <p class="small muted mb-3">{esc(TL['warfare']['libelle'])}</p>
    <div class="tierlist">{static_tl(TL['warfare']['tiers'])}</div>
    <div class="grid g-auto-sm mt-5">
      {''.join(f'<div class="card"><strong class="txt-green">{esc(k)}</strong><p class="small muted mt-1">{esc(v)}</p></div>' for k, v in TL['warfare']['justifications'].items())}
    </div>
  </div>
  <div class="tabpanel" data-panel="t-arm-ops">
    <div class="tierlist">{static_tl(TL['armes_operations']['tiers'])}</div>
    <div class="alert alert-blue mt-4"><span class="ico">ℹ</span><div>{esc(TL['armes_operations']['note_s12'])}</div></div>
  </div>
  <div class="tabpanel" data-panel="t-arm-war">
    <div class="tierlist">{static_tl(TL['armes_warfare']['tiers'])}</div>
    <div class="alert alert-blue mt-4"><span class="ico">ℹ</span><div>{esc(TL['armes_warfare']['note_s12'])}</div></div>
  </div>
</div></section>

<section class="section"><div class="wrap">
  <div class="section-head" data-reveal>
    <div class="eyebrow">Outil</div><h2>Composez votre tier list</h2>
    <p class="lead">Glissez les opérateurs dans les rangs. Au clavier : focus sur un opérateur puis flèches haut / bas.
    Votre classement est sauvegardé localement dans votre navigateur.</p>
  </div>
  <div id="tier-editor" data-reveal>
    <div class="tierlist mb-4">{rows_tl}</div>
    <div class="hud-panel">
      <div class="hud-head">Opérateurs à placer</div>
      <div class="tier-drop" style="min-height:60px">{pool}</div>
    </div>
    <div class="flex gap-3 mt-4">
      <button class="btn btn-primary" id="tl-export">Copier ma tier list</button>
      <button class="btn btn-ghost" id="tl-reset">Réinitialiser</button>
    </div>
  </div>
</div></section>

<section class="section-sm"><div class="wrap">
  <div class="card" data-reveal>
    <h3 class="card-title">Meilleurs picks en solo</h3>
    <div class="grid g-3 gap-4 mt-3">
      {''.join(f'<div class="hud-panel"><div class="hud-head">{esc(c["operateur"])}</div><p class="small">{esc(c["raison"])}</p></div>' for c in TL['solo_operations']['classement'])}
    </div>
  </div>
</div></section>
"""
html_tl = (head("Tier list Saison 12", "Tier list Delta Force Saison 12 Aurora : opérateurs classés séparément pour "
                "Operations et Warfare, tier list des armes et éditeur drag & drop pour composer la vôtre.",
                depth=D, canonical="pages/encyclopedie/tier-list.html",
                image="assets/images/season/saison_aurora_01.jpg")
           + navbar(D) + '<main id="main">' + tl_body + "</main>" + footer(D) + scripts(D, TOOLS_JS))
print(write("pages/encyclopedie/tier-list.html", html_tl))


# =========================================================== ÉCONOMIE
mon = "".join(f"""<div class="card card-accent{'-orange' if m['nom']=='Delta Coins' else ''}" data-reveal>
    <h3 class="card-title">{esc(m['nom'])}</h3>
    <p class="tiny muted mb-2">{esc(m['type'])}</p>
    <p class="small mb-2"><strong class="txt-green">Obtention :</strong> {esc(m['obtention'])}</p>
    <ul class="small muted mb-3">{''.join(f'<li>{esc(u)}</li>' for u in m['usages'])}</ul>
    {f'<div class="alert ' + ('alert-red' if m['nom']=='Delta Coins' else 'alert-green') + '"><span class="ico">' + ('⚠' if m['nom']=='Delta Coins' else '✓') + '</span><div class="small">' + esc(m['regle']) + '</div></div>' if m.get('regle') else ''}
  </div>""" for m in EC["monnaies"])

ah = EC["hotel_des_ventes"]
ah_strat = "".join(f"<li>{esc(s)}</li>" for s in ah["strategies"])
ah_items = "".join(f'<tr><td><strong>{esc(o["objet"])}</strong>{f"<br><span class=\'tiny muted\'>{esc(o["note"])}</span>" if o.get("note") else ""}</td>'
                   f'<td class="num mono txt-gold">{esc(o["prix_guide"])}</td><td class="small">{esc(o.get("carte","—"))}</td></tr>'
                   for o in ah["objets_a_forte_valeur"])
paliers = "".join(f'<tr><td class="num">{p["niveau"]}</td><td>{esc(p["deblocage"])}</td></tr>'
                  for p in EC["progression"]["operations_level"]["paliers_cles"])
cd_ = "".join(f"<li>{esc(c)}</li>" for c in EC["conseils_debutant"])

ec_body = f"""
{page_hero("Progression", "Économie &amp; <span class='grad-text'>Hôtel des Ventes</span>",
           "Tekniq Alloys, Delta Coins, marché entre joueurs et paliers de niveau. "
           "Comprendre l'économie, c'est arrêter de perdre des raids pour rien.",
           "assets/images/heroes/hazardops_extraction_01.jpg", D)}

<section class="section-sm"><div class="wrap">
  {crumbs([("Encyclopédie", "pages/encyclopedie/index.html"), ("Économie", None)], D)}
  <div class="grid g-2 gap-4 mb-5">
    <figure class="img-frame" data-reveal><img src="../../assets/images/economy/economie_marche_01.jpg" alt="Comptoir de marché noir aux étagères chargées de matériel" loading="lazy" decoding="async"><figcaption>L'hôtel des ventes — où se fait le vrai profit</figcaption></figure>
    <figure class="img-frame" data-reveal data-delay="90"><img src="../../assets/images/economy/economie_atelier_01.jpg" alt="Établi de fabrication d'armure avec plaques céramiques et presse" loading="lazy" decoding="async"><figcaption>Fabriquer plutôt qu'acheter : la marge est souvent de 50 000 Alloys</figcaption></figure>
  </div>
  <div class="mb-4" style="max-width:560px">{audio_briefing("economie_briefing_01.mp3", "Économie", "", D)}</div>
  <div class="alert" data-reveal><span class="ico" aria-hidden="true">💲</span>
  <div>{esc(EC['_meta']['avertissement'])}</div></div>
</div></section>

<section class="section"><div class="wrap">
  <div class="section-head" data-reveal><div class="eyebrow">Monnaies</div><h2>Les trois devises</h2></div>
  <div class="grid g-3 gap-5">{mon}</div>
</div></section>

<section class="section"><div class="wrap">
  <div class="section-head" data-reveal><div class="eyebrow">Marché joueurs</div><h2>{esc(ah['nom'])}</h2>
  <p class="lead">{esc(ah['principe'])}</p></div>
  <div class="grid g-2 gap-5">
    <div class="card card-accent-blue" data-reveal>
      <h3 class="card-title" style="font-size:1rem">Stratégies</h3>
      <p class="small muted mb-2">{esc(ah['slots'])}</p>
      <ul class="small">{ah_strat}</ul>
    </div>
    <div data-reveal>
      <div class="table-wrap"><table class="df" style="min-width:0">
        <thead><tr><th>Objet</th><th class="num">Prix guide</th><th>Carte</th></tr></thead>
        <tbody>{ah_items}</tbody></table></div>
    </div>
  </div>
  <div class="text-center mt-5"><a class="btn btn-ghost" href="../outils/index.html#raid">Calculer la rentabilité de vos raids</a></div>
</div></section>

<section class="section"><div class="wrap">
  <div class="grid g-2 gap-6">
    <div>
      <div class="section-head" data-reveal><div class="eyebrow">Operations Level</div><h2>Paliers clés</h2></div>
      <p class="small muted mb-3">{esc(EC['progression']['operations_level']['role'])}</p>
      <div class="table-wrap" data-reveal><table class="df" style="min-width:0">
        <thead><tr><th class="num">Niveau</th><th>Déblocage</th></tr></thead><tbody>{paliers}</tbody></table></div>
      <p class="small muted mt-2">{esc(EC['progression']['operations_level']['bonus_exp'])}</p>
    </div>
    <div>
      <div class="section-head" data-reveal><div class="eyebrow">Les bases</div><h2>Conseils débutant</h2></div>
      <div class="card card-accent" data-reveal><ul class="small">{cd_}</ul></div>
      <div class="alert alert-green mt-4" data-reveal><span class="ico" aria-hidden="true">✓</span>
      <div>{esc(EC['progression']['pas_de_wipe'])}</div></div>
    </div>
  </div>
</div></section>

<section class="section" id="boucle-profit"><div class="wrap">
  <div class="section-head" data-reveal>
    <div class="eyebrow">Revenu passif</div><h2>{esc(BP.get('titre',''))}</h2>
    <p class="lead">{esc(BP.get('principe',''))}</p>
  </div>
  <div class="grid g-2 gap-6">
    <div>
      <div class="card card-accent-gold" data-reveal>
        <h3 class="card-title" style="font-size:1rem">La routine quotidienne</h3>
        <ol class="small">{bp_steps}</ol>
      </div>
      <div class="alert alert-orange mt-4" data-reveal><span class="ico" aria-hidden="true">⚠</span>
      <div class="small">{esc(BP.get('avertissement',''))}</div></div>
    </div>
    <div>
      <figure class="img-frame" data-reveal>
        <img src="../../assets/images/economy/economie_atelier_01.jpg" alt="Établi d'armurier avec outils et composants" loading="lazy" decoding="async">
        <figcaption>Les ateliers tournent pendant que vous jouez (illustration générée par IA, pas une capture du jeu)</figcaption>
      </figure>
      <div class="card card-accent-green mt-4" data-reveal>
        <h3 class="card-title" style="font-size:1rem">Quels ateliers d'abord</h3>
        <p class="small">{esc(BP.get('priorite_ateliers',''))}</p>
      </div>
    </div>
  </div>
</div></section>

<section class="section" id="vendre"><div class="wrap">
  <div class="section-head" data-reveal>
    <div class="eyebrow">Arbitrage</div><h2>{esc(VE2.get('titre',''))}</h2>
    <p class="lead">{esc(VE2.get('regle',''))}</p>
  </div>
  <div class="alert alert-green mb-4" data-reveal><span class="ico" aria-hidden="true">★</span>
  <div class="small">{esc(VE2.get('seuil',''))}</div></div>
  <div class="table-wrap" data-reveal><table class="df" style="min-width:720px">
    <thead><tr><th>Rareté</th><th>Où vendre</th><th>Note</th></tr></thead>
    <tbody>{ve_rows}</tbody>
  </table></div>
  <div class="card card-accent-blue mt-5" data-reveal>
    <h3 class="card-title" style="font-size:1rem">À savoir</h3>
    <ul class="small">{ve_sav}</ul>
  </div>
</div></section>

<section class="section" id="tickets"><div class="wrap wrap-narrow">
  <div class="section-head" data-reveal><div class="eyebrow">Réduire le coût d'entrée</div><h2>{esc(TK.get('titre',''))}</h2>
    <p class="lead">{esc(TK.get('principe',''))}</p></div>
  <div class="card card-accent-gold" data-reveal><ul class="small">{tk_pts}</ul></div>
</div></section>
"""

MT = EC["methodes_terrain"]
AM = MT["astuces_munitions"]
_mt = "".join(f"""<article class="card card-accent-{m['accent']}" data-reveal data-delay="{i*60}">
    <h3 class="card-title" style="font-size:1.02rem">{esc(m['nom'])}</h3>
    <p class="small">{esc(m['detail'])}</p>
    <p class="small txt-{m['accent']}" style="margin:.5rem 0 0"><strong>{esc(m['cle'])}</strong></p>
  </article>""" for i, m in enumerate(MT["methodes"]))

ec_terrain = f"""
<section class="section" id="methodes"><div class="wrap">
  <div class="section-head" data-reveal>
    <div class="eyebrow">Argent</div><h2>{esc(MT['titre'])}</h2>
    <p class="lead">{esc(MT['intro'])}</p>
  </div>
  <div class="grid g-2 gap-4 mb-5">{_mt}</div>
  <div class="grid g-2 gap-6">
    <div>
      <div class="card card-accent-gold" data-reveal>
        <h3 class="card-title" style="font-size:1.05rem">{esc(AM['titre'])}</h3>
        <p class="small">{esc(AM['detail'])}</p>
        <div class="divider" style="margin:.9rem 0"></div>
        <p class="small mono txt-blue" style="margin:0 0 .5rem">{esc(AM['raccourci'])}</p>
        <p class="small txt-green" style="margin:0"><strong>{esc(AM['regle'])}</strong></p>
      </div>
      <div class="alert alert-orange mt-4" data-reveal><span class="ico" aria-hidden="true">!</span>
      <div class="small">{esc(MT.get('plafond_easy', EC.get('plafond_easy','')))}</div></div>
    </div>
    <div>
      <figure class="img-frame" data-reveal>
        <img src="../../assets/images/misc/haavk_conteneur_01.jpg" alt="Conteneur maritime d'entreprise ouvert dans un hangar poussiéreux, caisses grises empilées" loading="lazy" decoding="async">
        <figcaption>Les conteneurs d'entreprise attirent bien moins de monde que l'Administration (illustration générée par IA, pas une capture du jeu)</figcaption>
      </figure>
      <figure class="img-frame mt-4" data-reveal data-delay="80">
        <img src="../../assets/images/misc/gear_ticket_01.jpg" alt="Équipement de dotation gratuite disposé à plat sur une toile kaki" loading="lazy" decoding="async">
        <figcaption>Un ticket d'équipement ne coûte rien : tout ce qui ressort avec vous est du bénéfice net (illustration générée par IA, pas une capture du jeu)</figcaption>
      </figure>
    </div>
  </div>
</div></section>
"""
html_ec = (head("Économie & Hôtel des Ventes", "Comprendre l'économie de Delta Force : Tekniq Alloys contre Delta Coins, "
                "Hôtel des Ventes, paliers de niveau Operations et conseils pour arrêter de perdre des Alloys.",
                depth=D, canonical="pages/encyclopedie/economie.html",
                image="assets/images/heroes/hazardops_extraction_01.jpg")
           + navbar(D) + '<main id="main">' + ec_body + ec_terrain + "</main>" + footer(D) + scripts(D))
print(write("pages/encyclopedie/economie.html", html_ec))


# ====================================================== ARTISANAT & ENCHÈRES
AT = load("artisanat")

FR = AT["frais"]
PRN = AT["principe"]

at_ateliers = "".join(f"""<article class="card card-accent-blue" data-reveal data-delay="{i*60}">
    <div class="flex-between mb-2"><h4 class="card-title" style="font-size:1rem;margin:0">{esc(a['nom'])}</h4>
      <span class="badge badge-grey">{esc(a['rythme'])}</span></div>
    <p class="small">{esc(a['produit'])}</p>
    <p class="small muted">{esc(a['profil'])}</p>
  </article>""" for i, a in enumerate(AT["ateliers"]))

at_rows = "".join(f"""<tr>
    <td><strong>{esc(r['objet'])}</strong></td>
    <td class="small muted">{esc(r['atelier'])}</td>
    <td class="mono small num">{esc(r['cout'])}</td>
    <td class="mono small num">{esc(r['vente'])}</td>
    <td class="mono small num txt-green">{esc(r['marge'])}</td>
    <td class="mono small num">{esc(r['duree'])}</td>
    <td class="small muted">{esc(r['note'])}</td>
  </tr>""" for r in AT["rentables"])

at_meth = "".join(f"""<article class="card card-accent-orange" data-reveal data-delay="{i*55}">
    <div class="hud tiny txt-orange mb-2">ÉTAPE {m['n']:02d}</div>
    <h4 class="card-title" style="font-size:.98rem">{esc(m['titre'])}</h4>
    <p class="small muted">{esc(m['detail'])}</p>
  </article>""" for i, m in enumerate(AT["methode"]))

at_pieges = "".join(f"<li>{esc(x)}</li>" for x in AT["pieges"])

EN = AT["encheres"]
en_rows = "".join(f"""<tr><td><strong>{esc(l['rarete'])}</strong></td>
    <td class="txt-{'green' if l['ou'] == 'Enchères' else 'orange'}">{esc(l['ou'])}</td>
    <td class="small muted">{esc(l['pourquoi'])}</td></tr>""" for l in EN["lignes"])

art_body = f"""
{page_hero("Économie", "Artisanat &amp; <span class='grad-text'>hôtel des ventes</span>",
           "Le seul revenu du jeu qui tombe pendant que vous ne jouez pas. "
           "Deux calculateurs pour décider en dix secondes si une production vaut huit heures d'atelier.",
           "assets/images/misc/artisanat_atelier_01.jpg", D)}

<section class="section-sm"><div class="wrap">
  {crumbs([("Outils", "index.html"), ("Artisanat &amp; enchères", None)], D)}
  <div class="mb-4" style="max-width:560px">{audio_briefing("artisanat_briefing_01.mp3", "Artisanat", "", D)}</div>
  <div class="alert alert-red" data-reveal><span class="ico" aria-hidden="true">⚠</span>
  <div class="small">{esc(AT['_meta']['avertissement'])}</div></div>
</div></section>

<section class="section" id="calculateurs"><div class="wrap">
  <div class="section-head" data-reveal>
    <div class="eyebrow">Les deux outils</div><h2>Calculer avant de produire</h2>
    <p class="lead">{esc(FR['contenu'])}</p>
  </div>

  <div class="grid g-2 gap-5">
    <div class="card card-accent-green" data-reveal id="craft-calc">
      <h3 class="card-title" style="font-size:1.05rem">Calculateur d'artisanat</h3>
      <p class="small muted mb-3">Coût des matériaux, prix de vente, durée de production. Le résultat tient compte de la commission.</p>
      <div class="grid g-2 gap-3">
        <label class="small">Coût des matériaux (Alloys)
          <input type="number" id="cc-cout" value="163000" min="0" step="1000" class="inp"></label>
        <label class="small">Prix de vente attendu (Alloys)
          <input type="number" id="cc-vente" value="443000" min="0" step="1000" class="inp"></label>
        <label class="small">Durée de production (heures)
          <input type="number" id="cc-duree" value="8" min="0.5" step="0.5" class="inp"></label>
        <label class="small">Commission (%)
          <input type="number" id="cc-frais" value="{FR['taux']}" min="0" max="50" step="0.5" class="inp"></label>
      </div>
      <div class="divider"></div>
      <div class="grid g-3 gap-3">
        <div class="stat-card"><div class="hud tiny muted">PROFIT NET</div>
          <div class="num txt-green" id="cc-net" style="font-size:1.4rem">—</div></div>
        <div class="stat-card"><div class="hud tiny muted">PAR HEURE</div>
          <div class="num txt-blue" id="cc-heure" style="font-size:1.4rem">—</div></div>
        <div class="stat-card"><div class="hud tiny muted">MARGE</div>
          <div class="num txt-gold" id="cc-marge" style="font-size:1.4rem">—</div></div>
      </div>
      <p class="small mt-3" id="cc-verdict"></p>
    </div>

    <div class="card card-accent-gold" data-reveal data-delay="90" id="market-calc">
      <h3 class="card-title" style="font-size:1.05rem">Enchères ou marchand ?</h3>
      <p class="small muted mb-3">La question qui décide de chaque objet de votre sac. Comparez le net réel des deux options.</p>
      <div class="grid g-2 gap-3">
        <label class="small">Prix à l'hôtel des ventes
          <input type="number" id="mc-ah" value="14000" min="0" step="500" class="inp"></label>
        <label class="small">Prix chez le marchand
          <input type="number" id="mc-vendor" value="9000" min="0" step="500" class="inp"></label>
        <label class="small">Commission (%)
          <input type="number" id="mc-frais" value="{FR['taux']}" min="0" max="50" step="0.5" class="inp"></label>
        <label class="small">Cases d'inventaire occupées
          <input type="number" id="mc-slots" value="1" min="1" step="1" class="inp"></label>
      </div>
      <div class="divider"></div>
      <div class="grid g-3 gap-3">
        <div class="stat-card"><div class="hud tiny muted">NET ENCHÈRES</div>
          <div class="num txt-green" id="mc-net" style="font-size:1.4rem">—</div></div>
        <div class="stat-card"><div class="hud tiny muted">ÉCART</div>
          <div class="num txt-blue" id="mc-ecart" style="font-size:1.4rem">—</div></div>
        <div class="stat-card"><div class="hud tiny muted">PAR CASE</div>
          <div class="num txt-gold" id="mc-case" style="font-size:1.4rem">—</div></div>
      </div>
      <p class="small mt-3" id="mc-verdict"></p>
    </div>
  </div>

  <div class="alert alert-blue mt-5" data-reveal><span class="ico" aria-hidden="true">i</span>
  <div class="small"><strong>Formule :</strong> <span class="mono">{esc(FR['formule'])}</span> — {esc(FR['regle_5s'])}</div></div>
  <div class="alert alert-green mt-3" data-reveal><span class="ico" aria-hidden="true">★</span>
  <div class="small">{esc(FR['supply_station'])}</div></div>
</div></section>

<section class="section" id="ateliers"><div class="wrap">
  <div class="grid g-2 gap-6">
    <div>
      <div class="section-head" data-reveal><div class="eyebrow">4 ateliers</div><h2>{esc(PRN['titre'])}</h2>
        <p class="lead">{esc(PRN['contenu'])}</p></div>
      <div class="alert alert-orange" data-reveal><span class="ico" aria-hidden="true">!</span>
      <div class="small"><strong>Règle d'or :</strong> {esc(PRN['regle_or'])}</div></div>
    </div>
    <figure class="img-frame" data-reveal>
      <img src="../../assets/images/misc/artisanat_armure_01.jpg" alt="Établi d'armurier avec porte-plaques ouvert, plaques céramiques et casque balistique" loading="lazy" decoding="async">
      <figcaption>Les gilets d'élite restent la valeur sûre historique de l'établi d'armure (illustration générée par IA, pas une capture du jeu)</figcaption>
    </figure>
  </div>
  <div class="grid g-auto-md gap-4 mt-5">{at_ateliers}</div>
</div></section>

<section class="section" id="rentables"><div class="wrap">
  <div class="section-head" data-reveal>
    <div class="eyebrow">{len(AT['rentables'])} productions</div><h2>Ce qui rapporte, et à quelle vitesse</h2>
    <p class="lead">Instantanés de marché relevés entre 2025 et fin 2026. Lisez la colonne « marge » comme un ordre
    de grandeur, jamais comme une promesse — puis recalculez avec le calculateur ci-dessus.</p>
  </div>
  <div class="table-wrap" data-reveal><table class="df" style="min-width:1020px">
    <thead><tr><th class="sortable">Objet</th><th>Atelier</th><th class="num">Coût</th><th class="num">Vente</th>
      <th class="num">Marge</th><th class="num">Durée</th><th>Note</th></tr></thead>
    <tbody>{at_rows}</tbody>
  </table></div>
  <figure class="img-frame mt-6" data-reveal>
    <img src="../../assets/images/misc/artisanat_ammo_01.jpg" alt="Gros plan macro sur des cartouches de fusil dorées dans un plateau de rechargement" loading="lazy" decoding="async">
    <figcaption>Les munitions dorées : la production la plus rentable du Black Site, et celle que vous consommez vous-même (illustration générée par IA, pas une capture du jeu)</figcaption>
  </figure>
</div></section>

<section class="section" id="methode-craft"><div class="wrap">
  <div class="section-head" data-reveal><div class="eyebrow">Méthode</div><h2>Six réflexes avant de lancer une production</h2></div>
  <div class="grid g-auto-md gap-4 mb-6">{at_meth}</div>
  <div class="grid g-2 gap-6">
    <div class="card card-accent-red" data-reveal>
      <h3 class="card-title" style="font-size:1rem">{len(AT['pieges'])} pièges</h3>
      <ul class="small">{at_pieges}</ul>
    </div>
    <div>
      <h3 class="mb-2">{esc(EN['titre'])}</h3>
      <div class="table-wrap" data-reveal><table class="df">
        <thead><tr><th>Rareté</th><th>Où vendre</th><th>Pourquoi</th></tr></thead>
        <tbody>{en_rows}</tbody></table></div>
      <div class="alert alert-gold mt-3" data-reveal><span class="ico" aria-hidden="true">★</span>
      <div class="small">{esc(EN['slots'])}</div></div>
    </div>
  </div>
  <figure class="img-frame mt-6" data-reveal style="max-width:760px;margin-left:auto;margin-right:auto">
    <img src="../../assets/images/misc/encheres_terminal_01.jpg" alt="Comptoir d'échange improvisé dans un conteneur, caisses scellées et balance" loading="lazy" decoding="async">
    <figcaption>La règle des cinq secondes : quelques centaines d'Alloys d'écart ne justifient jamais un emplacement de vente (illustration générée par IA, pas une capture du jeu)</figcaption>
  </figure>
</div></section>

<section class="section-sm"><div class="wrap">
  <div class="grid g-3 gap-4">
    <a class="card card-accent" href="../hazard-ops/departements.html" data-reveal><h3 class="card-title" style="font-size:1rem">Départements</h3>
      <p class="small muted">Vos emplacements de vente dépendent de cet arbre.</p></a>
    <a class="card card-accent" href="../hazard-ops/black-site.html" data-reveal data-delay="80"><h3 class="card-title" style="font-size:1rem">Black Site</h3>
      <p class="small muted">Les 11 stations et le planificateur d'amélioration.</p></a>
    <a class="card card-accent" href="../encyclopedie/economie.html" data-reveal data-delay="160"><h3 class="card-title" style="font-size:1rem">Économie</h3>
      <p class="small muted">La boucle de profit de bout en bout.</p></a>
  </div>
</div></section>
"""

html_art = (head("Artisanat du Black Site & hôtel des ventes — calculateurs de marge",
                 "Calculateur d'artisanat et comparateur enchères/marchand pour Delta Force. "
                 "Commission de 15 %, profit par heure d'atelier, 12 productions rentables chiffrées "
                 "et la règle des cinq secondes pour décider où vendre.",
                 depth=D, canonical="pages/outils/artisanat.html",
                 image="assets/images/misc/artisanat_atelier_01.jpg")
            + navbar(D) + '<main id="main">' + art_body + "</main>" + footer(D) + scripts(D, TOOLS_JS))
print(write("pages/outils/artisanat.html", html_art))


# ====================================================== DUELS & SOLO
DU = load("duels")

du_peek = "".join(f"""<article class="card card-accent-orange" data-reveal data-delay="{i*55}">
    <div class="hud tiny txt-orange mb-2">RÈGLE {i+1:02d}</div>
    <h4 class="card-title" style="font-size:.98rem">{esc(r['nom'])}</h4>
    <p class="small muted">{esc(r['detail'])}</p>
  </article>""" for i, r in enumerate(DU["peek"]["regles"]))

VI = DU["vitesses"]
vi_prat = "".join(f"<li>{esc(x)}</li>" for x in VI["pratique"])

SO = DU["solo"]
so_regles = "".join(f"""<article class="card card-accent-green" data-reveal data-delay="{i*50}">
    <h4 class="card-title" style="font-size:.98rem">{esc(r['titre'])}</h4>
    <p class="small muted">{esc(r['detail'])}</p>
  </article>""" for i, r in enumerate(SO["regles"]))
so_ops = "".join(f"""<div class="card card-accent-blue" data-reveal data-delay="{i*60}">
    <h4 class="card-title" style="font-size:.95rem">{esc(o['nom'])}</h4>
    <p class="small muted">{esc(o['pourquoi'])}</p></div>""" for i, o in enumerate(SO["operateurs"]))

EC = DU["ecoute"]
ec_lignes = "".join(f"<li>{esc(x)}</li>" for x in EC["lignes"])
du_err = "".join(f"<li>{esc(x)}</li>" for x in DU["erreurs"])

CH = DU["checklist"]
ch_items = "".join(f"""<li class="check-row">
    <label><input type="checkbox" data-check="{esc(c['id'])}"> <span>{esc(c['label'])}</span></label>
    <span class="hud tiny muted">{esc(c['duree'])}</span>
  </li>""" for c in CH["items"])

WF = DU["warfare"]
wf_lignes = "".join(f"<li>{esc(x)}</li>" for x in WF["lignes"])

duels_body = f"""
{page_hero("Micro-combat", "Duels, angles et <span class='grad-text'>jeu en solo</span>",
           "La plupart des duels sont décidés avant le premier tir : qui a l'information, "
           "qui a l'angle, qui a choisi le moment. Le réflexe arrive en troisième — "
           "ce qui est une excellente nouvelle, parce que les deux premiers s'apprennent.",
           "assets/images/heroes/duels_hero_01.jpg", D)}

<section class="section-sm"><div class="wrap">
  {crumbs([("Astuces pro", "index.html"), ("Duels &amp; solo", None)], D)}
  <div class="mb-4" style="max-width:560px">{audio_briefing("duels_briefing_01.mp3", "Duels & solo", "", D)}</div>
  <p class="lead" data-reveal style="max-width:74ch">{esc(DU['principe'])}</p>
</div></section>

<section class="section" id="peek"><div class="wrap">
  <div class="section-head" data-reveal>
    <div class="eyebrow">{len(DU['peek']['regles'])} règles</div><h2>{esc(DU['peek']['titre'])}</h2>
  </div>
  <div class="grid g-auto-md gap-4 mb-5">{du_peek}</div>
  <div class="grid g-2 gap-6">
    <figure class="img-frame" data-reveal>
      <img src="../../assets/images/misc/duel_jiggle_peek_01.jpg" alt="Opérateur en mouvement rapide dans l'encadrement d'une porte, silhouette floutée par le déplacement" loading="lazy" decoding="async">
      <figcaption>Le pas dansé déstabilise la visée adverse — mais pas celle d'un joueur qui attend (illustration générée par IA, pas une capture du jeu)</figcaption>
    </figure>
    <figure class="img-frame" data-reveal data-delay="80">
      <img src="../../assets/images/misc/duel_lean_01.jpg" alt="Opérateur penché à droite derrière un pilier de béton, arme épaulée" loading="lazy" decoding="async">
      <figcaption>Pencher à droite expose moins de corps : l'arme est déjà de ce côté (illustration générée par IA, pas une capture du jeu)</figcaption>
    </figure>
  </div>
  <div class="alert alert-blue mt-5" data-reveal><span class="ico" aria-hidden="true">i</span>
  <div class="small">{esc(DU['peek']['latence'])}</div></div>
</div></section>

<section class="section" id="vitesses"><div class="wrap wrap-narrow">
  <div class="section-head" data-reveal><div class="eyebrow">Mécanique</div><h2>{esc(VI['titre'])}</h2>
    <p class="lead">{esc(VI['contenu'])}</p></div>
  <div class="card card-accent-orange" data-reveal><ul class="small">{vi_prat}</ul></div>
</div></section>

<section class="section" id="solo"><div class="wrap">
  <div class="section-head" data-reveal>
    <div class="eyebrow">Seul contre trois</div><h2>{esc(SO['titre'])}</h2>
    <p class="lead">{esc(SO['principe'])}</p>
  </div>
  <div class="grid g-auto-md gap-4 mb-5">{so_regles}</div>
  <h3 class="mb-3">Quatre opérateurs qui pardonnent la solitude</h3>
  <div class="grid g-auto-sm gap-4">{so_ops}</div>
</div></section>

<section class="section" id="ecoute"><div class="wrap">
  <div class="grid g-2 gap-6">
    <div>
      <div class="section-head" data-reveal><div class="eyebrow">Audio</div><h2>{esc(EC['titre'])}</h2></div>
      <div class="card card-accent-green" data-reveal><ul class="small">{ec_lignes}</ul></div>
    </div>
    <div>
      <div class="section-head" data-reveal><div class="eyebrow">{len(DU['erreurs'])} erreurs</div><h2>Ce qui vous tue</h2></div>
      <div class="card card-accent-red" data-reveal><ul class="small">{du_err}</ul></div>
    </div>
  </div>
</div></section>

<section class="section" id="warfare-score"><div class="wrap wrap-narrow">
  <div class="section-head" data-reveal><div class="eyebrow">Havoc Warfare</div><h2>{esc(WF['titre'])}</h2>
    <p class="lead">{esc(WF['contenu'])}</p></div>
  <div class="card card-accent-blue" data-reveal><ul class="small">{wf_lignes}</ul></div>
</div></section>

<section class="section" id="checklist"><div class="wrap">
  <div class="grid g-2 gap-6">
    <div>
      <div class="section-head" data-reveal><div class="eyebrow">Routine</div><h2>{esc(CH['titre'])}</h2>
        <p class="lead">{esc(CH['contenu'])}</p></div>
      <div class="card card-accent-gold" data-reveal>
        <div class="flex-between mb-3">
          <span class="hud tiny muted">PROGRESSION</span>
          <span class="num txt-gold" id="ck-count">0 / {len(CH['items'])}</span>
        </div>
        <div class="statbar mb-4"><div class="fill" id="ck-fill" data-pct="0" style="width:0%"></div></div>
        <ul class="checklist" id="ck-list">{ch_items}</ul>
        <button class="btn btn-ghost mt-3" id="ck-reset" type="button">Réinitialiser la journée</button>
        <p class="small muted mt-2">Vos cases sont conservées dans ce navigateur et se réinitialisent quand vous le décidez.</p>
      </div>
    </div>
    <figure class="img-frame" data-reveal>
      <img src="../../assets/images/misc/checklist_progression_01.jpg" alt="Table de planification tactique avec grille papier, crayon gras, boussole et chronomètre" loading="lazy" decoding="async">
      <figcaption>Quatre systèmes de progression coexistent sans partager le moindre point d'expérience (illustration générée par IA, pas une capture du jeu)</figcaption>
    </figure>
  </div>
</div></section>

<section class="section-sm"><div class="wrap">
  <div class="grid g-3 gap-4">
    <a class="card card-accent" href="index.html" data-reveal><h3 class="card-title" style="font-size:1rem">Réglages &amp; astuces</h3>
      <p class="small muted">Audio, sensibilité et configuration compétitive.</p></a>
    <a class="card card-accent" href="../operateurs/contre-jeu.html" data-reveal data-delay="80"><h3 class="card-title" style="font-size:1rem">Contre-jeu</h3>
      <p class="small muted">Neutraliser les capacités adverses.</p></a>
    <a class="card card-accent" href="../armurerie/gunsmith.html" data-reveal data-delay="160"><h3 class="card-title" style="font-size:1rem">Gunsmith</h3>
      <p class="small muted">Pourquoi votre vitesse de visée s'effondre.</p></a>
  </div>
</div></section>
"""

html_duels = (head("Duels, angles et jeu en solo — micro-combat Delta Force",
                   "Techniques de duel dans Delta Force : pas de côté double, inclinaison droite, préchargement "
                   "d'angle, jeu en solo contre des escouades, discipline sonore, score Warfare et routine "
                   "quotidienne de progression avec checklist interactive.",
                   depth=D, canonical="pages/astuces-pro/duels.html",
                   image="assets/images/heroes/duels_hero_01.jpg")
              + navbar(D) + '<main id="main">' + duels_body + "</main>" + footer(D) + scripts(D, TOOLS_JS))
print(write("pages/astuces-pro/duels.html", html_duels))
