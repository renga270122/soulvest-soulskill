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
echo "Android host project generated without overwriting Dart source. Review Android networking settings before testing."
