from django.shortcuts import render, redirect
from django.views import View, generic
from django.http import HttpRequest, HttpResponse

import base64

from celery import current_app

from utilities.tasks import classify_text, classify_document


class IndexView(generic.TemplateView):
    template_name = "classifier/index.html"


class ClassifyTextView(View):
    template_name: str = "classifier/text-classifier-page.html"

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
        text = request.POST["text"]
        res = classify_text.apply_async(args=[text])
        return redirect(f"/text?id={res.task_id}")


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
        contents = base64.b64encode(file.read()).decode()
        res = classify_document.apply_async(args=[contents])
        return redirect(f"/document?id={res.task_id}")
