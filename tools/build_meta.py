#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_meta.py — Mandel Brick & mode Classé (page méta avancée de Hazard Ops)."""

from site_common import (head, navbar, footer, scripts, write, esc,
                         load, crumbs, page_hero, audio_briefing)

MB = load("mandel_brick")
RK = load("ranked")
RINT = RK["interrupteur"]
RCQ = RK["ce_qui_compte"]
RALT = RK["echelle_alternative"]
rk_cq = "".join(f"""<article class="card card-accent-blue" data-reveal data-delay="{i*80}">
    <h4 class="card-title" style="font-size:1rem">{esc(m['mode'])}</h4>
    <div class="hud tiny txt-green mb-2">{esc(m['mesure'])}</div>
    <p class="small muted">{esc(m['detail'])}</p></article>""" for i, m in enumerate(RCQ))
rk_alt = "".join(f"""<tr><td><strong>{esc(p['grade'])}</strong></td>
    <td class="mono num txt-gold">{esc(p['points'])}</td></tr>""" for p in RALT["paliers"])

D = 2

# ------------------------------------------------------------------ essentiel
essentiel = "".join(f"<li>{esc(x)}</li>" for x in MB["essentiel"])

# ----------------------------------------------------------------- rendement
rdt_rows = "".join(f"""<tr>
    <td><strong>{esc(r['contexte'])}</strong></td>
    <td data-sort="{esc(r['par_heure'])}"><span class="txt-green mono">{esc(r['par_heure'])}</span></td>
    <td class="small muted">{esc(r['detail'])}</td>
  </tr>""" for r in MB["rendement"])

# ----------------------------------------------------------------- procédure
etapes = "".join(f"""<div class="card card-accent" data-reveal data-delay="{i*60}">
    <div class="hud tiny txt-green mb-2">ÉTAPE {i+1:02d}</div>
    <p class="small">{esc(s)}</p>
  </div>""" for i, s in enumerate(MB["procedure"]))

contre = "".join(f"<li>{esc(x)}</li>" for x in MB["contre_jeu"])

# -------------------------------------------------------------------- ranked
dbl = "".join(f"""<div class="stat-card" data-reveal>
    <div class="stat-label">{esc(d['mode'])}</div>
    <div class="stat-value" style="font-size:1.15rem">{esc(d['condition'])}</div>
  </div>""" for d in RK["deblocage"])

bareme = "".join(f"""<tr>
    <td><strong>{esc(a['action'])}</strong></td>
    <td data-sort="{esc(a['points'].split()[0].replace(',','.'))}"><span class="mono txt-gold">{esc(a['points'])}</span></td>
    <td><span class="badge {'badge-red' if 'maximum' in a['cap'] else 'badge-green'}">{esc(a['cap'])}</span></td>
    <td class="small muted">{esc(a['note'])}</td>
  </tr>""" for a in RK["bareme_operations"])

lecture = "".join(f"<li>{esc(x)}</li>" for x in RK["lecture"])

ladder = "".join(f"""<div class="tier-row" data-reveal data-delay="{i*40}">
    <div class="tier-label" style="background:var(--tier-{'s' if i>=6 else 'a' if i>=4 else 'b' if i>=2 else 'c'})">{i+1}</div>
    <div class="tier-drop" style="justify-content:space-between;padding-inline:1rem">
      <strong>{esc(g['grade'])}</strong>
      <span class="mono small muted">{esc(g['points'])} pts</span>
    </div>
  </div>""" for i, g in enumerate(RK["echelle"]))

MC = RK["cartes_merite"]
mc_rules = "".join(f"<li>{esc(x)}</li>" for x in MC["regles"])
climb = "".join(f"""<div class="card card-accent" data-reveal data-delay="{i*70}">
    <div class="hud tiny txt-green mb-2">LEVIER {i+1:02d}</div>
    <p class="small">{esc(x)}</p></div>""" for i, x in enumerate(RK["climb_warfare"]))

# ---------------------------------------------------------------------- body
body = f"""
{page_hero("Méta avancée", "Mandel Brick &amp; <span class='grad-text'>mode Classé</span>",
           "La ressource la plus disputée du jeu et le barème qui décide de votre rang. "
           "Deux systèmes liés : la brique vaut 20 points de Mérite, sans plafond.",
           "assets/images/misc/mandelbrick_01.jpg", D, badge="SAISON 12")}

<section class="section-sm"><div class="wrap">
  {crumbs([("Hazard Operations", "index.html"), ("Mandel Brick & Classé", None)], D)}
  <div class="mb-4" style="max-width:560px">{audio_briefing("mandelbrick_briefing_01.mp3", "Mandel Brick", "", D)}</div>

  <div class="alert alert-green" data-reveal><span class="ico" aria-hidden="true">◆</span>
  <div><strong>Ce qu'il faut retenir :</strong><ul class="small mt-2">{essentiel}</ul></div></div>
</div></section>

<section class="section" id="rendement"><div class="wrap">
  <div class="section-head" data-reveal>
    <div class="eyebrow">Rendement réel</div><h2>Combien de briques par heure ?</h2>
    <p class="lead">Chiffres issus de mesures communautaires, pas de données officielles. L'écart solo/escouade
    vient presque entièrement de la mécanique de copie.</p>
  </div>
  <div class="table-wrap" data-reveal>
    <table class="df">
      <thead><tr><th class="sortable">Contexte</th><th class="sortable">Par heure</th><th>Détail</th></tr></thead>
      <tbody>{rdt_rows}</tbody>
    </table>
  </div>
  <p class="tiny muted mt-3">⚑ Le pity à 75 scans et le Top 25 % Warfare sont les deux seules voies
  <strong>sans risque d'extraction</strong>. Un joueur qui perd systématiquement ses duels gagne plus par ces routes.</p>
</div></section>

<section class="section" id="procedure"><div class="wrap">
  <div class="section-head" data-reveal>
    <div class="eyebrow">Déroulé</div><h2>Sécuriser une brique, étape par étape</h2>
    <p class="lead">Le décodage dure 4 minutes. C'est long, c'est bruyant, et tout le monde sur la carte le sait.</p>
  </div>
  <div class="grid g-auto-sm">{etapes}</div>
</div></section>

<section class="section"><div class="wrap">
  <div class="grid g-2 gap-6">
    <div>
      <div class="section-head" data-reveal><div class="eyebrow">De l'autre côté</div><h2>Contre-jeu</h2></div>
      <div class="card card-accent-red" data-reveal><ul class="small">{contre}</ul></div>
    </div>
    <div>
      <div class="section-head" data-reveal><div class="eyebrow">Erreur fréquente</div><h2>La Safe Box n'extrait pas</h2></div>
      <div class="card card-accent-orange" data-reveal>
        <p class="small">Déposer la brique — ou n'importe quel objet de mission — dans la Safe Box
        <strong>ne valide aucun objectif d'extraction</strong>. La Safe Box protège la valeur en cas de mort ;
        elle ne remplace jamais une sortie réussie.</p>
        <div class="divider"></div>
        <p class="small muted">Beaucoup de contrats échoués viennent uniquement de cette confusion.</p>
      </div>
    </div>
  </div>
</div></section>

<section class="section" id="classe"><div class="wrap">
  <div class="section-head" data-reveal>
    <div class="eyebrow">Mode Classé</div><h2>Barème des points de Mérite</h2>
    <p class="lead">{esc(RK['regle_cle'])}</p>
  </div>
  <div class="grid g-2 gap-4 mb-5">{dbl}</div>
  <div class="table-wrap" data-reveal>
    <table class="df">
      <thead><tr><th class="sortable">Action</th><th class="sortable">Points</th><th>Plafond</th><th>Lecture</th></tr></thead>
      <tbody>{bareme}</tbody>
    </table>
  </div>
  <div class="alert alert-blue mt-5" data-reveal><span class="ico" aria-hidden="true">💡</span>
  <div><strong>Comment lire ce barème :</strong><ul class="small mt-2">{lecture}</ul></div></div>
</div></section>

<section class="section" id="echelle"><div class="wrap">
  <div class="grid g-2 gap-6">
    <div>
      <div class="section-head" data-reveal><div class="eyebrow">Progression</div><h2>L'échelle des grades</h2>
        <p class="lead">Sept paliers documentés, par tranches de 300 points de Mérite.</p></div>
      <div class="tierlist" data-reveal>{ladder}</div>
    </div>
    <div>
      <div class="section-head" data-reveal><div class="eyebrow">Multiplicateur</div><h2>Cartes 2× Mérite</h2></div>
      <div class="card card-accent-gold" data-reveal>
        <p class="small mb-3">{esc(MC['effet'])}</p>
        <ul class="small">{mc_rules}</ul>
        <div class="divider"></div>
        <p class="tiny muted">Obtention : {esc(MC['obtention'])}</p>
      </div>
    </div>
  </div>
</div></section>

<section class="section" id="monter"><div class="wrap">
  <div class="section-head" data-reveal>
    <div class="eyebrow">Warfare</div><h2>Monter vite, sans forcer les duels</h2>
    <p class="lead">Le classé mesure un score par minute, pas un ratio d'éliminations. C'est une excellente
    nouvelle pour qui ne gagne pas ses duels à l'adresse pure.</p>
  </div>
  <div class="grid g-auto-sm">{climb}</div>
</div></section>

<section class="section-sm"><div class="wrap">
  <div class="grid g-3 gap-4">
    <a class="card card-accent" href="index.html" data-reveal><h3 class="card-title" style="font-size:1rem">Hazard Operations</h3>
      <p class="small muted">La boucle de raid, les 6 cartes et l'économie.</p></a>
    <a class="card card-accent" href="boss.html" data-reveal data-delay="80"><h3 class="card-title" style="font-size:1rem">Boss &amp; butin</h3>
      <p class="small muted">Qui garde les conteneurs, et avec quoi.</p></a>
    <a class="card card-accent" href="../astuces-pro/index.html" data-reveal data-delay="160"><h3 class="card-title" style="font-size:1rem">Astuces pro</h3>
      <p class="small muted">Conseils de terrain et parcours faible-PvP.</p></a>
  </div>
</div></section>

<section class="section" id="classe-operations"><div class="wrap">
  <div class="section-head" data-reveal>
    <div class="eyebrow">Mode Classé</div><h2>{esc(RINT["titre"])}</h2>
    <p class="lead">{esc(RINT["contenu"])}</p>
  </div>
  <div class="grid g-2 gap-4 mb-6">{rk_cq}</div>

  <div class="grid g-2 gap-6">
    <figure class="img-frame" data-reveal>
      <img src="../../assets/images/misc/classe_grades_01.jpg" alt="Rangée d'insignes de grade militaires gravés sur une plaque métallique rétroéclairée" loading="lazy" decoding="async">
      <figcaption>Les paliers débloquent des récompenses strictement cosmétiques (illustration générée par IA, pas une capture du jeu)</figcaption>
    </figure>
    <div>
      <h3 class="mb-2">{esc(RALT["titre"])}</h3>
      <div class="alert alert-orange mb-3" data-reveal><span class="ico" aria-hidden="true">!</span>
      <div class="small">{esc(RALT["avertissement"])}</div></div>
      <div class="table-wrap" data-reveal><table class="df">
        <thead><tr><th>Grade</th><th>Points</th></tr></thead><tbody>{rk_alt}</tbody></table></div>
      <p class="small muted mt-2">{esc(RALT["recompenses"])}</p>
    </div>
  </div>
</div></section>

"""


MO = RK["montee_operations"]
ST = MO["strategie"]
_bar = "".join(f"""<tr><td class="small">{esc(b['action'])}</td>
    <td class="num txt-gold mono"><strong>+{esc(b['pts'])}</strong></td></tr>""" for b in MO["bareme"])

rk_montee = f"""
<section class="section" id="montee"><div class="wrap">
  <div class="section-head" data-reveal>
    <div class="eyebrow">Classé Operations</div><h2>{esc(MO['titre'])}</h2>
  </div>
  <div class="alert alert-orange mb-4" data-reveal><span class="ico" aria-hidden="true">!</span>
  <div class="small">{esc(MO['avertissement'])}</div></div>
  <div class="grid g-2 gap-6">
    <div>
      <div class="table-wrap" data-reveal><table class="df">
        <thead><tr><th>Action</th><th>Points</th></tr></thead><tbody>{_bar}</tbody></table></div>
      <div class="alert alert-blue mt-3" data-reveal><span class="ico" aria-hidden="true">i</span>
      <div class="small">{esc(MO['nuance'])}</div></div>
      <figure class="img-frame mt-4" data-reveal>
        <img src="../../assets/images/misc/rat_run_01.jpg" alt="Silhouette accroupie immobile dans l'ombre d'une cage d'escalier face à une porte ensoleillée" loading="lazy" decoding="async">
        <figcaption>La méthode la plus fiable n'est pas la plus rapide (illustration générée par IA, pas une capture du jeu)</figcaption>
      </figure>
    </div>
    <div>
      <div class="card card-accent-green" data-reveal>
        <div class="hud tiny txt-green mb-2">STRATÉGIE</div>
        <h3 class="card-title" style="font-size:1.05rem">{esc(ST['nom'])}</h3>
        <p class="small">{esc(ST['detail'])}</p>
        <div class="divider" style="margin:.9rem 0"></div>
        <p class="small txt-orange" style="margin:0 0 .6rem"><strong>{esc(ST['eviter'])}</strong></p>
        <p class="small muted" style="margin:0">{esc(ST['verdict'])}</p>
      </div>
    </div>
  </div>
</div></section>
"""
html = (head("Mandel Brick & mode Classé — farm, rendement et barème de Mérite",
             "Guide du Mandel Brick dans Delta Force Saison 12 : rendement par heure solo et en escouade, "
             "mécanique de copie, pity à 75 scans, et barème complet des points de Mérite du mode Classé.",
             depth=D, canonical="pages/hazard-ops/mandel-brick.html",
             image="assets/images/misc/mandelbrick_01.jpg")
        + navbar(D) + '<main id="main">' + body + rk_montee + "</main>" + footer(D) + scripts(D))
print(write("pages/hazard-ops/mandel-brick.html", html))
