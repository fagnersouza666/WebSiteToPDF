# WebSiteToPDF

Uma ferramenta Python poderosa para converter sites completos em arquivos PDF, com suporte a navegação recursiva e processamento em paralelo.

## 🚀 Funcionalidades

- Converte páginas web para PDF mantendo a formatação original
- Navegação recursiva através dos links do site
- Processamento em paralelo para maior velocidade
- Compressão automática dos PDFs gerados
- Opção de juntar todos os PDFs em um único arquivo
- Suporte a configurações personalizadas de PDF

## 📋 Pré-requisitos

Antes de utilizar o projeto, você deve instalar o programa **WkHtmlToPDF** conforme o seu sistema operacional.

### Windows

1. Download direto:
   - Acesse o site oficial: [https://wkhtmltopdf.org/downloads.html](https://wkhtmltopdf.org/downloads.html)
   - Baixe o instalador Windows (64 bits): `wkhtmltox-x.x.x.msi` (onde `x.x.x` é a versão)
2. Execute o instalador `.msi`
3. O instalador adicionará automaticamente o `wkhtmltopdf` ao PATH do sistema

### Linux

#### Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install wkhtmltopdf
```

#### Fedora/RHEL
```bash
sudo dnf install wkhtmltopdf
```

## 🔧 Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/WebSiteToPDF.git
cd WebSiteToPDF
```

2. Instale as dependências Python:
```bash
pip install -r requirements.txt
```

## 💻 Como Usar

### Uso Básico

```python
from webtopdf import WebToPDF

# Inicialize o conversor
converter = WebToPDF(
    base_url="https://exemplo.com",  # URL base do site
    docs_path="/docs",               # Caminho inicial para começar a conversão
    output_dir="pdfs",              # Diretório onde os PDFs serão salvos
    processes=4                      # Número de processos paralelos
)

# Execute a conversão
converter.run()
```

### Funcionalidades Adicionais

1. Comprimir PDFs individualmente:
```python
converter.compress_pdf("arquivo.pdf", quality="medium")  # Qualidade: low, medium, high
```

2. Comprimir todos os PDFs gerados:
```python
converter.compress_all_pdfs()
```

3. Juntar todos os PDFs em um único arquivo:
```python
converter.merge_all_pdfs()  # Gera 'documentacao_completa.pdf'
```

## 📦 Dependências Principais

- beautifulsoup4: Para análise de HTML
- pdfkit: Conversão de HTML para PDF
- PyPDF2: Manipulação de arquivos PDF
- requests: Requisições HTTP
- tqdm: Barras de progresso

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests.

