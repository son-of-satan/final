from django.shortcuts import render, redirect
from django.views import View, generic
from django.http import HttpRequest, HttpResponse

from django_celery_results.models import TaskResult
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.authtoken.models import Token

from common.tasks import classify_text, classify_document
from common.utilities import handle_document, handle_text, get_tasks
from .forms import ClassifyTextForm, ClassifyDocumentForm


class IndexView(generic.TemplateView):
    template_name = "classifier/index.html"


class ClassifyTextView(LoginRequiredMixin, View):
    template_name: str = "classifier/classify-text-page.html"

    def get(self, request: HttpRequest, format=None):
        form = ClassifyTextForm()
        context = {"form": form}
        return render(request, self.template_name, context=context)

    def post(self, request: HttpRequest, format=None):
        form = ClassifyTextForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            text = form.cleaned_data["text"]

            user = request.user
            handle_text(name, text, user)

            return redirect("classifier:tasks")

        context = {"form": form}
        return render(request, self.template_name, context=context)


class ClassifyDocumentView(LoginRequiredMixin, View):
    template_name: str = "classifier/classify-document-page.html"

    def get(self, request: HttpRequest, format=None):
        form = ClassifyDocumentForm()
        context = {"form": form}
        return render(request, self.template_name, context=context)

    def post(self, request: HttpRequest, format=None):
        form = ClassifyDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data["name"]
            document = request.FILES["document"]
            user = request.user

            handle_document(name, document, user)

            return redirect("classifier:tasks")

        context = {"form": form}
        return render(request, self.template_name, context=context)


class TasksView(LoginRequiredMixin, View):
    template_name: str = "classifier/tasks-page.html"

    def get(self, request: HttpRequest, format=None):
        user = request.user
        tasks = get_tasks(user)
        context = {"tasks": tasks}
        return render(request, self.template_name, context=context)


class RegenerateTokenView(LoginRequiredMixin, View):
    template_name: str = "classifier/regenerate-token-page.html"

    def get(self, request: HttpRequest, format=None):
        user = request.user
        try:
            Token.objects.get(user=user).delete()
        except:
            pass

        token = Token.objects.create(user=user)

        context = {"token": token}
        return render(request, self.template_name, context=context)
