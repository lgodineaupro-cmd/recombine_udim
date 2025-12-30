# Presentation Brassart

Version statique de la présentation Reveal.js.

Structure principale:

- `html/` : pages HTML (point d'entrée `html/index.html`)
- `assets/` : images, vidéos
- `reference/typo` : polices

But de ce dépôt
- Permettre le contrôle de version et la collaboration via GitHub
- Déployer automatiquement la version statique située dans `html/` sur GitHub Pages

Ce que j'ai ajouté
- `.gitignore` — ignore fichiers locaux
- `LICENSE` — MIT
- `.github/workflows/pages.yml` — workflow GitHub Actions pour déployer `html/` sur GitHub Pages (branche `gh-pages`)
- `publish.ps1` — script PowerShell d'initialisation et push pour créer le remote et pousser la branche `main`

Comment publier (rapide)

1. Créez un nouveau repository sur GitHub (vide) — notez l'URL, par ex. `https://github.com/USERNAME/REPO.git`.
2. Depuis la racine du projet (`presentation_brassart`) lancez le script PowerShell pour initialiser et pousser :

```powershell
.\publish.ps1
```

3. Sur GitHub, activez GitHub Pages sur la branche `gh-pages` (le workflow CI crée automatiquement la branche `gh-pages` après un push sur `main`).

Remarques
- Le script `publish.ps1` vous demandera l'URL du repo distant. Vous devez disposer des droits pour pousser vers ce repo.
- Le workflow utilise le token `GITHUB_TOKEN` fourni par Actions; vérifiez les permissions Pages si nécessaire.

Si vous voulez, je peux:
- exécuter localement les commandes git (si vous m'en donnez l'autorisation et accès), ou
- vous guider pas à pas pour créer le repo et pousser.
Presentation Brassart - structure initiale

Structure créée:
- html/: page principale `index.html` (slides)
- css/: `style.css` pour styles et animations
- js/: `script.js` pour la navigation clavier/boutons
- assets/images, assets/videos: dossiers pour vos médias
- reference/: page de références/inspirations

Comment utiliser:
1. Ouvrez `presentation_brassart/html/index.html` dans votre navigateur.
2. Remplacez les fichiers `../assets/images/placeholder.jpg` et `../assets/videos/placeholder.mp4` par vos médias.
3. Éditez `../css/style.css` pour personnaliser couleurs/animations.
