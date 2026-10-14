"""
Crée un projet QGIS par chapitre dans qgis/, prêt pour l'export qgis2web :
fonds de carte IGN, styles communs (sauvegardés dans qgis/styles/), alias de
champs lisibles pour les popups, champs techniques masqués.

Relancer le script écrase les projets .qgz (jamais les données). Après des
retouches à la main dans QGIS, ne le relance plus ou enregistre sous un autre nom.

Lancement : scripts\\lancer.bat 03_creer_projets_qgis.py
"""
from qgis.core import (
    QgsCategorizedSymbolRenderer, QgsCoordinateReferenceSystem, QgsCoordinateTransform,
    QgsDataSourceUri, QgsEditorWidgetSetup, QgsFillSymbol, QgsLineSymbol, QgsMarkerSymbol,
    QgsPalLayerSettings, QgsProject, QgsRasterLayer, QgsReferencedRectangle,
    QgsRendererCategory, QgsTextBufferSettings, QgsTextFormat, QgsVectorLayer,
    QgsVectorLayerSimpleLabeling,
)
from qgis.PyQt.QtGui import QColor, QFont

from _qgis import PROJET_GPKG, RACINE, REFERENTIEL, demarrer_qgis

# Charte provisoire : à remplacer par la charte graphique du SMAVD
EAU = '47,127,193'
EAU_CLAIR = '169,207,238'
HYDROELEC = '106,76,147'
OUVRAGE = '45,45,45'
PERIMETRE = '227,155,59'
DIGUE = '184,67,47'
NATURE = '58,143,92'
LIMITE = '107,107,107'
PASTELS = ['#8dd3c7', '#fdb462', '#bebada', '#fb8072', '#80b1d3', '#b3de69', '#fccde5',
           '#bc80bd', '#ccebc5', '#ffed6f', '#d9d9d9', '#a6cee3', '#f4a582', '#92c5de']

WMTS = ('https://data.geopf.fr/wmts?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0'
        '&LAYER={}&STYLE={}&TILEMATRIXSET=PM&FORMAT={}'
        '&TILEMATRIX={{z}}&TILEROW={{y}}&TILECOL={{x}}')
FONDS = {
    'Plan IGN': ('GEOGRAPHICALGRIDSYSTEMS.PLANIGNV2', 'normal', 'image/png', 19),
    'Photos aériennes 1950-1965': (
        'ORTHOIMAGERY.ORTHOPHOTOS.1950-1965', 'BDORTHOHISTORIQUE', 'image/png', 18),
    'Photos aériennes actuelles': ('ORTHOIMAGERY.ORTHOPHOTOS', 'normal', 'image/jpeg', 19),
}

QGIS_DIR = RACINE / 'qgis'
STYLES = QGIS_DIR / 'styles'


# --- Couches ---------------------------------------------------------------

def fond(nom):
    couche, style, fmt, zmax = FONDS[nom]
    # encodedUri() encode l'URL comme le fait QGIS : un « ? » encodé à la main
    # (%3F) donne un fond vide
    uri = QgsDataSourceUri()
    uri.setParam('type', 'xyz')
    uri.setParam('url', WMTS.format(couche, style, fmt))
    uri.setParam('zmin', '0')
    uri.setParam('zmax', str(zmax))
    return QgsRasterLayer(bytes(uri.encodedUri()).decode(), nom, 'wms')


def vecteur(gpkg, couche, nom, filtre=None):
    lyr = QgsVectorLayer(f'{gpkg}|layername={couche}', nom, 'ogr')
    if not lyr.isValid():
        raise RuntimeError(f'Couche introuvable : {couche} dans {gpkg}')
    if filtre:
        lyr.setSubsetString(filtre)
    return lyr


def popup(lyr, alias):
    """Champs de popup : alias lisibles ; tout champ absent de `alias` est masqué."""
    for i, champ in enumerate(lyr.fields()):
        if champ.name() in alias:
            lyr.setFieldAlias(i, alias[champ.name()])
        else:
            lyr.setEditorWidgetSetup(i, QgsEditorWidgetSetup('Hidden', {}))


# --- Styles ----------------------------------------------------------------

def remplissage(lyr, couleur, opacite=255, contour='255,255,255', epaisseur=0.3, style='solid'):
    lyr.renderer().setSymbol(QgsFillSymbol.createSimple({
        'color': f'{couleur},{opacite}', 'outline_color': contour,
        'outline_width': str(epaisseur), 'outline_style': style}))


def contour_seul(lyr, couleur, epaisseur=0.5, style='dash'):
    lyr.renderer().setSymbol(QgsFillSymbol.createSimple({
        'style': 'no', 'outline_color': couleur, 'outline_width': str(epaisseur),
        'outline_style': style}))


def ligne(lyr, couleur, epaisseur, style='solid'):
    lyr.renderer().setSymbol(QgsLineSymbol.createSimple({
        'line_color': couleur, 'line_width': str(epaisseur), 'line_style': style,
        'capstyle': 'round', 'joinstyle': 'round'}))


def point(lyr, couleur, taille=3.2, forme='circle'):
    lyr.renderer().setSymbol(QgsMarkerSymbol.createSimple({
        'name': forme, 'color': couleur, 'outline_color': '255,255,255',
        'outline_width': '0.6', 'size': str(taille)}))


def categories(lyr, champ):
    valeurs = sorted({f[champ] for f in lyr.getFeatures()})
    cats = []
    for i, v in enumerate(valeurs):
        sym = QgsFillSymbol.createSimple({
            'color': PASTELS[i % len(PASTELS)], 'outline_color': '255,255,255',
            'outline_width': '0.4'})
        sym.setOpacity(0.8)
        cats.append(QgsRendererCategory(v, sym, v))
    lyr.setRenderer(QgsCategorizedSymbolRenderer(champ, cats))


def etiquettes(lyr, champ):
    fmt = QgsTextFormat()
    fmt.setFont(QFont('Arial'))
    fmt.setSize(9)
    fmt.setColor(QColor(30, 30, 30))
    halo = QgsTextBufferSettings()
    halo.setEnabled(True)
    halo.setSize(1)
    halo.setColor(QColor(255, 255, 255))
    fmt.setBuffer(halo)
    reglages = QgsPalLayerSettings()
    reglages.fieldName = champ
    reglages.setFormat(fmt)
    reglages.dist = 1.5
    lyr.setLabeling(QgsVectorLayerSimpleLabeling(reglages))
    lyr.setLabelsEnabled(True)


# --- Couches stylées, partagées par les chapitres ---------------------------

REF, PRJ = str(REFERENTIEL), str(PROJET_GPKG)


def durance_axe():
    lyr = vecteur(REF, 'durance_axe', 'La Durance')
    ligne(lyr, EAU, 0.9)
    popup(lyr, {'toponyme': "Cours d'eau"})
    return lyr


def durance_lit():
    lyr = vecteur(REF, 'durance_lit', 'Lit de la Durance')
    remplissage(lyr, EAU_CLAIR, contour=EAU, epaisseur=0.1)
    popup(lyr, {})
    return lyr


def lac():
    lyr = vecteur(REF, 'lac_serre_poncon', 'Lac de Serre-Ponçon')
    remplissage(lyr, EAU, opacite=200, contour=EAU, epaisseur=0.1)
    popup(lyr, {'toponyme': 'Nom'})
    return lyr


def canal_edf():
    lyr = vecteur(REF, 'canal_edf', 'Canal EDF')
    ligne(lyr, HYDROELEC, 0.7, 'dash')
    popup(lyr, {'cpx_toponyme_de_cours_d_eau': 'Nom'})
    return lyr


def barrages():
    # Les nombreux seuils sans nom encombrent la carte : on garde les ouvrages nommés
    lyr = vecteur(REF, 'barrages_durance', 'Barrages', 'toponyme IS NOT NULL')
    ligne(lyr, OUVRAGE, 1.6)
    popup(lyr, {'toponyme': 'Nom', 'nature_detaillee': 'Type'})
    return lyr


def evenements(chapitre):
    lyr = vecteur(PRJ, 'evenements', 'Repères du récit', f'chapitre = {chapitre}')
    point(lyr, PERIMETRE, 4.2)
    popup(lyr, {'titre': 'Repère', 'date': 'Date', 'texte': 'Récit', 'source': 'Source'})
    etiquettes(lyr, 'titre')
    return lyr


def departements(codes):
    liste = ', '.join(f"'{c}'" for c in codes)
    lyr = vecteur(REF, 'departements', 'Départements', f'code_insee IN ({liste})')
    contour_seul(lyr, LIMITE, 0.6)
    popup(lyr, {'nom_officiel': 'Département'})
    return lyr


def perimetre_1976():
    lyr = vecteur(PRJ, 'perimetre_1976', 'Communes fondatrices (1976)')
    remplissage(lyr, PERIMETRE, opacite=150)
    popup(lyr, {'nom': 'Commune', 'departement': 'Département', 'statut': 'Statut'})
    return lyr


def communes_riveraines():
    lyr = vecteur(REF, 'communes_riveraines', 'Communes riveraines')
    contour_seul(lyr, '255,255,255', 0.3, 'solid')
    popup(lyr, {'nom_officiel': 'Commune'})
    return lyr


def epci_riverains():
    lyr = vecteur(PRJ, 'epci_riverains', 'Intercommunalités riveraines')
    categories(lyr, 'nom')
    popup(lyr, {'nom': 'Intercommunalité', 'nature': 'Type'})
    return lyr


def levees():
    lyr = vecteur(REF, 'levees_durance', 'Digues et levées')
    ligne(lyr, DIGUE, 0.8)
    popup(lyr, {})
    return lyr


def stations():
    lyr = vecteur(REF, 'stations_vigicrues', 'Stations de mesure des crues')
    point(lyr, '11,114,133', 3.4, 'square')
    popup(lyr, {'lbentcru': 'Station', 'lbentitehy': "Cours d'eau"})
    return lyr


def natura(type_site):
    nom = {'sic': 'Natura 2000 : habitats (SIC)', 'zps': 'Natura 2000 : oiseaux (ZPS)'}[type_site]
    lyr = vecteur(REF, f'natura2000_{type_site}', nom)
    if type_site == 'sic':
        remplissage(lyr, NATURE, opacite=110, contour=NATURE, epaisseur=0.3)
    else:
        contour_seul(lyr, NATURE, 0.6)
    popup(lyr, {'nom_site': 'Site', 'date_crea': 'Création', 'operateur': 'Opérateur',
                'url_fiche': 'Fiche INPN'})
    return lyr


# --- Chapitres -------------------------------------------------------------
# dossier, titre, résumé, couches (du haut vers le bas), fonds (le 1er est visible),
# couches servant à cadrer la vue

CHAPITRES = [
    ('01_avant_1976', 'Avant 1976 : une rivière aménagée',
     "Serre-Ponçon, le canal EDF et les barrages transforment la Durance.",
     lambda: [evenements(1), barrages(), canal_edf(), lac(), durance_axe(), durance_lit()],
     ['Plan IGN', 'Photos aériennes 1950-1965', 'Photos aériennes actuelles'],
     ['Lit de la Durance', 'Lac de Serre-Ponçon']),
    ('02_naissance_1976', '1976 : naissance du SMAVD',
     "Les départements des Bouches-du-Rhône et de Vaucluse et 31 communes s'unissent.",
     lambda: [evenements(2), durance_axe(), perimetre_1976(), departements(['13', '84'])],
     ['Plan IGN'], ['Communes fondatrices (1976)']),
    ('03_crues_digues', 'Gérer le lit et se protéger des crues',
     "Digues, surveillance des crues et gestion du domaine public fluvial (1982).",
     lambda: [stations(), levees(), durance_axe(), durance_lit()],
     ['Plan IGN', 'Photos aériennes actuelles'], ['Digues et levées']),
    ('04_environnement', 'Le virage environnemental',
     "La Durance reconnue pour sa biodiversité : Natura 2000 (1997, 2003).",
     lambda: [natura('zps'), natura('sic'), durance_axe()],
     ['Plan IGN', 'Photos aériennes actuelles'], ['Natura 2000 : habitats (SIC)']),
    ('05_serre_poncon_au_rhone', 'De Serre-Ponçon au Rhône',
     "2005 : extension du périmètre. 2010 : EPTB. 2018 : la GEMAPI et les intercommunalités.",
     lambda: [durance_axe(), lac(), communes_riveraines(), epci_riverains(),
              departements(['04', '05', '13', '84'])],
     ['Plan IGN'], ['Intercommunalités riveraines']),
]


def creer_projet(dossier, titre, resume, couches, fonds, cadrage):
    projet = QgsProject.instance()
    projet.clear()
    web = QgsCoordinateReferenceSystem('EPSG:3857')
    projet.setTitle(titre)
    md = projet.metadata()
    md.setTitle(titre)
    md.setAbstract(resume)
    projet.setMetadata(md)

    racine = projet.layerTreeRoot()
    for lyr in couches():
        projet.addMapLayer(lyr, False)
        racine.addLayer(lyr)
        # Style réutilisable : clic droit > Propriétés > Style > Charger le style
        nom_source = lyr.source().split('layername=')[-1].split('|')[0]
        lyr.saveNamedStyle(str(STYLES / f'{nom_source}.qml'))
    groupe = racine.addGroup('Fonds de carte')
    for i, nom in enumerate(fonds):
        lyr = fond(nom)
        projet.addMapLayer(lyr, False)
        groupe.addLayer(lyr).setItemVisibilityChecked(i == 0)
    # Après l'ajout des couches : sinon QGIS reprend le SCR de la première (Lambert-93).
    # Pseudo-Mercator = même projection que la carte web.
    projet.setCrs(web)

    emprise = None
    for nom in cadrage:
        cible = projet.mapLayersByName(nom)[0]
        vers_web = QgsCoordinateTransform(cible.crs(), web, projet)
        rect = vers_web.transformBoundingBox(cible.extent())
        if emprise is None:
            emprise = rect
        else:
            emprise.combineExtentWith(rect)
    emprise.scale(1.08)
    projet.viewSettings().setDefaultViewExtent(QgsReferencedRectangle(emprise, web))
    projet.viewSettings().setPresetFullExtent(QgsReferencedRectangle(emprise, web))

    chemin = QGIS_DIR / f'{dossier}.qgz'
    projet.write(str(chemin))
    print(f'{chemin.name:32} {len(projet.mapLayers())} couches')


def main():
    app = demarrer_qgis()  # noqa: F841
    STYLES.mkdir(parents=True, exist_ok=True)
    for chapitre in CHAPITRES:
        creer_projet(*chapitre)
    QgsProject.instance().clear()


if __name__ == '__main__':
    main()
