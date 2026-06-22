#!/bin/bash
set -euo pipefail
if ! declare -F gs_install_deb_from_url >/dev/null 2>&1; then
  _gs_tools=""
  if [[ -n "${BASH_SOURCE[0]:-}" ]]; then
    _gs_tools="$(cd "$(dirname "${BASH_SOURCE[0]}")/../tools" 2>/dev/null && pwd || true)"
  fi
  if [[ -z "$_gs_tools" || ! -f "$_gs_tools/install_lib.sh" ]]; then
    echo "Biblioteca GS install_lib.sh nao encontrada" >&2
    exit 1
  fi
  # shellcheck source=/dev/null
  source "$_gs_tools/install_lib.sh"
fi
gs_install_apt_packages remmina remmina-plugin-vnc remmina-plugin-rdp remmina-plugin-secret
echo "Remmina instalado via apt"
