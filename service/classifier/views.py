from binascii import b2a_base64
from django.shortcuts import render, redirect
from django.views import View, generic
from django.http import HttpRequest, HttpResponse

import base64

from celery import current_app
from django_celery_results.models import TaskResult

from common.tasks import classify_text, classify_document
from .forms import ClassifyTextForm, ClassifyDocumentForm


class IndexView(generic.TemplateView):
    template_name = "classifier/index.html"


class ClassifyTextView(View):
    template_name: str = "classifier/text-classifier-page.html"

    def get(self, request: HttpRequest, format=None):
        form = ClassifyTextForm()
        context = {"form": form}

        # id = request.GET.get("id", None)
        # context = {}
        # if id:
        #     res = classify_text.AsyncResult(id)
        #     if res.ready():
        #         context = {"genres": res.get()}
        #     else:
        #         context = {"in_progress": True}
        # else:
        #     pass

        return render(request, self.template_name, context=context)

    def post(self, request: HttpRequest, format=None):
        form = ClassifyTextForm(request.POST)
        if form.is_valid():
            return redirect("classifier:tasks")

        context = {"form": form}
        return render(request, self.template_name, context=context)

        # text = request.POST["text"]
        # res = classify_text.apply_async(kwargs={"text": text})
        # return redirect(f"/text?id={res.task_id}")


class ClassifyDocumentView(View):
    template_name: str = "classifier/document-classifier-page.html"

    def get(self, request: HttpRequest, format=None):
        id = request.GET.get("id", None)
        context = {}
        if id:
            res = classify_text.AsyncResult(id)
            if res.ready():
                context = {"genres": res.get()}
            else:
                context = {"in_progress": True}
        else:
            pass

        return HttpResponse(render(request, self.template_name, context=context))

    def post(self, request: HttpRequest, format=None):
        file = request.FILES["document"]
        res = classify_document.apply_async(
            kwargs={"contents": base64.b64encode(file.read()).decode()}
        )
        return redirect(f"/document?id={res.task_id}")


class TasksView(View):
    template_name: str = "classifier/results-page.html"

    def get(self, request: HttpRequest, format=None):
        context = {"results": TaskResult.objects.all()}
        return HttpResponse(render(request, self.template_name, context=context))
