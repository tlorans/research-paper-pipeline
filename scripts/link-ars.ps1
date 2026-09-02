# Windows wrapper. Prefer: uv run python scripts/link_ars.py
$ErrorActionPreference = "Stop"
$Script = Join-Path $PSScriptRoot "link_ars.py"
if (Get-Command uv -ErrorAction SilentlyContinue) {
    uv run python $Script @args
} else {
    python $Script @args
}
