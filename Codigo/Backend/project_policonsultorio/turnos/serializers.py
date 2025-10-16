from rest_framework import serializers
from .models import Turno, Pago
from datetime import datetime, timedelta
from medicos.models import Horario
from datetime import datetime, timedelta, time
from django.utils.dateparse import parse_date

#Serializer de pago
class PagoSerializer(serializers.ModelSerializer):
    idTurno = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Pago
        fields = ["monto", "estadoPago", "idTurno"]

#Serializer registro de turno
class RegistroTurnoSerializer(serializers.ModelSerializer):
    monto = serializers.DecimalField(max_digits=10, decimal_places=2, write_only=True)

    class Meta:
        model = Turno
        fields = ["fecha", "hora", "dniPaciente", "dniMedico", "monto"]
    
    """
    Nota:
        Validamos que no haya turnos superpuestos para el mismo médico.
        Debe haber un intervalo de 20 min entre cada turno.
    """
    #Método para realizar las validaciones del registro
    def validate(self, data):
        medico = data.get("dniMedico")
        fecha = data.get("fecha")
        hora = data.get("hora")

        if not (medico and fecha and hora):
            return data

        #Creamos un objeto que contenga la fecha y hora del turno
        nuevo_dt = datetime.combine(fecha, hora)
        #Definimos los intervalos de 20 minutos entre turno y turno
        intervalo = timedelta(minutes=20)

        #Obtenemos todos los turnos del médico en la fecha dada
        instance_pk = getattr(self.instance, "pk", None)
        existentes = Turno.objects.filter(dniMedico=medico, fecha=fecha)
        if instance_pk:
            existentes = existentes.exclude(pk=instance_pk)

        #Compara el horario de cada turno con cada turno existente (evitamos que dos pacientes se asignen el mismo turno)
        for t in existentes:
            existente_dt = datetime.combine(t.fecha, t.hora)
            #Si hay una diferencia horaria menor a 20min, lanzamos error
            if abs((existente_dt - nuevo_dt)) < intervalo:
                raise serializers.ValidationError(
                    f"Horario no disponible: existe un turno a las {t.hora}. Deben respetarse {int(intervalo.total_seconds()/60)} minutos entre turnos."
                )
        return data

    """
        Modificamos el create del turno.
        Primero creamos el turno y luego le vinculamos el pago correspondiente
    """
    def create(self, validated_data):
        monto = validated_data.pop("monto")
        turno = Turno.objects.create(**validated_data)
        Pago.objects.create(idTurno=turno, monto=monto)
        return turno

#Serializer de turno
class TurnoSerializer(serializers.ModelSerializer):
    pago = PagoSerializer(read_only=True)

    class Meta:
        model = Turno
        fields = ["id", "fecha", "hora", "estadoAsistencia", "dniPaciente", "dniMedico", "pago"]
        #Campos no obligatorios
        extra_kwargs = {
            "dniPaciente": {"required": False},
            "dniMedico": {"required": False},
            "estadoAsistencia": {"required": False},
        }

    #Método para realizar las validaciones generales
    def validate(self, data):
        #Si es un nuevo turno, obtenemos los valores indicados, sino usa los actuales
        medico = data.get("dniMedico") or getattr(self.instance, "dniMedico", None)
        fecha = data.get("fecha") or getattr(self.instance, "fecha", None)
        hora = data.get("hora") or getattr(self.instance, "hora", None)

        if not (medico and fecha and hora):
            return data

        #Validamos que la fecha no puede ser anterior a la de hoy
        hoy = datetime.now().date()
        if fecha < hoy:
            raise serializers.ValidationError("No se puede asignar un turno en una fecha anterior a la de hoy.")

        #Comrpobamos que le médico trabaje el día seleccionado
        mapping = {0: "LUN", 1: "MAR", 2: "MIE", 3: "JUE", 4: "VIE", 5: "SAB", 6: "DOM"}
        dia_semana = mapping[fecha.weekday()]
        horarios = Horario.objects.filter(dniMedico=medico, diaSemana=dia_semana)
        if not horarios.exists():
            raise serializers.ValidationError("El médico no atiende en el día seleccionado.")

        #Validamos que el horario seleccionado esté dentro de los intervalos de atención del médico
        intervalos = []
        for h in horarios:
            inicio = datetime.combine(fecha, h.horaInicio)
            fin = datetime.combine(fecha, h.horaFin)
            actual = inicio
            while actual < fin:
                intervalos.append(actual.time())
                actual += timedelta(minutes=20)

        if hora not in intervalos:
            raise serializers.ValidationError("La hora seleccionada no corresponde a un intervalo válido de atención.")

        #Comrpobamos que no haya superposición de horario (se verifican los intervalos como se hizo anteriormente)
        nuevo_dt = datetime.combine(fecha, hora)
        intervalo = timedelta(minutes=20)

        instance_pk = getattr(self.instance, "pk", None)
        existentes = Turno.objects.filter(dniMedico=medico, fecha=fecha)
        if instance_pk:
            existentes = existentes.exclude(pk=instance_pk)

        for t in existentes:
            existente_dt = datetime.combine(t.fecha, t.hora)
            if abs((existente_dt - nuevo_dt)) < intervalo:
                raise serializers.ValidationError(
                    f"Horario no disponible: existe un turno a las {t.hora}. "
                    f"Deben respetarse {int(intervalo.total_seconds() / 60)} minutos entre turnos."
                )

        return data


