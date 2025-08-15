from django.shortcuts import render

from rest_framework import viewsets
from .models import Medico, Horario
from .serializers import MedicoSerializer, HorarioSerializer

class MedicoViewSet(viewsets.ModelViewSet):
    queryset = Medico.objects.all()
    serializer_class = MedicoSerializer

class HorarioViewSet(viewsets.ModelViewSet):
    queryset = Horario.objects.all()
    serializer_class = HorarioSerializer

    # Filtrar horarios por médico (opcional)
    def get_queryset(self):
        queryset = super().get_queryset()
        dni_medico = self.request.query_params.get('dni_medico')
        if dni_medico:
            queryset = queryset.filter(dniMedico=dni_medico)
        return queryset
