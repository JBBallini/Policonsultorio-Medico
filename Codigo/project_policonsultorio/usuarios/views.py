from django.shortcuts import render

from rest_framework import viewsets
from .models import Usuario, Administrador, Secretario
from .serializers import UsuarioSerializer, AdministradorSerializer, SecretarioSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class AdministradorViewSet(viewsets.ModelViewSet):
    queryset = Administrador.objects.all()
    serializer_class = AdministradorSerializer

class SecretarioViewSet(viewsets.ModelViewSet):
    queryset = Secretario.objects.all()
    serializer_class = SecretarioSerializer