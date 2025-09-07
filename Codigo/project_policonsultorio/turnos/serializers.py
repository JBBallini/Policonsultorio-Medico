
# turnos/serializers.py
from rest_framework import serializers
from .models import Turno, Pago
from datetime import datetime, timedelta

class PagoSerializer(serializers.ModelSerializer):
    idTurno = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Pago
        fields = ["monto", "estadoPago", "idTurno"]

class RegistroTurnoSerializer(serializers.ModelSerializer):
    monto = serializers.DecimalField(max_digits=10, decimal_places=2, write_only=True)

    class Meta:
        model = Turno
        fields = ["fecha", "hora", "dniPaciente", "dniMedico", "monto"]
    
    def validate(self, data):
        medico = data.get("dniMedico")
        fecha = data.get("fecha")
        hora = data.get("hora")

        if not (medico and fecha and hora):
            return data

        nuevo_dt = datetime.combine(fecha, hora)
        intervalo = timedelta(minutes=20)

        # Excluir instancia actual si es update
        instance_pk = getattr(self.instance, "pk", None)
        existentes = Turno.objects.filter(dniMedico=medico, fecha=fecha)
        if instance_pk:
            existentes = existentes.exclude(pk=instance_pk)

        for t in existentes:
            existente_dt = datetime.combine(t.fecha, t.hora)
            if abs((existente_dt - nuevo_dt)) < intervalo:
                raise serializers.ValidationError(
                    f"Horario no disponible: existe un turno a las {t.hora}. Deben respetarse {int(intervalo.total_seconds()/60)} minutos entre turnos."
                )
        return data

    def create(self, validated_data):
        monto = validated_data.pop("monto")
        turno = Turno.objects.create(**validated_data)
        Pago.objects.create(idTurno=turno, monto=monto)
        return turno

class TurnoSerializer(serializers.ModelSerializer):
    pago = PagoSerializer(read_only=True)

    class Meta:
        model = Turno
        fields = ["fecha", "hora", "estadoAsistencia", "dniPaciente", "dniMedico", "pago"]

    # Aplica misma validación para creaciones/updates directas via /api/turnos/
    def validate(self, data):
        medico = data.get("dniMedico") or getattr(self.instance, "dniMedico", None)
        fecha = data.get("fecha") or getattr(self.instance, "fecha", None)
        hora = data.get("hora") or getattr(self.instance, "hora", None)

        if not (medico and fecha and hora):
            return data

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
                    f"Horario no disponible: existe un turno a las {t.hora}. Deben respetarse {int(intervalo.total_seconds()/60)} minutos entre turnos."
                )
        return data
