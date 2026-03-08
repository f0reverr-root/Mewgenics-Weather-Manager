# GitHub Release Checklist (No Code Signing)

1. Create a public GitHub repository (for example: `mewgenics-weather-tool`).
2. Upload these source files at minimum:
   - `mewgenics_weather_tool.py`
   - `icon.ico`
   - `build_release.ps1`
3. Commit and push to `main`.
4. In GitHub, create a release tag (for example: `v1.0.0`).
5. Upload release artifact:
   - `release/MewgenicsWeatherTool.zip`
6. Paste SHA256 from `release/SHA256.txt` into release notes.
7. Keep GitHub's auto-generated `Source code (zip)` and `Source code (tar.gz)` attached.
8. On your mod page, link to:
   - Repository URL
   - Specific release URL
   - SHA256 line from release notes

## Suggested Release Notes Template

Copy from `RELEASE_NOTES_TEMPLATE.md`.
