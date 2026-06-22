#!/bin/bash
set -euo pipefail
URL="https://version.adspower.net/software/linux-x64-global/AdsPower-Global-5.12.28-x64.deb"
TMP="/tmp/gs-ads-power.deb"
# Confira a URL mais recente em https://www.adspower.com/download antes de instalar.
curl -fsSL --retry 3 --connect-timeout 30 -o "$TMP" "$URL"

sudo dpkg -i "$TMP" || sudo apt-get install -f -y
rm -f "$TMP"
echo "ADS Power instalado"
