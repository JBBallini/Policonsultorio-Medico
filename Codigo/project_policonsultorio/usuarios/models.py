
from django.db import models

class Rol(models.TextChoices):
    MEDICO = 'MEDICO', 'Médico'
    SECRETARIO = 'SECRETARIO', 'Secretario'
    ADMINISTRADOR = 'ADMINISTRADOR', 'Administrador'

class Usuario(models.Model):
    id = models.AutoField(primary_key=True)
    
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)
    rol = models.CharField(max_length=15, choices=Rol.choices)

    def __str__(self):
        return f"{self.username} ({self.rol})"

# Clases para Administrador y Secretario
class Administrador(models.Model):
    dniAdministrador = models.CharField(max_length=20, primary_key=True)

    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    email = models.EmailField()

    #PK con usuario
    idUsuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        related_name='administrador'
    )

    def __str__(self):
        return f"Admin: {self.nombre} {self.apellido}"

class Secretario(models.Model):
    dniSecretario = models.CharField(max_length=20, primary_key=True)

    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    email = models.EmailField()

    #PK con usuario
    idUsuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        related_name='secretario'
    )

    def __str__(self):
        return f"Secretario: {self.nombre} {self.apellido}"
