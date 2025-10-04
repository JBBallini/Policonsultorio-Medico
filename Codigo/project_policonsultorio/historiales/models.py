
from django.db import models
from pacientes.models import Paciente
from medicos.models import Medico

#Entidad del Historial médico de un paciente
class HistorialMedico(models.Model):
    id = models.AutoField(primary_key=True)

    #Relacion 1 a 1 del historial médico con el paciente
    dniPaciente = models.OneToOneField(
        Paciente, 
        on_delete=models.CASCADE,
        related_name='historial'
    )

    def __str__(self):
        return f"Historial de {self.dniPaciente}"

#Entidad del Registro Historial donde se guardarán las observaciones del médico
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