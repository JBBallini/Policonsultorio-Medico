# turnos/serializers.py
from rest_framework import serializers
from .models import Turno, Pago
from pacientes.models import Paciente  # Para relaciones
from medicos.models import Medico      # Para relaciones

class TurnoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turno
        fields = '__all__'  # Incluye todos los campos del modelo

    # Opcional: Mostrar nombres de paciente y médico en la respuesta (en lugar de solo DNI)
    def to_representation(self, instance):
        response = super().to_representation(instance)
        # Datos del paciente
        response['paciente'] = {
            'nombre': instance.dniPaciente.nombre,
            'apellido': instance.dniPaciente.apellido
        }
        # Datos del médico
        response['medico'] = {
            'nombre': instance.dniMedico.nombre,
            'apellido': instance.dniMedico.apellido,
            'especialidad': instance.dniMedico.especialidad
        }
        return response

class PagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pago
        fields = '__all__'

    # Opcional: Mostrar detalles del turno asociado al pago
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['turno'] = {
            'fecha': instance.idTurno.fecha,
            'hora': instance.idTurno.hora,
            'medico': instance.idTurno.dniMedico.nombre + " " + instance.idTurno.dniMedico.apellido
        }
        return response