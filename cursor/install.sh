#!/bin/bash
set -euo pipefail
URL="https://downloads.cursor.com/aptrepo/pool/c/cu/cursor_0.48.8_amd64.deb"
TMP="/tmp/gs-cursor.deb"
# Atualize download_url em install.json quando houver nova versao oficial.
curl -fsSL --retry 3 --connect-timeout 30 -o "$TMP" "$URL"

sudo dpkg -i "$TMP" || sudo apt-get install -f -y
rm -f "$TMP"
echo "Cursor instalado"
