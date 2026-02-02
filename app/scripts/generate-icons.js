const Jimp = require('jimp');
const path = require('path');

const ASSETS_DIR = path.join(__dirname, '..', 'assets');

// Colors
const PRIMARY_BLUE = 0x007AFFFF; // #007AFF
const WHITE = 0xFFFFFFFF;
const DARK_BLUE = 0x0056B3FF;

async function createIcon(size, filename, isAdaptive = false) {
  const image = new Jimp(size, size, isAdaptive ? 0x00000000 : PRIMARY_BLUE);

  // Draw a simple link/bookmark shape
  const centerX = size / 2;
  const centerY = size / 2;
  const iconSize = size * 0.5;

  // Draw bookmark shape (simplified rectangle with folded corner)
  const bookmarkWidth = iconSize * 0.6;
  const bookmarkHeight = iconSize * 0.8;
  const startX = centerX - bookmarkWidth / 2;
  const startY = centerY - bookmarkHeight / 2;
  const foldSize = bookmarkWidth * 0.25;

  // Fill bookmark body
  for (let y = startY; y < startY + bookmarkHeight; y++) {
    for (let x = startX; x < startX + bookmarkWidth; x++) {
      // Skip folded corner area
      if (x > startX + bookmarkWidth - foldSize && y < startY + foldSize) {
        continue;
      }
      if (x >= 0 && x < size && y >= 0 && y < size) {
        image.setPixelColor(WHITE, Math.floor(x), Math.floor(y));
      }
    }
  }

  // Draw fold triangle (darker shade)
  for (let i = 0; i < foldSize; i++) {
    for (let j = 0; j < foldSize - i; j++) {
      const x = startX + bookmarkWidth - foldSize + i;
      const y = startY + j;
      if (x >= 0 && x < size && y >= 0 && y < size) {
        image.setPixelColor(0xE0E0E0FF, Math.floor(x), Math.floor(y));
      }
    }
  }

  // Draw a small link symbol (chain link) in the center
  const linkSize = iconSize * 0.25;
  const linkY = centerY + bookmarkHeight * 0.1;

  // Left circle of chain
  const leftLinkX = centerX - linkSize * 0.4;
  const rightLinkX = centerX + linkSize * 0.4;
  const linkRadius = linkSize * 0.3;

  // Draw chain link circles
  for (let angle = 0; angle < Math.PI * 2; angle += 0.02) {
    for (let r = linkRadius * 0.6; r <= linkRadius; r += 0.5) {
      // Left link
      const lx = leftLinkX + Math.cos(angle) * r;
      const ly = linkY + Math.sin(angle) * r * 0.6;
      if (lx >= 0 && lx < size && ly >= 0 && ly < size) {
        image.setPixelColor(isAdaptive ? PRIMARY_BLUE : DARK_BLUE, Math.floor(lx), Math.floor(ly));
      }

      // Right link
      const rx = rightLinkX + Math.cos(angle) * r;
      const ry = linkY + Math.sin(angle) * r * 0.6;
      if (rx >= 0 && rx < size && ry >= 0 && ry < size) {
        image.setPixelColor(isAdaptive ? PRIMARY_BLUE : DARK_BLUE, Math.floor(rx), Math.floor(ry));
      }
    }
  }

  // Draw connecting line
  const lineY = linkY;
  for (let x = leftLinkX; x <= rightLinkX; x++) {
    for (let thickness = -1; thickness <= 1; thickness++) {
      const py = lineY + thickness;
      if (x >= 0 && x < size && py >= 0 && py < size) {
        image.setPixelColor(isAdaptive ? PRIMARY_BLUE : DARK_BLUE, Math.floor(x), Math.floor(py));
      }
    }
  }

  await image.writeAsync(path.join(ASSETS_DIR, filename));
  console.log(`Created: ${filename} (${size}x${size})`);
}

async function createSplashIcon(size, filename) {
  const image = new Jimp(size, size, 0x00000000); // Transparent background

  const centerX = size / 2;
  const centerY = size / 2;
  const iconSize = size * 0.7;

  // Draw a filled bookmark shape
  const bookmarkWidth = iconSize * 0.6;
  const bookmarkHeight = iconSize * 0.8;
  const startX = centerX - bookmarkWidth / 2;
  const startY = centerY - bookmarkHeight / 2;
  const foldSize = bookmarkWidth * 0.2;

  // Fill bookmark body with primary blue
  for (let y = startY; y < startY + bookmarkHeight; y++) {
    for (let x = startX; x < startX + bookmarkWidth; x++) {
      if (x > startX + bookmarkWidth - foldSize && y < startY + foldSize) {
        continue;
      }
      if (x >= 0 && x < size && y >= 0 && y < size) {
        image.setPixelColor(PRIMARY_BLUE, Math.floor(x), Math.floor(y));
      }
    }
  }

  // Draw fold
  for (let i = 0; i < foldSize; i++) {
    for (let j = 0; j < foldSize - i; j++) {
      const x = startX + bookmarkWidth - foldSize + i;
      const y = startY + j;
      if (x >= 0 && x < size && y >= 0 && y < size) {
        image.setPixelColor(DARK_BLUE, Math.floor(x), Math.floor(y));
      }
    }
  }

  // Draw white link symbol
  const linkSize = iconSize * 0.2;
  const linkY = centerY + bookmarkHeight * 0.05;
  const leftLinkX = centerX - linkSize * 0.35;
  const rightLinkX = centerX + linkSize * 0.35;
  const linkRadius = linkSize * 0.25;

  for (let angle = 0; angle < Math.PI * 2; angle += 0.02) {
    for (let r = linkRadius * 0.5; r <= linkRadius; r += 0.5) {
      const lx = leftLinkX + Math.cos(angle) * r;
      const ly = linkY + Math.sin(angle) * r * 0.5;
      if (lx >= 0 && lx < size && ly >= 0 && ly < size) {
        image.setPixelColor(WHITE, Math.floor(lx), Math.floor(ly));
      }

      const rx = rightLinkX + Math.cos(angle) * r;
      const ry = linkY + Math.sin(angle) * r * 0.5;
      if (rx >= 0 && rx < size && ry >= 0 && ry < size) {
        image.setPixelColor(WHITE, Math.floor(rx), Math.floor(ry));
      }
    }
  }

  for (let x = leftLinkX; x <= rightLinkX; x++) {
    for (let thickness = -1; thickness <= 1; thickness++) {
      const py = linkY + thickness;
      if (x >= 0 && x < size && py >= 0 && py < size) {
        image.setPixelColor(WHITE, Math.floor(x), Math.floor(py));
      }
    }
  }

  await image.writeAsync(path.join(ASSETS_DIR, filename));
  console.log(`Created: ${filename} (${size}x${size})`);
}

async function main() {
  console.log('Generating LinkNote app icons...\n');

  try {
    // Main app icon (iOS and general)
    await createIcon(1024, 'icon.png', false);

    // Android adaptive icon (foreground on transparent)
    await createIcon(1024, 'adaptive-icon.png', true);

    // Splash screen icon
    await createSplashIcon(200, 'splash-icon.png');

    // Favicon for web
    await createIcon(48, 'favicon.png', false);

    console.log('\nAll icons generated successfully!');
  } catch (error) {
    console.error('Error generating icons:', error);
    process.exit(1);
  }
}

main();
