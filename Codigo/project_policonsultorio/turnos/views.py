from django.shortcuts import render

# turnos/views.py
from rest_framework import viewsets
from .models import Turno, Pago
from .serializers import TurnoSerializer, PagoSerializer

class TurnoViewSet(viewsets.ModelViewSet):
    queryset = Turno.objects.all()
    serializer_class = TurnoSerializer

    # Filtrar turnos por paciente o médico (opcional)
    def get_queryset(self):
        queryset = super().get_queryset()
        dni_paciente = self.request.query_params.get('dni_paciente')
        dni_medico = self.request.query_params.get('dni_medico')
        
        if dni_paciente:
            queryset = queryset.filter(dniPaciente=dni_paciente)
        if dni_medico:
            queryset = queryset.filter(dniMedico=dni_medico)
        return queryset

class PagoViewSet(viewsets.ModelViewSet):
    queryset = Pago.objects.all()
    serializer_class = PagoSerializer
