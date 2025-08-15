
from rest_framework import serializers
from .models import Usuario, Administrador, Secretario

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}  # No mostrar en respuestas

class AdministradorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Administrador
        fields = '__all__'

class SecretarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Secretario
        fields = '__all__'