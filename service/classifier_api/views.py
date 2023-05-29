from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import authentication, permissions
from django.contrib.auth.models import User

from utilities.tasks import classify_text, classify_document


class ClassifyTextAPIView(APIView):
    def post(self, request: Request, format=None):
        text = request.data["text"]
        genres = classify_text(text)
        return Response({"message": "ok", "genres": genres})


class ClassifyDocumentAPIView(APIView):
    def post(self, request: Request, format=None):
        file = request.FILES["document"]
        genres = classify_document(file)
        return Response({"message": "ok", "genres": genres})
