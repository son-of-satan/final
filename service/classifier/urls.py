from django.urls import path

from . import views
from utilities.classifier import classifier
from utilities.document_converter import document_converter


app_name = "classifier"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("text", views.ClassifyTextView.as_view(classifier=classifier), name="text"),
    path(
        "file",
        views.ClassifyFileView.as_view(
            classifier=classifier, document_converter=document_converter
        ),
        name="file",
    ),
]
