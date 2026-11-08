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
  "$WEB_DIR/icons/Icon-512.png" \
  "$WEB_DIR/icons/Icon-maskable-192.png" \
  "$WEB_DIR/icons/Icon-maskable-512.png"; do
  test -s "$file" || { echo "Missing PWA file: $file" >&2; exit 1; }
done
node --check "$WEB_DIR/sw.js"
node - "$WEB_DIR" <<'NODE'
const fs = require('node:fs');
const path = require('node:path');
const webDir = process.argv[2];
const manifest = JSON.parse(fs.readFileSync(path.join(webDir, 'manifest.json'), 'utf8'));
const html = fs.readFileSync(path.join(webDir, 'index.html'), 'utf8');
if (manifest.name !== 'SoulSkill — Career Transition Companion') throw new Error('Unexpected PWA name');
if (manifest.display !== 'standalone') throw new Error('PWA must use standalone display');
if (!manifest.start_url || !manifest.scope) throw new Error('PWA start_url and scope are required');
for (const size of ['192x192', '512x512']) {
  const icon = manifest.icons.find((item) => item.sizes === size && item.purpose === 'any');
  if (!icon) throw new Error('Missing standard icon: ' + size);
  const iconPath = path.join(webDir, icon.src);
  const bytes = fs.readFileSync(iconPath);
  if (bytes.readUInt32BE(16) !== Number(size.split('x')[0])) throw new Error('Incorrect icon dimensions: ' + iconPath);
}
for (const icon of manifest.icons.filter((item) => item.purpose === 'maskable')) {
  if (!fs.existsSync(path.join(webDir, icon.src))) throw new Error('Missing maskable icon: ' + icon.src);
}
if (!html.includes('rel="manifest"') || !html.includes('flutter_bootstrap.js') || !html.includes("register('sw.js'")) {
  throw new Error('Web entry point is missing PWA metadata, Flutter bootstrap, or service-worker registration');
}
console.log('SoulSkill PWA assets and manifest validation passed.');
NODE
