# WebSiteToPDF

Converte todo o site para PDF.

## Pré-requisitos

Antes de utilizar o projeto, você deve instalar o programa **WkHtmlToPDF** conforme o seu sistema operacional.

### Windows

1. Download direto:
   - Acesse o site oficial: [https://wkhtmltopdf.org/downloads.html](https://wkhtmltopdf.org/downloads.html)
   - Baixe o instalador Windows (64 bits): `wkhtmltox-x.x.x.msi` (onde `x.x.x` é a versão).
2. Execute o instalador `.msi`.
3. O instalador adicionará automaticamente o `wkhtmltopdf` ao PATH do sistema.

### Linux

#### Ubuntu/Debian

Via `apt`:
```bash
sudo apt-get update
sudo apt-get install wkhtmltopdf
```

#### Fedora/RHEL

Via `dnf`:
```bash
sudo dnf install wkhtmltopdf
```

## Instalando as dependências Python

Após a instalação do **wkhtmltopdf**, instale as dependências Python do projeto:

```bash
pip install -r requirements.txt
