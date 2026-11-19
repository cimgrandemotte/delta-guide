#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_detonation.py — Mode Detonation 5v5 (pose / désamorçage)."""

from site_common import (head, navbar, footer, scripts, write, esc,
                         load, crumbs, page_hero, audio_briefing)

DT = load("detonation")
D = 2

regles = "".join(f"""<tr>
    <td><strong>{esc(r['mecanique'])}</strong></td>
    <td class="small muted">{esc(r['detail'])}</td>
  </tr>""" for r in DT["regles"])

EC = DT["economie"]
eco_rules = "".join(f"<li>{esc(x)}</li>" for x in EC["regles"])

cartes = "".join(f"""<article class="card card-accent-blue" data-reveal data-delay="{i*90}">
    <div class="flex items-center justify-between gap-2 mb-2">
      <h3 class="card-title" style="font-size:1.05rem">{esc(c['nom'])}</h3>
      <span class="badge badge-grey">{esc(c['profil'])}</span>
    </div>
    <p class="small muted">{esc(c['conseil'])}</p>
  </article>""" for i, c in enumerate(DT["cartes"]))

att = "".join(f"""<div class="card card-accent-orange" data-reveal data-delay="{i*55}">
    <div class="hud tiny txt-orange mb-2">ATTAQUE {i+1:02d}</div>
    <p class="small">{esc(x)}</p></div>""" for i, x in enumerate(DT["tactiques_attaque"]))

dfs = "".join(f"""<div class="card card-accent-blue" data-reveal data-delay="{i*55}">
    <div class="hud tiny txt-blue mb-2">DÉFENSE {i+1:02d}</div>
    <p class="small">{esc(x)}</p></div>""" for i, x in enumerate(DT["tactiques_defense"]))

s12 = "".join(f"<li>{esc(x)}</li>" for x in DT["changements_s12"])

TM = EC["table_manches"]
tm_rows = "".join("<tr>" + "".join(
    f'<td class="{"mono num txt-gold" if j==1 else ("small" if j==2 else "")}"><strong>{esc(c)}</strong></td>'
    if j == 0 else f'<td class="{"mono num txt-gold" if j==1 else "small muted"}">{esc(c)}</td>'
    for j, c in enumerate(l)) + "</tr>" for l in TM["lignes"])

px_rows = "".join(f"""<tr>
    <td><strong>{esc(p['objet'])}</strong></td>
    <td class="mono num txt-gold">{esc(p['prix'])}</td>
    <td class="small muted">{esc(p['categorie'])}</td>
  </tr>""" for p in EC["prix_reperes"])

RV = EC["revenus"]
rv_rows = "".join(f"""<tr>
    <td><strong>{esc(r['source'])}</strong></td>
    <td class="mono num muted">{esc(r['avant'])}</td>
    <td class="mono num txt-green">{esc(r['apres'])}</td>
  </tr>""" for r in RV["lignes"])

PA = DT["patch_15_octobre"]
pa_win = "".join(f"<li>{esc(x)}</li>" for x in PA["gagnants"])
pa_los = "".join(f"<li>{esc(x)}</li>" for x in PA["perdants"])
err_det = "".join(f"""<div class="card card-accent-red" data-reveal data-delay="{i*55}">
    <div class="hud tiny txt-red mb-2">PIÈGE {i+1:02d}</div>
    <p class="small">{esc(x)}</p></div>""" for i, x in enumerate(DT["erreurs_frequentes"]))

body = f"""
{page_hero("Mode tactique", "Deton<span class='grad-text'>ation</span>",
           "Cinq contre cinq, aucune réapparition, une économie par manche. Le format le plus exigeant "
           "de Delta Force — et celui où l'utilitaire compte autant que l'adresse.",
           "assets/images/detonation/detonation_site_01.jpg", D, badge="BÊTA")}

<section class="section-sm"><div class="wrap">
  {crumbs([("Detonation", None)], D)}
  <div class="mb-4" style="max-width:560px">{audio_briefing("detonation_briefing_01.mp3", "Detonation", "", D)}</div>
  <div class="alert alert-orange" data-reveal><span class="ico" aria-hidden="true">⚠</span>
  <div class="small">{esc(DT['avertissement'])}</div></div>
</div></section>

<section class="section" id="regles"><div class="wrap">
  <div class="section-head" data-reveal>
    <div class="eyebrow">Fondamentaux</div><h2>Les règles du mode</h2>
    <p class="lead">Quatre secondes pour poser, six pour désamorcer. Tout le mode tient dans cet écart.</p>
  </div>
  <div class="table-wrap" data-reveal><table class="df" style="min-width:620px">
    <thead><tr><th>Mécanique</th><th>Détail</th></tr></thead>
    <tbody>{regles}</tbody>
  </table></div>
</div></section>

<section class="section" id="economie"><div class="wrap">
  <div class="grid g-2 gap-6">
    <div>
      <div class="section-head" data-reveal><div class="eyebrow">Gestion</div><h2>L'économie d'Alloys</h2>
        <p class="lead">{esc(EC['principe'])}</p></div>
      <div class="card card-accent-gold" data-reveal><ul class="small">{eco_rules}</ul></div>
    </div>
    <div>
      <div class="section-head" data-reveal><div class="eyebrow">Déblocages</div><h2>Jetons d'arme</h2></div>
      <div class="card card-accent" data-reveal>
        <p class="small">{esc(EC['tokens'])}</p>
        <div class="divider"></div>
        <p class="small muted">Conséquence pratique : votre arsenal en Detonation ne reflète pas celui de Warfare.
        Prévoyez de dépenser vos premiers jetons sur une arme polyvalente plutôt que sur une curiosité.</p>
      </div>
      <figure class="img-frame mt-4" data-reveal>
        <img src="../../assets/images/detonation/detonation_manoir_01.jpg" alt="Cour intérieure d'un manoir abandonné aux angles multiples" loading="lazy" decoding="async">
        <figcaption>Shariq Manor — couloirs et cour centrale (illustration générée par IA, pas une capture du jeu)</figcaption>
      </figure>
    </div>
  </div>
</div></section>

<section class="section" id="cartes"><div class="wrap">
  <div class="section-head" data-reveal><div class="eyebrow">{len(DT['cartes'])} cartes</div><h2>Les terrains</h2></div>
  <div class="grid g-2 gap-4">{cartes}</div>
</div></section>

<section class="section" id="tactiques"><div class="wrap">
  <div class="section-head" data-reveal>
    <div class="eyebrow">Jeu d'équipe</div><h2>Attaquer</h2>
    <p class="lead">Une seule idée structure toute l'attaque : après la pose, votre objectif change complètement.</p>
  </div>
  <div class="grid g-auto-sm mb-6">{att}</div>

  <div class="section-head" data-reveal><div class="eyebrow">Jeu d'équipe</div><h2>Défendre</h2></div>
  <div class="grid g-auto-sm">{dfs}</div>
</div></section>

<section class="section" id="s12"><div class="wrap wrap-narrow">
  <div class="section-head" data-reveal><div class="eyebrow">Saison 12</div><h2>Ce qui a changé</h2></div>
  <div class="card card-accent-green" data-reveal><ul class="small">{s12}</ul></div>
  <div class="alert alert-red mt-5" data-reveal><span class="ico" aria-hidden="true">⚠</span>
  <div class="small">{esc(DT['rappel_operateurs'])}</div></div>
</div></section>

<section class="section" id="table-economie"><div class="wrap">
  <div class="section-head" data-reveal>
    <div class="eyebrow">Chiffres</div><h2>L'argent, manche par manche</h2>
    <p class="lead">{esc(TM['note'])}</p>
  </div>
  <div class="alert alert-orange mb-4" data-reveal><span class="ico" aria-hidden="true">⚠</span>
  <div class="small">{esc(TM['avertissement'])}</div></div>
  <div class="grid g-2 gap-6">
    <div>
      <div class="table-wrap" data-reveal><table class="df" style="min-width:420px">
        <thead><tr><th>Manche</th><th>Alloys</th><th>Armes débloquées</th></tr></thead>
        <tbody>{tm_rows}</tbody></table></div>
      <h3 class="card-title mt-5 mb-3" style="font-size:1rem">{esc(RV['titre'])}</h3>
      <div class="table-wrap" data-reveal><table class="df" style="min-width:420px">
        <thead><tr><th>Source</th><th>Avant</th><th>Après</th></tr></thead>
        <tbody>{rv_rows}</tbody></table></div>
      <p class="small muted mt-3">{esc(RV['consequence'])}</p>
    </div>
    <div>
      <h3 class="card-title mb-3" style="font-size:1rem">Prix repères</h3>
      <div class="table-wrap" data-reveal><table class="df" style="min-width:380px">
        <thead><tr><th>Objet</th><th>Alloys</th><th>Type</th></tr></thead>
        <tbody>{px_rows}</tbody></table></div>
      <figure class="img-frame mt-4" data-reveal>
        <img src="../../assets/images/detonation/detonation_achat_01.jpg" alt="Table d'armurerie avec armes, gilets et grenades alignés avant une partie" loading="lazy" decoding="async">
        <figcaption>La phase d'achat : armure et utilitaire sortent du même portefeuille que l'arme (illustration générée par IA, pas une capture du jeu)</figcaption>
      </figure>
    </div>
  </div>
</div></section>

<section class="section" id="patch-octobre"><div class="wrap">
  <div class="section-head" data-reveal>
    <div class="eyebrow">Méta</div><h2>{esc(PA['titre'])}</h2>
    <p class="lead">{esc(PA['avertissement'])}</p>
  </div>
  <div class="grid g-2 gap-4 mb-5">
    <div class="card card-accent-green" data-reveal>
      <h3 class="card-title" style="font-size:1rem">Gagnants</h3>
      <ul class="small">{pa_win}</ul>
    </div>
    <div class="card card-accent-red" data-reveal data-delay="80">
      <h3 class="card-title" style="font-size:1rem">Perdants</h3>
      <ul class="small">{pa_los}</ul>
    </div>
  </div>
  <div class="card card-accent-gold" data-reveal>
    <h3 class="card-title" style="font-size:1rem">{esc(DT['achat_type']['titre'])}</h3>
    <p class="small">{esc(DT['achat_type']['contenu'])}</p>
  </div>
  <div class="alert alert-blue mt-4" data-reveal><span class="ico" aria-hidden="true">i</span>
  <div class="small"><strong>Classé —</strong> {esc(PA['classe'])}</div></div>
</div></section>

<section class="section" id="pieges"><div class="wrap">
  <div class="section-head" data-reveal><div class="eyebrow">À éviter</div><h2>Les cinq pièges du débutant</h2></div>
  <div class="grid g-auto-sm gap-4">{err_det}</div>
  <figure class="img-frame mt-6" data-reveal>
    <img src="../../assets/images/detonation/detonation_transit_01.jpg" alt="Quai de gare surélevé aux longues lignes de vue dégagées" loading="lazy" decoding="async">
    <figcaption>Transit — des lignes de vue longues qui récompensent un fusil stable (illustration générée par IA, pas une capture du jeu)</figcaption>
  </figure>
</div></section>

<section class="section-sm"><div class="wrap">
  <div class="grid g-3 gap-4">
    <a class="card card-accent" href="../havoc-warfare/index.html" data-reveal><h3 class="card-title" style="font-size:1rem">Havoc Warfare</h3>
      <p class="small muted">L'autre extrême : 32 contre 32 et des véhicules.</p></a>
    <a class="card card-accent" href="../hazard-ops/index.html" data-reveal data-delay="80"><h3 class="card-title" style="font-size:1rem">Hazard Operations</h3>
      <p class="small muted">Le mode extraction et son économie persistante.</p></a>
    <a class="card card-accent" href="../saison-aurora/index.html" data-reveal data-delay="160"><h3 class="card-title" style="font-size:1rem">Saison Aurora</h3>
      <p class="small muted">Toutes les notes de patch, triées par mode.</p></a>
  </div>
</div></section>
"""

html = (head("Detonation — guide du mode 5v5 pose et désamorçage",
             "Guide complet du mode Detonation de Delta Force : règles 5v5, économie d'Alloys par manche, "
             "cartes Transit et Shariq Manor, tactiques d'attaque et de défense, changements de la Saison 12.",
             depth=D, canonical="pages/detonation/index.html",
             image="assets/images/detonation/detonation_site_01.jpg")
        + navbar(D) + '<main id="main">' + body + "</main>" + footer(D) + scripts(D))
print(write("pages/detonation/index.html", html))
