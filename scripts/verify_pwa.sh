#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(pwd)"
WEB_DIR="$ROOT_DIR/soulskill_mobile/web"
for file in \
  "$WEB_DIR/index.html" \
  "$WEB_DIR/manifest.json" \
  "$WEB_DIR/sw.js" \
  "$WEB_DIR/favicon.png" \
  "$WEB_DIR/icons/Icon-192.png" \
  "$WEB_DIR/icons/Icon-maskable-192.png" \
  "$WEB_DIR/icons/Icon-512.svg" \
  "$WEB_DIR/icons/Icon-maskable-512.svg"; do
  test -s "$file" || { echo "Missing PWA file: $file" >&2; exit 1; }
done
node --check "$WEB_DIR/sw.js"
python3 - "$WEB_DIR" <<'PY'
import json
import pathlib
import struct
import sys
import zlib

web_dir = pathlib.Path(sys.argv[1])
manifest = json.loads((web_dir / "manifest.json").read_text(encoding="utf-8"))
html = (web_dir / "index.html").read_text(encoding="utf-8")

if manifest.get("name") != "SoulSkill — Career Transition Companion":
    raise SystemExit("Unexpected PWA name")
if manifest.get("display") != "standalone":
    raise SystemExit("PWA must use standalone display")
if not manifest.get("start_url") or not manifest.get("scope"):
    raise SystemExit("PWA start_url and scope are required")

def validate_png(path, expected):
    data = path.read_bytes()
    if not data.startswith(b"\x89PNG\r\n\x1a\n"):
        raise SystemExit(f"Invalid PNG signature: {path}")
    width, height = struct.unpack(">II", data[16:24])
    if (width, height) != (expected, expected):
        raise SystemExit(f"Incorrect PNG dimensions: {path} ({width}x{height})")
    offset = 8
    while offset < len(data):
        length = struct.unpack(">I", data[offset:offset + 4])[0]
        chunk_type = data[offset + 4:offset + 8]
        chunk_data = data[offset + 8:offset + 8 + length]
        stored_crc = struct.unpack(">I", data[offset + 8 + length:offset + 12 + length])[0]
        actual_crc = zlib.crc32(chunk_type + chunk_data) & 0xffffffff
        if stored_crc != actual_crc:
            raise SystemExit(f"Corrupt PNG chunk in {path}")
        offset += 12 + length
        if chunk_type == b"IEND":
            break
    if offset != len(data):
        raise SystemExit(f"Malformed PNG structure: {path}")

for path, expected in [
    (web_dir / "icons/Icon-192.png", 192),
    (web_dir / "icons/Icon-maskable-192.png", 192),
]:
    validate_png(path, expected)

for relative in ["icons/Icon-512.svg", "icons/Icon-maskable-512.svg"]:
    svg = (web_dir / relative).read_text(encoding="utf-8")
    if "<svg" not in svg or 'viewBox="0 0 512 512"' not in svg:
        raise SystemExit(f"Invalid 512px SVG icon: {relative}")

icons = manifest.get("icons", [])
for required in [
    ("192x192", "image/png"),
    ("512x512", "image/svg+xml"),
]:
    if not any(icon.get("sizes") == required[0] and icon.get("type") == required[1] for icon in icons):
        raise SystemExit(f"Manifest is missing a {required[0]} {required[1]} icon")

if 'rel="manifest"' not in html or 'flutter_bootstrap.js' not in html or "register('sw.js'" not in html:
    raise SystemExit("Web entry point is missing manifest, Flutter bootstrap or service-worker registration")

print("SoulSkill PWA assets, PNG integrity and manifest validation passed.")
PY
