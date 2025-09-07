from django.shortcuts import render
from rest_framework import viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.dateparse import parse_date
from datetime import datetime, timedelta
from django.db import transaction

from .models import Turno, Pago
from .serializers import TurnoSerializer, PagoSerializer, RegistroTurnoSerializer
from medicos.models import Medico, Horario
from pacientes.models import Paciente

import calendar


class TurnoViewSet(viewsets.ModelViewSet):
    queryset = Turno.objects.all()
    serializer_class = TurnoSerializer

    @action(detail=False, methods=["get"], url_path="disponibilidad")
    def disponibilidad(self, request):
        medico_id = request.query_params.get("medico")
        fecha = request.query_params.get("fecha")

        if not medico_id or not fecha:
            return Response({"error": "Se requiere medico y fecha"}, status=400)

        fecha = parse_date(fecha)
        try:
            medico = Medico.objects.get(dniMedico=medico_id)
        except Medico.DoesNotExist:
            return Response({"error": "El médico no existe"}, status=404)

        #Días de la semana a usar
        mapping = {
            0: "LUN", 1: "MAR", 2: "MIE", 3: "JUE", 4: "VIE", 5: "SAB", 6: "DOM"
        }
        dia_semana = mapping[fecha.weekday()]

        horarios = Horario.objects.filter(dniMedico=medico, diaSemana=dia_semana)
        if not horarios.exists():
            return Response({"error": "El médico no atiende en ese día"}, status=400)

        # Generar intervalos de 20 minutos
        intervalos = []
        for h in horarios:
            inicio = datetime.combine(fecha, h.horaInicio)
            fin = datetime.combine(fecha, h.horaFin)
            actual = inicio
            while actual < fin:
                intervalos.append(actual.time())
                actual += timedelta(minutes=20)

        turnos_ocupados = Turno.objects.filter(
            dniMedico=medico,
            fecha=fecha
        ).values_list("hora", flat=True)

        disponibles = [hora.strftime("%H:%M") for hora in intervalos if hora not in turnos_ocupados]

        return Response({
            "fecha": fecha,
            "diaSemana": dia_semana,
            "medico": f"{medico.nombre} {medico.apellido}",
            "especialidad": medico.especialidad,
            "disponibles": disponibles
        })


# Registro de turno con validaciones
class RegistroTurnoView(generics.CreateAPIView):
    queryset = Turno.objects.all()
    serializer_class = RegistroTurnoSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        medico = serializer.validated_data["dniMedico"]
        paciente = serializer.validated_data["dniPaciente"]
        fecha = serializer.validated_data["fecha"]
        hora = serializer.validated_data["hora"]

        # Validar que el paciente este registrado
        if not Paciente.objects.filter(dniPaciente=paciente.dniPaciente).exists():
            return Response({"error": "El paciente no se encuentra registrado en el sistema"}, status=400)

        # Validar que no esté ocupado el horario seleccionado
        if Turno.objects.filter(dniMedico=medico, fecha=fecha, hora=hora).exists():
            return Response({"error": "El horario seleccionado ya está ocupado"}, status=400)

        #Validamos los días de la semana
        mapping = {0: "LUN", 1: "MAR", 2: "MIE", 3: "JUE", 4: "VIE", 5: "SAB", 6: "DOM"}
        dia_semana = mapping[fecha.weekday()]

        horarios = Horario.objects.filter(dniMedico=medico, diaSemana=dia_semana)
        if not horarios.exists():
            return Response({"error": "El médico no atiende en ese día"}, status=400)

        # Generar intervalos válidos de 20min
        intervalos = []
        for h in horarios:
            inicio = datetime.combine(fecha, h.horaInicio)
            fin = datetime.combine(fecha, h.horaFin)
            actual = inicio
            while actual < fin:
                intervalos.append(actual.time())
                actual += timedelta(minutes=20)

        # Validar que la hora solicitada esté en los intervalos de 20min
        if hora not in intervalos:
            return Response(
                {"error": "La hora seleccionada no corresponde a un intervalo válido de 20 minutos"},
                status=400
            )

        # Si esta todo bien, crea el turno
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)


class PagoViewSet(viewsets.ModelViewSet):
    queryset = Pago.objects.all()
    serializer_class = PagoSerializer

    # GET /api/pagos/por-turno/{idTurno}/ (Para ver los pagos por turno)
    @action(detail=False, methods=["get"], url_path="por-turno/(?P<id_turno>[^/.]+)")
    def por_turno(self, request, id_turno=None):
        try:
            pago = Pago.objects.get(idTurno=id_turno)
            serializer = self.get_serializer(pago)
            return Response(serializer.data)
        except Pago.DoesNotExist:
            return Response({"error": "No existe un pago asociado a ese turno"}, status=404)

    # POST /api/pagos/{idPago}/registrar-pago/
    @action(detail=True, methods=["post"], url_path="registrar-pago")
    def registrar_pago(self, request, pk=None):
        try:
            pago = self.get_object()
            pago.estadoPago = True
            pago.save()
            return Response({"message": "Pago registrado correctamente", "pago": self.get_serializer(pago).data})
        except Exception as e:
            return Response({"error": str(e)}, status=400)
