"""
Télécharge les données de référence de la StoryMap et les range dans
donnees/referentiel.gpkg (Lambert-93, EPSG:2154).

Sources : Géoplateforme IGN (BD TOPO, ADMIN EXPRESS), INPN (Natura 2000), Vigicrues.
Licence : Etalab 2.0 — à citer sur chaque carte web.

Relançable : referentiel.gpkg est reconstruit à chaque exécution. Les données
saisies à la main (numérisation, récit) vont dans donnees/smavd_50ans.gpkg,
que ce script ne touche jamais.

Lancement : scripts\\lancer.bat 01_telecharger_donnees.py
            scripts\\lancer.bat 01_telecharger_donnees.py affluents   (une seule couche)
"""
import json
import sys
import urllib.parse
import urllib.request

from osgeo import gdal

from _qgis import DONNEES, REFERENTIEL, demarrer_qgis

gdal.UseExceptions()

WFS = 'https://data.geopf.fr/wfs/ows'
PAGE = 5000
# Emprise de travail, de Serre-Ponçon au Rhône (lon/lat)
EMPRISE = (4.70, 43.60, 6.45, 44.60)
BBOX_CQL = "BBOX(geometrie, {}, {}, {}, {}, 'EPSG:4326')".format(*EMPRISE)
# Bassin entier, de la source (Montgenèvre) au Rhône : d'autres « Durance » existent ailleurs en France
BBOX_BASSIN = "BBOX(geometrie, 4.70, 43.60, 6.80, 45.00, 'EPSG:4326')"

# nom de la couche -> (type WFS, filtre CQL, champs conservés)
COUCHES = {
    'durance_axe': (
        'BDTOPO_V3:cours_d_eau', f"toponyme = 'la Durance' AND {BBOX_BASSIN}",
        ['toponyme', 'code_hydrographique', 'importance']),
    'affluents': (
        'BDTOPO_V3:cours_d_eau',
        "toponyme IN ('le Rhône', 'le Verdon', 'le Buëch', 'la Bléone', 'l''Ubaye', "
        f"'l''Asse', 'le Calavon', 'le Jabron') AND {BBOX_BASSIN}",
        ['toponyme', 'importance']),
    # Les surfaces en eau ne portent pas le nom du cours d'eau : le lit de la Durance
    # est extrait plus bas par croisement avec l'axe
    'surfaces_eau': (
        'BDTOPO_V3:surface_hydrographique', f"nature = 'Ecoulement naturel' AND {BBOX_CQL}",
        ['nature', 'persistance']),
    'lac_serre_poncon': (
        'BDTOPO_V3:plan_d_eau', "toponyme = 'Lac de Serre-Ponçon'",
        ['toponyme', 'nature']),
    'canal_edf': (
        'BDTOPO_V3:troncon_hydrographique',
        "(cpx_toponyme_de_cours_d_eau LIKE '%E.D.F%' OR cpx_toponyme_de_cours_d_eau LIKE '%EDF%'"
        f" OR cpx_toponyme_de_cours_d_eau ILIKE '%usinier%') AND {BBOX_CQL}",
        ['cpx_toponyme_de_cours_d_eau', 'classe_de_largeur', 'position_par_rapport_au_sol']),
    'levees': (
        'BDTOPO_V3:ligne_orographique', f"nature = 'Levée' AND {BBOX_CQL}",
        ['nature']),
    'barrages': (
        'BDTOPO_V3:construction_lineaire', f"nature = 'Barrage' AND {BBOX_CQL}",
        ['nature', 'nature_detaillee', 'toponyme']),
    'communes': (
        'ADMINEXPRESS-COG-CARTO.LATEST:commune', BBOX_CQL,
        ['nom_officiel', 'code_insee', 'code_insee_du_departement', 'population',
         'codes_siren_des_epci']),
    'epci': (
        'ADMINEXPRESS-COG-CARTO.LATEST:epci', BBOX_CQL,
        ['nom_officiel', 'code_siren', 'nature']),
    'departements': (
        'ADMINEXPRESS-COG-CARTO.LATEST:departement',
        "code_insee IN ('04', '05', '13', '83', '84')",
        ['nom_officiel', 'code_insee']),
    'natura2000_sic': (
        'patrinat_sic:sic', "nom_site = 'La Durance'",
        ['nom_site', 'date_crea', 'operateur', 'url_fiche', 'surf_off']),
    'natura2000_zps': (
        'patrinat_zps:zps', "nom_site = 'La Durance'",
        ['nom_site', 'date_crea', 'operateur', 'url_fiche', 'surf_off']),
    'stations_vigicrues': (
        'VIGICRUES:stations', "lbentitehy LIKE '%Durance%'",
        ['cdentcru', 'lbentcru', 'lbentitehy']),
}


def telecharger(typename, cql):
    """Télécharge une couche WFS page par page ; renvoie la liste des fichiers GeoJSON."""
    dossier = DONNEES / 'sources'
    dossier.mkdir(parents=True, exist_ok=True)
    fichiers, debut = [], 0
    while True:
        params = {
            'SERVICE': 'WFS', 'VERSION': '2.0.0', 'REQUEST': 'GetFeature',
            'TYPENAMES': typename, 'OUTPUTFORMAT': 'application/json',
            'SRSNAME': 'EPSG:2154', 'COUNT': PAGE, 'STARTINDEX': debut,
            'CQL_FILTER': cql,
        }
        url = WFS + '?' + urllib.parse.urlencode(params)
        with urllib.request.urlopen(url, timeout=300) as rep:
            contenu = rep.read()
        n = len(json.loads(contenu)['features'])
        if n == 0:
            break
        fichier = dossier / f"{typename.replace(':', '_')}_{debut // PAGE}.geojson"
        fichier.write_bytes(contenu)
        fichiers.append(fichier)
        if n < PAGE:
            break
        debut += PAGE
    return fichiers


def charger(fichiers, nom, champs):
    """Ajoute les pages GeoJSON dans referentiel.gpkg sous le nom de couche donné."""
    for i, f in enumerate(fichiers):
        if i:
            mode = 'append'
        else:
            mode = 'overwrite' if REFERENTIEL.exists() else None
        # -select est interdit avec -append : on passe par une requête SQL
        gdal.VectorTranslate(
            str(REFERENTIEL), str(f), format='GPKG', accessMode=mode, layerName=nom,
            SQLStatement=f'SELECT {", ".join(champs)} FROM "{f.stem}"', dstSRS='EPSG:2154',
            geometryType='PROMOTE_TO_MULTI', makeValid=True,
        )


def deriver():
    """Couches utiles au récit, déduites des données brutes."""
    import processing
    ref = str(REFERENTIEL)

    def couche(nom):
        return f'{ref}|layername={nom}'

    def sortie(nom):
        return f'ogr:dbname=\'{ref}\' table="{nom}" (geom)'

    processing.run('native:buffer', {
        'INPUT': couche('durance_axe'), 'DISTANCE': 1000, 'DISSOLVE': True,
        'OUTPUT': sortie('durance_tampon_1km')})
    # Communes touchées par la rivière (axe ou lit en eau)
    processing.run('native:buffer', {
        'INPUT': couche('durance_axe'), 'DISTANCE': 50, 'DISSOLVE': True,
        'OUTPUT': sortie('durance_tampon_50m')})
    processing.run('native:extractbylocation', {
        'INPUT': couche('communes'), 'PREDICATE': [0],
        'INTERSECT': couche('durance_tampon_50m'), 'OUTPUT': sortie('communes_riveraines')})
    processing.run('native:extractbylocation', {
        'INPUT': couche('surfaces_eau'), 'PREDICATE': [0],
        'INTERSECT': couche('durance_tampon_50m'), 'OUTPUT': sortie('durance_lit')})
    for brut, final in (('levees', 'levees_durance'), ('barrages', 'barrages_durance')):
        processing.run('native:extractbylocation', {
            'INPUT': couche(brut), 'PREDICATE': [0],
            'INTERSECT': couche('durance_tampon_1km'), 'OUTPUT': sortie(final)})


def main():
    """Sans argument : tout reconstruire. Avec des noms de couches : ne mettre à jour qu'elles
    (utile quand un projet QGIS ouvert verrouille le fichier)."""
    app = demarrer_qgis()  # noqa: F841 — doit rester en vie pendant le script
    choix = sys.argv[1:]
    inconnues = set(choix) - set(COUCHES)
    if inconnues:
        sys.exit(f'Couches inconnues : {", ".join(inconnues)}')
    if not choix and REFERENTIEL.exists():
        REFERENTIEL.unlink()
    for nom, (typename, cql, champs) in COUCHES.items():
        if choix and nom not in choix:
            continue
        fichiers = telecharger(typename, cql)
        charger(fichiers, nom, champs)
        n = sum(len(json.loads(f.read_bytes())['features']) for f in fichiers)
        print(f'{nom:22} {n:6} objets')
    if not choix:
        deriver()
        print('Couches dérivées : communes_riveraines, durance_lit, levees_durance, barrages_durance')
    print(f'Terminé : {REFERENTIEL}')


if __name__ == '__main__':
    main()
