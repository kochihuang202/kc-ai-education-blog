# Tooling Log

Date: 2026-06-01

Installed tools:

- `Microsoft.WinGet.Client` PowerShell module `1.12.440`, installed for the current user to bootstrap winget.
- Windows Package Manager / winget `v1.28.240`, installed through `Repair-WinGetPackageManager`.
- Git for Windows `2.54.0`, installed with winget package `Git.Git`.
- GitHub CLI `2.93.0`, installed with winget package `GitHub.cli`.

Notes:

- PowerShell script execution is restricted on this machine, so project npm scripts run Astro through `scripts/astro.mjs` with `ASTRO_TELEMETRY_DISABLED=1`.
- `npm install` needed one-time `--strict-ssl=false` because npm registry access hit `SELF_SIGNED_CERT_IN_CHAIN`.
- Current shell sessions may not see new PATH entries until restarted. Verified executable paths:
  - `C:\Program Files\Git\cmd\git.exe`
  - `C:\Users\ji3cp\AppData\Local\Microsoft\WinGet\Packages\GitHub.cli_Microsoft.Winget.Source_8wekyb3d8bbwe\bin\gh.exe`
