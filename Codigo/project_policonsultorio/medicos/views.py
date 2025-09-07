from django.shortcuts import render

from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import MedicoSerializer, HorarioSerializer
from .models import Medico, Horario

class MedicoViewSet(viewsets.ModelViewSet):
    queryset = Medico.objects.all()
    serializer_class = MedicoSerializer

# Endpoint personalizado para registrar médicos
class RegistroMedicoView(APIView):
    def post(self, request):
        serializer = MedicoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Médico registrado correctamente", "medico": serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Registro de horarios
class HorarioViewSet(viewsets.ModelViewSet):
    queryset = Horario.objects.all()
    serializer_class = HorarioSerializer

    # Filtrar horarios por médico
    def get_queryset(self):
        queryset = super().get_queryset()
        dni_medico = self.request.query_params.get('dni_medico')
        if dni_medico:
            queryset = queryset.filter(dniMedico=dni_medico)
        return queryset


