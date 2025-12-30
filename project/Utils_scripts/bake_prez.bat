@echo off
REM Se placer à la racine du projet (là où se trouve ce .bat)
cd /d %~dp0..
REM Lancer le script Python depuis la racine
python Utils_scripts/bake_presentation.py
if %ERRORLEVEL% neq 0 (
    echo Erreur lors de la génération de la présentation bakée.
    pause
    exit /b 1
)
echo --- Présentation bakée générée avec succès ! ---
pause
