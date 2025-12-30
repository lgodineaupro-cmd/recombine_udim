import os
import shutil
from PIL import Image

# Configuration
IMAGE_DIR = 'assets/images'
BACKUP_DIR = 'assets/images_backup'
MAX_WIDTH = 800  # Largeur max réduite pour alléger le fichier final
JPEG_QUALITY = 80 # Qualité JPEG (0-100)

def compress_images():
    # 1. Création du backup
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
        print(f"Dossier de sauvegarde créé : {BACKUP_DIR}")

    print(f"--- Démarrage de l'optimisation dans {IMAGE_DIR} ---")
    
    files = [f for f in os.listdir(IMAGE_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    total_saved = 0

    for filename in files:
        filepath = os.path.join(IMAGE_DIR, filename)
        backup_path = os.path.join(BACKUP_DIR, filename)
        
        # Sauvegarde de l'original si pas déjà fait
        if not os.path.exists(backup_path):
            shutil.copy2(filepath, backup_path)
        
        original_size = os.path.getsize(filepath)
        
        try:
            with Image.open(filepath) as img:
                # Redimensionnement si trop grand
                if img.width > MAX_WIDTH:
                    ratio = MAX_WIDTH / img.width
                    new_height = int(img.height * ratio)
                    img = img.resize((MAX_WIDTH, new_height), Image.Resampling.LANCZOS)
                    print(f"Redimensionné : {filename} -> {MAX_WIDTH}x{new_height}")

                # Sauvegarde optimisée
                if filename.lower().endswith('.png'):
                    # Pour PNG, on optimise et on réduit les couleurs si possible pour gagner de la place
                    # (L'optimisation PNG de base de PIL est limitée, mais ça aide)
                    img.save(filepath, optimize=True)
                elif filename.lower().endswith(('.jpg', '.jpeg')):
                    # Pour JPEG, on joue sur la qualité
                    img.save(filepath, quality=JPEG_QUALITY, optimize=True)
                
                new_size = os.path.getsize(filepath)
                saved = original_size - new_size
                total_saved += saved
                
                if saved > 0:
                    print(f"✅ {filename}: {original_size/1024/1024:.2f} Mo -> {new_size/1024/1024:.2f} Mo (Gain: {saved/1024/1024:.2f} Mo)")
                else:
                    print(f"➖ {filename}: Pas de gain significatif")

        except Exception as e:
            print(f"❌ Erreur sur {filename}: {e}")

    print(f"\n--- TERMINÉ ---")
    print(f"Espace total économisé : {total_saved/1024/1024:.2f} Mo")
    print(f"Les originaux sont dans : {BACKUP_DIR}")

if __name__ == "__main__":
    compress_images()
