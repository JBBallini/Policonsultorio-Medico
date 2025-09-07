from django.shortcuts import render

from rest_framework import viewsets
from .models import Paciente, Responsable
from .serializers import PacienteSerializer, ResponsableSerializer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

class PacienteViewSet(viewsets.ModelViewSet):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer

class ResponsableViewSet(viewsets.ModelViewSet):
    queryset = Responsable.objects.all()
    serializer_class = ResponsableSerializer

#Creamos una vista para el registro de paciente que luego utilizaremos para un endpoint
class RegistroPacienteView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PacienteSerializer(data=request.data)
        if serializer.is_valid():
            paciente = serializer.save()
            return Response(
                {"message": "Paciente registrado correctamente", "data": serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
