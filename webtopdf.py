import os
import requests
from bs4 import BeautifulSoup
import pdfkit
from urllib.parse import urljoin, urlparse
from multiprocessing import Pool, Manager
from tqdm import tqdm
import time
from PyPDF2 import PdfReader, PdfWriter
import logging
from typing import List, Tuple, Optional
from pathlib import Path
from pdf_config import PDFConfig


class WebToPDF:
    IGNORED_EXTENSIONS = {".css", ".js", ".png", ".jpg", ".jpeg", ".gif", ".svg"}

    def __init__(
        self,
        base_url: str,
        docs_path: str,
        output_dir: str = "pdfsite",
        processes: int = 4,
    ):
        self.base_url = base_url.rstrip("/")
        self.docs_path = docs_path
        self.output_dir = Path(output_dir)
        self.processes = processes
        self.pdf_config = PDFConfig()

        self._setup_logger()
        self._setup_output_dir()

    """Configura o logger da aplicação"""

    def _setup_logger(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    """Cria o diretório de saída se não existir"""

    def _setup_output_dir(self) -> None:
        self.output_dir.mkdir(parents=True, exist_ok=True)

    """Verifica se a URL é válida para processamento"""

    def is_valid_url(self, url: str) -> bool:
        if not url.startswith(self.base_url):
            return False
        return not any(url.lower().endswith(ext) for ext in self.IGNORED_EXTENSIONS)

    """Salva uma página como PDF"""

    def save_page_as_pdf(self, url: str) -> Optional[str]:
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()

            clean_filename = (
                url.replace(self.base_url, "").replace("/", "_").strip("_") or "index"
            )
            output_file = self.output_dir / f"{clean_filename}.pdf"

            pdfkit.from_url(url, str(output_file), options=self.pdf_config.options)
            return url
        except Exception as e:
            self.logger.error(f"Erro ao processar {url}: {str(e)}")
            return None

    """Obtém todos os links válidos de uma página"""

    def get_page_links(self, url: str) -> List[str]:
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            base_domain = urlparse(self.base_url).netloc

            return [
                self.normalize_url(link["href"], url)
                for link in soup.find_all("a", href=True)
                if self._is_valid_link(link["href"])
                and urlparse(self.normalize_url(link["href"], url)).netloc
                == base_domain
            ]
        except Exception as e:
            self.logger.error(f"Erro ao obter links de {url}: {e}")
            return []

    """Verifica se o link é válido para processamento"""

    def _is_valid_link(self, href: str) -> bool:
        return href and not href.startswith(("#", "mailto:", "tel:"))

    """Normaliza URLs relativas para absolutas"""

    @staticmethod
    def normalize_url(url: str, current_url: str) -> str:
        full_url = urljoin(current_url, url)
        parsed = urlparse(full_url)
        return f"{parsed.scheme}://{parsed.netloc}{parsed.path}".rstrip("/")

    """Processa um lote de URLs"""

    def _process_url_batch(
        self,
        pool: Pool,
        current_batch: List[str],
        urls_to_process: List[str],
        visited: List[str],
        successful_pdfs: Manager,
    ) -> None:
        self.logger.info("Gerando PDFs...")
        results = list(
            tqdm(
                pool.imap_unordered(self.save_page_as_pdf, current_batch),
                total=len(current_batch),
            )
        )
        successful_pdfs.value += sum(1 for r in results if r is not None)

        self.logger.info("Obtendo links...")
        new_links = list(
            tqdm(
                pool.imap_unordered(self.get_page_links, current_batch),
                total=len(current_batch),
            )
        )

        for links in new_links:
            new_urls = [link for link in links if link not in visited]
            urls_to_process.extend(new_urls)

    """Processa URLs em paralelo"""

    def process_urls_parallel(self) -> Tuple[int, int]:
        with Manager() as manager:
            visited = manager.list()
            urls_to_process = manager.list([f"{self.base_url}{self.docs_path}"])
            successful_pdfs = manager.Value("i", 0)

            with Pool(processes=self.processes) as pool:
                while urls_to_process:
                    current_batch = self._get_next_batch(urls_to_process, visited)
                    if not current_batch:
                        continue

                    self._process_url_batch(
                        pool, current_batch, urls_to_process, visited, successful_pdfs
                    )
                    time.sleep(0.1)

            return len(visited), successful_pdfs.value

    """Obtém o próximo lote de URLs para processamento"""

    def _get_next_batch(
        self, urls_to_process: List[str], visited: List[str], batch_size: int = 10
    ) -> List[str]:
        batch = []
        while urls_to_process and len(batch) < batch_size:
            url = urls_to_process.pop(0)
            if url not in visited and self.is_valid_url(url):
                visited.append(url)
                batch.append(url)
        return batch

    """Comprime um arquivo PDF"""

    def compress_pdf(self, input_path: str, quality: str = "medium") -> bool:
        try:
            reader = PdfReader(input_path)
            writer = PdfWriter()

            for page in reader.pages:
                writer.add_page(page)

            if quality == "low":
                writer.compress_content_streams()
            elif quality == "medium":
                writer.compress_content_streams(level=6)
            else:
                writer.compress_content_streams(level=4)

            output_path = input_path.replace(".pdf", "_compressed.pdf")
            with open(output_path, "wb") as output_file:
                writer.write(output_file)

            os.replace(output_path, input_path)
            return True
        except Exception as e:
            self.logger.error(f"Erro ao comprimir {input_path}: {str(e)}")
            return False

    """Comprime todos os PDFs no diretório de saída"""

    def compress_all_pdfs(self) -> int:
        self.logger.info("Comprimindo PDFs gerados...")
        pdf_files = [f for f in os.listdir(self.output_dir) if f.endswith(".pdf")]

        compressed = 0
        for pdf in tqdm(pdf_files, desc="Comprimindo"):
            if self.compress_pdf(os.path.join(self.output_dir, pdf)):
                compressed += 1

        return compressed

    """Junta todos os PDFs em um único arquivo"""

    def merge_all_pdfs(self) -> bool:
        self.logger.info("Juntando todos os PDFs em um único arquivo...")
        pdf_files = [f for f in os.listdir(self.output_dir) if f.endswith(".pdf")]

        if not pdf_files:
            self.logger.warning("Nenhum PDF encontrado para juntar")
            return False

        try:
            merger = PdfWriter()
            for pdf in tqdm(pdf_files, desc="Juntando PDFs"):
                pdf_path = os.path.join(self.output_dir, pdf)
                merger.append(pdf_path)

            output_path = os.path.join(self.output_dir, "documentacao_completa.pdf")
            with open(output_path, "wb") as output_file:
                merger.write(output_file)

            self.logger.info(f"PDF final salvo em: {output_path}")
            return True
        except Exception as e:
            self.logger.error(f"Erro ao juntar PDFs: {str(e)}")
            return False

    """Executa todo o processo"""

    def run(self) -> None:
        self.logger.info(f"Iniciando processamento paralelo de {self.base_url}")
        total_urls, total_pdfs = self.process_urls_parallel()

        compressed_pdfs = self.compress_all_pdfs()
        merge_success = self.merge_all_pdfs()

        self.logger.info("Processamento concluído!")
        self.logger.info(f"Total de URLs visitadas: {total_urls}")
        self.logger.info(f"Total de PDFs gerados com sucesso: {total_pdfs}")
        self.logger.info(f"Total de PDFs comprimidos: {compressed_pdfs}")
        if merge_success:
            self.logger.info("PDFs unidos com sucesso em um único arquivo!")


if __name__ == "__main__":
    converter = WebToPDF(
        base_url="dominio_do_site",  # exemplo: https://web3-ethereum-defi.readthedocs.io
        docs_path="/caminho_para_a_documentação",  # exemplo: /api/
        output_dir="diretorio_de_saida",
        processes=4,
    )
    converter.run()
