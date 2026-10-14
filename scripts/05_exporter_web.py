"""
Exporte les couches de la StoryMap en GeoJSON léger pour la page MapLibre (web/donnees/),
et calcule les chiffres affichés dans le récit (web/donnees/chiffres.json).

Chaque couche est simplifiée (tolérance en mètres, en Lambert-93), réduite aux champs
utiles et écrite en WGS84 avec 5 décimales (~1 m), au format RFC 7946.

Lancement : scripts\\lancer.bat 05_exporter_web.py
"""
import json

from qgis.core import (
    QgsCoordinateReferenceSystem, QgsCoordinateTransformContext, QgsDistanceArea,
    QgsFeature, QgsGeometry, QgsProject, QgsVectorFileWriter, QgsVectorLayer,
)

from _qgis import PROJET_GPKG, RACINE, REFERENTIEL, demarrer_qgis

SORTIE = RACINE / 'web' / 'donnees'
REF, PRJ = str(REFERENTIEL), str(PROJET_GPKG)

# nom du fichier -> (gpkg, couche, filtre, tolérance de simplification en m, champs gardés)
COUCHES = {
    'lit': (REF, 'durance_lit', None, 8, []),
    'lac': (REF, 'lac_serre_poncon', None, 15, []),
    'affluents': (REF, 'affluents', None, 80, ['toponyme']),
    'canal_edf': (REF, 'canal_edf', None, 15, []),
    'barrages': (REF, 'barrages_durance', 'toponyme IS NOT NULL', 0, ['toponyme']),
    'perimetre_1976': (PRJ, 'perimetre_1976', None, 30, ['nom', 'departement']),
    'departements': (REF, 'departements', None, 150, ['nom_officiel', 'code_insee']),
    'communes_riveraines': (REF, 'communes_riveraines', None, 40,
                            ['nom_officiel', 'code_insee_du_departement']),
    'epci': (PRJ, 'epci_riverains', None, 100, ['nom']),
    'levees': (REF, 'levees_durance', None, 5, []),
    'stations': (REF, 'stations_vigicrues', None, 0, ['lbentcru']),
    'natura_sic': (REF, 'natura2000_sic', None, 10, ['nom_site']),
    'natura_zps': (REF, 'natura2000_zps', None, 10, ['nom_site']),
}
# Couches sans attribut fusionnées en un seul objet : beaucoup plus légères
FUSIONNER = {'lit', 'canal_edf'}

# Codes et non objets QgsCoordinateReferenceSystem : un SCR créé avant le démarrage
# de QGIS est invalide, et la reprojection est alors ignorée sans erreur
L93 = 'EPSG:2154'
WGS84 = 'EPSG:4326'


def charger(gpkg, couche, filtre=None):
    lyr = QgsVectorLayer(f'{gpkg}|layername={couche}', couche, 'ogr')
    if not lyr.isValid():
        raise RuntimeError(f'Couche introuvable : {couche}')
    if filtre:
        lyr.setSubsetString(filtre)
    return lyr


def ecrire(lyr, nom, champs):
    import processing
    # Reprojection explicite : certaines couches WFS portent un SCR sans code EPSG,
    # que la transformation du writer ignore
    lyr = processing.run('native:reprojectlayer', {
        'INPUT': lyr, 'TARGET_CRS': WGS84, 'OUTPUT': 'memory:'})['OUTPUT']
    options = QgsVectorFileWriter.SaveVectorOptions()
    options.driverName = 'GeoJSON'
    options.layerOptions = ['RFC7946=YES', 'COORDINATE_PRECISION=5', 'WRITE_NAME=NO']
    if champs:
        options.attributes = [lyr.fields().indexOf(c) for c in champs]
    else:
        options.skipAttributeCreation = True
    chemin = SORTIE / f'{nom}.geojson'
    erreur, message, _, _ = QgsVectorFileWriter.writeAsVectorFormatV3(
        lyr, str(chemin), QgsCoordinateTransformContext(), options)
    if erreur:
        raise RuntimeError(f'{nom} : {message}')
    print(f'{nom:22} {lyr.featureCount():5} objets  {chemin.stat().st_size / 1024:7.0f} Ko')


def simplifier(lyr, tolerance):
    import processing
    if tolerance <= 0:
        return lyr
    return processing.run('native:simplifygeometries', {
        'INPUT': lyr, 'METHOD': 0, 'TOLERANCE': tolerance, 'OUTPUT': 'memory:'})['OUTPUT']


def trace_durance():
    """Un seul tracé continu, de l'amont vers le Rhône : sert à l'animation du tracé
    (line-progress) et au calcul de la longueur.

    Dans la BD TOPO, la Durance est un réseau de tronçons avec des bras secondaires
    (tresses) : on prend le plus court chemin dans ce réseau, du point le plus en amont
    du cours principal jusqu'à la confluence (point le plus à l'ouest)."""
    import processing
    axe = charger(REF, 'durance_axe')
    principal = max(axe.getFeatures(), key=lambda f: f.geometry().length())

    def extremites(geom):
        parties = geom.asMultiPolyline() if geom.isMultipart() else [geom.asPolyline()]
        return [pt for p in parties for pt in (p[0], p[-1])]

    amont = max(extremites(principal.geometry()), key=lambda pt: pt.y())
    aval = min((pt for f in axe.getFeatures() for pt in extremites(f.geometry())),
               key=lambda pt: pt.x())
    chemin = processing.run('native:shortestpathpointtopoint', {
        'INPUT': axe, 'STRATEGY': 0, 'TOLERANCE': 5,
        'START_POINT': f'{amont.x()},{amont.y()} [{L93}]',
        'END_POINT': f'{aval.x()},{aval.y()} [{L93}]',
        'OUTPUT': 'memory:'})['OUTPUT']
    trace = next(chemin.getFeatures()).geometry()
    if trace.isMultipart():
        trace = QgsGeometry.fromPolylineXY([pt for p in trace.asMultiPolyline() for pt in p])

    mesure = QgsDistanceArea()
    mesure.setSourceCrs(QgsCoordinateReferenceSystem(L93), QgsProject.instance().transformContext())
    mesure.setEllipsoid('GRS80')
    longueur_km = mesure.measureLength(trace) / 1000

    lyr = QgsVectorLayer('LineString?crs=EPSG:2154', 'trace', 'memory')
    f = QgsFeature()
    f.setGeometry(trace.simplify(20))
    lyr.dataProvider().addFeature(f)
    return lyr, longueur_km


def mesureur(lyr):
    mesure = QgsDistanceArea()
    mesure.setSourceCrs(lyr.crs(), QgsProject.instance().transformContext())
    mesure.setEllipsoid('GRS80')
    return mesure


def longueur_totale_km(lyr):
    mesure = mesureur(lyr)
    return sum(mesure.measureLength(f.geometry()) for f in lyr.getFeatures()) / 1000


def surface_totale_ha(lyr):
    mesure = mesureur(lyr)
    return sum(mesure.measureArea(f.geometry()) for f in lyr.getFeatures()) / 10000


def main():
    app = demarrer_qgis()  # noqa: F841
    SORTIE.mkdir(parents=True, exist_ok=True)

    trace, longueur_durance = trace_durance()
    ecrire(trace, 'durance', [])
    import processing
    for nom, (gpkg, couche, filtre, tol, champs) in COUCHES.items():
        lyr = simplifier(charger(gpkg, couche, filtre), tol)
        if nom == 'barrages':
            # Un barrage fait quelques centaines de mètres : invisible en ligne à l'échelle
            # de la vallée, on le représente par un point
            lyr = processing.run('native:centroids', {'INPUT': lyr, 'OUTPUT': 'memory:'})['OUTPUT']
        if nom in FUSIONNER:
            lyr = processing.run('native:dissolve', {'INPUT': lyr, 'OUTPUT': 'memory:'})['OUTPUT']
        ecrire(lyr, nom, champs)

    chiffres = {
        'longueur_durance_km': round(longueur_durance),
        'longueur_levees_km': round(longueur_totale_km(charger(REF, 'levees_durance'))),
        'communes_fondatrices_identifiees': charger(PRJ, 'perimetre_1976').featureCount(),
        'communes_riveraines': charger(REF, 'communes_riveraines').featureCount(),
        'stations_vigicrues': charger(REF, 'stations_vigicrues').featureCount(),
        'natura_sic_ha': round(surface_totale_ha(charger(REF, 'natura2000_sic'))),
        'natura_zps_ha': round(surface_totale_ha(charger(REF, 'natura2000_zps'))),
    }
    (SORTIE / 'chiffres.json').write_text(json.dumps(chiffres, ensure_ascii=False, indent=2),
                                          encoding='utf-8')
    print(json.dumps(chiffres, ensure_ascii=False))


if __name__ == '__main__':
    main()
