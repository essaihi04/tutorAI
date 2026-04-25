# Script PowerShell pour tester et corriger la connectivité Supabase
# Exécuter en tant qu'administrateur

Write-Host "=== Test de connectivité Supabase ===" -ForegroundColor Cyan

# Test 1: Ping Google (vérifier Internet)
Write-Host "`n1. Test de connexion Internet..." -ForegroundColor Yellow
$pingGoogle = Test-Connection -ComputerName google.com -Count 2 -Quiet
if ($pingGoogle) {
    Write-Host "   ✓ Connexion Internet OK" -ForegroundColor Green
} else {
    Write-Host "   ✗ Pas de connexion Internet" -ForegroundColor Red
    exit 1
}

# Test 2: Résolution DNS Supabase
Write-Host "`n2. Test de résolution DNS Supabase..." -ForegroundColor Yellow
$supabaseHost = "db.yzvlmulpqnovduqhhtjf.supabase.co"

try {
    $dnsResult = Resolve-DnsName -Name $supabaseHost -ErrorAction Stop
    Write-Host "   ✓ DNS résolu: $($dnsResult.IPAddress)" -ForegroundColor Green
} catch {
    Write-Host "   ✗ Échec de résolution DNS" -ForegroundColor Red
    Write-Host "`n   Tentative avec DNS Google (8.8.8.8)..." -ForegroundColor Yellow
    
    try {
        $dnsResult = Resolve-DnsName -Name $supabaseHost -Server 8.8.8.8 -ErrorAction Stop
        Write-Host "   ✓ DNS résolu avec Google DNS: $($dnsResult.IPAddress)" -ForegroundColor Green
        
        Write-Host "`n   💡 Solution: Changez vos serveurs DNS pour utiliser Google DNS" -ForegroundColor Cyan
        Write-Host "      DNS Préféré: 8.8.8.8" -ForegroundColor White
        Write-Host "      DNS Auxiliaire: 8.8.4.4" -ForegroundColor White
    } catch {
        Write-Host "   ✗ Échec même avec Google DNS" -ForegroundColor Red
    }
}

# Test 3: Test de port
Write-Host "`n3. Test de connectivité port 5432..." -ForegroundColor Yellow
$portTest = Test-NetConnection -ComputerName $supabaseHost -Port 5432 -WarningAction SilentlyContinue

if ($portTest.TcpTestSucceeded) {
    Write-Host "   ✓ Port 5432 accessible" -ForegroundColor Green
} else {
    Write-Host "   ✗ Port 5432 non accessible" -ForegroundColor Red
    Write-Host "   Raisons possibles:" -ForegroundColor Yellow
    Write-Host "   - Pare-feu Windows bloque la connexion" -ForegroundColor White
    Write-Host "   - Antivirus bloque la connexion" -ForegroundColor White
    Write-Host "   - Problème réseau/FAI" -ForegroundColor White
}

Write-Host "`n=== Recommandations ===" -ForegroundColor Cyan
Write-Host "1. Utilisez Docker Desktop avec PostgreSQL local (RECOMMANDÉ)" -ForegroundColor White
Write-Host "2. Changez vos DNS pour Google DNS (8.8.8.8, 8.8.4.4)" -ForegroundColor White
Write-Host "3. Désactivez temporairement votre antivirus/pare-feu" -ForegroundColor White
Write-Host "4. Essayez avec un VPN" -ForegroundColor White
