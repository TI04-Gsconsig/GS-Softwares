#!/usr/bin/env python3
"""Gera pastas padrao do catalogo GS-Softwares."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SOFTWARE = [
    {
        "slug": "slack",
        "name": "Slack",
        "version": "4.39",
        "developer": "Slack Technologies",
        "official_url": "https://slack.com/downloads/linux",
        "summary": "Comunicacao corporativa por canais, mensagens e integracoes.",
        "purpose": "Centralizar conversas da equipe com historico e busca.",
        "keywords": ["slack", "sl", "comunicacao", "chat"],
        "install_method": "flatpak",
        "dependencies": ["flatpak", "flathub"],
        "flatpak_ref": "com.slack.Slack",
    },
    {
        "slug": "cursor",
        "name": "Cursor",
        "version": "latest",
        "developer": "Anysphere",
        "official_url": "https://cursor.com/download",
        "summary": "Editor de codigo com assistente de IA integrado.",
        "purpose": "Desenvolvimento de software com produtividade e IA.",
        "keywords": ["cursor", "ide", "editor", "ia"],
        "install_method": "deb",
        "dependencies": ["curl", "dpkg"],
        "download_url": "https://downloads.cursor.com/aptrepo/pool/c/cu/cursor_0.48.8_amd64.deb",
        "download_sha256": "",
        "deb_note": "Atualize download_url em install.json quando houver nova versao oficial.",
    },
    {
        "slug": "whatsapp-web",
        "name": "WhatsApp Web",
        "version": "web",
        "developer": "Meta",
        "official_url": "https://web.whatsapp.com",
        "summary": "Atalho do WhatsApp Web no navegador, como aplicativo na area de trabalho.",
        "purpose": "Acesso rapido ao WhatsApp corporativo sem instalar app nativo.",
        "keywords": ["whatsapp", "whats", "web", "wa"],
        "install_method": "webapp",
        "dependencies": ["google-chrome ou chromium"],
    },
    {
        "slug": "google-chrome",
        "name": "Google Chrome",
        "version": "stable",
        "developer": "Google",
        "official_url": "https://www.google.com/chrome/",
        "summary": "Navegador web oficial do Google para Linux.",
        "purpose": "Navegacao, apps web e compatibilidade corporativa.",
        "keywords": ["chrome", "google", "navegador", "browser"],
        "install_method": "deb",
        "dependencies": ["curl", "dpkg", "apt"],
        "download_url": "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb",
    },
    {
        "slug": "remmina",
        "name": "Remmina",
        "version": "repo",
        "developer": "Remmina Project",
        "official_url": "https://remmina.org/",
        "summary": "Cliente de desktop remoto (RDP, VNC, SSH) para suporte e operacao.",
        "purpose": "Acesso remoto a PCs da frota e servidores.",
        "keywords": ["remmina", "vnc", "rdp", "remote", "desktop"],
        "install_method": "apt",
        "dependencies": ["apt"],
        "apt_packages": "remmina remmina-plugin-vnc remmina-plugin-rdp remmina-plugin-secret",
    },
    {
        "slug": "ads-power",
        "name": "ADS Power",
        "version": "latest",
        "developer": "AdsPower",
        "official_url": "https://www.adspower.com/download",
        "summary": "Navegador antidetect para multiplos perfis e automacao.",
        "purpose": "Gestao de perfis de navegador para operacoes comerciais.",
        "keywords": ["ads", "adspower", "ads power", "antidetect", "browser"],
        "install_method": "deb",
        "dependencies": ["curl", "dpkg"],
        "download_url": "https://version.adspower.net/software/linux-x64-global/AdsPower-Global-5.12.28-x64.deb",
        "download_sha256": "",
        "deb_note": "Confira a URL mais recente em https://www.adspower.com/download antes de instalar.",
    },
]

ICON_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" role="img" aria-hidden="true">
  <rect width="64" height="64" rx="14" fill="#2563eb"/>
  <path d="M18 42V22h12c6 0 10 3 10 8s-4 8-10 8H26v4H18zm8-12h4c2.2 0 3.5-1 3.5-2.5S32.2 25 30 25h-4v5z" fill="#fff"/>
</svg>
"""

README_TEMPLATE = """# {name}

## Descricao

{summary}

## Finalidade

{purpose}

## Requisitos

- Linux Mint (64 bits)
- Conexao com a internet
- Permissao de administrador (sudo) para instalacao
- Dependencias: {deps}

## Instalacao automatica

```bash
cd {slug}
chmod +x install.sh
./install.sh
```

## Instalacao manual

1. Acesse o site oficial: {official_url}
2. Baixe a versao para Linux conforme indicado pelo fabricante.
3. Siga as instrucoes oficiais de instalacao.
4. Valide a integridade do arquivo quando checksum estiver disponivel em `install.json`.

## Atualizacao

Execute novamente `./install.sh` ou use os comandos em `install.json` (`update_commands`).

## Remocao

Consulte `install.json` (`remove_commands`) ou execute `./install.sh --uninstall` quando disponivel.

## Solucao de problemas

| Problema | O que fazer |
|----------|-------------|
| Download falhou | Verifique internet, proxy e URL oficial em `install.json`. |
| Permissao negada | Confirme senha sudo e usuario com privilegios de administrador. |
| Versao desatualizada | Atualize `download_url` / `version` em `install.json` a partir do site oficial. |
| Flatpak nao encontrado | Instale com `sudo apt install flatpak` e adicione Flathub. |

## Links oficiais

- Site: {official_url}
- Catalogo GS-Softwares: repositorio corporativo centralizado
"""


def install_sh(slug: str, item: dict) -> str:
    method = item["install_method"]
    if method == "flatpak":
        ref = item["flatpak_ref"]
        return f"""#!/bin/bash
set -euo pipefail
REF={json.dumps(ref)}
if ! command -v flatpak >/dev/null 2>&1; then
  echo "Instalando flatpak..." >&2
  sudo apt-get update -qq
  sudo DEBIAN_FRONTEND=noninteractive apt-get install -y flatpak
fi
flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo >/dev/null 2>&1 || true
flatpak install --noninteractive -y flathub "$REF"
echo "{item['name']} instalado via Flatpak"
"""
    if method == "apt":
        pkgs = item["apt_packages"]
        return f"""#!/bin/bash
set -euo pipefail
sudo apt-get update -qq
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y {pkgs}
echo "{item['name']} instalado via apt"
"""
    if method == "webapp":
        return """#!/bin/bash
set -euo pipefail
APP_NAME="WhatsApp Web"
APP_URL="https://web.whatsapp.com"
APP_ID="whatsapp-web"
DESKTOP_DIR="$HOME/.local/share/applications"
find_browser() {
  for path in /opt/google/chrome/google-chrome google-chrome google-chrome-stable chromium chromium-browser; do
    if command -v "$path" >/dev/null 2>&1; then command -v "$path"; return 0; fi
    [[ -x "$path" ]] && printf '%s\\n' "$path" && return 0
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
"""
    url = item.get("download_url", "")
    note = item.get("deb_note", "")
    sha = item.get("download_sha256", "")
    verify = ""
    if sha:
        verify = f'echo "{sha}  /tmp/gs-{slug}.deb" | sha256sum -c -'
    return f"""#!/bin/bash
set -euo pipefail
URL={json.dumps(url)}
TMP="/tmp/gs-{slug}.deb"
{("# " + note) if note else ""}
curl -fsSL --retry 3 --connect-timeout 30 -o "$TMP" "$URL"
{verify}
sudo dpkg -i "$TMP" || sudo apt-get install -f -y
rm -f "$TMP"
echo "{item['name']} instalado"
"""


def build_install_json(item: dict) -> dict:
    slug = item["slug"]
    method = item["install_method"]
    base = {
        "name": item["name"],
        "slug": slug,
        "version": item["version"],
        "developer": item["developer"],
        "official_url": item["official_url"],
        "install_method": method,
        "dependencies": item["dependencies"],
        "install_commands": [f"./{slug}/install.sh"],
        "remove_commands": [],
        "update_commands": [f"./{slug}/install.sh"],
        "download_urls": [],
    }
    if method == "flatpak":
        base["flatpak_ref"] = item["flatpak_ref"]
        base["remove_commands"] = [f"flatpak uninstall -y {item['flatpak_ref']}"]
        base["update_commands"] = [f"flatpak update -y {item['flatpak_ref']}"]
    elif method == "apt":
        base["apt_packages"] = item["apt_packages"]
        base["remove_commands"] = [
            f"sudo apt-get remove -y {item['apt_packages'].split()[0]}"
        ]
    elif method == "deb":
        base["download_urls"] = [item.get("download_url", "")]
        if item.get("download_sha256"):
            base["download_sha256"] = item["download_sha256"]
        base["remove_commands"] = [f"sudo apt-get remove -y {slug}"]
    elif method == "webapp":
        base["webapp_url"] = "https://web.whatsapp.com"
        base["remove_commands"] = ["rm -f $HOME/.local/share/applications/whatsapp-web.desktop"]
    return base


def build_metadata(item: dict) -> dict:
    return {
        "id": item["slug"],
        "slug": item["slug"],
        "name": item["name"],
        "version": item["version"],
        "developer": item["developer"],
        "official_url": item["official_url"],
        "description": item["summary"],
        "summary": item["summary"],
        "purpose": item["purpose"],
        "keywords": item["keywords"],
        "category": "corporate",
        "platform": "linux-mint",
        "install_method": item["install_method"],
        "icon": "downloads/icon.svg",
        "catalog_source": "GS-Softwares",
    }


def main() -> None:
    slugs = []
    for item in SOFTWARE:
        slug = item["slug"]
        slugs.append(slug)
        base = ROOT / slug
        (base / "downloads").mkdir(parents=True, exist_ok=True)
        (base / "downloads" / "icon.svg").write_text(ICON_SVG, encoding="utf-8")
        (base / "README.md").write_text(
            README_TEMPLATE.format(
                name=item["name"],
                summary=item["summary"],
                purpose=item["purpose"],
                deps=", ".join(item["dependencies"]),
                slug=slug,
                official_url=item["official_url"],
            ),
            encoding="utf-8",
        )
        (base / "install.json").write_text(
            json.dumps(build_install_json(item), ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        script = install_sh(slug, item)
        path = base / "install.sh"
        path.write_text(script, encoding="utf-8")
        path.chmod(0o755)
        (base / "metadata.json").write_text(
            json.dumps(build_metadata(item), ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    catalog = {
        "catalog_version": 1,
        "name": "GS-Softwares",
        "description": "Catalogo corporativo de softwares para Linux Mint",
        "software": slugs,
    }
    (ROOT / "catalog.json").write_text(
        json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Gerado catalogo com {len(slugs)} softwares em {ROOT}")


if __name__ == "__main__":
    main()
