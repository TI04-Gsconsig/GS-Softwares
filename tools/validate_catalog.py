#!/usr/bin/env python3
"""Valida URLs e scripts do catalogo GS-Softwares."""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)


def curl_head(url: str) -> tuple[int, str]:
    result = subprocess.run(
        [
            "curl",
            "-sI",
            "-L",
            "-A",
            USER_AGENT,
            "--connect-timeout",
            "20",
            "--max-time",
            "60",
            url,
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    status = 0
    for line in (result.stdout or "").splitlines():
        if line.startswith("HTTP/"):
            try:
                status = int(line.split()[1])
            except (IndexError, ValueError):
                pass
    final_url = ""
    for line in reversed((result.stdout or "").splitlines()):
        if line.lower().startswith("location:"):
            final_url = line.split(":", 1)[1].strip()
            break
    return status, final_url


def validate_url(url: str) -> tuple[bool, str]:
    if not url:
        return False, "URL vazia"
    status, final_url = curl_head(url)
    if status in {200, 302}:
        note = f"HTTP {status}"
        if final_url:
            note += f" -> {final_url}"
        return True, note
    return False, f"HTTP {status or 'erro'}"


def load_catalog_slugs() -> list[str]:
    catalog = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))
    return [str(item) for item in catalog.get("software", [])]


def main() -> int:
    errors: list[str] = []
    checks: list[str] = []

    for slug in load_catalog_slugs():
        install_json = json.loads((ROOT / slug / "install.json").read_text(encoding="utf-8"))
        method = str(install_json.get("install_method", "")).strip().lower()
        install_sh = ROOT / slug / "install.sh"
        if not install_sh.is_file():
            errors.append(f"{slug}: install.sh ausente")
            continue

        script = install_sh.read_text(encoding="utf-8")
        if "sudo " in script and "gs_run_as_root" not in script and "id -u" not in script:
            errors.append(f"{slug}: install.sh usa sudo sem helper root-aware")

        if method == "deb":
            mode = str(install_json.get("download_mode", "")).strip().lower()
            urls = install_json.get("download_urls") if isinstance(install_json.get("download_urls"), list) else []
            if mode == "dynamic" or slug == "ads-power":
                ok, note = validate_url("https://www.adspower.net/download")
                checks.append(f"ads-power: pagina oficial -> {note}")
                if not ok:
                    errors.append("ads-power: pagina oficial inacessivel")
            elif not urls:
                errors.append(f"{slug}: deb sem download_urls")
            else:
                for url in urls:
                    ok, note = validate_url(str(url))
                    checks.append(f"{slug}: {url} -> {note}")
                    if not ok:
                        errors.append(f"{slug}: URL invalida ({note})")

        if method == "flatpak":
            ref = str(install_json.get("flatpak_ref", "")).strip()
            if not ref:
                errors.append(f"{slug}: flatpak sem flatpak_ref")

        if method == "apt":
            pkgs = str(install_json.get("apt_packages", "")).strip()
            if not pkgs:
                errors.append(f"{slug}: apt sem apt_packages")

        remove = install_json.get("remove_commands") if isinstance(install_json.get("remove_commands"), list) else []
        if not remove:
            errors.append(f"{slug}: remove_commands vazio")

    for line in checks:
        print(line)
    if errors:
        print("\nFalhas:", file=sys.stderr)
        for err in errors:
            print(f"- {err}", file=sys.stderr)
        return 1
    print(f"\nOK: {len(load_catalog_slugs())} softwares validados")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
