#!/usr/bin/env bash
set -euo pipefail

# Vercel builds run in a clean Linux image. Install the same pinned Flutter
# SDK used by the repository's GitHub Actions workflow before compiling web.
FLUTTER_VERSION="3.47.9"
FLUTTER_ARCHIVE="flutter_linux_${FLUTTER_VERSION}-stable.tar.xz"
FLUTTER_URL="https://storage.googleapis.com/flutter_infra_release/releases/stable/linux/${FLUTTER_ARCHIVE}"
FLUTTER_HOME="${HOME}/.cache/flutter-sdk"

export CI=true
export FLUTTER_SUPPRESS_ANALYTICS=true
export PUB_ENVIRONMENT="ci:vercel"

mkdir -p "${HOME}/.cache"
if [[ ! -x "${FLUTTER_HOME}/bin/flutter" ]]; then
  curl --fail --location --retry 3 "${FLUTTER_URL}" --output "${HOME}/.cache/${FLUTTER_ARCHIVE}"
  mkdir -p "${FLUTTER_HOME}"
  tar -xf "${HOME}/.cache/${FLUTTER_ARCHIVE}" --strip-components=1 -C "${FLUTTER_HOME}"
fi

export PATH="${FLUTTER_HOME}/bin:${PATH}"
flutter --version
flutter config --no-analytics
flutter pub get
flutter build web --release

test -s build/web/index.html
test -s build/web/manifest.json
test -s build/web/sw.js
test -s build/web/icons/Icon-192.png
test -s build/web/icons/Icon-maskable-192.png

echo "SoulSkill Flutter web build completed."
