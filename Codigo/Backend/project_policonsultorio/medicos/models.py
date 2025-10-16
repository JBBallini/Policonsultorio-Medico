# medico/models.py
from django.db import models
from usuarios.models import Usuario

#Entidad del médico
class Medico(models.Model):
    dniMedico = models.CharField(max_length=20, primary_key=True)

    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    email = models.EmailField()
    especialidad = models.CharField(max_length=50)
    matricula = models.CharField(max_length=50)

    #Relacion 1 a 1 entre Médico y Usuario
    idUsuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        related_name='medico',
        null=True,
        blank=True
    )

    def __str__(self):
        return f"Dr. {self.apellido} ({self.especialidad})"

#Modelo del horario de cada médico con los días restringidos y elección de un rango horario
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
        #Choices se usa, en este caso, para decir que días tomar
        choices=DIAS_SEMANA,
        default='LUN' 
    )

    #Rango Horario de trabajo
    horaInicio = models.TimeField()
    horaFin = models.TimeField()

    #Relación 1 a N de entre médico y horarios
    dniMedico = models.ForeignKey(
        Medico,
        on_delete=models.CASCADE,
        related_name='horarios'
    )

    def __str__(self):
        return f"{self.get_diaSemana_display()} {self.horaInicio}-{self.horaFin}"
