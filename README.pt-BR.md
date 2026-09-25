# WiGlyph

Uma aplicação desktop privada e multiplataforma para compartilhar acesso a redes Wi-Fi por meio de QR codes.

O WiGlyph gera localmente QR codes compatíveis com redes Wi-Fi, permitindo compartilhar credenciais sem precisar digitar manualmente o nome da rede ou a senha. A aplicação foi projetada para oferecer um fluxo rápido no desktop, sem contas, serviços externos, telemetria ou armazenamento permanente de credenciais.

**[English](README.md) | Português (Brasil)**

![Prévia da aplicação WiGlyph](.github/assets/wiglyph-preview.png)

## Funcionalidades

- Geração de QR codes para redes WPA, WEP e abertas
- Suporte a redes ocultas
- Cópia do QR code gerado diretamente para a área de transferência
- Exportação de QR codes como imagens PNG
- Histórico temporário com até cinco redes geradas recentemente
- Restauração de QR codes anteriores durante a sessão atual
- Invalidação automática de QR codes desatualizados quando as configurações da rede são alteradas
- Processamento totalmente local e offline
- Interface desktop nativa desenvolvida com Qt
- Suporte a Windows e Linux

## Privacidade

O WiGlyph processa as credenciais de Wi-Fi inteiramente no dispositivo local.

A aplicação não:

- envia credenciais para serviços externos;
- exige conta ou autenticação;
- utiliza ferramentas de análise ou telemetria;
- persiste senhas de Wi-Fi ou configurações de rede entre sessões.

O histórico é mantido apenas em memória durante a sessão atual da aplicação. Ao fechar o WiGlyph, ele é descartado.

Os QR codes gerados contêm, por natureza, as credenciais de Wi-Fi necessárias para conexão à rede. Portanto, QR codes salvos ou copiados devem ser tratados com o mesmo cuidado que as próprias credenciais.

## Download

Os binários pré-compilados são distribuídos por meio da página de Releases do GitHub.

### Windows

Baixe:

```text
WiGlyph-2.0.0-windows-x86_64-setup.exe
```

Execute o instalador normalmente. O WiGlyph é instalado para o usuário atual e não exige privilégios de administrador.

### Linux

Baixe:

```text
WiGlyph-2.0.0-linux-x86_64.AppImage
```

Torne o AppImage executável:

```bash
chmod +x WiGlyph-2.0.0-linux-x86_64.AppImage
```

Depois, execute:

```bash
./WiGlyph-2.0.0-linux-x86_64.AppImage
```

Nenhuma instalação global do Python ou Qt é necessária para nenhuma das distribuições.

## Desenvolvimento

### Requisitos

- Python 3.11 ou superior
- Git

Clone o repositório:

```bash
git clone https://github.com/arthurcfranklin/wiglyph.git
cd wiglyph
```

Crie um ambiente virtual:

```bash
python -m venv .venv
```

Ative-o no Linux:

```bash
source .venv/bin/activate
```

Ou no Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Instale o projeto com as dependências de desenvolvimento e build:

```bash
python -m pip install --upgrade pip
python -m pip install -e ".[dev,build]"
```

Execute o WiGlyph a partir do código-fonte:

```bash
python -m wiglyph
```

## Testes

Execute a suíte automatizada de testes:

```bash
python -m pytest -q
```

Valide a sintaxe Python:

```bash
python -m compileall -q src tests packaging
```

## Build

O WiGlyph utiliza o PyInstaller para criar bundles independentes da aplicação.

Faça o build utilizando a especificação do projeto:

```bash
python -m PyInstaller --clean --noconfirm WiGlyph.spec
```

### Windows

O instalador para Windows é criado a partir do bundle do PyInstaller utilizando o Inno Setup e a configuração localizada em:

```text
packaging/windows/WiGlyph.iss
```

### Linux

As versões para Linux são distribuídas como AppImages. A configuração do AppDir está localizada em:

```text
packaging/linux/
```

O build reproduzível para Linux é automatizado por meio de:

```text
.github/workflows/build-linux.yml
```

Os AppImages de release são gerados no ambiente de CI, em vez de um sistema de desenvolvimento rolling release.

## Estrutura do Projeto

```text
wiglyph/
├── .github/
│   ├── assets/
│   └── workflows/
├── assets/
│   └── icons/
├── packaging/
│   ├── linux/
│   ├── windows/
│   └── launcher.py
├── src/
│   └── wiglyph/
│       ├── core/
│       ├── ui/
│       └── utils/
├── tests/
├── pyproject.toml
├── README.md
├── README.pt-BR.md
└── WiGlyph.spec
```

## Tecnologias

O WiGlyph é desenvolvido com:

- Python
- PySide6 / Qt 6
- qrcode
- Pillow
- PyInstaller
- AppImage
- Inno Setup

## Versão

Versão atual: `2.0.0`

## Licença

O WiGlyph é licenciado sob a [Licença MIT](LICENSE).

Copyright © 2026 Arthur Franklin.
