from django.shortcuts import render

from rest_framework import viewsets
from .models import Usuario, Administrador, Secretario
from .serializers import UsuarioSerializer, AdministradorSerializer, SecretarioSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics, permissions


#CRUD para Usuario
class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

    #Modificamos los permisos para crear el primer admin del sistema y que no necesite permisos
    def get_permissions(self):
        if self.action == "create":
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

#CRUD para Administrador
class AdministradorViewSet(viewsets.ModelViewSet):
    queryset = Administrador.objects.all()
    serializer_class = AdministradorSerializer

#CRUD para Medico
class SecretarioViewSet(viewsets.ModelViewSet):
    queryset = Secretario.objects.all()
    serializer_class = SecretarioSerializer

class CambiarPasswordView(generics.UpdateAPIView):
    """
    Permite al usuario autenticado cambiar su contraseña.
    Inicialmente, el usuario tendrá su contraseña igual a su DNI.
    Luego, podrá modificarla usando este endpoint.
    """
    queryset = Usuario.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    #Modificamos el update para actualizar la contraseña, se requiere la vieja y una nueva contraseña
    def update(self, request, *args, **kwargs):
        usuario = request.user
        vieja_password = request.data.get("vieja_password")
        nueva_password = request.data.get("nueva_password")

        #Comprobamos que la contraseña vieja sea correcta, sino error
        if not vieja_password or not nueva_password:
            return Response(
                {"error": "Debe proporcionar la contraseña actual y la nueva."},
                status=status.HTTP_400_BAD_REQUEST
            )

        #Verificar la contraseña anterior
        if not usuario.check_password(vieja_password):
            return Response(
                {"error": "La contraseña actual es incorrecta."},
                status=status.HTTP_400_BAD_REQUEST
            )

        #Realizamos el cambio de contraseña por la nueva
        usuario.set_password(nueva_password)
        usuario.save()

        return Response(
            {"success": "Contraseña actualizada correctamente."},
            status=status.HTTP_200_OK
        )