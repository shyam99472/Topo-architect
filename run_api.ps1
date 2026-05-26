# Start FastAPI with Ollama settings from topo_architect/.env
$Root = Split-Path $PSScriptRoot -Parent
Set-Location $Root
$env:PYTHONPATH = $Root

$envFile = Join-Path $PSScriptRoot ".env"
if (Test-Path $envFile) {
    Get-Content $envFile | ForEach-Object {
        $line = $_.Trim()
        if (-not $line -or $line.StartsWith("#")) { return }
        if ($line -match "^\s*export\s+(.+)$") { $line = $Matches[1] }
        if ($line -match "^([^=]+)=(.*)$") {
            $name = $Matches[1].Trim()
            $value = $Matches[2].Trim().Trim('"').Trim("'")
            Set-Item -Path "env:$name" -Value $value
        }
    }
    Write-Host "Loaded $envFile"
    Write-Host "OLLAMA_BASE_URL = $env:OLLAMA_BASE_URL"
    Write-Host "OLLAMA_API_KEY  = set ($($env:OLLAMA_API_KEY.Length) chars)"
} else {
    Write-Warning "Missing $envFile — copy from .env.example"
}

& "$PSScriptRoot\.venv\Scripts\python.exe" -m uvicorn topo_architect.app.main:app --reload --host 127.0.0.1 --port 8000
