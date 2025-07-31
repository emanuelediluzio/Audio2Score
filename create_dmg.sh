#!/bin/bash

create-dmg \
  --volname "Audio2Score" \
  --volicon "icons/app.icns" \
  --background "icons/background.png" \
  --window-pos 200 120 \
  --window-size 500 300 \
  --icon-size 100 \
  --icon "Audio2Score.app" 100 120 \
  --app-drop-link 400 120 \
  "Audio2Score.dmg" \
  "dist/Audio2Score.app"

