from django.shortcuts import render

from rest_framework import viewsets
from .models import Paciente, Responsable
from .serializers import PacienteSerializer, ResponsableSerializer

class PacienteViewSet(viewsets.ModelViewSet):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer

class ResponsableViewSet(viewsets.ModelViewSet):
    queryset = Responsable.objects.all()
    serializer_class = ResponsableSerializer
