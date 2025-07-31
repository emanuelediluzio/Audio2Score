#!/bin/bash

# Usage: ./png_to_icns.sh icons/source_icon.png

INPUT=$1
NAME="app"

mkdir -p icons/$NAME.iconset

sips -z 16 16     $INPUT --out icons/$NAME.iconset/icon_16x16.png
sips -z 32 32     $INPUT --out icons/$NAME.iconset/icon_16x16@2x.png
sips -z 32 32     $INPUT --out icons/$NAME.iconset/icon_32x32.png
sips -z 64 64     $INPUT --out icons/$NAME.iconset/icon_32x32@2x.png
sips -z 128 128   $INPUT --out icons/$NAME.iconset/icon_128x128.png
sips -z 256 256   $INPUT --out icons/$NAME.iconset/icon_128x128@2x.png
sips -z 256 256   $INPUT --out icons/$NAME.iconset/icon_256x256.png
sips -z 512 512   $INPUT --out icons/$NAME.iconset/icon_256x256@2x.png
cp $INPUT icons/$NAME.iconset/icon_512x512.png
cp $INPUT icons/$NAME.iconset/icon_512x512@2x.png

iconutil -c icns icons/$NAME.iconset -o icons/$NAME.icns
rm -rf icons/$NAME.iconset

echo "✅ Icona .icns generata in icons/$NAME.icns"
