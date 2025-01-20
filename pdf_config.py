from dataclasses import dataclass


@dataclass
class PDFConfig:
    """Configuração para geração de PDFs"""

    options: dict = None

    def __post_init__(self):
        self.options = {
            "quiet": "",
            "enable-local-file-access": None,
            "encoding": "UTF-8",
            "no-outline": None,
            "disable-javascript": None,
        }
