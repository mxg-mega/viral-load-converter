#!/usr/bin/env bash
# build_appimage.sh
# Wrap the PyInstaller one-dir output (dist/ViralLoadCalculator/) in an
# AppImage using appimagetool.
#
# Usage:  ./tools/build_appimage.sh
# Output: ViralLoadCalculator-x86_64.AppImage in the project root.

set -euo pipefail

# ---------------------------------------------------------------------------
# Resolve project root (the directory containing this script's parent).
# ---------------------------------------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
APP_NAME="ViralLoadCalculator"
APP_ID="viral-load-calculator"
APP_DIR_SRC="dist/${APP_NAME}"
APPDIR="AppDir"
TOOLS_CACHE="tools/.cache"
APPIMAGETOOL_VERSION="continuous"
APPIMAGETOOL="${TOOLS_CACHE}/appimagetool-x86_64.AppImage"
OUTPUT_APPIMAGE="${PROJECT_ROOT}/${APP_NAME}-x86_64.AppImage"

# ---------------------------------------------------------------------------
# Sanity checks
# ---------------------------------------------------------------------------
if [ ! -d "${APP_DIR_SRC}" ]; then
  echo "ERROR: PyInstaller output not found at ${APP_DIR_SRC}" >&2
  echo "Run: pyinstaller viral_load_calculator.spec --noconfirm --clean" >&2
  exit 1
fi

if [ ! -f "tools/appimage/AppRun" ]; then
  echo "ERROR: tools/appimage/AppRun missing" >&2
  exit 1
fi

if [ ! -f "tools/appimage/${APP_ID}.desktop" ]; then
  echo "ERROR: tools/appimage/${APP_ID}.desktop missing" >&2
  exit 1
fi

# ---------------------------------------------------------------------------
# Download appimagetool (cached locally)
# ---------------------------------------------------------------------------
mkdir -p "${TOOLS_CACHE}"

if [ ! -x "${APPIMAGETOOL}" ]; then
  echo "Downloading appimagetool (${APPIMAGETOOL_VERSION})..."
  # Try primary source first
  if ! curl -fL --retry 3 -o "${APPIMAGETOOL}" \
    "https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage" 2>/dev/null; then
    echo "Primary source failed, trying fallback..."
    curl -fL --retry 3 -o "${APPIMAGETOOL}" \
    "https://github.com/AppImageCommunity/appimagetool/releases/download/${APPIMAGETOOL_VERSION}/appimagetool-x86_64.AppImage"
  fi
  chmod +x "${APPIMAGETOOL}"
fi

# ---------------------------------------------------------------------------
# Stage AppDir structure
# ---------------------------------------------------------------------------
echo "Staging AppDir..."
rm -rf "${APPDIR}"
mkdir -p "${APPDIR}/usr"

# Copy PyInstaller one-dir contents into AppDir/usr/.
cp -a "${APP_DIR_SRC}/." "${APPDIR}/usr/"

# AppRun launcher and desktop entry.
install -m 0755 "tools/appimage/AppRun" "${APPDIR}/AppRun"
install -m 0644 "tools/appimage/${APP_ID}.desktop" "${APPDIR}/${APP_ID}.desktop"

# Icon: AppImage convention is the file at the AppDir root with the same
# stem as the Icon= value in the .desktop file (no extension needed).
if [ -f "resources/app_icon.png" ]; then
  install -m 0644 "resources/app_icon.png" "${APPDIR}/${APP_ID}.png"
fi

# ---------------------------------------------------------------------------
# Build the AppImage
# ---------------------------------------------------------------------------
echo "Running appimagetool..."

# APPIMAGE_EXTRACT_AND_RUN=1 lets appimagetool work on FUSE-less systems
# (e.g. CI runners, sandboxed environments).
export APPIMAGE_EXTRACT_AND_RUN=1
ARCH=x86_64 "${APPIMAGETOOL}" "${APPDIR}" "${OUTPUT_APPIMAGE}"

# ---------------------------------------------------------------------------
# Done
# ---------------------------------------------------------------------------
echo
echo "AppImage built: ${OUTPUT_APPIMAGE}"
ls -lh "${OUTPUT_APPIMAGE}"
file "${OUTPUT_APPIMAGE}"
