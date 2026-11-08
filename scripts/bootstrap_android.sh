#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MOBILE_DIR="$ROOT_DIR/soulskill_mobile"

if ! command -v flutter >/dev/null 2>&1; then
  echo "Flutter SDK was not found. Install Flutter and run 'flutter doctor' first." >&2
  exit 1
fi

cd "$MOBILE_DIR"

if [[ -d android ]]; then
  echo "Android host project already exists at $MOBILE_DIR/android"
  exit 0
fi

flutter create --platforms=android --org ai.soulvest --project-name soulskill_mobile .
echo "Android host project generated. Review the Android manifest and local API networking settings."
