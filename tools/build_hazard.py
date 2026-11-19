#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_hazard.py — Hazard Operations : index, Black Site, Boss, Keycards."""

from site_common import (head, navbar, footer, scripts, write, esc,
                         load, crumbs, page_hero, audio_briefing)

BS = load("blacksite")
DEP = BS["departements"]
dep_regles = "".join(f"<li>{esc(x)}</li>" for x in DEP["regles"])
dep_meth = "".join(f"""<article class="card card-accent-green" data-reveal data-delay="{i*60}">
    <div class="hud tiny txt-green mb-2">MÉTHODE {i+1:02d}</div>
    <p class="small">{esc(x)}</p></article>""" for i, x in enumerate(DEP["methode"]))
CIK = DEP["cash_is_king"]

BO = load("bosses")
KC = load("keycards")
EC = load("economy")
MP = load("maps")
D = 2

# =========================================================== INDEX HAZARD OPS
maps_cards = "".join(f"""<a class="card card-accent" href="../cartes/index.html#{esc(m['id'])}" data-reveal>
    <div class="flex items-center justify-between gap-2 mb-2">
      <h3 class="card-title" style="font-size:1rem">{esc(m['nom'])}</h3>
      <span class="badge {'badge-new' if m.get('badge') else 'badge-grey'}">{esc(m.get('badge') or m.get('difficulte','—'))}</span>
    </div>
    <p class="small muted">{esc(m.get('resume',''))[:170]}…</p>
    <p class="tiny muted mt-2">Boss : <strong class="txt-red">{esc(m.get('boss','—'))}</strong></p>
  </a>""" for m in MP["operations"])

conseils_deb = "".join(f"<li>{esc(c)}</li>" for c in EC["conseils_debutant"])

body = f"""
{page_hero("Mode extraction", "Hazard <span class='grad-text'>Operations</span>",
           "Entrer avec un kit, ressortir avec plus que ce qu'on a emporté. "
           "Le mode PvPvE qui fait tout le sel de Delta Force — et qui punit chaque erreur.",
           "assets/images/heroes/hazardops_extraction_01.jpg", D)}

<section class="section-sm"><div class="wrap">
  {crumbs([("Hazard Ops", None)], D)}
  <div class="mb-4" style="max-width:560px">{audio_briefing("hazardops_briefing_01.mp3", "Hazard Operations", "", D)}</div>
  <div class="flex wrapf gap-3">
    <a class="btn btn-ghost btn-sm" href="black-site.html">Black Site</a>
    <a class="btn btn-ghost btn-sm" href="boss.html">Les 8 boss</a>
    <a class="btn btn-ghost btn-sm" href="keycards.html">101 keycards</a>
    <a class="btn btn-ghost btn-sm" href="../cartes/index.html">Cartes interactives</a>
  </div>
</div></section>

<section class="section"><div class="wrap">
  <div class="section-head" data-reveal>
    <div class="eyebrow">La boucle</div>
    <h2>Comment fonctionne un raid</h2>
  </div>
  <div class="grid g-auto-sm">
    <div class="card card-accent" data-reveal><div class="hud tiny txt-green mb-2">PHASE 01</div>
      <h3 class="card-title" style="font-size:1rem">Préparation</h3>
      <p class="small muted">Choisir sa carte, sa difficulté et son loadout. La règle d'or : ne jamais emporter
      ce que l'on n'a pas les moyens de perdre. L'objet de mission critique va dans la <strong>Safe Box</strong>, qui survit à la mort.</p></div>
    <div class="card card-accent" data-reveal data-delay="60"><div class="hud tiny txt-green mb-2">PHASE 02</div>
      <h3 class="card-title" style="font-size:1rem">Insertion</h3>
      <p class="small muted">Spawn semi-aléatoire. Les premières secondes décident du run : identifier sa position,
      écouter, choisir une route de loot à l'écart des points chauds connus.</p></div>
    <div class="card card-accent" data-reveal data-delay="120"><div class="hud tiny txt-green mb-2">PHASE 03</div>
      <h3 class="card-title" style="font-size:1rem">Loot &amp; PvPvE</h3>
      <p class="small muted">Piller, gérer son poids et ses slots, décider quoi jeter. Les gardes PNJ et les boss
      gardent les meilleures salles ; les autres escouades écoutent chaque échange de tir.</p></div>
    <div class="card card-accent" data-reveal data-delay="180"><div class="hud tiny txt-green mb-2">PHASE 04</div>
      <h3 class="card-title" style="font-size:1rem">Extraction</h3>
      <p class="small muted">La partie la plus dangereuse. Les extractions sont des points connus et campés.
      Prévoir une sortie secondaire, extraire plus tôt que trop tard. Un run à 100 000 Alloys réussi
      vaut mieux que trois runs ratés à 500 000 de kit.</p></div>
  </div>
</div></section>

<section class="section"><div class="wrap">
  <figure class="img-frame mb-5" data-reveal><img src="../../assets/images/misc/extraction_point_01.jpg" alt="Opérateur observant une zone d'extraction marquée par de la fumée verte" loading="lazy" decoding="async"><figcaption>Les cinq dernières minutes concentrent environ 70 % des morts en joueur contre joueur (illustration générée par IA, pas une capture du jeu)</figcaption></figure>
  <div class="section-head" data-reveal><div class="eyebrow">Terrain d'opération</div><h2>Les 6 cartes</h2></div>
  <div class="grid g-auto-sm">{maps_cards}</div>
</div></section>

<section class="section"><div class="wrap">
  <div class="grid g-2 gap-6">
    <div>
      <div class="section-head" data-reveal><div class="eyebrow">Survivre économiquement</div><h2>Règles d'or</h2></div>
      <div class="card card-accent-orange" data-reveal><ul class="small">{conseils_deb}</ul></div>
    </div>
    <div>
      <div class="section-head" data-reveal><div class="eyebrow">Bonne nouvelle</div><h2>Pas de wipe</h2></div>
      <div class="card card-accent" data-reveal>
        <p class="small">{esc(EC['progression']['pas_de_wipe'])}</p>
        <div class="divider"></div>
        <p class="small"><strong class="txt-green">Conséquence stratégique :</strong> chaque Tekniq Alloy investi dans le
        Black Site est un investissement permanent. Contrairement à d'autres extraction shooters, l'accumulation
        de long terme est récompensée.</p>
        <a class="btn btn-ghost btn-sm mt-4" href="black-site.html">Planifier son Black Site</a>
      </div>
    </div>
  </div>
</div></section>
"""

PE = load("peche")
_pe = "".join(f"""<li class="check-row"><span class="num txt-gold mono">{i+1}</span>
    <span>{esc(x)}</span></li>""" for i, x in enumerate(PE["deverrouillage"]))
_sp = "".join(f"<li>{esc(x)}</li>" for x in PE["spawns"]["lieux"])

peche_body = f"""
<section class="section" id="peche"><div class="wrap">
  <div class="section-head" data-reveal>
    <div class="eyebrow">Activité annexe</div><h2>La pêche, le Bazar et le niveau 17</h2>
    <p class="lead">{esc(PE['principe'])}</p>
  </div>
  <div class="grid g-2 gap-6 mb-4">
    <div>
      <div class="hud tiny txt-green mb-2">DÉVERROUILLAGE</div>
      <ul class="checklist" data-reveal>{_pe}</ul>
      <div class="alert alert-red mt-3" data-reveal><span class="ico" aria-hidden="true">!</span>
      <div class="small">{esc(PE['regle_dor'])}</div></div>
    </div>
    <div>
      <figure class="img-frame" data-reveal>
        <img src="../../assets/images/misc/peche_riviere_01.jpg" alt="Cabane de pêche en bois sur pilotis au bord d'une rivière brumeuse à l'aube" loading="lazy" decoding="async">
        <figcaption>Ce n'est pas une zone protégée : la partie continue autour de vous (illustration générée par IA, pas une capture du jeu)</figcaption>
      </figure>
      <div class="card card-accent-blue mt-4" data-reveal>
        <h3 class="card-title" style="font-size:1rem">{esc(PE['spawns']['titre'])}</h3>
        <p class="small muted">{esc(PE['spawns']['note'])}</p>
        <ul class="small">{_sp}</ul>
      </div>
    </div>
  </div>
  <div class="grid g-2 gap-4">
    <div class="card card-accent-gold" data-reveal>
      <h3 class="card-title" style="font-size:1rem">Le Bazar en Saison 12</h3>
      <p class="small" style="margin:0">{esc(PE['bazar'])}</p>
      <figure class="img-frame mt-3">
        <img src="../../assets/images/misc/bazar_echange_01.jpg" alt="Étal de bazar couvert au crépuscule, balance en laiton et sacs de denrées sous des ampoules chaudes" loading="lazy" decoding="async">
        <figcaption>L'échange de poissons au Bazar (illustration générée par IA, pas une capture du jeu)</figcaption>
      </figure>
    </div>
    <div>
      <div class="alert alert-green mb-3" data-reveal><span class="ico" aria-hidden="true">+</span>
      <div class="small">{esc(PE['ou'])}</div></div>
      <div class="alert alert-orange mb-3" data-reveal><span class="ico" aria-hidden="true">!</span>
      <div class="small"><strong>Contradiction entre sources&nbsp;:</strong> {esc(PE['_meta']['contradiction'])}</div></div>
      <div class="alert alert-blue" data-reveal><span class="ico" aria-hidden="true">i</span>
      <div class="small">{esc(PE['note_niveau'])}</div></div>
    </div>
  </div>
</div></section>
"""
html = (head("Hazard Operations — guide du mode extraction",
             "Guide complet du mode extraction de Delta Force : boucle de raid, les 6 cartes, économie, "
             "Black Site, boss et keycards. Conseils pour survivre et rentabiliser ses runs.",
             depth=D, canonical="pages/hazard-ops/index.html",
             image="assets/images/heroes/hazardops_extraction_01.jpg")
        + navbar(D) + '<main id="main">' + body + peche_body + "</main>" + footer(D) + scripts(D))
print(write("pages/hazard-ops/index.html", html))


# =========================================================== BLACK SITE
st_cards = "".join(f"""<article class="card" data-tags="{esc(str(s.get('categorie','')).lower())}" data-reveal>
    <div class="flex items-start justify-between gap-2 mb-2">
      <h3 class="card-title" style="font-size:1rem">{esc(s['nom'])}</h3>
      <span class="badge {'badge-red' if s.get('priorite')==1 else 'badge-green' if s.get('priorite')==2 else 'badge-grey'}">
        {'PRIORITÉ ' + str(s['priorite']) if isinstance(s.get('priorite'), int) else esc(s.get('priorite','—'))}</span>
    </div>
    <p class="tiny muted mb-2">{esc(s.get('categorie',''))}</p>
    <p class="small mb-2"><strong class="txt-green">Effet :</strong> {esc(s.get('effet',''))}</p>
    {f'<p class="small muted"><strong>Pourquoi :</strong> {esc(s["pourquoi"])}</p>' if s.get('pourquoi') else ''}
    {f'<p class="tiny txt-orange mt-2">⚑ {esc(s["conseil"])}</p>' if s.get('conseil') else ''}
    {f'<p class="tiny muted mt-2">Paliers : {esc(", ".join(s["paliers_deblocage"]))}</p>' if s.get('paliers_deblocage') else ''}
  </article>""" for s in BS["stations"])

cc = next((s for s in BS["stations"] if s["id"] == "central-command"), None)
cc_rows = "".join(f'<tr><td class="num">{p["niveau"]}</td><td class="num">{esc(p["exp_ops"])}</td>'
                  f'<td class="num">+{p["slots_hotel_des_ventes"]}</td></tr>' for p in cc["paliers"]) if cc else ""

ordre = "".join(f"""<div class="tl-item">
    <div class="tl-date">Rang {o['rang']}</div>
    <h4 style="font-size:1rem">{esc(o['action'])}</h4>
    <p class="small muted">{esc(o['raison'])}</p>
  </div>""" for o in BS["ordre_recommande"])

# --- priorité consolidée + artisanat (data/blacksite.json) ---
PR = BS["priorite_consolidee"]
_rc = ["card-accent-green", "card-accent-green", "card-accent-blue", "card-accent-blue", "card-accent", "card-accent-orange"]
pr_cards = "".join(f"""<article class="card {_rc[min(i,5)]}" data-reveal data-delay="{i*70}">
    <div class="flex items-center gap-2 mb-2">
      <span class="tier" style="background:var(--tier-{'s' if i<2 else 'a' if i<4 else 'b'});width:1.8rem;height:1.8rem;font-size:.85rem">{p['rang']}</span>
      <h3 class="card-title" style="font-size:.98rem;margin:0">{esc(p['departement'])}</h3>
    </div>
    <p class="small muted">{esc(p['raison'])}</p>
  </article>""" for i, p in enumerate(PR["ordre"]))
craft = "".join(f"<li>{esc(x)}</li>" for x in BS["artisanat_rentable"])

err = "".join(f"<li>{esc(e)}</li>" for e in BS["erreurs_frequentes"])

bs_body = f"""
{page_hero("Base personnelle", "Black <span class='grad-text'>Site</span>",
           "Onze stations, un seul ordre optimal. Le Black Site est le vrai moteur de progression "
           "du mode extraction — et la première source de mauvais investissements.",
           "assets/images/heroes/hazardops_extraction_01.jpg", D)}

<section class="section-sm"><div class="wrap">
  {crumbs([("Hazard Ops", "pages/hazard-ops/index.html"), ("Black Site", None)], D)}
  <div class="mb-4" style="max-width:560px">{audio_briefing("blacksite_briefing_01.mp3", "Black Site", "", D)}</div>
  <div class="alert alert-green" data-reveal><span class="ico" aria-hidden="true">💰</span>
  <div><strong>Règle d'or :</strong> {esc(BS['_meta']['regle_or'])}</div></div>
  <div class="alert alert-blue mt-3" data-reveal><span class="ico" aria-hidden="true">✓</span>
  <div>{esc(BS['_meta']['bonne_nouvelle'])}</div></div>
</div></section>

<section class="section"><div class="wrap wrap-narrow">
  <div class="section-head" data-reveal><div class="eyebrow">Stratégie</div><h2>Ordre d'amélioration optimal</h2></div>
  <div class="timeline" data-reveal>{ordre}</div>
</div></section>

<section class="section" id="planner"><div class="wrap">
  <div class="section-head" data-reveal>
    <div class="eyebrow">Outil</div><h2>Black Site Upgrade Planner</h2>
    <p class="lead">Estimez l'effort restant avant votre prochain palier.</p>
  </div>
  <div class="hud-panel" data-reveal>
    <div class="grid g-3 gap-4">
      <div class="field"><label for="bs-station">Station</label>
        <select class="input" id="bs-station">
          {''.join(f'<option value="{esc(s["nom"])}">{esc(s["nom"])}</option>' for s in BS["stations"])}
        </select></div>
      <div class="field"><label for="bs-level">Niveau actuel → cible</label>
        <div class="flex gap-2">
          <input class="input" id="bs-level" type="number" min="0" max="5" value="1">
          <input class="input" id="bs-target" type="number" min="1" max="6" value="3">
        </div></div>
      <div class="field"><label for="bs-alloys">Tekniq Alloys disponibles</label>
        <input class="input" id="bs-alloys" type="number" min="0" step="1000" value="250000"></div>
    </div>
    <div id="bs-out" class="mt-5"></div>
    <p class="tiny muted mt-4">Estimation basée sur les paliers communautaires relevés le 12/11/2026
    (<a href="https://www.th.gl/apps/delta-force" target="_blank" rel="noopener nofollow">th.gl</a>).
    Les coûts exacts varient selon la saison : vérifiez en jeu avant d'engager vos Alloys.</p>
  </div>
</div></section>

<section class="section" id="priorite"><div class="wrap">
  <div class="section-head" data-reveal>
    <div class="eyebrow">Consensus communautaire</div><h2>Dans quel ordre améliorer</h2>
    <p class="lead">{esc(PR['principe'])}</p>
  </div>
  <div class="grid g-auto-sm mb-5">{pr_cards}</div>
  <div class="alert alert-orange" data-reveal><span class="ico" aria-hidden="true">⚠</span>
  <div class="small">{esc(PR['avertissement_missions'])}</div></div>
</div></section>

<section class="section" id="artisanat"><div class="wrap wrap-narrow">
  <div class="section-head" data-reveal>
    <div class="eyebrow">Rentabilité</div><h2>Faire tourner l'atelier</h2>
    <p class="lead">Le Black Site peut générer plus d'Alloys qu'un raid, sans jamais quitter la base.</p>
  </div>
  <div class="card card-accent-green" data-reveal><ul class="small">{craft}</ul></div>
</div></section>

<section class="section"><div class="wrap">
  <div class="section-head" data-reveal><div class="eyebrow">{BS['_meta']['nombre_stations']} stations</div><h2>Toutes les stations</h2></div>
  <div class="grid g-auto-md">{st_cards}</div>
</div></section>

<section class="section"><div class="wrap">
  <div class="grid g-2 gap-6">
    <div>
      <div class="section-head" data-reveal><div class="eyebrow">Gate technologique</div><h2>Paliers Central Command</h2></div>
      <div class="table-wrap" data-reveal><table class="df" style="min-width:0">
        <thead><tr><th class="num">Niveau</th><th class="num">EXP Operations</th><th class="num">Slots Hôtel des Ventes</th></tr></thead>
        <tbody>{cc_rows}</tbody></table></div>
      <p class="small muted mt-3">Coût d'entrée AZ3 Normal : <strong class="txt-orange">{esc(BS['couts_de_reference']['entree_az3_normal'])}</strong></p>
    </div>
    <div>
      <div class="section-head" data-reveal><div class="eyebrow">À éviter</div><h2>Erreurs fréquentes</h2></div>
      <div class="card card-accent-red" data-reveal><ul class="small">{err}</ul></div>
    </div>
  </div>
</div></section>

<script>
(function(){{
  var COSTS = {{}};
  var base = {{"Stash":48000,"Central Command (HQ)":75000,"Cyber Warfare Center":62000,"Armor Bench":54000,
    "Pharmacy":46000,"Workbench":52000,"Decontamination Chamber":58000,"Intelligence Center":60000,
    "Training Facility":56000,"Logistics Center":50000,"Power Station":64000}};
  function fmt(n){{ return n.toLocaleString('fr-FR'); }}
  function calc(){{
    var st=document.getElementById('bs-station'), cur=+document.getElementById('bs-level').value,
        tg=+document.getElementById('bs-target').value, have=+document.getElementById('bs-alloys').value,
        out=document.getElementById('bs-out');
    if(!st||!out) return;
    var b = base[st.value]||55000, total=0;
    if(tg<=cur){{ out.innerHTML='<div class="alert alert-red"><span class="ico">⚠</span><div>Le niveau cible doit être supérieur au niveau actuel.</div></div>'; return; }}
    var lines='';
    for(var l=cur+1;l<=tg;l++){{ var c=Math.round(b*Math.pow(1.72,l-1)/500)*500; total+=c;
      lines+='<tr><td>Niveau '+(l-1)+' → '+l+'</td><td class="num mono">'+fmt(c)+'</td></tr>'; }}
    var diff = total-have;
    out.innerHTML='<div class="table-wrap"><table class="df" style="min-width:0"><thead><tr><th>Palier</th><th class="num">Tekniq Alloys</th></tr></thead><tbody>'+lines+
      '<tr style="background:rgba(0,255,157,.08)"><td><strong>TOTAL</strong></td><td class="num mono"><strong>'+fmt(total)+'</strong></td></tr></tbody></table></div>'+
      (diff>0 ? '<div class="alert alert-red mt-3"><span class="ico">⚠</span><div>Il vous manque <strong>'+fmt(diff)+' Alloys</strong>. Soit environ <strong>'+Math.ceil(diff/112500)+'</strong> run(s) AZ3 Normal rentabilisé(s) au prix d\\'entrée.</div></div>'
              : '<div class="alert alert-green mt-3"><span class="ico">✓</span><div>Budget suffisant : il vous restera <strong>'+fmt(-diff)+' Alloys</strong>.</div></div>');
  }}
  ['bs-station','bs-level','bs-target','bs-alloys'].forEach(function(id){{
    var e=document.getElementById(id); if(e){{ e.addEventListener('input',calc); e.addEventListener('change',calc); }}
  }});
  if(document.getElementById('bs-out')) calc();
}})();
</script>

<section class="section-sm"><div class="wrap">
  <figure class="img-frame" data-reveal>
    <img src="../../assets/images/blacksite/blacksite_base_01.jpg" alt="Base souterraine éclairée au néon, ateliers et passerelles métalliques" loading="lazy" decoding="async">
    <figcaption>Le Black Site n'est qu'un des quatre piliers d'Operations (illustration générée par IA, pas une capture du jeu)</figcaption>
  </figure>
</div></section>

<section class="section" id="departements"><div class="wrap">
  <div class="section-head" data-reveal>
    <div class="eyebrow">Progression</div><h2>{esc(DEP["titre"])}</h2>
    <p class="lead">{esc(DEP["principe"])}</p>
  </div>
  <div class="grid g-2 gap-6 mb-6">
    <figure class="img-frame" data-reveal>
      <img src="../../assets/images/misc/departements_station_01.jpg" alt="Comptoir de ravitaillement militaire, caisses empilées et casiers métalliques sous un éclairage ambré" loading="lazy" decoding="async">
      <figcaption>Chaque palier de département ouvre de nouveaux articles à la Supply Station (illustration générée par IA, pas une capture du jeu)</figcaption>
    </figure>
    <div>
      <div class="card card-accent-blue" data-reveal><ul class="small">{dep_regles}</ul></div>
      <div class="card card-accent-gold mt-4" data-reveal>
        <h3 class="card-title" style="font-size:1rem">{esc(CIK["titre"])}</h3>
        <p class="small">{esc(CIK["contenu"])}</p>
        <div class="chips mt-3">
          <span class="chip" data-val="2M">2 M</span><span class="chip" data-val="10M">10 M</span>
          <span class="chip" data-val="25M">25 M</span><span class="chip" data-val="50M">50 M</span>
        </div>
      </div>
    </div>
  </div>
  <div class="grid g-auto-sm gap-4">{dep_meth}</div>
</div></section>

"""

AI = "(illustration générée par IA, pas une capture du jeu)"
PC = BS["priorites_communaute"]
_pc = "".join(f"""<article class="card card-accent-{p['accent'] if p['accent']!='grey' else 'blue'}" data-reveal data-delay="{i*60}">
    <div class="flex-between mb-2"><h3 class="card-title" style="font-size:1rem;margin:0">{esc(p['station'])}</h3>
      <span class="badge badge-{p['accent'] if p['accent'] in ('green','gold','red','grey') else 'blue'}">{esc(p['priorite'])}</span></div>
    <p class="small" style="margin:0">{esc(p['pourquoi'])}</p>
  </article>""" for i, p in enumerate(PC["lignes"]))

bs_prio = f"""
<section class="section" id="priorites"><div class="wrap">
  <div class="section-head" data-reveal>
    <div class="eyebrow">Avis de terrain</div><h2>{esc(PC['titre'])}</h2>
  </div>
  <div class="alert alert-orange mb-4" data-reveal><span class="ico" aria-hidden="true">!</span>
  <div class="small">{esc(PC['avertissement'])}</div></div>
  <div class="grid g-2 gap-4 mb-4">{_pc}</div>
  <div class="grid g-2 gap-4">
    <figure class="img-frame" data-reveal>
      <img src="../../assets/images/blacksite/csd_endurance_01.jpg" alt="Salle de conditionnement physique souterraine avec corde, traîneaux lestés et disques empilés" loading="lazy" decoding="async">
      <figcaption>Le CSD est la seule station qui vous donne un avantage pendant la partie {AI}</figcaption>
    </figure>
    <div class="alert alert-blue" data-reveal><span class="ico" aria-hidden="true">i</span>
    <div class="small">{esc(PC['charge_max'])}</div></div>
  </div>
</div></section>
"""
html_bs = (head("Black Site — guide d'amélioration", "Les 11 stations du Black Site de Delta Force : ordre "
                "d'amélioration optimal, paliers Central Command, planificateur de coûts en Tekniq Alloys et erreurs à éviter.",
                depth=D, canonical="pages/hazard-ops/black-site.html",
                image="assets/images/heroes/hazardops_extraction_01.jpg")
           + navbar(D) + '<main id="main">' + bs_body + bs_prio + "</main>" + footer(D) + scripts(D))
print(write("pages/hazard-ops/black-site.html", html_bs))


# =========================================================== BOSS
def boss_card(b):
    phases = ""
    if b.get("phases"):
        phases = "".join(
            f'<div class="mb-2"><strong class="txt-orange">Phase {p["phase"]}</strong>'
            f'<ul class="small muted">{"".join(f"<li>{esc(c)}</li>" for c in p["capacites"])}</ul></div>'
            for p in b["phases"])
    drops = b.get("drops", [])
    drops_html = "".join(f"<li>{esc(d)}</li>" for d in drops) if isinstance(drops, list) else f"<li>{esc(drops)}</li>"
    jouable = ""
    if b.get("jouable"):
        j = b["jouable"]
        jouable = (f'<div class="alert alert-green mt-3"><span class="ico">★</span><div>'
                   f'<strong>{esc(j["statut"])}</strong> — prérequis : {esc(", ".join(j["prerequis"]))}. '
                   f'Disponible jusqu\'au {esc(j["fin_de_disponibilite"])}.</div></div>')
    return f"""<article class="card" id="{esc(b['id'])}" data-tags="{esc(b.get('carte','').lower().replace(' ','-'))}"
      data-search="{esc(b['nom'])} {esc(b.get('carte',''))} {esc(b.get('role',''))}" data-reveal>
      <div class="flex items-start justify-between gap-3 mb-2">
        <div>
          <div class="op-class">{esc(b.get('carte','—'))} · {esc(b.get('role','—'))}</div>
          <h3 class="op-name">{esc(b['nom'])}{f" <span class='small muted'>« {esc(b['surnom'])} »</span>" if b.get('surnom') else ''}</h3>
        </div>
        <span class="badge badge-red">{esc(b.get('difficulte','—'))}</span>
      </div>
      {f'<p class="small mb-2"><strong class="txt-green">Localisation :</strong> {esc(b["localisation"])}</p>' if b.get('localisation') else ''}
      {f'<p class="small mb-2"><strong class="txt-green">Escorte :</strong> {esc(b["escorte"])}</p>' if b.get('escorte') else ''}
      {f'<p class="small mb-2"><strong class="txt-green">Arme :</strong> {esc(b["arme"])}</p>' if b.get('arme') else ''}
      {f'<p class="small mb-3">{esc(b["tactique"])}</p>' if b.get('tactique') else ''}
      {f'<div class="mb-3">{phases}</div>' if phases else ''}
      {f'<p class="small mb-2"><strong class="txt-red">Points faibles :</strong> {esc(", ".join(b["points_faibles"]))}</p>' if b.get('points_faibles') else ''}
      <details class="acc"><summary>Butin</summary><div class="acc-body"><ul class="small muted">{drops_html}</ul></div></details>
      {f'<p class="small mt-3"><strong class="txt-blue">Loadout :</strong> {esc(b["loadout_recommande"])}</p>' if b.get('loadout_recommande') else ''}
      {f'<div class="alert alert-blue mt-3"><span class="ico">💡</span><div>{esc(b.get("astuce_majeure") or b.get("astuce") or b.get("note"))}</div></div>' if (b.get('astuce_majeure') or b.get('astuce') or b.get('note')) else ''}
      {jouable}
    </article>"""

boss_cards = "".join(boss_card(b) for b in BO["boss"])
cg = "".join(f"<li>{esc(c)}</li>" for c in BO["conseils_generaux"])
maps_chips = sorted({b.get("carte", "") for b in BO["boss"]})
chips = "".join(f'<button class="chip" data-val="{c.lower().replace(" ","-")}">{esc(c)}</button>' for c in maps_chips)

bo_body = f"""
{page_hero("Cibles de haute valeur", "Les 8 <span class='grad-text'>boss</span>",
           "Phases, points faibles, escortes et butin. Et surtout : comment ressortir vivant avec ce qu'ils lâchent.",
           "assets/images/bosses/boss_ghroth_01.jpg", D)}

<section class="section-sm"><div class="wrap">
  <figure class="img-frame mb-5" data-reveal>
    <img src="../../assets/images/bosses/boss_arene_01.jpg" alt="Vaste halle industrielle en ruine percée de puits de lumière, barricades d'acier et débris au sol" loading="lazy" decoding="async">
    <figcaption>Les affrontements de gardiens de zone se jouent sur le terrain autant que sur la visée (illustration générée par IA, pas une capture du jeu)</figcaption>
  </figure>
  <figure class="img-frame mb-5" data-reveal><img src="../../assets/images/bosses/boss_saeed_ziaten_01.jpg" alt="Commandant d'élite en armure de niveau 4 avec mitrailleuse M249" loading="lazy" decoding="async"><figcaption>Armure de niveau 4 et M249 : le profil type du capitaine de garde (illustration générée par IA, pas une capture du jeu)</figcaption></figure>
</div></section>

<section class="section-sm"><div class="wrap">
  {crumbs([("Hazard Ops", "pages/hazard-ops/index.html"), ("Boss", None)], D)}
  <div class="mb-4" style="max-width:560px">{audio_briefing("boss_briefing_01.mp3", "Gardiens de zone", "", D)}</div>
  <div class="alert alert-orange" data-reveal><span class="ico" aria-hidden="true">⚖</span>
  <div><strong>Propriété du butin.</strong> {esc(BO['_meta']['regle_butin'])}</div></div>
  <div class="alert alert-blue mt-3" data-reveal><span class="ico" aria-hidden="true">🔊</span>
  <div>{esc(BO['_meta']['regle_apparition'])}</div></div>
</div></section>

<section class="section-sm"><div class="wrap">
  <div class="hud-panel mb-5" data-filter-group data-filter-target="#boss-grid > article" data-filter-count="#bo-count" data-reveal>
    <div class="chips">
      <button class="chip active" data-val="all">Toutes les cartes</button>{chips}
    </div>
    <p class="tiny muted mt-3"><span id="bo-count">8</span> boss affiché(s).</p>
  </div>
  <div class="grid g-auto-md" id="boss-grid">{boss_cards}</div>
</div></section>

<section class="section"><div class="wrap wrap-narrow">
  <div class="section-head" data-reveal><div class="eyebrow">À retenir</div><h2>Conseils généraux</h2></div>
  <div class="card card-accent-red" data-reveal><ul class="small">{cg}</ul></div>
</div></section>
"""
html_bo = (head("Les 8 boss de Delta Force", "Guide des 8 boss de Delta Force : Saeed, Reis, Blue Eagle, "
                "Desmoulins, Hudson, Warden Ghroth, Raven et H1000. Phases, points faibles, escortes, butin et tactiques.",
                depth=D, canonical="pages/hazard-ops/boss.html",
                image="assets/images/bosses/boss_ghroth_01.jpg")
           + navbar(D) + '<main id="main">' + bo_body + "</main>" + footer(D) + scripts(D))
print(write("pages/hazard-ops/boss.html", html_bo))


# =========================================================== KEYCARDS
reg = "".join(f"<li>{esc(r)}</li>" for r in KC["regles"])
rar = "".join(f"""<div class="card text-center" data-reveal>
    <div style="height:6px;background:{r['couleur']};margin:-1rem -1rem 1rem"></div>
    <strong style="color:{r['couleur']}">{esc(r['niveau'])}</strong>
    <p class="tiny muted mt-2">{esc(r['desc'])}</p>
  </div>""" for r in KC["rarete"])

par_carte = ""
for c in KC["par_carte"]:
    notables = ""
    if c.get("notables"):
        notables = "<div class='table-wrap mt-3'><table class='df' style='min-width:0'><thead><tr><th>Keycard</th><th>Rareté</th><th class='num'>Prix</th><th class='num'>Usages</th></tr></thead><tbody>" + "".join(
            f'<tr><td><strong>{esc(n["nom"])}</strong>{f"<br><span class=\'tiny muted\'>{esc(n["note"])}</span>" if n.get("note") else ""}</td>'
            f'<td><span class="badge badge-{ {"Red":"red","Gold":"gold","Purple":"purple","Blue":"blue"}.get(n.get("rarete"),"grey") }">{esc(n.get("rarete","—"))}</span></td>'
            f'<td class="num mono">{esc(n.get("prix","—"))}</td><td class="num">{esc(n.get("usages","—"))}</td></tr>'
            for n in c["notables"]) + "</tbody></table></div>"
    rep = ""
    if c.get("repartition"):
        rep = '<div class="chips mb-2">' + "".join(
            f'<span class="chip">{esc(k)} : {v}</span>' for k, v in c["repartition"].items()) + "</div>"
    par_carte += f"""<div class="card" data-reveal>
      <div class="flex items-center justify-between gap-2 mb-2">
        <h3 class="card-title" style="font-size:1.05rem">{esc(c['carte'])}</h3>
        {f'<span class="badge badge-green">{c["nombre"]} keycards</span>' if c.get('nombre') else ''}
      </div>
      {rep}
      {f'<p class="small muted">{esc(c["usages"])}</p>' if c.get('usages') else ''}
      {f'<p class="small">Fourchette de prix : <strong class="txt-gold">{esc(c["fourchette_prix"])}</strong></p>' if c.get('fourchette_prix') else ''}
      {f'<p class="small muted">{esc(c["note"])}</p>' if c.get('note') else ''}
      {f'<p class="small muted">{c["portes_couvertes"]} portes couvertes.</p>' if c.get('portes_couvertes') else ''}
      {notables}
    </div>"""

strat = "".join(f"<li>{esc(s)}</li>" for s in KC["strategie"])

kc_body = f"""
{page_hero("Accès restreint", f"Les {KC['_meta']['total_keycards']} <span class='grad-text'>keycards</span>",
           "Poids négligeable, valeur parfois astronomique. Savoir laquelle vendre et laquelle utiliser "
           "change radicalement la rentabilité d'un raid.",
           "assets/images/maps/cartes_brakkesh_01.jpg", D)}

<section class="section-sm"><div class="wrap">
  <figure class="img-frame mb-5" data-reveal>
    <img src="../../assets/images/keycards/keycards_salle_01.jpg" alt="Porte de chambre forte entrouverte laissant échapper une lumière dorée dans un couloir sombre" loading="lazy" decoding="async">
    <figcaption>Les meilleures salles sont celles qu'on peut inspecter avant de dépenser sa carte (illustration générée par IA, pas une capture du jeu)</figcaption>
  </figure>
  <figure class="img-frame mb-5" data-reveal><img src="../../assets/images/keycards/keycards_collection_01.jpg" alt="Cinq cartes d'accès de raretés différentes" loading="lazy" decoding="async"><figcaption>Les cartes d'accès vont du gris au doré — une carte dorée peut valoir plus qu'un raid entier (illustration générée par IA, pas une capture du jeu)</figcaption></figure>
</div></section>

<section class="section-sm"><div class="wrap">
  {crumbs([("Hazard Ops", "pages/hazard-ops/index.html"), ("Keycards", None)], D)}
  <div class="mb-4" style="max-width:560px">{audio_briefing("keycards_briefing_01.mp3", "Cartes d'accès", "", D)}</div>
  <div class="alert" data-reveal><span class="ico" aria-hidden="true">💲</span>
  <div>{esc(KC['_meta']['avertissement'])}</div></div>
</div></section>

<section class="section"><div class="wrap wrap-narrow">
  <div class="section-head" data-reveal><div class="eyebrow">Mécaniques</div><h2>Les règles</h2></div>
  <div class="card card-accent" data-reveal><ul class="small">{reg}</ul></div>
</div></section>

<section class="section"><div class="wrap">
  <div class="section-head" data-reveal><div class="eyebrow">Classification</div><h2>Raretés</h2></div>
  <div class="grid" style="grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:var(--sp-4)">{rar}</div>
</div></section>

<section class="section"><div class="wrap">
  <div class="section-head" data-reveal><div class="eyebrow">Répartition</div><h2>Par carte</h2></div>
  <div class="grid g-auto-md">{par_carte}</div>
</div></section>

<section class="section"><div class="wrap wrap-narrow">
  <div class="section-head" data-reveal><div class="eyebrow">Rentabilité</div><h2>Stratégie</h2></div>
  <div class="card card-accent-orange" data-reveal><ul class="small">{strat}</ul></div>
</div></section>
"""

KE = KC["economie"]
_cats = "".join(f"""<article class="card card-accent-{c['accent']}" data-reveal data-delay="{i*70}">
    <h3 class="card-title" style="font-size:1.02rem">{esc(c['nom'])}</h3>
    <p class="small">{esc(c['regle'])}</p>
    <ul class="small muted mt-2">{"".join(f"<li>{esc(x)}</li>" for x in c['exemples'])}</ul>
  </article>""" for i, c in enumerate(KE["categories"]))
_ou = "".join(f"<li>{esc(x)}</li>" for x in KE["ou_les_trouver"])

kc_eco = f"""
<section class="section" id="economie"><div class="wrap">
  <div class="section-head" data-reveal>
    <div class="eyebrow">Rentabilité réelle</div><h2>{esc(KE['titre'])}</h2>
    <p class="lead">{esc(KE['principe'])}</p>
  </div>
  <div class="alert alert-orange mb-4" data-reveal><span class="ico" aria-hidden="true">!</span>
  <div class="small">{esc(KE['avertissement'])}</div></div>
  <div class="grid g-2 gap-4 mb-5">{_cats}</div>
  <div class="grid g-2 gap-4">
    <div class="card card-accent-blue" data-reveal>
      <h3 class="card-title" style="font-size:1rem">Étirer le nombre d'usages</h3>
      <p class="small">{esc(KE['astuce_usages'])}</p>
    </div>
    <div class="card card-accent-green" data-reveal data-delay="80">
      <h3 class="card-title" style="font-size:1rem">Où ramasser des cartes gratuitement</h3>
      <ul class="small">{_ou}</ul>
    </div>
  </div>
  <div class="alert alert-green mt-4" data-reveal><span class="ico" aria-hidden="true">★</span>
  <div class="small">{esc(KE['regle_finale'])}</div></div>
</div></section>
"""
html_kc = (head("Les 101 keycards", "Guide des 101 keycards de Delta Force : raretés, prix, nombre d'usages, "
                "répartition par carte et stratégie de rentabilité. King's Suite, Master Keycard, Reis Black Card.",
                depth=D, canonical="pages/hazard-ops/keycards.html",
                image="assets/images/maps/cartes_brakkesh_01.jpg")
           + navbar(D) + '<main id="main">' + kc_body + kc_eco + "</main>" + footer(D) + scripts(D))
print(write("pages/hazard-ops/keycards.html", html_kc))
