<#
  publish.ps1
  Interactive script to initialize a local git repo and optionally push to GitHub.
  Usage: Open PowerShell at the project root and run: .\publish.ps1

  Notes:
  - This script does not store tokens. It will ask for the remote repository URL.
  - You may need a credential helper or PAT to authenticate when pushing.
#>

param()

Write-Host "== Initialize local git repository and create initial commit ==`n"

if (-not (Test-Path ".git")) {
    git init
    git checkout -b main
    Write-Host "Git repository initialized (branch 'main')."
} else {
    Write-Host "A git repository already exists here."
}

git add -A
try {
    git commit -m "Initial commit: add presentation files"
} catch {
    Write-Host "No changes to commit or initial commit already present."
}

$remote = Read-Host "Enter the GitHub repo URL (e.g. https://github.com/USERNAME/REPO.git) or press Enter to skip"
if ($remote -and $remote.Trim() -ne "") {
    try {
        git remote add origin $remote
        Write-Host "Remote 'origin' added: $remote"
    } catch {
        Write-Host "Remote already exists - updating URL."
        git remote set-url origin $remote
    }

    Write-Host "Pushing to 'main' (you may be prompted to authenticate)..."
    git push -u origin main
    Write-Host "Push complete (check GitHub)."
} else {
    Write-Host "No remote provided - you can add one later with: git remote add origin https://github.com/USERNAME/REPO.git"
}

Write-Host "
Next recommended steps:
- Create a remote repository on GitHub if you have not already.
- Enable GitHub Pages settings if you want the site served from the 'gh-pages' branch.
- If needed, create a Personal Access Token and add it as a secret for CI deployments.
"
