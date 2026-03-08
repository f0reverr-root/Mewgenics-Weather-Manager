$ErrorActionPreference = 'Stop'

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

$appName = 'MewgenicsWeatherTool'
$entryScript = 'mewgenics_weather_tool.py'
$iconPath = 'icon.ico'
$releaseRoot = Join-Path $scriptDir 'release'
$distRoot = Join-Path $scriptDir 'dist'
$buildRoot = Join-Path $scriptDir 'build'

if (-not (Test-Path $entryScript)) {
    throw "Cannot find $entryScript in $scriptDir"
}

$pythonExe = 'C:/Python39/python.exe'
Write-Host "Using Python: $pythonExe"

Write-Host 'Cleaning old build outputs...'
Remove-Item -Recurse -Force $buildRoot,$distRoot,$releaseRoot -ErrorAction SilentlyContinue

$pyiArgs = @(
    '-m','PyInstaller',
    '--noconfirm',
    '--clean',
    '--windowed',
    '--onedir',
    '--noupx',
    '--name', $appName
)

if (Test-Path $iconPath) {
    $pyiArgs += @('--icon', $iconPath)
}

$pyiArgs += $entryScript

Write-Host 'Building onedir package...'
& $pythonExe @pyiArgs
if ($LASTEXITCODE -ne 0) {
    throw 'PyInstaller build failed.'
}

Write-Host 'Preparing release ZIP...'
New-Item -ItemType Directory -Path $releaseRoot | Out-Null
$zipPath = Join-Path $releaseRoot ("$appName.zip")
Compress-Archive -Path (Join-Path $distRoot "$appName\*") -DestinationPath $zipPath -Force

$hashLine = (Get-FileHash -Algorithm SHA256 $zipPath).Hash
$hashFile = Join-Path $releaseRoot 'SHA256.txt'
"$hashLine  $appName.zip" | Set-Content -Encoding ASCII $hashFile

Write-Host ''
Write-Host 'Release complete:' -ForegroundColor Green
Write-Host "  ZIP:  $zipPath"
Write-Host "  Hash: $hashLine"
Write-Host "  Hash file: $hashFile"
