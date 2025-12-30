@echo off
REM Script pour créer un package complet de la présentation (HTML + assets)
REM Ce package peut être copié sur n'importe quel PC

echo === Création du package de présentation ===
echo.

REM Se placer à la racine du projet
cd /d %~dp0..

REM Créer le dossier de package
if exist presentation_package rmdir /s /q presentation_package
mkdir presentation_package

REM Générer la présentation bakée
echo 1. Génération de la présentation bakée...
python Utils_scripts/bake_presentation.py
if %ERRORLEVEL% neq 0 (
    echo Erreur lors de la génération !
    pause
    exit /b 1
)

REM Copier le fichier HTML
echo 2. Copie du fichier HTML...
copy presentation_finale.html presentation_package\

REM Copier le dossier assets (pour les vidéos)
echo 3. Copie des ressources assets...
xcopy /E /I /Y assets presentation_package\assets

echo.
echo === Package créé avec succès ! ===
echo.
echo Le dossier "presentation_package" contient :
echo - presentation_finale.html (avec polices et images en base64)
echo - assets/ (avec les vidéos)
echo.
echo Tu peux copier ce dossier sur n'importe quel PC.
echo Ouvre "presentation_finale.html" pour lancer la présentation.
echo.
pause
