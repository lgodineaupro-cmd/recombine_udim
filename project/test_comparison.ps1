# Script de Test - Comparaison Preview vs Baké
# Usage: .\test_comparison.ps1

Write-Host "=== TEST DE COMPARAISON ===" -ForegroundColor Cyan
Write-Host ""

# Vérifier que le fichier baké existe
if (-not (Test-Path "presentation_finale.html")) {
    Write-Host "❌ Le fichier 'presentation_finale.html' n'existe pas." -ForegroundColor Red
    Write-Host "   Générez-le d'abord avec: python Utils_scripts/bake_presentation.py" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Fichier baké trouvé" -ForegroundColor Green

# Obtenir les chemins complets
$htmlPath = Join-Path $PSScriptRoot "html\index.html" | Resolve-Path
$bakedPath = Join-Path $PSScriptRoot "presentation_finale.html" | Resolve-Path

Write-Host ""
Write-Host "📁 Fichier source : $htmlPath" -ForegroundColor Gray
Write-Host "📁 Fichier baké   : $bakedPath" -ForegroundColor Gray
Write-Host ""

# Vérifier la taille du fichier baké
$bakedSize = (Get-Item $bakedPath).Length / 1MB
Write-Host "📊 Taille du fichier baké : $([math]::Round($bakedSize, 2)) MB" -ForegroundColor Cyan

if ($bakedSize -gt 50) {
    Write-Host "⚠️  Attention : Le fichier est très volumineux (> 50MB)" -ForegroundColor Yellow
    Write-Host "   Cela peut causer des lenteurs de chargement." -ForegroundColor Yellow
} elseif ($bakedSize -gt 30) {
    Write-Host "ℹ️  Le fichier est de taille moyenne (30-50MB)" -ForegroundColor Yellow
} else {
    Write-Host "✅ Taille du fichier optimale (< 30MB)" -ForegroundColor Green
}

Write-Host ""
Write-Host "🚀 Instructions de test :" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. La preview VS Code va s'ouvrir (source)" -ForegroundColor White
Write-Host "2. Le fichier baké va s'ouvrir dans votre navigateur par défaut" -ForegroundColor White
Write-Host "3. Naviguez vers la page 2 '01. Mon Parcours' dans les DEUX fenêtres" -ForegroundColor White
Write-Host "4. Comparez visuellement :" -ForegroundColor White
Write-Host "   - Position du titre '01. Mon Parcours'" -ForegroundColor Gray
Write-Host "   - Position des 4 hotspots (ARTFX, Canada, Ecosse, France)" -ForegroundColor Gray
Write-Host "   - Comportement au survol" -ForegroundColor Gray
Write-Host ""

$response = Read-Host "Continuer ? (O/N)"
if ($response -ne 'O' -and $response -ne 'o') {
    Write-Host "Test annulé." -ForegroundColor Yellow
    exit 0
}

Write-Host ""
Write-Host "🌐 Ouverture des fichiers..." -ForegroundColor Cyan

# Ouvrir le fichier source avec Live Preview (si extension installée)
# Sinon, ouvrir dans le navigateur par défaut
Write-Host "   → Ouverture de la preview (source)..." -ForegroundColor Gray
code $htmlPath

# Attendre 2 secondes
Start-Sleep -Seconds 2

# Ouvrir le fichier baké dans le navigateur par défaut
Write-Host "   → Ouverture du fichier baké..." -ForegroundColor Gray
Start-Process $bakedPath

Write-Host ""
Write-Host "✅ Les deux versions sont ouvertes !" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Checklist de vérification :" -ForegroundColor Cyan
Write-Host "   [ ] Le titre '01. Mon Parcours' est à la même position" -ForegroundColor White
Write-Host "   [ ] Les hotspots ARTFX, Canada, Ecosse, France sont bien positionnés" -ForegroundColor White
Write-Host "   [ ] Les interactions (survol, click) fonctionnent de la même façon" -ForegroundColor White
Write-Host "   [ ] L'image PARCOURS.png a la même taille" -ForegroundColor White
Write-Host ""
Write-Host "Si tout est ✅, les corrections sont réussies !" -ForegroundColor Green
Write-Host ""
