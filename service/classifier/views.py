from django.shortcuts import render, redirect
from django.views import View, generic
from django.http import HttpRequest, HttpResponse

from celery import current_app

from utilities.tasks import classify_text, classify_document


class IndexView(generic.TemplateView):
    template_name = "classifier/index.html"


class ClassifyTextView(View):
    template_name: str = "classifier/text-classifier-page.html"

    def get(self, request: HttpRequest, format=None):
        id = request.GET.get("id", "")
        res = classify_text.AsyncResult(id)
        print(res.status)
        print(classify_text.ignore_result)
        return HttpResponse(render(request, self.template_name))

    def post(self, request: HttpRequest, format=None):
        text = request.POST["text"]
        genres = self.classifier.classify([text])[0]
        context = {"text": text, "genres": genres}
        return HttpResponse(render(request, self.template_name, context=context))


class ClassifyDocumentView(View):
    template_name: str = "classifier/document-classifier-page.html"

    def get(self, request: HttpRequest, format=None):
        return HttpResponse(render(request, self.template_name))

    def post(self, request: HttpRequest, format=None):
        file = request.FILES["document"]

        genres = classify_document(file)
        context = {"genres": genres, "document": file}
        return HttpResponse(render(request, self.template_name, context=context))
