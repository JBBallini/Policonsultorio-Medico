from django.shortcuts import render

from rest_framework import viewsets
from .models import HistorialMedico, RegistroHistorial
from .serializers import HistorialMedicoSerializer, RegistroHistorialSerializer

#CRUD generado para los historiales asociados a los pacientes
class HistorialMedicoViewSet(viewsets.ModelViewSet):
    queryset = HistorialMedico.objects.all()
    serializer_class = HistorialMedicoSerializer

#CRUD generado para los registros de los historiales
class RegistroHistorialViewSet(viewsets.ModelViewSet):
    queryset = RegistroHistorial.objects.all()
    serializer_class = RegistroHistorialSerializer
