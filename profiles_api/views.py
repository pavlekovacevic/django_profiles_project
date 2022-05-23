from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response


class HelloApiView(APIView):
    """Test Api View"""

    def get(self, request, format=None):
        """Returns a list of ApiView features"""
        an_apiview = [
            "Uses http methods as functions(get, post, patch, put, delete)",
            "Is similar to a traditional Django view",
            "Gives you the most control over the app logic",
            "Is mapped manually to URLs"
        ]

        return Response({'message':'Hello', 'an_apiview':an_apiview})