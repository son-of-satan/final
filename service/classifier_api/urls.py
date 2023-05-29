#!/usr/bin/env python3

from django.urls import path

from . import views

from utilities.classifier import classifier
from utilities.document_converter import document_converter

app_name = "classifier_api"
urlpatterns = [
    path("text", views.ClassifyTextAPIView.as_view(classifier=classifier), name="text"),
    path(
        "document",
        views.ClassifyDocumentAPIView.as_view(
            classifier=classifier, document_converter=document_converter
        ),
        name="document",
    ),
]
