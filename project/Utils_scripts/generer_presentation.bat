@echo off
echo --- Lancement de la compression des images ---
python Utils_scripts/compress_images.py

echo --- Lancement de la compression des videos ---
python Utils_scripts/compress_videos.py

echo --- Lancement de la creation de la presentation finale ---
python Utils_scripts/bake_presentation.py

echo --- TERMINE ! ---
pause
