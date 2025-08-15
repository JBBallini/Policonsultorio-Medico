from django.shortcuts import render

from rest_framework import viewsets
from .models import HistorialMedico, RegistroHistorial
from .serializers import HistorialMedicoSerializer, RegistroHistorialSerializer

class HistorialMedicoViewSet(viewsets.ModelViewSet):
    queryset = HistorialMedico.objects.all()
    serializer_class = HistorialMedicoSerializer

class RegistroHistorialViewSet(viewsets.ModelViewSet):
    queryset = RegistroHistorial.objects.all()
    serializer_class = RegistroHistorialSerializer
