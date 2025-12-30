import os
import shutil
import sys

# On essaie d'importer moviepy
try:
    from moviepy.editor import VideoFileClip
except ImportError:
    try:
        from moviepy import VideoFileClip
    except ImportError:
        print("ERREUR: La librairie 'moviepy' n'est pas installée.")
        print("Installation automatique...")
        os.system(f"{sys.executable} -m pip install moviepy")
        try:
            from moviepy.editor import VideoFileClip
        except ImportError:
            try:
                from moviepy import VideoFileClip
            except ImportError:
                print("Echec de l'installation. Veuillez installer moviepy manuellement : pip install moviepy")
                sys.exit(1)

# Configuration
VIDEO_DIR = 'assets/videos'
BACKUP_DIR = 'assets/videos_backup'
TARGET_HEIGHT = 480   # 480p
BITRATE = "500k"      # 500 kbps

def compress_videos():
    if not os.path.exists(VIDEO_DIR):
        print(f"Dossier {VIDEO_DIR} introuvable.")
        return

    # 1. Création du backup
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
        print(f"Dossier de sauvegarde créé : {BACKUP_DIR}")

    print(f"--- Démarrage de l'optimisation vidéo dans {VIDEO_DIR} ---")
    print(f"Cible : {TARGET_HEIGHT}p @ {BITRATE}")
    
    files = [f for f in os.listdir(VIDEO_DIR) if f.lower().endswith(('.mp4', '.mov', '.avi', '.mkv'))]
    
    total_saved = 0

    for filename in files:
        filepath = os.path.join(VIDEO_DIR, filename)
        backup_path = os.path.join(BACKUP_DIR, filename)
        
        # Sauvegarde de l'original
        if not os.path.exists(backup_path):
            shutil.copy2(filepath, backup_path)
        
        original_size = os.path.getsize(filepath)
        
        try:
            print(f"Traitement de {filename}...")
            # Chargement du clip
            clip = VideoFileClip(filepath)
            
            # Redimensionnement si plus grand que la cible
            if clip.h > TARGET_HEIGHT:
                print(f"  Redimensionnement hauteur: {clip.h} -> {TARGET_HEIGHT}")
                
                # Gestion des versions MoviePy (1.x vs 2.x)
                if hasattr(clip, 'resized'):
                    # MoviePy 2.x
                    clip = clip.resized(height=TARGET_HEIGHT)
                elif hasattr(clip, 'resize'):
                    # MoviePy 1.x
                    clip = clip.resize(height=TARGET_HEIGHT)
                else:
                    print("  ⚠️ Impossible de redimensionner : méthode inconnue.")
            
            # Fichier temporaire
            temp_output = os.path.join(VIDEO_DIR, f"temp_{filename}")
            
            # Écriture du fichier compressé
            # Note: 'verbose' a été supprimé dans MoviePy 2.0
            clip.write_videofile(
                temp_output, 
                bitrate=BITRATE, 
                audio=False, 
                codec='libx264', 
                preset='slow', 
                logger=None
            )
            
            clip.close()
            
            # Vérification et remplacement
            if os.path.exists(temp_output):
                new_size = os.path.getsize(temp_output)
                saved = original_size - new_size
                
                if saved > 0:
                    os.replace(temp_output, filepath)
                    total_saved += saved
                    print(f"✅ {filename}: {original_size/1024/1024:.2f} Mo -> {new_size/1024/1024:.2f} Mo (Gain: {saved/1024/1024:.2f} Mo)")
                else:
                    print(f"➖ {filename}: Pas de gain significatif. On garde l'original.")
                    os.remove(temp_output)

        except Exception as e:
            print(f"❌ Erreur sur {filename}: {e}")
            temp_path = os.path.join(VIDEO_DIR, f"temp_{filename}")
            if os.path.exists(temp_path):
                 os.remove(temp_path)

    print(f"\n--- TERMINÉ ---")
    print(f"Espace total économisé : {total_saved/1024/1024:.2f} Mo")
    print(f"Les originaux sont dans : {BACKUP_DIR}")

if __name__ == "__main__":
    compress_videos()
