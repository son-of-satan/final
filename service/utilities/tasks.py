import tempfile

from celery import shared_task

from .classifier import Classifier
from .document_converter import DocumentConverter

classifier = Classifier("./data/model.pth", None, "./data/vocab.pth")
document_converter = DocumentConverter()


@shared_task()
def classify_text(text):
    genres = classifier.classify([text])[0]
    return genres


@shared_task()
def classify_document(file):
    temp = tempfile.NamedTemporaryFile()
    for chunk in file.chunks():
        temp.write(chunk)
    temp.flush()

    text = document_converter.convert(temp.name)
    genres = classifier.classify(text)

    return genres
