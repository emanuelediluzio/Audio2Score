#!/bin/bash

APP_NAME="Audio2Score"
VOL_NAME="Audio2Score"
ICON_PATH="icons/app.icns"
BACKGROUND="icons/dmg_background.png"
APP_PATH="dist/${APP_NAME}.app"

mkdir -p build/dmg_temp
cp -R "$APP_PATH" build/dmg_temp/
ln -s /Applications build/dmg_temp/Applications

create-dmg \
  --volname "$VOL_NAME" \
  --volicon "$ICON_PATH" \
  --background "$BACKGROUND" \
  --window-pos 200 120 \
  --window-size 500 300 \
  --icon-size 100 \
  --icon "${APP_NAME}.app" 100 120 \
  --icon "Applications" 400 120 \
  --hide-extension "${APP_NAME}.app" \
  --app-drop-link 400 120 \
  "Audio2Score.dmg" \
  "build/dmg_temp"

rm -r build/dmg_temp

echo "DMG creato: Audio2Score.dmg"
