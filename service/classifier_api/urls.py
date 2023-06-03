#!/usr/bin/env python3

from django.urls import path

from . import views

app_name = "classifier_api"
urlpatterns = [
    path("tasks", views.TasksAPIView.as_view(), name="tasks"),
    path("text", views.ClassifyTextAPIView.as_view(), name="text"),
    path("document", views.ClassifyDocumentAPIView.as_view(), name="document"),
]
