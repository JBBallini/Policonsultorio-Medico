# medico/models.py
from django.db import models
from usuarios.models import Usuario

#Tabla Medico
class Medico(models.Model):
    dniMedico = models.CharField(max_length=20, primary_key=True)

    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    email = models.EmailField()
    especialidad = models.CharField(max_length=50)
    matricula = models.CharField(max_length=50)

    #ForeignKey de Mecido con Usuario
    idUsuario = models.OneToOneField(  
        Usuario,
        on_delete=models.CASCADE,
        related_name='medico'
    )

    def __str__(self):
        return f"Dr. {self.apellido} ({self.especialidad})"

#Tabla Horario
class Horario(models.Model):
    id = models.AutoField(primary_key=True)

    horaInicio = models.TimeField()
    horaFin = models.TimeField()

    dniMedico = models.ForeignKey(
        Medico, 
        on_delete=models.CASCADE, 
        related_name='horarios'
    )
