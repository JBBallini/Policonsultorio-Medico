
from rest_framework import serializers
from .models import Medico, Horario
from usuarios.models import Usuario

class HorarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Horario
        fields = ["diaSemana","horaInicio", "horaFin"]

class MedicoSerializer(serializers.ModelSerializer):
    # Eliminamos idUsuario de los campos obligatorios y permitimos registrar un médico con varios horarios
    horarios = HorarioSerializer(many=True, required=False)

    class Meta:
        model = Medico
        fields = [
            "dniMedico",
            "nombre",
            "apellido",
            "telefono",
            "email",
            "especialidad",
            "matricula",
            "horarios"
        ]

    #Realizamos un overwrite del create de médicos para crearlos con sus horarios de trabajo (el médico se crea con lista de horarios)
    def create(self, validated_data):
        horarios_data = validated_data.pop('horarios', [])
        medico = Medico.objects.create(**validated_data)
        for horario in horarios_data:
            Horario.objects.create(dniMedico=medico, **horario)
        return medico

