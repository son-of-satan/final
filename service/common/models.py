from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    name = models.CharField(max_length=256)
    task_id = models.CharField(max_length=256)
    owner_id = models.OneToOneField(to=User, on_delete=models.CASCADE)
