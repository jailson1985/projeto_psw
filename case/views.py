from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Brewery, ModelContagemCervejaria
from .serializers import BrewerySerializer, ModelContagemCervejariaSerializer
from drf_yasg.utils import swagger_auto_schema

class BreweryList(APIView):
    
    @swagger_auto_schema(
        operation_description="Retorna uma lista de todas as cervejarias",
        responses={200: BrewerySerializer(many=True)},
    )
    def get(self, request, format=None):
        breweries = Brewery.objects.all()
        serializer = BrewerySerializer(breweries, many=True)
        return Response(serializer.data)

class ModelContagemCervejariaList(APIView):
    
    @swagger_auto_schema(
        operation_description="Retorna a contagem de cervejarias por tipo e local",
        responses={200: ModelContagemCervejariaSerializer(many=True)},
    )
    def get(self, request, format=None):
        counts = ModelContagemCervejaria.objects.all()
        serializer = ModelContagemCervejariaSerializer(counts, many=True)
        return Response(serializer.data)