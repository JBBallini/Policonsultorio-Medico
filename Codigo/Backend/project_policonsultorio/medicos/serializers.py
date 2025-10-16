
from rest_framework import serializers
from .models import Medico, Horario

#Serializer de los horarios
class HorarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Horario
        fields = ["diaSemana", "horaInicio", "horaFin"]

#Serializer de los médicos
class MedicoSerializer(serializers.ModelSerializer):
    #Al horario de los médicos le asignamos el serializer de horarios
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

    #Función que realiza las validaciones necesarias
    def validate(self, data):
        horarios = data.get('horarios', [])
        combinaciones = set()
        horarios_por_dia = {}

        for h in horarios:
            dia = h.get('diaSemana')
            inicio = h.get('horaInicio')
            fin = h.get('horaFin')

            #Comprobamos que la hora de inicio y fin no sean la misma
            if inicio == fin:
                raise serializers.ValidationError(
                    f"El horario de {dia} tiene la misma hora de inicio y fin."
                )
            
            #Comprobamos que la hora de inicio no sea mayor a la hora de fin
            if inicio > fin:
                raise serializers.ValidationError(
                    f"El horario de {dia} tiene una hora de inicio posterior a la hora de fin."
                )

            #Comrpobamos que no haya dias con horarios duplicados
            clave = (dia, inicio, fin)
            if clave in combinaciones:
                raise serializers.ValidationError(
                    f"El horario del día {dia} con el mismo rango ya fue agregado."
                )
            combinaciones.add(clave)

            #Se agrupan los horarios por dia
            if dia not in horarios_por_dia:
                horarios_por_dia[dia] = []
            horarios_por_dia[dia].append((inicio, fin))

        #Luego verificamos que no haya horarios dentro del mismo dia que esten solapados/superpuestos entre sí
        for dia, rangos in horarios_por_dia.items():
            rangos.sort()
            for i in range(1, len(rangos)):
                prev_fin = rangos[i - 1][1]
                curr_inicio = rangos[i][0]
                if curr_inicio < prev_fin:
                    raise serializers.ValidationError(
                        f"Los horarios del día {dia} se solapan entre {rangos[i - 1][0]}-{prev_fin} y {curr_inicio}-{rangos[i][1]}."
                    )

        return data
    
    #Método para el create
    def create(self, validated_data):
        horarios_data = validated_data.pop('horarios', [])
        #Se crea al médico
        medico = Medico.objects.create(**validated_data)
        #Agregamos la lista de horarios al médico
        for horario in horarios_data:
            Horario.objects.create(dniMedico=medico, **horario)
        return medico

    #Método para el update
    def update(self, instance, validated_data):
        horarios_data = validated_data.pop('horarios', None)
        nuevo_dni = validated_data.get('dniMedico', instance.dniMedico)

        #En caso de que se cambie el DNI del médico, borramos el médico actual y creamos uno nuevo
        if nuevo_dni != instance.dniMedico:
            instance.delete()
            nuevo_medico = Medico.objects.create(**validated_data)
            #Reasignamos los horarios
            if horarios_data:
                for horario in horarios_data:
                    Horario.objects.create(dniMedico=nuevo_medico, **horario)
            return nuevo_medico

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        #Si hay nuevos horarios para asignar, se borran los anteriores y se asignan los nuevos
        if horarios_data is not None:
            instance.horarios.all().delete()
            for horario in horarios_data:
                Horario.objects.create(dniMedico=instance, **horario)

        return instance

    #Método provisorio para probar JSON
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["horarios"] = HorarioSerializer(instance.horarios.all(), many=True).data
        return representation
