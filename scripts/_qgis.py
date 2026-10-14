"""Démarre QGIS sans interface pour les scripts du projet (à lancer via lancer.bat)."""
import os
import sys
from pathlib import Path

from qgis.core import QgsApplication

RACINE = Path(__file__).resolve().parent.parent
DONNEES = RACINE / 'donnees'
REFERENTIEL = DONNEES / 'referentiel.gpkg'
PROJET_GPKG = DONNEES / 'smavd_50ans.gpkg'


def demarrer_qgis():
    """Initialise QGIS et Processing ; garder la valeur renvoyée tant que le script tourne."""
    QgsApplication.setPrefixPath(os.environ['QGIS_PREFIX_PATH'], True)
    app = QgsApplication([], False)
    app.initQgis()
    sys.path.append(os.path.join(QgsApplication.prefixPath(), 'python', 'plugins'))
    from processing.core.Processing import Processing
    Processing.initialize()
    return app
