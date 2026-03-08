# Mewgenics Weather Manager

Simple Windows GUI tool to enable/disable Mewgenics weather effects and install a generated `weather.gon` into your game folder.

## Installation
Download the release ZIP, extract it to any folder, then run `MewgenicsWeatherTool.exe`.

If needed for your install location, run as administrator:
- Right click the EXE > Run as administrator
- Or EXE > Properties > Compatibility > Run this program as an administrator

## How to Use
- Toggle weather/disaster/creature effects on or off
- Click `Install to Game`
- Choose your game root directory
- Launch the game normally

## Uninstall
- Delete `data/weather.gon` from your game folder
- Delete `MewgenicsWeatherTool.exe` from where you extracted it

## Notes
THE MAP UI WILL STILL SHOW THE WEATHER/DISASTER/CREATURE EFFECT ICON AT THE TOP RIGHT CORNER BUT ONCE YOU LOAD INTO A FIGHT YOU WILL SEE IT'S NOT ACTIVE

## Build (Windows)
```powershell
PowerShell -ExecutionPolicy Bypass -File .\build_release.ps1
```

## Release artifacts
- `release/MewgenicsWeatherTool.zip`
- `release/SHA256.txt`
- `release/RELEASE_NOTES_v1.0.0.md`

## Verify release integrity
```powershell
certutil -hashfile .\release\MewgenicsWeatherTool.zip SHA256
```
Compare with `release/SHA256.txt`.
