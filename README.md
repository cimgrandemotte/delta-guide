# 🎖️ Delta Force — The Ultimate Operator's Guide

> **Every Raid. Every Operator. Every Edge.**

Guide communautaire francophone ultra-complet sur **Delta Force**, à jour de la **Saison 12 « Aurora »** (live le 10 novembre 2026).
Site statique, sans back-end, sans compte, sans tracker.

---

## 📋 Sommaire

- [Ce que contient le site](#-ce-que-contient-le-site)
- [Démarrage rapide](#-démarrage-rapide)
- [Architecture](#-architecture)
- [Régénérer le site](#-régénérer-le-site)
- [Mettre à jour les données](#-mettre-à-jour-les-données)
- [Déploiement](#-déploiement)
- [Checklist avant mise en ligne](#️-checklist-avant-mise-en-ligne)
- [Qualité, SEO, accessibilité](#-qualité-seo-accessibilité)
- [Méthodologie & sources](#-méthodologie--sources)
- [Licence & mentions légales](#-licence--mentions-légales)

---

## 🎯 Ce que contient le site

| Page | Contenu |
|---|---|
| **QG** (`index.html`) | Synthèse Saison 12, tier list par mode, codes du jour, accès à tout le guide |
| **Opérateurs** | Les **19 opérateurs** : capacités détaillées, forces, faiblesses, counters, tiers Operations **et** Warfare, 5 synergies d'escouade, ordre de déblocage en 7 rangs |
| **Armurerie** | **40+ armes** avec statistiques, accessoires et codes de build. AN-94 incluse |
| **Munitions** | Niveaux de pénétration 1→6, tous les calibres, prix, et les **5 nouvelles munitions** Aurora |
| **Codes de build** | **40 configurations** vérifiées, copiables en un clic |
| **Hazard Operations** | Boucle de raid, économie, règles de survie |
| **Black Site** | **11 stations**, ordre d'amélioration optimal, planificateur de coûts en Tekniq Alloys |
| **Boss** | Les **8 boss** : phases, points faibles, escortes, butin, loadouts |
| **Keycards** | Les **101 keycards** : raretés, prix, usages, stratégie de rentabilité |
| **Cartes** | **6 cartes interactives** Leaflet avec marqueurs filtrables |
| **Havoc Warfare** | **12 véhicules** avec tier list, contre-jeu anti-blindé, cartes dont Zenith Port |
| **Black Hawk Down** | Les **7 chapitres** de la campagne coopérative |
| **Saison Aurora** | Patch notes complets **séparés par mode**, **17 events** datés, season pass |
| **Astuces pro** | Réglages PC / console / mobile, audio, eDPI, plateformes |
| **Codes de portes** | Codes du jour par carte + emplacements permanents + secret CRACKED |
| **Encyclopédie** | Lexique de 22 termes, factions, chronologie, méthodologie |
| **Tier list** | Classements S12 par mode + **éditeur drag & drop** avec sauvegarde locale |
| **Économie** | Tekniq Alloys vs Delta Coins, Hôtel des Ventes, paliers de niveau |
| **Brakkesh 2.0 & factions** | Haavk contre Ahsarah : postes de contact, montée de l'insigne, niveau 2, chasses et les 8 événements datés |
| **Hot Zone 3v3v3** | Le mode sans risque pour la réserve : règles, économie de points par manche, cinq tactiques à trois équipes |
| **AZ3 & Supercritical** | La carte à radiation : 4 paliers de contamination, 3 voies d'extraction, la mission d'arrêt d'urgence en 8 étapes et les paliers de niveau Operations |
| **Outils** | 6 calculateurs interactifs (voir ci-dessous) |
| **News** | Events en cours au 19 novembre 2026 |

### 🛠️ Outils interactifs

1. **Calculateur TTK / STK / DPS** — 15 armes, 6 niveaux d'armure, 6 niveaux de munition, 5 zones d'impact
2. **Simulateur de pénétration T1→T6** — matrice complète 6×6 + verdict contextuel
3. **Calculateur de rentabilité de raid** — coût du kit vs taux d'extraction réel
4. **Calculateur eDPI** — conversion de sensibilité + profils de jeu
5. **Générateur de loadout aléatoire** — avec défi imposé
6. **Quiz tactique Aurora** — 12 questions avec explications
7. **Black Site Upgrade Planner** — coûts par palier et déficit d'Alloys
8. **Tier list drag & drop** — sauvegarde locale + export presse-papiers
9. **Copieur de codes de build** — un clic, prêt à importer en jeu
10. **6 cartes Leaflet** — marqueurs filtrables par catégorie
11. **Recherche globale** — `Ctrl+K` ou `/`, navigation clavier complète

---

## 🚀 Démarrage rapide

Le site est **100 % statique** : aucune compilation n'est nécessaire pour le consulter.

```bash
# Option 1 — ouvrir directement
open index.html

# Option 2 — serveur local (recommandé : évite les restrictions file://)
npx serve . -l 4173
# puis http://localhost:4173

# Option 3 — Python
python3 -m http.server 4173
```

**Prérequis** : aucun pour la consultation. Python 3.9+ uniquement pour régénérer les pages.

---

## 🏗️ Architecture

```
delta-force-ultimate-guide/
├── index.html                    # Quartier Général
├── pages/
│   ├── operateurs/index.html
│   ├── armurerie/               # index · munitions · builds
│   ├── hazard-ops/              # index · black-site · boss · keycards
│   ├── cartes/index.html        # 6 cartes Leaflet
│   ├── havoc-warfare/index.html
│   ├── black-hawk-down/index.html
│   ├── saison-aurora/index.html
│   ├── astuces-pro/             # index · codes-portes
│   ├── encyclopedie/            # index · tier-list · economie
│   ├── news/index.html
│   └── outils/index.html
├── assets/
│   ├── css/
│   │   ├── design-system.css     # tokens, reset, typo, grilles
│   │   ├── animations.css        # scanlines, glitch, radar, flip3D, parallaxe
│   │   ├── components.css        # navbar, cartes, tableaux, outils, footer
│   │   └── responsive.css        # 320 / 480 / 768 / 1024 / 1440 px
│   ├── js/
│   │   ├── app.js                # noyau : nav, reveal, SFX, compteurs, filtres, tri
│   │   ├── search.js             # recherche globale Ctrl+K
│   │   ├── tools.js              # tous les calculateurs
│   │   └── maps.js               # cartes Leaflet + repli hors-ligne
│   ├── images/                   # 10 visuels JPG générés par IA
│   └── audio/                    # briefings MP3 (optionnel)
├── data/                         # 15 fichiers JSON — SOURCE DE VÉRITÉ
│   ├── season12.json             # saison, patch notes, 17 events
│   ├── operators.json            # 19 opérateurs détaillés
│   ├── weapons.json              # armes, stats, accessoires
│   ├── ammo.json                 # calibres et pénétration
│   ├── builds.json               # 40 codes de build
│   ├── maps.json                 # 6 cartes Ops + cartes Warfare
│   ├── bosses.json               # 8 boss
│   ├── keycards.json             # 101 keycards
│   ├── blacksite.json            # 11 stations
│   ├── vehicles.json             # 12 véhicules
│   ├── tier_list.json            # classements par mode
│   ├── economy.json              # monnaies, Hôtel des Ventes
│   ├── settings.json             # réglages PC/console/mobile
│   ├── daily_codes.json          # codes de portes (horodatés)
│   └── bhd.json                  # campagne Black Hawk Down
├── research/
│   └── sources_log.json          # 42 sources datées + niveaux de confiance
├── tools/                        # générateurs Python (non publiés)
│   ├── site_common.py            # layout partagé : head, navbar, footer
│   ├── build_*.py                # un script par groupe de pages
│   ├── build_all.py              # régénère tout
│   ├── build_sitemap.py          # sitemap.xml + robots.txt
│   └── qa.py                     # contrôle qualité
├── sitemap.xml · robots.txt · manifest.json
├── vercel.json · netlify.toml · .github/workflows/deploy.yml
└── LICENSE (MIT) · .gitignore
```

**Principe clé** : les fichiers `data/*.json` sont la **source de vérité**. Les pages HTML sont générées à partir d'eux par les scripts `tools/build_*.py`. Ne modifiez pas le HTML à la main — modifiez le JSON puis régénérez.

---

## 🔄 Régénérer le site

```bash
cd tools
python3 build_all.py        # régénère les 20 pages
python3 build_sitemap.py    # régénère sitemap.xml + robots.txt
cd ..
python3 tools/qa.py         # contrôle qualité complet
```

Le script `qa.py` vérifie : liens internes morts, images manquantes, attribut `lang`, nombre de `<h1>`, meta description, canonical, `og:image`, attributs `alt`, repère `#main`, lien d'évitement, `rel` sur les liens externes. Il sort en code 1 si une erreur bloquante est détectée (utilisable en CI).

---

## 📊 Mettre à jour les données

### Codes de portes (changent **tous les jours**)

1. Relever les codes sur [playdeltaforce.com/events/hq](https://www.playdeltaforce.com/events/hq/) ou [deltaforceitems.com](https://deltaforceitems.com/)
2. Éditer `data/daily_codes.json` : champ `codes[].code` et `_meta.date_releve`
3. `cd tools && python3 build_home.py && python3 build_outils.py`

> ⚠️ Les restrictions **CORS** empêchent un site statique de récupérer ces codes automatiquement depuis le navigateur. La mise à jour est volontairement manuelle, et la date du relevé est affichée sur le site.

### Nouveau patch / nouvelle saison

1. Mettre à jour `data/season12.json` (ou créer `data/season13.json`)
2. Ajouter la source dans `research/sources_log.json` avec sa date et son niveau de confiance
3. `cd tools && python3 build_all.py && python3 build_sitemap.py`
4. `python3 tools/qa.py`

### Convention de données

Chaque fichier JSON contient :

- un bloc **`_meta`** : nom du fichier, description, `derniere_maj`, `sources[]`
- un champ **`confiance`** sur les faits sensibles : `confirme` · `probable` · `À CONFIRMER`
- un **avertissement explicite** quand un changement est **Detonation-only**

---

## 🌍 Déploiement

> **Cible configurée : GitHub Pages sur `https://delta-guide.duckdns.org`.**
> `SITE_URL`, `sitemap.xml`, `robots.txt`, les `canonical` et l'Open Graph pointent déjà tous sur ce domaine. Le fichier `CNAME` est en place.

### Ce qui est déjà fait dans le dépôt

| Fichier | Rôle |
|---|---|
| `CNAME` | Contient `delta-guide.duckdns.org`. **Ne le supprimez pas** : il survit aux clones et aux déploiements CI. |
| `.nojekyll` | Désactive le traitement Jekyll de GitHub Pages. Sans lui, les dossiers commençant par `_` seraient ignorés. |
| `404.html` | Servie automatiquement par GitHub Pages. Exclue du sitemap. |
| `.github/workflows/deploy.yml` | Régénère le site depuis les JSON, lance la QA en mode **bloquant**, vérifie les médias et l'absence de SVG/PNG, puis publie. |

### Mise en ligne, étape par étape

**1. Pousser le dépôt**

```bash
git init && git add . && git commit -m "Delta Force — The Ultimate Operator's Guide"
git branch -M main
git remote add origin git@github.com:<utilisateur>/<repo>.git
git push -u origin main
```

Le dépôt doit être **public** : GitHub Pages n'accepte les domaines personnalisés que sur les dépôts publics (hors plans payants).

**2. Activer Pages**

`Settings → Pages → Source : **GitHub Actions**`. Le workflow prend le relais à chaque push sur `main`.

**3. Déclarer le domaine**

`Settings → Pages → Custom domain` → `delta-guide.duckdns.org` → **Save**.

**4. Configurer le DNS côté DuckDNS**

C'est le seul point qui demande de l'attention. GitHub recommande un **CNAME** vers `<utilisateur>.github.io` pour un sous-domaine, mais le tableau de bord DuckDNS n'expose qu'un champ **adresse IP** — vérifiez-le chez eux avant d'écarter la solution CNAME.

Si seul le champ IP est disponible, renseignez-y **une** des quatre adresses officielles de GitHub Pages :

```
185.199.108.153
185.199.109.153
185.199.110.153
185.199.111.153
```

Ces quatre adresses sont équivalentes ; DuckDNS n'en acceptant qu'une, vous perdez la redondance mais le service fonctionne.

**5. Activer HTTPS**

Une fois le DNS propagé, revenez dans `Settings → Pages` et cochez **Enforce HTTPS**. GitHub émet un certificat Let's Encrypt automatiquement. La case reste grisée tant que la vérification DNS n'est pas passée — comptez de quelques minutes à 24 h.

**6. Vérifier**

```bash
dig delta-guide.duckdns.org +short
curl -sI https://delta-guide.duckdns.org | head -n 1      # attendu : HTTP/2 200
curl -sI https://delta-guide.duckdns.org/pages/cartes/index.html | head -n 1
```

### ⚠️ Pièges connus

| Piège | Conséquence | À faire |
|---|---|---|
| Dépôt privé | Le domaine personnalisé est refusé | Passer le dépôt en public |
| `CNAME` supprimé par un outil de build | Le domaine se détache à chaque déploiement | Le garder versionné à la racine |
| `.nojekyll` absent | Jekyll ignore les fichiers et dossiers préfixés `_` | Le garder à la racine |
| « Enforce HTTPS » grisé | DNS pas encore propagé ou mal configuré | Vérifier avec `dig`, patienter, puis retirer/remettre le domaine dans les réglages |
| Changement de domaine plus tard | Les `canonical` et le sitemap pointent dans le vide | Modifier `SITE_URL` dans `tools/site_common.py`, relancer `build_all.py` + `build_sitemap.py`, mettre à jour `CNAME` |
| Cartes Leaflet | Invisibles sans accès réseau | Repli textuel automatique — comportement voulu |

### Autres hébergeurs

`vercel.json` et `netlify.toml` restent fournis et fonctionnels (Cloudflare Pages, Surge, Nginx aussi). Ils sont inutiles pour GitHub Pages mais ne gênent pas.

---

## ✅ Qualité, SEO, accessibilité

**Contrôle qualité au dernier build (19/11/2026)** : **32 pages · 2 021 liens internes · 123 images · 0 erreur, 0 avertissement.**
Audits complémentaires tous au vert : 0 média manquant, 0 image orpheline, 0 page sans briefing audio, 0 fuite de f-string.

### Performance
- CSS découpé en 4 fichiers, aucune dépendance de build
- Polices Google chargées en `media="print" onload` (non bloquantes) + `<noscript>` de repli
- `loading="lazy"` et `decoding="async"` sur toutes les images hors hero
- `fetchpriority="high"` sur l'image du hero d'accueil
- Leaflet chargé uniquement sur la page Cartes, avec SRI
- Aucun framework, aucun tracker, aucun cookie

### SEO
- `<title>` et meta description uniques par page
- Open Graph + Twitter Card complets
- `canonical` et `hreflang` sur chaque page
- JSON-LD **Schema.org** : `WebPage` + `VideoGame` (Team Jade, Level Infinite, Garena, plateformes, genres)
- `sitemap.xml` (**31 URLs** — la page 404 en est volontairement exclue) et `robots.txt`
- `manifest.json` pour l'installation PWA

### Accessibilité (WCAG 2.1 AA visé)
- Lien d'évitement vers `#main` sur chaque page
- `aria-label`, `aria-expanded`, `aria-controls` sur la navigation
- Rôles `tablist` / `tab` sur les onglets, `dialog` sur la recherche
- Tri de tableaux activable au clavier (`Enter` / `Espace`)
- Tier list manipulable au clavier (flèches haut / bas)
- Recherche navigable aux flèches, `Enter`, `Échap`
- `prefers-reduced-motion` : toutes les animations sont neutralisées
- `prefers-contrast: more` : palette renforcée
- Focus visible systématique, `alt` sur toutes les images

### Responsive
Points de rupture testés : **320, 480, 768, 1024, 1440 px** + orientation paysage mobile.
Le curseur viseur personnalisé est désactivé sur tactile.

---

## 🔬 Méthodologie & sources

Ce guide ne recopie pas des données de mémoire : **42 sources publiques datées** ont été consultées et consignées dans `research/sources_log.json`, chacune avec sa date de publication, sa date de consultation, son usage et un niveau de confiance (`officiel` · `eleve` · `moyen` · `communautaire`).

### Écarts assumés avec les idées reçues

Quand les sources contredisent une information répandue, **nous suivons les sources** :

| Sujet | Idée répandue | Vérifié (novembre 2026) |
|---|---|---|
| Nombre d'opérateurs | 18 | **19** |
| Munitions Saison 12 | 2 (.300BLK TIV/TTV) | **5** (+ CINDER, 7N30, SPALL) |
| AZ3 Supercritical | disponible au lancement | **18 décembre 2026**, Ops niveau 30 |
| Tier list | une liste unique | **séparée Operations / Warfare** |
| Akh Canal | en rotation | **retirée de Warfare en S12** |
| The Mog | carte S12 | introduite en **S11** |
| Branko | opérateur confirmé | **absent du wiki de référence → « À CONFIRMER »** |

### ⚠️ Le piège de lecture des patch notes Aurora

Une large partie des changements d'opérateurs annoncés le 7 novembre 2026 sont **exclusifs au mode Detonation** : Toxik, Raptor, Morse, Uluru, Gizmo, Stinger, Hackclaw, Vlinder, Desmoulins, ainsi que les GE2 de Luna et Shepherd.

Les transposer à Operations ou Warfare est l'erreur la plus répandue dans les guides communautaires. **Sur ce site, chaque changement précise son mode d'application.**

### Limites honnêtes

- Delta Force est un **jeu en service continu** : tout guide est un instantané. Dernière vérification complète le **19 novembre 2026**.
- Le calculateur TTK/DPS utilise un **modèle pédagogique** calibré sur les règles publiées. Il donne des ordres de grandeur comparatifs, **pas** les valeurs exactes du moteur de jeu.
- Les marqueurs des cartes Leaflet situent les zones décrites dans les guides sur un **plan schématique**. Pour des coordonnées exactes, utilisez [deltaforce.th.gl](https://deltaforce.th.gl/).
- Les prix de l'Hôtel des Ventes sont **pilotés par les joueurs** et fluctuent en permanence.
- Les codes de build sont liés à une **version** et à une **région** (Global vs Garena) et peuvent expirer après un patch.

---

## 🖼️ À propos des images

Les **10 illustrations** du site sont des **créations originales générées par IA**, à usage d'ambiance.
Ce ne sont **pas** des captures du jeu et elles ne reproduisent pas ses assets. Nommage : `[page]_[sujet]_[index].jpg`.

---

## 📜 Licence & mentions légales

### Code
Le code source de ce site (HTML, CSS, JavaScript, scripts Python) est publié sous **licence MIT** — voir [`LICENSE`](LICENSE).

### Mentions légales

> Ce site est un **guide fan-made non officiel**, réalisé par des joueurs pour des joueurs, à but informatif et **sans but lucratif**.
>
> *Delta Force* est développé par **Team Jade** (**TiMi Studio Group**) et édité par **Level Infinite** et **Garena** selon les régions.
>
> Toutes les marques, noms, logos, images, personnages et éléments de jeu cités appartiennent à leurs propriétaires respectifs.
>
> Ce site **n'est ni affilié, ni approuvé, ni sponsorisé** par Team Jade, TiMi Studio Group, Level Infinite, Garena ou Tencent.
>
> Pour toute information officielle, référez-vous à [playdeltaforce.com](https://www.playdeltaforce.com/).

### Crédits
- Données : sources communautaires publiques listées dans `research/sources_log.json`
- Cartes interactives : [Leaflet.js](https://leafletjs.com/) (BSD-2-Clause)
- Polices : Google Fonts — Exo 2, Rajdhani, Inter, JetBrains Mono, Orbitron, Share Tech Mono (SIL OFL)

---

**🎖️ Every Raid. Every Operator. Every Edge.**
