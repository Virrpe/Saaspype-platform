#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

console.log('🧪 Luciq Desktop App Test Suite');
console.log('=====================================');

// Test 1: Check if package.json exists and has correct structure
console.log('\n1. Testing package.json...');
try {
  const packageJson = JSON.parse(fs.readFileSync('../package.json', 'utf8'));
  console.log('✅ package.json exists');
  console.log(`✅ App name: ${packageJson.name}`);
  console.log(`✅ Main entry: ${packageJson.main}`);
  console.log(`✅ Electron version: ${packageJson.devDependencies.electron}`);
} catch (error) {
  console.log('❌ package.json error:', error.message);
}

// Test 2: Check if Electron main.js exists
console.log('\n2. Testing Electron main.js...');
try {
  const mainJs = fs.readFileSync('../electron/main.js', 'utf8');
  console.log('✅ electron/main.js exists');
  console.log(`✅ File size: ${mainJs.length} characters`);
  
  // Check for key features
  const features = [
    'LuciqDesktopApp',
    'globalShortcut',
    'Tray',
    'spawnVisualWindow',
    'enableDesktopSnapping'
  ];
  
  features.forEach(feature => {
    if (mainJs.includes(feature)) {
      console.log(`✅ Feature found: ${feature}`);
    } else {
      console.log(`❌ Feature missing: ${feature}`);
    }
  });
} catch (error) {
  console.log('❌ main.js error:', error.message);
}

// Test 3: Check if preload.js exists
console.log('\n3. Testing preload.js...');
try {
  const preloadJs = fs.readFileSync('../electron/preload.js', 'utf8');
  console.log('✅ electron/preload.js exists');
  console.log(`✅ File size: ${preloadJs.length} characters`);
  
  // Check for key APIs
  const apis = [
    'contextBridge',
    'electronAPI',
    'spawnVisualWindow',
    'desktop',
    'aria'
  ];
  
  apis.forEach(api => {
    if (preloadJs.includes(api)) {
      console.log(`✅ API found: ${api}`);
    } else {
      console.log(`❌ API missing: ${api}`);
    }
  });
} catch (error) {
  console.log('❌ preload.js error:', error.message);
}

// Test 4: Check if Python server files exist
console.log('\n4. Testing Python server...');
try {
  const startFrontend = fs.readFileSync('../start_frontend_windows.py', 'utf8');
  console.log('✅ start_frontend_windows.py exists');
  
  if (startFrontend.includes('ai-terminal')) {
    console.log('✅ AI Terminal route configured');
  } else {
    console.log('❌ AI Terminal route missing');
  }
} catch (error) {
  console.log('❌ Python server error:', error.message);
}

// Test 5: Check if ARIA components exist
console.log('\n5. Testing ARIA components...');
const ariaFiles = [
  '../src/frontend/components/ps2-terminal-ai.js',
  '../src/frontend/components/ps2-visual-command-center.js',
  '../src/frontend/pages/features/ai-terminal.html'
];

ariaFiles.forEach(file => {
  try {
    const content = fs.readFileSync(file, 'utf8');
    console.log(`✅ ${file.replace('../', '')} exists (${content.length} chars)`);
  } catch (error) {
    console.log(`❌ ${file.replace('../', '')} missing`);
  }
});

// Test 6: Check node_modules
console.log('\n6. Testing dependencies...');
try {
  const nodeModules = fs.readdirSync('../node_modules');
  const electronExists = nodeModules.includes('electron');
  const electronBuilderExists = nodeModules.includes('electron-builder');
  const crossEnvExists = nodeModules.includes('cross-env');
  
  console.log(`✅ node_modules exists (${nodeModules.length} packages)`);
  console.log(`${electronExists ? '✅' : '❌'} Electron installed`);
  console.log(`${electronBuilderExists ? '✅' : '❌'} Electron Builder installed`);
  console.log(`${crossEnvExists ? '✅' : '❌'} Cross-env installed (Windows compatibility)`);
} catch (error) {
  console.log('❌ Dependencies error:', error.message);
}

console.log('\n🚀 Desktop App Test Complete!');
console.log('\nNext steps:');
console.log('1. Run: npm run dev (to start with Python server)');
console.log('2. Run: npm run electron (to start Electron only)');
console.log('3. Test global hotkey: Ctrl+Shift+A');
console.log('4. Test visual spawning: "Show me visuals" in ARIA');
console.log('5. Test window snapping: Drag windows to screen edges');
console.log('\n📖 Full demo guide: DESKTOP_AI_COMPANION_DEMO.md'); 