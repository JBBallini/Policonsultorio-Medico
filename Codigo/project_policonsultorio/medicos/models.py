# medico/models.py
from django.db import models
from usuarios.models import Usuario

class Medico(models.Model):
    dniMedico = models.CharField(max_length=20, primary_key=True)

    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    email = models.EmailField()
    especialidad = models.CharField(max_length=50)
    matricula = models.CharField(max_length=50)

    idUsuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        related_name='medico',
        null=True,
        blank=True
    )

    def __str__(self):
        return f"Dr. {self.apellido} ({self.especialidad})"


class Horario(models.Model):
    DIAS_SEMANA = [
        ('LUN', 'Lunes'),
        ('MAR', 'Martes'),
        ('MIE', 'Miércoles'),
        ('JUE', 'Jueves'),
        ('VIE', 'Viernes'),
    ]

    id = models.AutoField(primary_key=True)
    diaSemana = models.CharField(
        max_length=3,
        choices=DIAS_SEMANA,
        default='LUN' 
    )

    horaInicio = models.TimeField()
    horaFin = models.TimeField()

    dniMedico = models.ForeignKey(
        Medico,
        on_delete=models.CASCADE,
        related_name='horarios'
    )

    def __str__(self):
        return f"{self.get_diaSemana_display()} {self.horaInicio}-{self.horaFin}"
