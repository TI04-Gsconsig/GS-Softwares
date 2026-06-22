#!/bin/bash
set -euo pipefail
APP_NAME="WhatsApp Web"
APP_URL="https://web.whatsapp.com"
APP_ID="whatsapp-web"
DESKTOP_DIR="$HOME/.local/share/applications"
find_browser() {
  for path in /opt/google/chrome/google-chrome google-chrome google-chrome-stable chromium chromium-browser; do
    if command -v "$path" >/dev/null 2>&1; then command -v "$path"; return 0; fi
    [[ -x "$path" ]] && printf '%s\n' "$path" && return 0
  done
  return 1
}
browser="$(find_browser || true)"
if [[ -z "$browser" ]]; then
  echo "Chrome/Chromium nao encontrado. Instale google-chrome primeiro." >&2
  exit 1
fi
mkdir -p "$DESKTOP_DIR"
cat > "$DESKTOP_DIR/${APP_ID}.desktop" <<EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=${APP_NAME}
Exec=${browser} --app=${APP_URL} --class=${APP_ID}
Icon=web-whatsapp
Terminal=false
Categories=Network;Chat;
EOF
chmod +x "$DESKTOP_DIR/${APP_ID}.desktop"
for desk in "$HOME/Desktop" "$HOME/Área de trabalho" "$HOME/Area de Trabalho"; do
  [[ -d "$desk" ]] || continue
  cp "$DESKTOP_DIR/${APP_ID}.desktop" "$desk/${APP_NAME}.desktop"
done
echo "WhatsApp Web instalado"
