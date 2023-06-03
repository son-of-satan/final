from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import authentication, permissions
from django.contrib.auth.models import User

from common.utilities import handle_text, handle_document, get_tasks


class ClassifyTextAPIView(APIView):
    def post(self, request: Request, format=None):
        name = request.data["name"]
        text = request.data["text"]
        user = request.user
        handle_text(name, text, user)
        return Response({"message": "ok"})


class ClassifyDocumentAPIView(APIView):
    def post(self, request: Request, format=None):
        file = request.FILES["document"]
        user = request.user
        handle_text(None, user, user)
        return Response({"message": "ok"})


class TasksAPIView(APIView):
    def get(self, request: Request, format=None):
        user = request.user
        return Response(get_tasks(user))

    def delete(self, request: Request, format=None):
        pass
