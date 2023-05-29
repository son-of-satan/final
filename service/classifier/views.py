from copy import Error
from re import template
import tempfile
from django.shortcuts import render
from django.views import View, generic
from django.http import HttpRequest, HttpResponse

from utilities.classifier import Classifier
from utilities.document_converter import DocumentConverter


class IndexView(generic.TemplateView):
    template_name = "classifier/index.html"


class ClassifyTextView(View):
    template_name: str = "classifier/text-classifier-page.html"
    classifier: Classifier = None

    def __init__(self, classifier: Classifier, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.classifier: Classifier = classifier

    def get(self, request: HttpRequest, format=None):
        return HttpResponse(render(request, self.template_name))

    def post(self, request: HttpRequest, format=None):
        text = request.POST["text"]
        genres = self.classifier.classify([text])[0]
        context = {"text": text, "genres": genres}
        return HttpResponse(render(request, self.template_name, context=context))


class ClassifyFileView(View):
    template_name: str = "classifier/document-classifier-page.html"
    classifier: Classifier = None
    document_converter: DocumentConverter = None

    def __init__(
        self,
        classifier: Classifier,
        document_converter: DocumentConverter,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.classifier: Classifier = classifier
        self.document_converter: DocumentConverter = document_converter

    def get(self, request: HttpRequest, format=None):
        return HttpResponse(render(request, self.template_name))

    def post(self, request: HttpRequest, format=None):
        file = request.FILES["document"]
        temp = tempfile.NamedTemporaryFile()
        for chunk in file.chunks():
            temp.write(chunk)
        temp.flush()

        try:
            text = self.document_converter.convert(temp.name)
        except:
            context = {}
            return HttpResponse(render(request, self.template_name, context=context))

        genres = self.classifier.classify(text)
        context = {"genres": genres, "document": file}
        return HttpResponse(render(request, self.template_name, context=context))
