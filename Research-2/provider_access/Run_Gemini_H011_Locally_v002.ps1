# Research #2 — user-run Gemini H011 nondecisive credential entry
# This script does NOT contain a key. Never send a key in chat.
$ErrorActionPreference = "Stop"
$root = Join-Path $env:USERPROFILE "Research2"
$probe = Join-Path $root "gemini_h011_nondecisive_v002.py"
$secretPath = Join-Path $env:LOCALAPPDATA "Research2_gemini_authkey.tmp"
if (-not (Test-Path $probe)) { throw "Research2 Gemini sentinel not found" }
$secure = Read-Host "Paste temporary Gemini API key privately" -AsSecureString
$ptr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secure)
try {
    $key = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($ptr)
    if ([string]::IsNullOrWhiteSpace($key)) { throw "Empty key" }
    [System.IO.File]::WriteAllText($secretPath, $key.Trim(), (New-Object System.Text.UTF8Encoding($false)))
    $key = $null
    & py -3.12 $probe
    if ($LASTEXITCODE -ne 0) { throw "Gemini sentinel Python process failed" }
} finally {
    [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($ptr)
    $key = $null
    $secure.Dispose()
    if (Test-Path $secretPath) { Remove-Item -LiteralPath $secretPath -Force }
}
