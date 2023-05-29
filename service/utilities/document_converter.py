import pandoc
from pdfminer.high_level import extract_text, extract_text_to_fp
import magic
import io
import re


class DocumentConverter:
    def __init__(self):
        self.converters = {
            "application/pdf": self._convert_pdf,
            "application/epub+zip": self._convert_epub,
        }

    def convert(self, filename):
        document_type = magic.from_file(filename, mime=True)
        return self.converters[document_type](filename)

    def _convert_pdf(self, filename):
        text = extract_text(filename)
        text = re.sub("\s+", " ", text)
        text.strip()
        return text

    def _convert_epub(self, filename):
        doc = pandoc.read(source=filename, format="epub")
        text = pandoc.write(doc, format="plain")
        return text


document_converter = DocumentConverter()
