# Notify IndexNow (Bing, Yandex, Seznam) of new/updated URLs
# Usage : .\scripts\notify_indexnow.ps1 "https://moalim.online/blog/article1.html" "https://moalim.online/blog/article2.html"

param(
    [Parameter(Mandatory=$true, ValueFromRemainingArguments=$true)]
    [string[]]$Urls
)

$key = "a7f3c89e2d4b16058fc91ab3e7d204cb"
$keyLocation = "https://moalim.online/$key.txt"

$body = @{
    host        = "moalim.online"
    key         = $key
    keyLocation = $keyLocation
    urlList     = $Urls
} | ConvertTo-Json -Depth 3

Write-Host "Sending IndexNow notification for $($Urls.Count) URL(s)..." -ForegroundColor Cyan

try {
    $response = Invoke-RestMethod `
        -Uri "https://api.indexnow.org/IndexNow" `
        -Method Post `
        -Body $body `
        -ContentType "application/json; charset=utf-8"
    Write-Host "IndexNow accepted the request." -ForegroundColor Green
} catch {
    Write-Host "IndexNow error: $($_.Exception.Message)" -ForegroundColor Red
    if ($_.Exception.Response) {
        Write-Host "HTTP $([int]$_.Exception.Response.StatusCode) $($_.Exception.Response.StatusDescription)"
    }
}
