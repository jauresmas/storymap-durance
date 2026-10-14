"""
Crée les couches propres au récit dans donnees/smavd_50ans.gpkg :

- perimetre_1976 : communes fondatrices. HYPOTHÈSE : communes riveraines des
  Bouches-du-Rhône et de Vaucluse (30 trouvées, 31 annoncées en 1976), à confirmer
  avec l'arrêté interpréfectoral du 5 novembre 1976.
- epci_riverains : intercommunalités traversées par la Durance (acteurs GEMAPI).
- evenements : points du récit (titre, date, chapitre, texte, source, à vérifier).

Une couche déjà présente n'est jamais écrasée : tu peux la modifier à la main
dans QGIS puis relancer le script sans rien perdre.

Lancement : scripts\\lancer.bat 02_preparer_recit.py
"""
from qgis.core import (
    QgsCoordinateReferenceSystem, QgsCoordinateTransform, QgsFeature, QgsField,
    QgsGeometry, QgsPointXY, QgsProject, QgsVectorFileWriter, QgsVectorLayer,
)
from qgis.PyQt.QtCore import QVariant

from _qgis import PROJET_GPKG, REFERENTIEL, demarrer_qgis

STATUT_1976 = ("Hypothèse : communes riveraines 13 et 84. "
               "À confirmer avec l'arrêté interpréfectoral du 5 novembre 1976.")

# (titre, date, chapitre, texte, source, à vérifier, lon, lat)
EVENEMENTS = [
    ("Barrage de Serre-Ponçon", "1955-1960", 1,
     "Construit par EDF après la loi de 1955 sur l'aménagement de la Durance, le barrage "
     "crée le lac de Serre-Ponçon. La Durance devient une rivière régulée.",
     "À compléter (archives EDF, SMAVD)", "oui", 6.26739, 44.47030),
    ("Barrage de Mallemort", "années 1960-1970", 1,
     "Prise d'eau du canal EDF : une grande partie du débit de la Durance est dérivée "
     "vers les centrales hydroélectriques, jusqu'à l'étang de Berre.",
     "À compléter (archives EDF, SMAVD)", "oui", None, None),
    ("Mallemort, siège du SMAVD", "1976", 2,
     "Le syndicat est créé par les départements des Bouches-du-Rhône et de Vaucluse et "
     "31 communes riveraines (arrêté interpréfectoral du 5 novembre 1976). Son siège "
     "administratif est aujourd'hui à Mallemort.",
     "Délibération du Département des Bouches-du-Rhône ; BANATIC", "non", 5.182445, 43.729233),
]


def ecrire(couche, nom):
    """Écrit une couche dans smavd_50ans.gpkg, sauf si elle y existe déjà."""
    if PROJET_GPKG.exists():
        existante = QgsVectorLayer(f'{PROJET_GPKG}|layername={nom}', nom, 'ogr')
        if existante.isValid():
            print(f'{nom:16} déjà présente, conservée')
            return
    options = QgsVectorFileWriter.SaveVectorOptions()
    options.driverName = 'GPKG'
    options.layerName = nom
    if PROJET_GPKG.exists():
        options.actionOnExistingFile = QgsVectorFileWriter.CreateOrOverwriteLayer
    QgsVectorFileWriter.writeAsVectorFormatV3(
        couche, str(PROJET_GPKG), QgsProject.instance().transformContext(), options)
    print(f'{nom:16} {couche.featureCount():4} objets')


def refactoriser(entree, champs):
    """Ne garde que les champs utiles, renommés : champs = [(nom, expression, type)]."""
    import processing
    mapping = [{'name': n, 'expression': e, 'type': t, 'length': 0, 'precision': 0}
               for n, e, t in champs]
    return processing.run('native:refactorfields', {
        'INPUT': entree, 'FIELDS_MAPPING': mapping, 'OUTPUT': 'memory:'})['OUTPUT']


def main():
    app = demarrer_qgis()  # noqa: F841
    import processing
    ref = str(REFERENTIEL)
    texte, entier = QVariant.String, QVariant.Int

    fondatrices = processing.run('native:extractbyexpression', {
        'INPUT': f'{ref}|layername=communes_riveraines',
        'EXPRESSION': "code_insee_du_departement IN ('13', '84')",
        'OUTPUT': 'memory:'})['OUTPUT']
    ecrire(refactoriser(fondatrices, [
        ('nom', 'nom_officiel', texte), ('code_insee', 'code_insee', texte),
        ('departement', 'code_insee_du_departement', texte),
        ('population', 'population', entier),
        ('statut', f"'{STATUT_1976.replace(chr(39), chr(39) * 2)}'", texte),
    ]), 'perimetre_1976')

    epci = processing.run('native:extractbylocation', {
        'INPUT': f'{ref}|layername=epci', 'PREDICATE': [0],
        'INTERSECT': f'{ref}|layername=durance_tampon_50m', 'OUTPUT': 'memory:'})['OUTPUT']
    ecrire(refactoriser(epci, [
        ('nom', 'nom_officiel', texte), ('code_siren', 'code_siren', texte),
        ('nature', 'nature', texte),
    ]), 'epci_riverains')

    # Barrage de Mallemort : position reprise de la BD TOPO
    barrages = QgsVectorLayer(f'{ref}|layername=barrages_durance', 'b', 'ogr')
    mallemort = next(barrages.getFeatures("toponyme = 'Barrage de Mallemort'"))
    pt_mallemort = mallemort.geometry().centroid().asPoint()

    l93 = QgsCoordinateReferenceSystem('EPSG:2154')
    vers_l93 = QgsCoordinateTransform(
        QgsCoordinateReferenceSystem('EPSG:4326'), l93, QgsProject.instance())
    evts = QgsVectorLayer('Point?crs=EPSG:2154', 'evenements', 'memory')
    evts.dataProvider().addAttributes([
        QgsField('titre', texte), QgsField('date', texte), QgsField('chapitre', entier),
        QgsField('texte', texte), QgsField('photo', texte), QgsField('source', texte),
        QgsField('a_verifier', texte),
    ])
    evts.updateFields()
    for titre, date, chap, txt, source, verif, lon, lat in EVENEMENTS:
        f = QgsFeature(evts.fields())
        f.setAttributes([titre, date, chap, txt, '', source, verif])
        pt = pt_mallemort if lon is None else vers_l93.transform(QgsPointXY(lon, lat))
        f.setGeometry(QgsGeometry.fromPointXY(pt))
        evts.dataProvider().addFeature(f)
    ecrire(evts, 'evenements')
    print(f'Terminé : {PROJET_GPKG}')


if __name__ == '__main__':
    main()
