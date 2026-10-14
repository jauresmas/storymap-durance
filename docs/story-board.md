# Story-board : 50 ans au fil de la Durance

Version de travail, à valider avec la responsable de la communication.
Faits datés et sources : `frise_chronologique.csv`.

| # | Chapitre | Message clé | Carte (qgis/) | Données | Reste à faire |
|---|---|---|---|---|---|
| 1 | Avant 1976 : une rivière aménagée | EDF transforme la Durance : Serre-Ponçon, canal, barrages | `01_avant_1976.qgz` | Lit, axe, lac, canal EDF, barrages nommés, photos 1950-1965 et actuelles | Numériser la **bande active** de 1950 et d'aujourd'hui ; vérifier les dates EDF |
| 2 | 1976 : naissance du SMAVD | Deux départements et 31 communes s'unissent | `02_naissance_1976.qgz` | Communes fondatrices (hypothèse), départements 13 et 84, siège | Identifier la **31e commune** dans l'arrêté du 05/11/1976 |
| 3 | Gérer le lit et se protéger des crues | Concession du domaine public fluvial (1982), digues, crues | `03_crues_digues.qgz` | Digues et levées (BD TOPO), stations Vigicrues, lit | Dates et emprises des crues de 1994 ; digues gérées par le SMAVD (données internes) |
| 4 | Le virage environnemental | La Durance, milieu naturel remarquable | `04_environnement.qgz` | Natura 2000 SIC et ZPS | Rôle exact du SMAVD (animation ?) ; sites restaurés |
| 5 | De Serre-Ponçon au Rhône | 2005 extension, 2010 EPTB, 2018 GEMAPI | `05_serre_poncon_au_rhone.qgz` | Intercommunalités, communes riveraines, départements | Liste officielle des 13 EPCI membres (14 trouvés) |
| 6 | Et demain ? | PAPI 2024-2030, ressource en eau, climat | à créer | À définir | Écrire avec la communication |

## Sémiologie commune

- Eau : bleus (`#2f7fc1` axe, `#a9cfee` lit)
- Périmètres du SMAVD : ocre (`#e39b3b`)
- Hydroélectricité : violet en tirets (`#6a4c93`)
- Digues : rouge brique (`#b8432f`)
- Nature : vert (`#3a8f5c`)
- 3 ou 4 couches au maximum par carte, fond Plan IGN adouci

Charte provisoire : à remplacer par la charte graphique du SMAVD (couleurs dans
`scripts/03_creer_projets_qgis.py` et `web/commun/story.css`).
