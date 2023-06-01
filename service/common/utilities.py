from django.contrib.auth.models import User
from django.core.files.uploadedfile import UploadedFile
from celery.utils.serialization import base64encode

# from celery import celery_app
from django_celery_results.models import TaskResult

import json

from rest_framework import status
from .tasks import classify_text, classify_document
from .models import Task


def handle_text(name: str, text: str, user: User):
    truncated_text = text if len(text) < 64 else f"{text[61]}..."
    name = name if name else truncated_text

    result = classify_text.apply_async(kwargs={"text": text})
    result = TaskResult.objects.get(task_id=result.task_id)

    task = Task(name=name, result=result, owner=user)
    task.save()


def handle_document(name: str, document: UploadedFile, user: User):
    name = name if name else document.name
    contents = base64encode(document.read()).decode()

    result = classify_document.apply_async(kwargs={"contents": contents})
    result = TaskResult.objects.get(task_id=result.task_id)

    task = Task(name=name, result=result, owner=user)
    task.save()


def get_tasks(user: User):
    tasks = Task.objects.filter(owner=user)
    ret = []
    for task in tasks:
        name = task.name
        id = task.result.task_id
        status = task.result.status
        result = task.result.result
        genres = json.loads(result) if result else None

        ret.append(
            {
                "name": name,
                "id": id,
                "status": status,
                "result": genres,
            }
        )

    return ret
