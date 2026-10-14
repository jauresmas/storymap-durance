# StoryMap : 50 ans au fil de la Durance (SMAVD, 1976-2026)

Récit cartographique indépendant sur l'histoire du Syndicat mixte d'aménagement de la
vallée de la Durance, construit à partir de données publiques.
Chaîne de production : **QGIS / PyQGIS → GeoJSON → page web MapLibre GL JS**.

Projet personnel, non affilié au SMAVD.

## Arborescence

```
storymap-smavd/
├── donnees/
│   ├── referentiel.gpkg     données IGN / INPN / Vigicrues (re-téléchargeables)
│   ├── smavd_50ans.gpkg     couches du récit, à enrichir à la main dans QGIS
│   └── sources/             réponses WFS brutes
├── qgis/                    un projet QGIS par chapitre + styles .qml
├── web/                     LA STORYMAP (site statique)
│   ├── index.html           le dossier : couverture, 9 pièces, bordereau
│   ├── assets/css/          storymap.css (charte), fonts.css
│   ├── assets/js/           storymap.js (carte, caméra, cartouche, calque 1950)
│   ├── assets/fonts/        Archivo et Courier Prime, auto-hébergées (OFL)
│   ├── assets/vendor/       MapLibre GL JS 4.7.1
│   ├── donnees/             GeoJSON allégés + chiffres.json
│   ├── commun/, cartes/     exports qgis2web (cartes d'exploration, facultatif)
│   └── exports/             dossier de sortie de qgis2web
├── docs/                    frise chronologique sourcée, story-board
├── scripts/                 chaîne de production PyQGIS
├── PRODUCT.md, DESIGN.md    cadrage du produit et système visuel
└── .impeccable/             brief de conception et captures de contrôle
```

## Chaîne de production

Tous les scripts se lancent avec le Python de QGIS via `scripts\lancer.bat`.

| Étape | Commande | Effet |
|---|---|---|
| 1 | `scripts\lancer.bat 01_telecharger_donnees.py` | Reconstruit `referentiel.gpkg` depuis la Géoplateforme IGN (ou une couche : `… 01_telecharger_donnees.py affluents`) |
| 2 | `scripts\lancer.bat 02_preparer_recit.py` | Crée les couches du récit dans `smavd_50ans.gpkg` (jamais écrasées) |
| 3 | `scripts\lancer.bat 03_creer_projets_qgis.py` | Régénère les projets `.qgz` par chapitre |
| 4 | `scripts\lancer.bat 05_exporter_web.py` | Exporte les GeoJSON allégés et les chiffres de la StoryMap dans `web/donnees/` |
| (option) | qgis2web puis `scripts\lancer.bat 04_integrer_export.py 0X` | Cartes d'exploration qgis2web dans `web/cartes/` |

## Voir la StoryMap

Les données sont chargées par le navigateur : il faut un petit serveur web (un double-clic
sur `index.html` ne suffit pas).

```bash
python -m http.server 8765 --directory web
```

Puis ouvrir http://localhost:8765.

**Publication sur GitHub Pages** : le workflow `.github/workflows/pages.yml` publie le
dossier `web/` à chaque envoi sur `main`. À activer une fois dans le dépôt :
*Settings › Pages › Build and deployment › Source : GitHub Actions*.

Les données lourdes ne sont pas versionnées (`.gitignore`) : après un clonage, relancer
`scripts\lancer.bat 01_telecharger_donnees.py` pour recréer `donnees/referentiel.gpkg`.

## Avant publication

- Compléter dans `web/index.html` (bordereau) le lien du dépôt de code et le lien de
  contact, marqués « à ajouter ».
- Vérifier les pistes encore ouvertes de `docs/frise_chronologique.csv`.

## Règles du projet

- Chaque fait affiché est sourcé (lien en pied de pièce) ou présenté avec prudence.
- Données IGN, INPN et Vigicrues sous Licence Ouverte Etalab 2.0 : sources citées sur la page.
- Les couleurs de la carte reprennent la sémiologie des projets QGIS
  (`scripts/03_creer_projets_qgis.py` et `web/assets/js/storymap.js`).
