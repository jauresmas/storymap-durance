@echo off
REM Lance un script Python du projet avec le Python de QGIS.
REM Exemples : scripts\lancer.bat 01_telecharger_donnees.py
REM            scripts\lancer.bat 04_integrer_export.py 01
REM Adapter QGIS si QGIS est installe ailleurs.
set QGIS=C:\Program Files\QGIS 3.34.12
call "%QGIS%\bin\python-qgis-ltr.bat" "%~dp0%~1" %2 %3 %4
