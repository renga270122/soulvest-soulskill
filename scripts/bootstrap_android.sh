#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MOBILE_DIR="$ROOT_DIR/soulskill_mobile"

if ! command -v flutter >/dev/null 2>&1; then
  echo "Flutter SDK was not found. Install Flutter and run 'flutter doctor' first." >&2
  exit 1
fi

if [[ -d "$MOBILE_DIR/android" ]]; then
  echo "Android host project already exists at $MOBILE_DIR/android"
  exit 0
fi

TEMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TEMP_DIR"' EXIT

flutter create --platforms=android --org ai.soulvest --project-name soulskill_mobile "$TEMP_DIR/soulskill_mobile"
cp -a "$TEMP_DIR/soulskill_mobile/android" "$MOBILE_DIR/android"

# Permit local HTTP only in debug builds. Release builds must use HTTPS.
mkdir -p "$MOBILE_DIR/android/app/src/debug"
cat > "$MOBILE_DIR/android/app/src/debug/AndroidManifest.xml" <<'MANIFEST'
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    <application android:usesCleartextTraffic="true" />
</manifest>
MANIFEST

echo "Android host project generated without overwriting Dart source."
echo "Debug builds permit local HTTP for emulator/LAN development; release builds must use HTTPS."
