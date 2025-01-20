# WebSiteToPDF
Converte todo o site para PDF

Primeiro deverá ser instalado o programa WkHtmlToPDF:

Windows
Download direto:
Acesse o site oficial: https://wkhtmltopdf.org/downloads.html

Baixe o instalador Windows (64 bits): wkhtmltox-x.x.x.msi (onde x.x.x é a versão)
Execute o instalador .msi

O instalador adicionará automaticamente o wkhtmltopdf ao PATH do sistema

Linux (Ubuntu/Debian)
Via apt:
sudo apt-get update
sudo apt-get install wkhtmltopdf


Linux (Fedora/RHEL)
sudo dnf install wkhtmltopdf


Após a instalação do wkhtmltopdf, você pode instalar as dependências Python do projeto:
pip install -r requirements.txt

