# Creates topo_architect/.env for Ollama Cloud (run once)
$envPath = Join-Path $PSScriptRoot ".env"
if (Test-Path $envPath) {
    Write-Host ".env already exists: $envPath"
    exit 0
}
$key = Read-Host "Paste your OLLAMA_API_KEY"
@"
OLLAMA_API_KEY=$key
OLLAMA_BASE_URL=https://ollama.com
OLLAMA_TIMEOUT=30
"@ | Set-Content -Path $envPath -Encoding UTF8
Write-Host "Created $envPath — restart uvicorn (API server)."
