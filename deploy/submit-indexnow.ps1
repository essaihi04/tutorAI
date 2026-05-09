# =============================================================
# Moalim — IndexNow submission
# Notifie instantanément Bing, Yandex, IndexNow.org de toutes les URLs
# Usage : powershell -ExecutionPolicy Bypass -File deploy/submit-indexnow.ps1
# =============================================================

$key      = "a7f3c89e2d4b16058fc91ab3e7d204cb"
$siteHost = "moalim.online"
$keyLoc   = "https://moalim.online/a7f3c89e2d4b16058fc91ab3e7d204cb.txt"

$urls = @(
  # Pages principales
  "https://moalim.online/",
  "https://moalim.online/inscription",
  "https://moalim.online/signup",
  "https://moalim.online/orientation",
  "https://moalim.online/bac-diagnostic",
  # Trust pages
  "https://moalim.online/about.html",
  "https://moalim.online/contact.html",
  "https://moalim.online/mentions-legales.html",
  # Blog index
  "https://moalim.online/blog/",
  # Articles phares
  "https://moalim.online/blog/predictions-bac-2026-maroc.html",
  "https://moalim.online/blog/examen-national-bac-maroc-2026.html",
  "https://moalim.online/blog/seuils-admission-grandes-ecoles-maroc-2026.html",
  "https://moalim.online/blog/annales-bac-svt-maroc-corrigees.html",
  "https://moalim.online/blog/annales-bac-physique-chimie-maroc.html",
  "https://moalim.online/blog/annales-bac-mathematiques-maroc.html",
  "https://moalim.online/blog/programme-officiel-2-bac-svt.html",
  "https://moalim.online/blog/comment-reussir-bac-maroc-3-mois.html",
  "https://moalim.online/blog/concours-ensa-encg-cnaem-guide.html",
  "https://moalim.online/blog/orientation-post-bac-maroc.html",
  "https://moalim.online/blog/calcul-moyenne-bac-maroc.html",
  # Articles longue-traîne
  "https://moalim.online/blog/seuil-fmp-rabat-casablanca-2026.html",
  "https://moalim.online/blog/correction-bac-svt-2025-session-normale.html",
  "https://moalim.online/blog/correction-bac-physique-2025-session-normale.html",
  "https://moalim.online/blog/calcul-moyenne-2-bac-svt.html",
  "https://moalim.online/blog/calcul-moyenne-2-bac-pc.html",
  "https://moalim.online/blog/seuil-ensa-agadir-tanger-oujda-2026.html",
  "https://moalim.online/blog/loi-hardy-weinberg-exercice-corrige-bac.html",
  "https://moalim.online/blog/dosage-acide-base-bac-methode.html",
  "https://moalim.online/blog/cycle-krebs-explication-bac-svt.html",
  "https://moalim.online/blog/subduction-svt-bac-schema-explication.html"
)

$body = @{
  host        = $siteHost
  key         = $key
  keyLocation = $keyLoc
  urlList     = $urls
} | ConvertTo-Json -Depth 3

$endpoints = @(
  "https://api.indexnow.org/IndexNow",
  "https://www.bing.com/IndexNow",
  "https://yandex.com/indexnow"
)

Write-Host ""
Write-Host "▶ Soumission IndexNow — $($urls.Count) URLs" -ForegroundColor Cyan
Write-Host ""

foreach ($ep in $endpoints) {
  try {
    Invoke-RestMethod -Uri $ep -Method POST -Body $body -ContentType "application/json; charset=utf-8" -ErrorAction Stop | Out-Null
    Write-Host "  ✅ $ep → OK" -ForegroundColor Green
  } catch {
    $code = $_.Exception.Response.StatusCode.value__
    if ($code -eq 200 -or $code -eq 202) {
      Write-Host "  ✅ $ep → $code" -ForegroundColor Green
    } else {
      Write-Host "  WARN $ep -> $($_.Exception.Message)" -ForegroundColor Yellow
    }
  }
}

Write-Host ""
Write-Host "✅ Soumission terminée. Les moteurs indexeront sous 24-48h." -ForegroundColor Green
Write-Host "   Vérifie dans Bing Webmaster Tools : https://www.bing.com/webmasters" -ForegroundColor Gray
Write-Host ""
