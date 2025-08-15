
from django.db import models
from pacientes.models import Paciente
from medicos.models import Medico

#Tabla Historial Médico
class HistorialMedico(models.Model):
    id = models.AutoField(primary_key=True)

    dniPaciente = models.ForeignKey(
        Paciente, 
        on_delete=models.CASCADE, 
        related_name='historiales'
    )

    def __str__(self):
        return f"Historial de {self.dniPaciente}"

#Tabla Registro Historial
class RegistroHistorial(models.Model):
    id = models.AutoField(primary_key=True)

    fecha = models.DateField()
    observaciones = models.TextField()

    idHistorial = models.ForeignKey(
        HistorialMedico, 
        on_delete=models.CASCADE, 
        related_name='registros'
    )

    dniMedico = models.ForeignKey(
        Medico, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='registros'
    )
