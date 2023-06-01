from django.db import models
from django.contrib.auth.models import User
from django_celery_results.models import TaskResult


class Task(models.Model):
    name = models.CharField(max_length=256)
    result = models.OneToOneField(to=TaskResult, on_delete=models.CASCADE)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
