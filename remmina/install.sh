#!/bin/bash
set -euo pipefail
sudo apt-get update -qq
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y remmina remmina-plugin-vnc remmina-plugin-rdp remmina-plugin-secret
echo "Remmina instalado via apt"
