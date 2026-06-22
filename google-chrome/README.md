# Google Chrome

## Descricao

Navegador web oficial do Google para Linux.

## Finalidade

Navegacao, apps web e compatibilidade corporativa.

## Requisitos

- Linux Mint (64 bits)
- Conexao com a internet
- Permissao de administrador (sudo) para instalacao
- Dependencias: curl, dpkg, apt

## Instalacao automatica

```bash
cd google-chrome
chmod +x install.sh
./install.sh
```

## Instalacao manual

1. Acesse o site oficial: https://www.google.com/chrome/
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

- Site: https://www.google.com/chrome/
- Catalogo GS-Softwares: repositorio corporativo centralizado
