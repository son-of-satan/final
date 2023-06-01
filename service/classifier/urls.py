from django.urls import path

from . import views

app_name = "classifier"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("text", views.ClassifyTextView.as_view(), name="text"),
    path("document", views.ClassifyDocumentView.as_view(), name="document"),
    path("tasks", views.TasksView.as_view(), name="tasks"),
]
