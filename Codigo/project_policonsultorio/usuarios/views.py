from django.shortcuts import render

# usuarios/views.py
from rest_framework import viewsets
from .models import Usuario, Administrador, Secretario
from .serializers import UsuarioSerializer, AdministradorSerializer, SecretarioSerializer

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class AdministradorViewSet(viewsets.ModelViewSet):
    queryset = Administrador.objects.all()
    serializer_class = AdministradorSerializer

class SecretarioViewSet(viewsets.ModelViewSet):
    queryset = Secretario.objects.all()
    serializer_class = SecretarioSerializer
