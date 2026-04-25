$pids = @(18028, 9044)
foreach ($p in $pids) {
    try { Stop-Process -Id $p -Force -ErrorAction Stop; Write-Host "Killed $p" } catch { Write-Host "Already dead $p" }
}
