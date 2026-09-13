# Libere les ports du dev local (frontend Vite + backend uvicorn)
param([int[]]$Ports = @(5173, 8000))

foreach ($port in $Ports) {
    $lines = netstat -ano | Select-String ":$port\s" | Select-String "LISTENING"
    foreach ($line in $lines) {
        $procId = ($line -split '\s+')[-1]
        if ($procId -match '^\d+$' -and $procId -ne '0') {
            try {
                Stop-Process -Id $procId -Force -ErrorAction Stop
                Write-Host "Port $port libere (PID $procId)"
            } catch {
                Write-Host "Port $port : PID $procId deja arrete"
            }
        }
    }
}
