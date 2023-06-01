import tempfile
import base64

from celery import shared_task

from .classifier import Classifier
from .document_converter import DocumentConverter

classifier = Classifier("./data/model.pth", None, "./data/vocab.pth")
document_converter = DocumentConverter()


@shared_task()
def classify_text(text=None):
    genres = classifier.classify(text)[0]
    return genres


@shared_task()
def classify_document(contents=None):
    temp = tempfile.NamedTemporaryFile()
    temp.write(base64.b64decode(contents))
    temp.flush()

    text = document_converter.convert(temp.name)
    genres = classifier.classify(text)[0]
    return genres
