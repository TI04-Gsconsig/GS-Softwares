#!/bin/bash
set -euo pipefail
URL="https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb"
TMP="/tmp/gs-google-chrome.deb"

curl -fsSL --retry 3 --connect-timeout 30 -o "$TMP" "$URL"

sudo dpkg -i "$TMP" || sudo apt-get install -f -y
rm -f "$TMP"
echo "Google Chrome instalado"
