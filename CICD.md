# CI/CD Guide — Viral Load Calculator

This document explains how the build, test, and release pipelines work for
this project, and how you (the maintainer) should interact with them.

---

## Overview

The project ships installers for two platforms:

| Platform | Format       | Output file                          |
|----------|--------------|--------------------------------------|
| Windows  | Inno Setup   | `ViralLoadCalculator_Setup.exe`      |
| Linux    | AppImage     | `ViralLoadCalculator-x86_64.AppImage`|

Both are built by **GitHub Actions** and attached to a **GitHub Release**
when you push a version tag.

---

## Branching Strategy

The repository uses a three-tier flow:

```
feature/*  ──┐
             ├──►  test  ──►  master (with tag)  ──►  GitHub Release
hotfix/*   ──┘
```

- **`master`** — production. This is the only branch from which you cut
  version tags. Tags here trigger the release pipeline.
- **`test`** — post-production / staging. Push improvements here first.
  Every push to `test` runs the validation pipeline (lint + builds on
  both platforms) but does **not** publish anything. This is your
  pre-flight check.
- **`feature/*`** — short-lived branches. Branch off `test`, do your work,
  open a PR back into `test`. Hotfixes can branch off `master` and PR
  directly back.

### Recommended workflow for applying improvements

1. Branch from `test`:
   ```bash
   git checkout test
   git pull
   git checkout -b feature/my-improvement
   ```
2. Make your changes, commit, push, and open a PR into `test`.
3. Watch the **CI (Test)** workflow run on your PR. Both the Linux and
   Windows builds must pass.
4. Merge the PR into `test`.
5. Once `test` is stable, open a PR from `test` → `master`.
6. When `master` is ready for release, follow the steps below.

---

## Cutting a Release

Releases are triggered **only by pushing a git tag** that matches `v*`
(e.g. `v1.0.0`, `v1.2.3`, `v2.0.0-rc1`).

### Step 1 — Bump the version

In two places:

- `viral_load_calculator.iss` — line 5: `#define MyAppVersion "1.0.0"`
- `setup.py` — `version="1.0.0"`

Commit this on `master`:

```bash
git checkout master
git pull
# edit the two files above
git commit -am "Bump version to 1.0.0"
git push origin master
```

### Step 2 — Tag the release

```bash
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0
```

### Step 3 — Watch the pipeline

Go to the **Actions** tab in the GitHub repository. The
**Release Build** workflow will:

1. Build the Windows installer (`windows-latest` runner, Inno Setup).
2. Build the Linux AppImage (`ubuntu-22.04` runner, appimagetool).
3. Create a GitHub Release named `Release v1.0.0` and attach both
   binaries.

Both jobs run **in parallel**; the release is created only after both
succeed.

### Step 4 — Verify the release

Visit the **Releases** page of the repository. You should see
`Release v1.0.0` with both files attached:

- `ViralLoadCalculator_Setup.exe`
- `ViralLoadCalculator-x86_64.AppImage`

The release is public (assuming the repo is public) and is the canonical
distribution channel. Anyone with the link can download and install.

### Pre-release tags

Tags with a suffix like `v1.0.0-rc1` are also matched. To publish a tag
as a pre-release on GitHub, edit the release after creation and tick the
**This is a pre-release** checkbox. The `release.yml` workflow does not
mark pre-releases automatically.

---

## Where to Find Downloads

The installers live on the GitHub Releases page. Two convenient URLs:

- **All releases:**
  `https://github.com/<owner>/<repo>/releases`
- **A specific release (e.g. v1.0.0):**
  `https://github.com/<owner>/<repo>/releases/tag/v1.0.0`

For `mxg-mega/viral-load-converter`, replace `<owner>` with `mxg-mega`
and `<repo>` with `viral-load-converter`.

---

## Local Build

### Windows

Requires Python 3.11+ and Inno Setup Compiler.

```powershell
python -m pip install -r requirements.txt pyinstaller pillow
python tools/build_icon.py
pyinstaller viral_load_calculator.spec --noconfirm --clean
# Open Inno Setup Compiler GUI, load viral_load_calculator.iss, click Compile
```

The installer is written to `installer\ViralLoadCalculator_Setup.exe`.

### Linux

Requires Python 3.11+ and the Qt runtime libraries (already in the
GitHub Actions workflow; install via your package manager locally).

```bash
python -m pip install -r requirements.txt pyinstaller
pyinstaller viral_load_calculator.spec --noconfirm --clean
chmod +x tools/build_appimage.sh
./tools/build_appimage.sh
```

The AppImage is written to `ViralLoadCalculator-x86_64.AppImage`. To run:

```bash
chmod +x ViralLoadCalculator-x86_64.AppImage
./ViralLoadCalculator-x86_64.AppImage
```

---

## Pipeline Reference

### `release.yml` — `.github/workflows/release.yml`

- **Trigger:** push of any tag matching `v*`.
- **Permissions:** `contents: write` (needed to create releases).
- **Jobs:**
  - `build-windows` — PyInstaller one-dir build + Inno Setup on
    `windows-latest`. Uploads `ViralLoadCalculator_Setup.exe`.
  - `build-linux` — PyInstaller one-dir build + appimagetool on
    `ubuntu-22.04`. Uploads `ViralLoadCalculator-x86_64.AppImage`.
  - `release` — depends on both builds; downloads the artifacts and
    creates a GitHub Release with both attached.

### `test.yml` — `.github/workflows/test.yml`

- **Trigger:** push to `test`, or PR into `master`.
- **Permissions:** `contents: read` (no publishing).
- **Jobs:**
  - `lint` — compile-checks `main.py`, `models/`, `config.py`, and runs
    an offscreen import check (`QT_QPA_PLATFORM=offscreen python -c
    "import main"`).
  - `build-linux` — full PyInstaller + AppImage build on `ubuntu-22.04`.
  - `build-windows` — full PyInstaller + Inno Setup build on
    `windows-latest`.
- Builds produce workflow **artifacts** (visible in the Actions run
  page) but no GitHub Release is created.

---

## Troubleshooting

### "PyInstaller: UPX not found" warning

The spec sets `upx=False` to avoid this. If you re-enable UPX for
local builds, install it (`apt install upx-ucl` / `choco install upx`)
and put it on `PATH`.

### "Qt platform plugin could not be initialized" on Linux

Install the system Qt runtime libraries. On Ubuntu 22.04+:

```bash
sudo apt-get install libgl1 libegl1 libxkbcommon0 libdbus-1-3 \
  libxcb-cursor0 libxcb-icccm4 libxcb-image0 libxcb-keysyms1 \
  libxcb-randr0 libxcb-render-util0 libxcb-shape0 libxcb-sync1 \
  libxcb-xfixes0 libxcb-xinerama0 libxcb-xkb1 libxkbcommon-x11-0
```

On Ubuntu 24.04 you may also need `libfuse2t64` in place of `libfuse2`.

### AppImage will not launch locally

```bash
chmod +x ViralLoadCalculator-x86_64.AppImage
./ViralLoadCalculator-x86_64.AppImage
```

If FUSE is unavailable in your environment, AppImages can still be
extracted and run directly:

```bash
./ViralLoadCalculator-x86_64.AppImage --appimage-extract
./squashfs-root/AppRun
```

### Release was not created

Check the Actions tab for the workflow run. Common causes:

- The tag was not pushed to `master` (e.g. you tagged a feature branch).
- One of the two build jobs failed; the `release` job only runs if both
  succeed.
- The `softprops/action-gh-release@v2` action could not create a release
  because of repository settings (Settings → Actions → General → "Read
  and write permissions" must be enabled, or you must add the
  `GITHUB_TOKEN` permissions to the workflow).

### Inno Setup fails with "Resource update error: Icon file is invalid"

`viral_load_calculator.iss` references `resources\app_icon.ico`. Windows
`.ico` files cannot be used directly — they must be generated from a
source PNG. The Windows CI jobs run `python tools/build_icon.py` (which
uses Pillow) before PyInstaller and Inno Setup, producing
`resources/app_icon.ico` from `resources/app_icon.png` at multiple
sizes (16, 32, 48, 64, 128, 256). If you see this error locally, install
Pillow (`pip install pillow`) and run the script yourself.

### Inno Setup fails with "Could not find file: LICENSE"

`viral_load_calculator.iss` references `LICENSE` (no extension). Make
sure the file `LICENSE` is present at the repository root. (This was
fixed as part of CI setup; if you see this error, the fix was reverted.)

### Settings are not persisted when running the installed app

`config.py` writes to:
- Linux: `$XDG_CONFIG_HOME/viral-load-calculator/settings.json` (or
  `~/.config/viral-load-calculator/settings.json`).
- Windows: `%APPDATA%\ViralLoadCalculator\settings.json`.

If the user's home directory is read-only (rare), the save silently
fails and the bundled defaults are used on next launch.

---

## Pre-existing Bugs Fixed as Part of CI Setup

These were corrected before the pipelines were wired up:

1. **`viral_load_calculator.iss` typo:** `resources\app_icon..png`
   (double dot) → `resources\app_icon.png`.
2. **`viral_load_calculator.iss` wrong file:** `LicenseFile=LICENSE.txt`
   and `Source: "LICENSE.txt"` → `LICENSE` (matches the file in the
   repo).
3. **`viral_load_calculator.spec` was one-file:** Added a `COLLECT()`
   block so PyInstaller produces a `dist/ViralLoadCalculator/` directory
   (what the Inno Setup script already expected). Also disabled UPX
   (`upx=False`) so the build is reproducible without UPX installed.
4. **`config.py` wrote to `sys._MEIPASS`:** Now writes to a
   user-writable platform-appropriate location (XDG on Linux, APPDATA on
   Windows). Falls back to the bundled read-only defaults if the user's
   filesystem is read-only.

If any of these regress, the Windows installer build will fail in CI.

---

## Future Improvements

- **Code signing** — add a Windows Authenticode certificate and a
  `SignTool=` line to the Inno Setup script. Store the certificate
  securely as a GitHub Actions secret.
- **Linux signing** — sign the AppImage with GPG and ship a `.sig`
  attachment.
- **Automated updates** — add an `appimageupdate` tool integration or
  use `electron-updater`-style flows.
- **Tests** — add a `tests/` directory with pytest unit tests for the
  conversion logic in `models/base_model.py`.
- **Versioning automation** — replace the manual `MyAppVersion` bump
  with a single source of truth (e.g. `__version__` in
  `config.py` consumed by both the spec and the .iss).
