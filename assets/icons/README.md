# Soulvest App Icons

This directory contains app icons for PWA (Progressive Web App) functionality.

## Required Icons

The following icon sizes are needed for full PWA support:

### Required Sizes:
- 72x72 - For older Android devices
- 96x96 - For Chrome on Android
- 128x128 - For Chrome Web Store
- 144x144 - For Windows 8 tiles
- 152x152 - For iOS devices
- 192x192 - Standard Android icon
- 384x384 - For high-res displays
- 512x512 - Required for PWA, maskable icon

## How to Generate Icons

### Option 1: Using Online Tool (Easiest)
1. Visit https://realfavicongenerator.net/ or https://www.pwabuilder.com/
2. Upload a square logo (minimum 512x512px recommended)
3. Download the generated icon pack
4. Extract to this directory

### Option 2: Using ImageMagick (Command Line)
```bash
# Install ImageMagick first
# Create all sizes from a source image (source.png)

magick source.png -resize 72x72 icon-72x72.png
magick source.png -resize 96x96 icon-96x96.png
magick source.png -resize 128x128 icon-128x128.png
magick source.png -resize 144x144 icon-144x144.png
magick source.png -resize 152x152 icon-152x152.png
magick source.png -resize 192x192 icon-192x192.png
magick source.png -resize 384x384 icon-384x384.png
magick source.png -resize 512x512 icon-512x512.png
```

### Option 3: Using Python (Pillow)
```python
from PIL import Image

sizes = [72, 96, 128, 144, 152, 192, 384, 512]
source = Image.open('source.png')

for size in sizes:
    resized = source.resize((size, size), Image.LANCZOS)
    resized.save(f'icon-{size}x{size}.png')
```

## Icon Design Guidelines

### Brand Colors (Soulvest):
- Primary: #667eea (Purple)
- Secondary: #764ba2 (Darker Purple)
- Accent: #f093fb (Pink)
- Background: #FFF8F0 (Cream)

### Design Tips:
- Use simple, recognizable design
- High contrast for visibility
- Avoid text (icons are small)
- Square format with rounded corners
- Safe area: 80% center (avoid edges)
- Test on different backgrounds

### Recommended Design:
```
✨ Symbol (Sparkle/Star)
+ "S" letter or full "SOULVEST" text
On gradient purple background
```

## Temporary Placeholder

Until you create proper icons, you can use:
1. Emoji as icon (✨)
2. Text-based icon (letter "S")
3. Simple colored square

The app will work without icons, but PWA installation will look better with proper icons.

## Files to Create:
- [ ] icon-72x72.png
- [ ] icon-96x96.png
- [ ] icon-128x128.png
- [ ] icon-144x144.png
- [ ] icon-152x152.png
- [ ] icon-192x192.png
- [ ] icon-384x384.png
- [ ] icon-512x512.png

## Testing Icons:
After adding icons:
1. Clear browser cache
2. Open manifest.json to verify paths
3. Use Chrome DevTools > Application > Manifest
4. Check "Add to Home Screen" preview
