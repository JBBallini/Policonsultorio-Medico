from rest_framework import serializers
from .models import HistorialMedico, RegistroHistorial

class HistorialMedicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistorialMedico
        fields = '__all__'

class RegistroHistorialSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroHistorial
        fields = '__all__'