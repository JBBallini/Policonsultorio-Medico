# turnos/models.py
from django.db import models
from pacientes.models import Paciente
from medicos.models import Medico

#Tabla de Turnos
class Turno(models.Model):
    id = models.AutoField(primary_key=True)

    fecha = models.DateField()
    hora = models.TimeField()
    estadoAsistencia = models.BooleanField(default=False)

    dniPaciente = models.ForeignKey(
        Paciente, 
        on_delete=models.CASCADE, 
        related_name='turnos'
    )

    dniMedico = models.ForeignKey(
        Medico, 
        on_delete=models.CASCADE, 
        related_name='turnos'
    )

    def __str__(self):
        return f"Turno {self.id} - {self.fecha} {self.hora}"

#Tabla de Pago
class Pago(models.Model):
    id = models.AutoField(primary_key=True)

    monto = models.DecimalField(max_digits=10, decimal_places=2)
    estadoPago = models.BooleanField(default=False)
    
    idTurno = models.OneToOneField(
        Turno, 
        on_delete=models.CASCADE, 
        related_name='pago'
    )
