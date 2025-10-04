
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
    #Se agrega un campo paciente que puede estar vacío
    responsable = ResponsableSerializer(required=False)

    class Meta:
        model = Paciente
        fields = '__all__'

    """
        Realizamos un overwrite al create.
        Lo que haremos será tomar los datos del responsable, si es que se creó.
        Se crea al paciente, luego si tiene responsable se crea un objeto "responsable" y se lo agrega
        al campo "responsable" del paciente.
    """
    # Creamos un paciente y, a la par, un responsable (registro de pacientes)
    def create(self, validated_data):
        responsable_data = validated_data.pop("responsable", None)
        paciente = Paciente.objects.create(**validated_data)

        if responsable_data:
            Responsable.objects.create(paciente=paciente, **responsable_data)

        return paciente

    #Función que calcula la edad del paciente para saber si es menor y requiere responsable
    def validate(self, data):
        fecha_nacimiento = data.get("fechaNacimiento")
        responsable = self.initial_data.get("responsable")

        if fecha_nacimiento:
            edad = (date.today() - fecha_nacimiento).days
            #Si el paciente es menor y no posee responsable, lanza error
            if edad < 18 and not responsable:
                raise serializers.ValidationError(
                    "Un paciente menor de edad debe tener un responsable."
                )
        return data
