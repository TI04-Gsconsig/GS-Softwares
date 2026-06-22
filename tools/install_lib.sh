# Biblioteca compartilhada de instalacao GS-Softwares.
# Usada pelos install.sh e injetada pelo painel pc-fleet antes da execucao remota.

gs_curl() {
  curl -fsSL --retry 3 --connect-timeout 30 -L \
    -A "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" \
    "$@"
}

gs_run_as_root() {
  if [[ "$(id -u)" -eq 0 ]]; then
    "$@"
  else
    sudo "$@"
  fi
}

gs_require_command() {
  local cmd="$1"
  local pkg="${2:-$1}"
  if command -v "$cmd" >/dev/null 2>&1; then
    return 0
  fi
  echo "Instalando dependencia: $pkg" >&2
  export DEBIAN_FRONTEND=noninteractive
  gs_run_as_root apt-get update -qq
  gs_run_as_root apt-get install -y "$pkg"
}

gs_validate_deb_file() {
  local file="$1"
  if [[ ! -s "$file" ]]; then
    echo "Download vazio ou ausente: $file" >&2
    return 1
  fi
  if command -v file >/dev/null 2>&1; then
    if ! file "$file" | grep -qiE 'debian|package|archive'; then
      echo "Arquivo baixado nao parece um pacote .deb valido" >&2
      return 1
    fi
  fi
  return 0
}

gs_download_deb_url() {
  local url="$1"
  local dest="$2"
  if [[ -z "$url" ]]; then
    echo "URL de download vazia" >&2
    return 1
  fi
  echo "Baixando pacote..." >&2
  if ! gs_curl -o "$dest" "$url"; then
    echo "Falha ao baixar: $url" >&2
    return 1
  fi
  gs_validate_deb_file "$dest"
}

gs_resolve_adspower_deb_url() {
  gs_curl "https://www.adspower.net/download" \
    | grep -oE 'https://version[^"'\'' ]+AdsPower-Global-[0-9.]+-x64\.deb' \
    | head -1
}

gs_install_deb_file() {
  local deb="$1"
  gs_validate_deb_file "$deb"
  export DEBIAN_FRONTEND=noninteractive
  if [[ "$(id -u)" -eq 0 ]]; then
    dpkg -i "$deb" || apt-get install -f -y
  else
    sudo dpkg -i "$deb" || sudo apt-get install -f -y
  fi
}

gs_install_deb_from_url() {
  local url="$1"
  local tmp="$2"
  gs_require_command curl curl
  gs_download_deb_url "$url" "$tmp"
  gs_install_deb_file "$tmp"
  rm -f "$tmp"
}

gs_install_deb_from_adspower_latest() {
  local tmp="$1"
  local url
  url="$(gs_resolve_adspower_deb_url || true)"
  if [[ -z "$url" ]]; then
    echo "Nao foi possivel obter a URL de download do ADS Power" >&2
    return 1
  fi
  gs_install_deb_from_url "$url" "$tmp"
}

gs_install_apt_packages() {
  export DEBIAN_FRONTEND=noninteractive
  gs_run_as_root apt-get update -qq
  gs_run_as_root apt-get install -y "$@"
}

gs_flatpak_install_user() {
  local ref="$1"
  local remote="${2:-flathub}"
  gs_require_command flatpak flatpak
  flatpak remote-add --user --if-not-exists "$remote" https://flathub.org/repo/flathub.flatpakrepo >/dev/null 2>&1 || true
  if flatpak info --user "$ref" >/dev/null 2>&1; then
    flatpak update --user --noninteractive -y "$ref"
  else
    flatpak install --user --noninteractive -y "$remote" "$ref"
  fi
  local apps_dir="${HOME}/.local/share/flatpak/exports/share/applications"
  if [[ -d "$apps_dir" ]] && command -v update-desktop-database >/dev/null 2>&1; then
    update-desktop-database "$apps_dir" 2>/dev/null || true
  fi
}
