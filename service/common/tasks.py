import tempfile
import base64

from celery import states, shared_task
from celery.signals import before_task_publish
from django_celery_results.models import TaskResult

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


@before_task_publish.connect
def create_task_result_on_publish(sender=None, headers=None, body=None, **kwargs):
    if "task" not in headers:
        return

    TaskResult.objects.store_result(
        "application/json",
        "utf-8",
        headers["id"],
        None,
        states.PENDING,
        task_name=headers["task"],
        task_args=headers["argsrepr"],
        task_kwargs=headers["kwargsrepr"],
    )
