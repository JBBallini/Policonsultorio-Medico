
from django.db import models
from usuarios.models import Usuario

class Paciente(models.Model):
    dniPaciente = models.CharField(max_length=20, primary_key=True)
    
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    email = models.EmailField()
    fechaNacimiento = models.DateField()
    direccion = models.TextField()
    tipoSangre = models.CharField(max_length=5)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Responsable(models.Model):
    dniResponsable = models.CharField(max_length=20, primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    email = models.EmailField()
    fechaNacimiento = models.DateField()
    direccion = models.TextField()
    tipoSangre = models.CharField(max_length=5)

    #Se define la relación 1 a 1 de Paciente a Responsable
    paciente = models.OneToOneField(
        Paciente, 
        on_delete=models.CASCADE,
        related_name='responsable'
    )