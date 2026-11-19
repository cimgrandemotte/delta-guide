#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_operateurs.py — Page des 19 opérateurs."""

from site_common import (head, navbar, footer, scripts, write, esc,
                         load, crumbs, page_hero, audio_briefing)

ops = load("operators")
D = 2
CLASSES = ["Assault", "Engineer", "Support", "Recon"]
CLASS_COLOR = {"Assault": "red", "Engineer": "gold", "Support": "green", "Recon": "blue"}


def tier_badge(t):
    if not t or t in ("—", "N/A"):
        return '<span class="badge badge-grey">—</span>'
    return f'<span class="tier tier-{esc(t)}" style="width:1.5rem;height:1.5rem;font-size:.78rem">{esc(t)}</span>'


# ------------------------------------------------------------------ CARTES
cards = []
for i, o in enumerate(ops["operateurs"]):
    cls = o.get("classe", "—")
    color = CLASS_COLOR.get(cls, "grey")
    new = '<span class="badge badge-new">NOUVEAU S12</span>' if o.get("badge") == "NEW S12" else ""
    conf = ('<span class="badge badge-grey">À CONFIRMER</span>'
            if o.get("badge") == "À CONFIRMER" else "")
    caps = "".join(
        f"""<div class="mb-3">
          <div class="flex items-center gap-2 mb-1">
            <strong class="txt-green">{esc(c['nom'])}</strong>
            <span class="badge badge-grey">{esc(c.get('type',''))}</span>
          </div>
          <p class="small muted">{esc(c.get('desc',''))}</p>
          {f'<p class="tiny txt-orange mt-1">⚑ {esc(c["note"])}</p>' if c.get('note') else ''}
        </div>""" for c in o.get("capacites", []))

    forces = "".join(f"<li>{esc(x)}</li>" for x in o.get("forces", []))
    faibl = "".join(f"<li>{esc(x)}</li>" for x in o.get("faiblesses", []))
    conseils = "".join(f"<li>{esc(x)}</li>" for x in o.get("conseils", []))
    counters = o.get("counters", [])
    counters_html = ("".join(f'<span class="chip">{esc(c)}</span>' for c in counters)
                     if isinstance(counters, list) else f'<p class="small muted">{esc(counters)}</p>')

    cards.append(f"""<article class="card op-card" id="{esc(o['id'])}"
      data-tags="{esc(cls.lower())} {'new' if new else ''} tier-{esc(o.get('tier_ops','x')).lower()}"
      data-search="{esc(o['nom'])} {esc(o.get('nom_reel',''))} {esc(cls)} {esc(o.get('resume',''))}"
      data-reveal data-delay="{(i % 3) * 70}">
      <div class="flex items-start justify-between gap-3 mb-3">
        <div>
          <div class="op-class">{esc(cls)}</div>
          <h3 class="op-name">{esc(o['nom'])}</h3>
          <p class="tiny muted">{esc(o.get('nom_reel') or 'Identité non publiée')}</p>
        </div>
        <div class="flex gap-1">{new}{conf}</div>
      </div>

      <div class="flex gap-4 mb-3 small">
        <span class="flex items-center gap-1">{tier_badge(o.get('tier_ops'))} <span class="tiny muted">OPS</span></span>
        <span class="flex items-center gap-1">{tier_badge(o.get('tier_warfare'))} <span class="tiny muted">WARFARE</span></span>
      </div>

      <p class="small mb-3">{esc(o.get('resume',''))}</p>

      <details class="acc">
        <summary>Capacités &amp; fiche détaillée</summary>
        <div class="acc-body">
          <div class="hud-head" style="margin-top:0">Capacités</div>
          {caps}
          <div class="grid g-2 gap-4 mt-4">
            <div>
              <div class="hud-head txt-green">Forces</div>
              <ul class="small muted">{forces}</ul>
            </div>
            <div>
              <div class="hud-head" style="color:var(--df-red);border-bottom-color:var(--line-2)">Faiblesses</div>
              <ul class="small muted">{faibl}</ul>
            </div>
          </div>
          {f'<div class="hud-head mt-4">Conseils de jeu</div><ul class="small muted">{conseils}</ul>' if conseils else ''}
          {f'<div class="hud-head mt-4">Counters</div><div class="chips">{counters_html}</div>' if counters else ''}
          <div class="divider"></div>
          <p class="tiny muted"><strong>Arrivée :</strong> {esc(o.get('arrivee','—'))}<br>
          <strong>Déblocage :</strong> {esc(o.get('deblocage','—'))}</p>
        </div>
      </details>
    </article>""")

cards_html = "".join(cards)

# ------------------------------------------------------------------ SYNERGIES
syn = "".join(
    f"""<div class="card card-accent-blue" data-reveal>
      <h3 class="card-title" style="font-size:1rem">{esc(s.get('nom', '—'))}</h3>
      <div class="chips mb-2">{''.join(f'<span class="chip active">{esc(m)}</span>' for m in s.get('composition', s.get('operateurs', [])))}</div>
      <p class="small muted">{esc(s.get('pourquoi', s.get('effet', s.get('description',''))))}</p>
    </div>""" for s in ops.get("synergies", []))

# ------------------------------------------------------------------ DÉBLOCAGE
unlock = "".join(
    f"""<div class="tl-item">
      <div class="tl-date">Priorité {esc(u.get('rang', '?'))}</div>
      <h4 style="font-size:1rem">{esc(u.get('operateur', u.get('action','—')))}
        <span class="badge badge-green">{esc(u.get('cout','—'))}</span></h4>
      <p class="small muted">{esc(u.get('raison', u.get('pourquoi','')))}</p>
    </div>""" for u in ops.get("ordre_deblocage_recommande", []))

filters = "".join(f'<button class="chip" data-val="{c.lower()}">{c}</button>' for c in CLASSES)

body = f"""
{page_hero("Dossiers personnels", "Les <span class='grad-text'>19 opérateurs</span>",
           "Classe, capacités, forces, faiblesses, counters et tier par mode. "
           "Chaque fiche précise <strong>à quel mode s'applique</strong> chaque changement d'équilibrage.",
           "assets/images/operators/operateurs_martelo_01.jpg", D)}

<section class="section-sm"><div class="wrap">
  <figure class="img-frame mb-5" data-reveal><img src="../../assets/images/operators/operateurs_escouade_01.jpg" alt="Quatre opérateurs aux rôles distincts dans une zone de préparation" loading="lazy" decoding="async"><figcaption>Brèche, ingénierie, soutien médical, reconnaissance : les quatre rôles d'une escouade équilibrée (illustration générée par IA, pas une capture du jeu)</figcaption></figure>
</div></section>

<section class="section-sm"><div class="wrap">
  {crumbs([("Opérateurs", None)], D)}
</div></section>

<section class="section-sm"><div class="wrap">
  <div class="grid g-3 gap-4"><figure class="img-frame" data-reveal data-delay="0"><img src="../../assets/images/operators/operateurs_recon_01.jpg" alt="Spécialiste reconnaissance déployant un drone sur un toit" loading="lazy" decoding="async"><figcaption>Reconnaissance — l'information avant le contact</figcaption></figure><figure class="img-frame" data-reveal data-delay="80"><img src="../../assets/images/operators/operateurs_support_01.jpg" alt="Médecin de combat soignant un coéquipier derrière un muret" loading="lazy" decoding="async"><figcaption>Soutien — le rôle qui génère le plus de score par minute</figcaption></figure><figure class="img-frame" data-reveal data-delay="160"><img src="../../assets/images/operators/operateurs_ingenieur_01.jpg" alt="Ingénieur de combat soudant le blindage d'un véhicule" loading="lazy" decoding="async"><figcaption>Ingénierie — réparer et neutraliser compte plus qu'éliminer</figcaption></figure></div>
  <p class="tiny muted mt-3">Illustrations générées par IA, pas des captures du jeu.</p>
  <div class="mb-4" style="max-width:560px">{audio_briefing("operateurs_briefing_01.mp3", "Opérateurs", "", D)}</div>
  <div class="alert alert-red" data-reveal>
    <span class="ico" aria-hidden="true">⚠</span>
    <div><strong>Changements Detonation-only.</strong> Les buffs et nerfs d'Aurora concernant
    Toxik, Raptor, Morse, Uluru, Gizmo, Stinger, Hackclaw, Vlinder, Desmoulins et les GE2 de Luna et Shepherd
    ne s'appliquent <em>qu'au mode Detonation</em>. Ils sont signalés comme tels dans chaque fiche.</div>
  </div>
</div></section>

<section class="section-sm"><div class="wrap">
  <div class="hud-panel" data-filter-group data-filter-target=".op-card"
       data-filter-input="#op-search" data-filter-count="#op-count" data-reveal>
    <div class="flex wrapf items-center justify-between gap-4">
      <div class="chips">
        <button class="chip active" data-val="all">Tous</button>
        {filters}
        <button class="chip" data-val="new">Nouveautés S12</button>
      </div>
      <div class="field" style="min-width:230px">
        <label for="op-search">Recherche</label>
        <input class="input" id="op-search" type="search" placeholder="Nom, classe, capacité…">
      </div>
    </div>
    <p class="tiny muted mt-3"><span id="op-count">19</span> opérateur(s) affiché(s) sur 19.</p>
  </div>
</div></section>

<section class="section-sm"><div class="wrap">
  <div class="grid g-auto-md">{cards_html}</div>
</div></section>

<section class="section"><div class="wrap">
  <div class="section-head" data-reveal>
    <div class="eyebrow">Composition d'escouade</div>
    <h2>Synergies</h2>
    <p class="lead">Une escouade n'est pas une addition de bons opérateurs : c'est une combinaison de rôles.</p>
  </div>
  <div class="grid g-auto-md">{syn}</div>
</div></section>

<section class="section"><div class="wrap wrap-narrow">
  <div class="section-head" data-reveal>
    <div class="eyebrow">Progression</div>
    <h2>Ordre de déblocage recommandé</h2>
  </div>
  <div class="timeline" data-reveal>{unlock}</div>
</div></section>

<section class="section-sm"><div class="wrap">
  <div class="alert alert-blue" data-reveal>
    <span class="ico" aria-hidden="true">ℹ</span>
    <div><strong>Note sur Branko.</strong> Cet opérateur circule dans plusieurs listes communautaires mais
    <strong>n'apparaît pas dans le roster du wiki de référence</strong>. Sa fiche est conservée avec la mention
    « À CONFIRMER » tant qu'une source officielle ne tranche pas.</div>
  </div>
</div></section>
"""

html = (head("Les 19 opérateurs", "Fiches complètes des 19 opérateurs de Delta Force : classes, capacités, "
             "forces, faiblesses, counters, tier list Operations et Warfare, synergies d'escouade et ordre "
             "de déblocage. À jour Saison 12 Aurora, avec Martelo.",
             depth=D, canonical="pages/operateurs/index.html",
             image="assets/images/operators/operateurs_martelo_01.jpg")
        + navbar(D) + '<main id="main">' + body + "</main>" + footer(D) + scripts(D))

print(write("pages/operateurs/index.html", html))


# ====================================================== CONTRE-JEU
CJ = load("contre_jeu")

ru = CJ["regle_universelle"]
ru_q = "".join(f"""<li class="mb-2"><strong class="txt-blue num">{i+1}.</strong> {esc(q)}</li>"""
               for i, q in enumerate(ru["questions"]))

def _menace_card(m, i):
    lim = "".join(f"<li>{esc(x)}</li>" for x in m["limites"])
    return f"""<article class="card card-accent-orange" data-reveal data-delay="{(i%3)*70}" data-filter-item data-tags="{esc(m['nom'].lower())} {esc(m['role'].lower())}">
    <div class="flex-between mb-2">
      <h3 class="card-title" style="font-size:1.15rem;margin:0">{esc(m['nom'])}</h3>
      <span class="badge badge-grey">{esc(m['role'])}</span>
    </div>
    <div class="hud tiny txt-red mb-2">MENACE · {esc(m['menace'])}</div>
    <p class="small">{esc(m['ce_que_ca_fait'])}</p>
    <div class="divider"></div>
    <div class="hud tiny txt-orange mb-1">LIMITES EXPLOITABLES</div>
    <ul class="small muted">{lim}</ul>
    <div class="divider"></div>
    <div class="hud tiny txt-green mb-1">COMMENT LE CONTRER</div>
    <p class="small">{esc(m['contre'])}</p>
    <div class="divider"></div>
    <p class="small muted"><strong class="txt-blue">Si vous le jouez :</strong> {esc(m['piege_pour_le_lanceur'])}</p>
    <p class="small muted"><strong class="txt-red">Vrai danger :</strong> {esc(m['danger_reel'])}</p>
  </article>"""

menaces = "".join(_menace_card(m, i) for i, m in enumerate(CJ["menaces"]))
compo = "".join(f"<li class='mb-2'>{esc(x)}</li>" for x in CJ["compositions"]["lignes"])
SON = CJ["sonore"]

cj_body = f"""
{page_hero("Tactique", "Le <span class='grad-text'>contre-jeu</span> des capacités",
           "Chaque capacité a une portée, un angle et une fenêtre. Les connaître transforme "
           "un kit qu'on subit en un kit qu'on exploite — et la plupart des contres ne sont pas "
           "des capacités opposées, mais des réflexes.",
           "assets/images/heroes/contrejeu_hero_01.jpg", D)}

<section class="section-sm"><div class="wrap">
  {crumbs([("Opérateurs", "index.html"), ("Contre-jeu", None)], D)}
  <div class="mb-4" style="max-width:560px">{audio_briefing("contrejeu_briefing_01.mp3", "Contre-jeu", "", D)}</div>
  <p class="lead" data-reveal style="max-width:72ch">{esc(CJ['principe'])}</p>
  <div class="alert alert-blue mt-4" data-reveal><span class="ico" aria-hidden="true">i</span>
  <div class="small">{esc(CJ['_meta']['avertissement'])}</div></div>
</div></section>

<section class="section" id="reflexe"><div class="wrap">
  <div class="grid g-2 gap-6">
    <div>
      <div class="section-head" data-reveal><div class="eyebrow">Le réflexe</div><h2>{esc(ru['titre'])}</h2></div>
      <div class="card card-accent-blue" data-reveal><ul class="small" style="list-style:none;padding-left:0">{ru_q}</ul></div>
    </div>
    <figure class="img-frame" data-reveal>
      <img src="../../assets/images/operators/operateurs_drone_scan_01.jpg" alt="Petit drone quadrirotor stationnaire dans un couloir industriel enfumé" loading="lazy" decoding="async">
      <figcaption>Drones, grappins et projectiles ont de larges boîtes de collision : un tir les annule (illustration générée par IA, pas une capture du jeu)</figcaption>
    </figure>
  </div>
</div></section>

<section class="section" id="menaces"><div class="wrap">
  <div class="section-head" data-reveal>
    <div class="eyebrow">{len(CJ['menaces'])} menaces</div><h2>Fiche de contre, opérateur par opérateur</h2>
    <p class="lead">Pour chacun : ce que la capacité fait, où elle s'arrête, et le geste qui l'annule.</p>
  </div>
  <div class="grid g-auto-md gap-4">{menaces}</div>
</div></section>

<section class="section" id="composition"><div class="wrap">
  <div class="grid g-2 gap-6">
    <figure class="img-frame" data-reveal>
      <img src="../../assets/images/operators/operateurs_bouclier_01.jpg" alt="Opérateur accroupi derrière un bouclier balistique dans l'encadrement d'une porte" loading="lazy" decoding="async">
      <figcaption>Dans un couloir sans contournement, le bouclier reste un vrai problème (illustration générée par IA, pas une capture du jeu)</figcaption>
    </figure>
    <div>
      <div class="section-head" data-reveal><div class="eyebrow">Escouade</div><h2>{esc(CJ['compositions']['titre'])}</h2></div>
      <div class="card card-accent-green" data-reveal><ul class="small">{compo}</ul></div>
      <div class="card card-accent-gold mt-4" data-reveal>
        <h3 class="card-title" style="font-size:1rem">{esc(SON['titre'])}</h3>
        <p class="small">{esc(SON['contenu'])}</p>
      </div>
    </div>
  </div>
</div></section>

<section class="section-sm"><div class="wrap">
  <div class="grid g-3 gap-4">
    <a class="card card-accent" href="index.html" data-reveal><h3 class="card-title" style="font-size:1rem">Les 19 opérateurs</h3>
      <p class="small muted">Fiches complètes, classes et capacités.</p></a>
    <a class="card card-accent" href="../encyclopedie/tier-list.html" data-reveal data-delay="80"><h3 class="card-title" style="font-size:1rem">Tier list</h3>
      <p class="small muted">Classements séparés Operations et Warfare.</p></a>
    <a class="card card-accent" href="../detonation/index.html" data-reveal data-delay="160"><h3 class="card-title" style="font-size:1rem">Detonation</h3>
      <p class="small muted">Un exemplaire d'opérateur par équipe.</p></a>
  </div>
</div></section>
"""

html_cj = (head("Contre-jeu — neutraliser les capacités adverses",
                "Comment contrer chaque opérateur de Delta Force : portée réelle du scan de Luna, "
                "cône de détection de Hackclaw, régénération de D-Wolf, bouclier de Sineva, charge frontale "
                "de Martelo. Limites exploitables et gestes qui annulent chaque capacité.",
                depth=D, canonical="pages/operateurs/contre-jeu.html",
                image="assets/images/heroes/contrejeu_hero_01.jpg")
           + navbar(D) + '<main id="main">' + cj_body + "</main>" + footer(D) + scripts(D))
print(write("pages/operateurs/contre-jeu.html", html_cj))
