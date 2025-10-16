from rest_framework import serializers
from .models import Paciente, Responsable
from datetime import date
from django.utils.dateparse import parse_date

#Serializer para el responsable del paciente
class ResponsableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Responsable
        #Se exluye el campo paciente ya que esta automatizadada la relación en el paciente
        exclude = ['paciente']
        #Decimos que no es necesario el paciente al crear al responsable y las validaciones en el dni para evitar problemas al cambiarlo
        extra_kwargs = {
            "paciente": {"required": False},
            "dniResponsable": {"validators": []},
        }

#Serializer para el paciente
class PacienteSerializer(serializers.ModelSerializer):
    #Se crea al responsable con el serializer del mismo y decimos que no es requerido obligatoriamente
    responsable = ResponsableSerializer(required=False, allow_null=True)

    class Meta:
        model = Paciente
        fields = '__all__'

    #Validaciones que se realizan
    def validate(self, data):
        fecha_nacimiento = data.get("fechaNacimiento")
        responsable_data = self.initial_data.get("responsable")

        #Validamos que la fecha de nacimiento no sea mayor a la actual
        if fecha_nacimiento and isinstance(fecha_nacimiento, str):
            fecha_nacimiento = parse_date(fecha_nacimiento)
        if fecha_nacimiento and fecha_nacimiento > date.today():
            raise serializers.ValidationError("La fecha de nacimiento mayor a la de hoy.")

        #Calculamos la edad del paciente
        edad_paciente = (
            date.today().year
            - fecha_nacimiento.year
            - ((date.today().month, date.today().day) < (fecha_nacimiento.month, fecha_nacimiento.day))
        )

        #Validaciones que se realizan teniendo en cuenta el responsable y solo se hacen si existe responsable
        if responsable_data:
            dni_responsable = responsable_data.get("dniResponsable")
            fecha_resp = responsable_data.get("fechaNacimiento")

            #Validamos que la fecha de nacimiento no sea mayor a la actual del responsable
            if fecha_resp:
                if isinstance(fecha_resp, str):
                    fecha_resp = parse_date(fecha_resp)
                if not fecha_resp:
                    raise serializers.ValidationError("Fecha de nacimiento del responsable inválida.")
                if fecha_resp > date.today():
                    raise serializers.ValidationError("La fecha de nacimiento del responsable no puede ser posterior a hoy.")

                #Calculamos la edad del responsable y comprobamos que sea mayor de edad
                edad_responsable = (
                    date.today().year
                    - fecha_resp.year
                    - ((date.today().month, date.today().day) < (fecha_resp.month, fecha_resp.day))
                )
                if edad_responsable < 18:
                    raise serializers.ValidationError("El responsable debe ser mayor de edad.")

            #Comprobamos que el paciente el responsable no tengan el mismo DNI
            if dni_responsable == data.get("dniPaciente"):
                raise serializers.ValidationError("El responsable no puede tener el mismo DNI que el paciente.")

            #Comprobamos que el dni del responsable no coincida con el dni de un paciente existente en la BD
            if dni_responsable:
                if Paciente.objects.filter(dniPaciente=dni_responsable).exclude(dniPaciente=data.get("dniPaciente")).exists():
                    raise serializers.ValidationError(
                        "El responsable no puede tener un DNI que ya está registrado como paciente."
                    )

        #Obligamos a que si el paciente es menor de edad, se le deba asignar un responsable
        if edad_paciente < 18 and not responsable_data:
            raise serializers.ValidationError("Un paciente menor de edad debe tener un responsable.")

        return data

    #Método para el create
    def create(self, validated_data):
        #Quiamos al responsable
        responsable_data = validated_data.pop("responsable", None)
        #Creamos al paciente
        paciente = Paciente.objects.create(**validated_data)
        #Si tiene responsable, creamos al responsable y lo sumamos al paciente
        if responsable_data:
            Responsable.objects.create(paciente=paciente, **responsable_data)
        return paciente

    #Método para el update
    def update(self, instance, validated_data):
        #Quiamos al responsable
        responsable_data = validated_data.pop('responsable', None)
        #Realizamos las validaciones anteriores antes de actualizar
        validated_data_for_check = {**validated_data, "responsable": responsable_data}
        self.validate(validated_data_for_check)

        #Si se cambia el dni del paciente, lo eliminamos y creamos uno nuevo con el dni actualizado y el resto de datos guardados del eliminado
        new_dni = validated_data.get('dniPaciente', None)

        if new_dni and new_dni != instance.dniPaciente:
            old_dni = instance.dniPaciente
            paciente_data = {**validated_data}
            instance.delete()
            new_paciente = Paciente.objects.create(**paciente_data)

            if responsable_data:
                Responsable.objects.update_or_create(
                    paciente=new_paciente,
                    defaults=responsable_data
                )
            return new_paciente

        #Actualizamos al paciente actual
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        #Responsable en el update
        if responsable_data is not None:
            responsable_instance = getattr(instance, 'responsable', None)

            #Comprobamos si el paciente tiene responsable
            if responsable_instance:
                new_dni_resp = responsable_data.get("dniResponsable")
                #Si se cambia el dni del responsable, se realiza la misma lógica que el paciente
                if new_dni_resp and responsable_instance.dniResponsable != new_dni_resp:
                    responsable_instance.delete()
                    Responsable.objects.create(paciente=instance, **responsable_data)
                #Si no se cambia el dni, solo se actualizan los demas datos
                else:
                    for attr, value in responsable_data.items():
                        if attr == "dniResponsable":
                            continue
                        setattr(responsable_instance, attr, value)
                    responsable_instance.save()
            #Si no hay responsable, revisamos si hay uno con ese DNI en la BD
            else:
                dni_responsable = responsable_data.get("dniResponsable")
                existing_responsable = Responsable.objects.filter(dniResponsable=dni_responsable).first()
                #Si ese responsable ya existe, se reasigna al paciente actual
                if existing_responsable:
                    existing_responsable.paciente = instance
                    for attr, value in responsable_data.items():
                        setattr(existing_responsable, attr, value)
                    existing_responsable.save()
                #Si el paciente no tiene responsable, le creamos uno
                else:
                    Responsable.objects.create(paciente=instance, **responsable_data)

        return instance
