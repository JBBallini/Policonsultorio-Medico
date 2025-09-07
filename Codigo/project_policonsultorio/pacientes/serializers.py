
from rest_framework import serializers
from .models import Paciente, Responsable
from datetime import date

class ResponsableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Responsable
        fields = '__all__'

        #Al crear un paciente, el responsable no lo hacemos obligatorio
        extra_kwargs = {
            "paciente": {"required": False}
        }

class PacienteSerializer(serializers.ModelSerializer):
    responsable = ResponsableSerializer(required=False)

    class Meta:
        model = Paciente
        fields = '__all__'

    # Creamos un paciente y, a la par, un responsable (registro de pacientes)
    def create(self, validated_data):
        responsable_data = validated_data.pop("responsable", None)
        paciente = Paciente.objects.create(**validated_data)

        if responsable_data:
            Responsable.objects.create(paciente=paciente, **responsable_data)

        return paciente

    #Comprobamos si el paciente es menor de edad para saber si hay que asignar un paciente
    def validate(self, data):
        fecha_nacimiento = data.get("fechaNacimiento")
        responsable = self.initial_data.get("responsable")

        if fecha_nacimiento:
            edad = (date.today() - fecha_nacimiento).days // 365
            if edad < 18 and not responsable:
                raise serializers.ValidationError(
                    "Un paciente menor de edad debe tener un responsable."
                )
        return data
