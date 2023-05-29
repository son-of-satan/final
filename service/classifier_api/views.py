from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import authentication, permissions
from django.contrib.auth.models import User

from utilities.classifier import Classifier
from utilities.document_converter import DocumentConverter

import tempfile


class ClassifyTextAPIView(APIView):
    classifier = None

    def __init__(self, classifier: Classifier, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.classifier = classifier

    def post(self, request: Request, format=None):
        text = request.data["text"]
        genres = self.classifier.classify([text])[0]
        return Response({"message": "ok", "genres": genres})


class ClassifyDocumentAPIView(APIView):
    classifier = None
    document_converter = None

    def __init__(
        self,
        classifier: Classifier,
        document_converter: DocumentConverter,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.classifier = classifier
        self.document_converter = document_converter

    def post(self, request: Request, format=None):
        file = request.FILES
        temp = tempfile.NamedTemporaryFile()
        for chunk in file.chunks():
            temp.write(chunk)
        temp.flush()

        try:
            text = self.document_converter.convert(temp.name)
        except:
            return Response({"message": "invalid file"}, status=500)

        genres = self.classifier.classify(text)
        return Response({"message": "ok", "genres": genres})
