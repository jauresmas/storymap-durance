"""
Intègre un export qgis2web dans la StoryMap.

1. Dans qgis2web, exporter vers le dossier web/exports/ : qgis2web y crée un
   sous-dossier qgis2web_AAAA_MM_JJ-HH_MM_SS...
2. Lancer, avec le numéro du chapitre :
       scripts\\lancer.bat 04_integrer_export.py 01
   Le dernier export est copié dans web/cartes/01_avant_1976/ (le contenu
   précédent est remplacé), puis reçoit le style commun web/commun/custom.css
   et le script web/commun/custom.js.

Ne modifie jamais les fichiers d'un export à la main : mets les retouches dans
web/commun/, elles s'appliquent à toutes les cartes et survivent aux ré-exports.
"""
import shutil
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
EXPORTS = RACINE / 'web' / 'exports'
CARTES = RACINE / 'web' / 'cartes'
AJOUT = ('<link rel="stylesheet" href="../../commun/custom.css">\n'
         '<script src="../../commun/custom.js"></script>\n')


def main():
    if len(sys.argv) != 2:
        sys.exit('Usage : lancer.bat 04_integrer_export.py <chapitre>   (ex. 01)')
    chapitres = sorted(CARTES.glob(f'{sys.argv[1]}*'))
    if len(chapitres) != 1:
        sys.exit(f'Chapitre introuvable ou ambigu : {sys.argv[1]} '
                 f'(dossiers : {", ".join(p.name for p in CARTES.iterdir())})')
    exports = sorted(EXPORTS.glob('qgis2web_*'), key=lambda p: p.stat().st_mtime)
    if not exports:
        sys.exit(f'Aucun export qgis2web dans {EXPORTS}')

    source, cible = exports[-1], chapitres[0]
    shutil.rmtree(cible)
    shutil.copytree(source, cible)
    index = cible / 'index.html'
    html = index.read_text(encoding='utf-8')
    if 'commun/custom.css' not in html:
        html = html.replace('</body>', AJOUT + '</body>', 1)
        index.write_text(html, encoding='utf-8')
    print(f'{source.name}  ->  web/cartes/{cible.name}/')


if __name__ == '__main__':
    main()
