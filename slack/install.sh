#!/bin/bash
set -euo pipefail
REF="com.slack.Slack"
if ! command -v flatpak >/dev/null 2>&1; then
  echo "Instalando flatpak..." >&2
  sudo apt-get update -qq
  sudo DEBIAN_FRONTEND=noninteractive apt-get install -y flatpak
fi
flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo >/dev/null 2>&1 || true
flatpak install --noninteractive -y flathub "$REF"
echo "Slack instalado via Flatpak"
