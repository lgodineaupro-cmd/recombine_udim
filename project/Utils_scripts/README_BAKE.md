# Documentation - Génération de la Présentation Bakée

## Problèmes Corrigés

### 1. Différences entre Preview VS Code et Présentation Bakée

**Problème identifié :**
- La page 2 "01. Mon Parcours" ne se déployait pas correctement dans le fichier baké
- Le titre avait un comportement différent
- Les hotspots n'étaient pas calés au bon endroit

**Solutions appliquées :**

#### A. Corrections dans `html/index.html`
1. **Stabilisation du layout de l'image PARCOURS :**
   - Ajout de `width:100%` sur le container `.transparent-backdrop`
   - Ajout de `loading="eager"` sur l'image pour forcer son chargement immédiat
   - Ajout de `aspect-ratio: auto` et `object-fit: contain` pour maintenir les proportions
   - Ajout de `z-index:100` et `pointer-events:none` sur le titre h2

2. **Correction des positions des hotspots :**
   - Ajout de `top:0; left:0; width:100%; height:100%` sur `.parcours-overlay` pour garantir qu'elle couvre exactement l'image

3. **Ajout d'un gestionnaire de chargement d'image :**
   - Fonction `ensureParcoursImageLoaded()` qui attend que l'image soit complètement chargée avant de positionner les hotspots
   - Force un recalcul du layout après le chargement de l'image

#### B. Améliorations dans `Utils_scripts/bake_presentation.py`

1. **Optimisation de la taille du fichier :**
   - Les vidéos > 10MB ne sont plus encodées en base64
   - Les vidéos lourdes restent en référence relative (`./assets/videos/...`)
   - Réduction de la taille finale de 55MB à ~31MB

2. **Ajout de CSS spécifique au fichier baké :**
   - CSS injecté automatiquement pour garantir que le layout de la page "Mon Parcours" soit stable
   - Force les positions et dimensions avec `!important` pour éviter les conflits

3. **Correction des chemins relatifs :**
   - Les chemins `../assets/` sont convertis en `./assets/` dans le fichier baké
   - Gestion correcte des ressources qui ne peuvent pas être encodées en base64

## Utilisation

### Générer la présentation finale

```bash
# Depuis la racine du projet
python Utils_scripts/bake_presentation.py
```

### Générer avec compression préalable (recommandé)

```bash
# Utiliser le script batch qui fait tout automatiquement
.\Utils_scripts\generer_presentation.bat
```

Ce script :
1. Compresse les images (crée des backups dans `assets/images_backup/`)
2. Compresse les vidéos (crée des backups dans `assets/videos_backup/`)
3. Génère la présentation finale avec les ressources optimisées

## Résultat

Le fichier `presentation_finale.html` généré :
- ✅ Est identique visuellement à la preview VS Code
- ✅ Contient toutes les images encodées en base64
- ✅ Conserve les vidéos en références externes (pour éviter un fichier trop lourd)
- ✅ Fonctionne en mode standalone (pas besoin de serveur web)
- ✅ Respecte exactement le positionnement des hotspots sur la page "Mon Parcours"
- ✅ Le titre "01. Mon Parcours" est correctement positionné

## Notes Importantes

1. **Vidéos :** Les fichiers vidéo de plus de 10MB ne sont PAS inclus en base64. Assurez-vous que le dossier `assets/videos/` est présent à côté du fichier `presentation_finale.html` lors de la distribution.

2. **Taille du fichier :** Le fichier final fait environ 31MB à cause des images en base64. C'est normal.

3. **Compatibilité :** Le fichier fonctionne dans tous les navigateurs modernes (Chrome, Firefox, Edge, Safari).

4. **Preview VS Code :** Pour voir la présentation, ouvrez `html/index.html` avec "Live Preview" dans VS Code, ou utilisez un serveur web local.

## Dépannage

### La vidéo ne se charge pas dans le fichier baké
**Solution :** Vérifiez que le dossier `assets/videos/` existe et contient le fichier `.mp4`

### Les hotspots sont mal positionnés
**Solution :** Vérifiez que vous avez régénéré le fichier avec la dernière version du script

### Le fichier est trop volumineux
**Solution :** Réduisez la taille des images avec `python Utils_scripts/compress_images.py` avant de générer
