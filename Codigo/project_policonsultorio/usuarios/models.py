
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

#Creamos un usuario personalizado que haga de admin inicial del sistema
class UsuarioManager(BaseUserManager):
    def create_user(self, username, password=None, rol=None, **extra_fields):
        if not username:
            raise ValueError("El usuario debe tener un nombre de usuario")
        user = self.model(username=username, rol=rol, **extra_fields)
        #Hacemos un "Hash" de la contraseña
        user.set_password(password)
        user.save(using=self._db)
        return user

    #Definimos como va a ser el administrador ya que será el encargado de dar de alta usuarios
    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("rol", "ADMINISTRADOR")
        user = self.create_user(username, password, **extra_fields)
        #Permisos totales en Django (son campos en la tabla Usuario)
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)
        return user
    
#Roles que se podrán obtener en el sistema
class Rol(models.TextChoices):
    MEDICO = 'MEDICO', 'Médico'
    SECRETARIO = 'SECRETARIO', 'Secretario'
    ADMINISTRADOR = 'ADMINISTRADOR', 'Administrador'

#Entindad Usuario
#Hereda de AbstractBaseUser y PermissionsMixin para la autenticación
class Usuario(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    
    username = models.CharField(max_length=50, unique=True)
    rol = models.CharField(max_length=15, choices=Rol.choices)

    #Le asignamos al Usuario los mismos campos que el admin pero el "staff" queda en false
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UsuarioManager()

    #Se indica que el login a la aplicación se debe realizar con un username y un rol ya que son campos obligatorios
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["rol"]

    def __str__(self):
        return f"{self.username} ({self.rol})"

#Entidad para Administrador
class Administrador(models.Model):
    dniAdministrador = models.CharField(max_length=20, primary_key=True)

    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    email = models.EmailField()

    #Relación 1 a 1 del Administrador con Usuario
    idUsuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        related_name='administrador'
    )

    def __str__(self):
        return f"Admin: {self.nombre} {self.apellido}"

#Entidad para Secretario
class Secretario(models.Model):
    dniSecretario = models.CharField(max_length=20, primary_key=True)

    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    email = models.EmailField()

    #Relación 1 a 1 del Secretario con Usuario
    idUsuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        related_name='secretario'
    )

    def __str__(self):
        return f"Secretario: {self.nombre} {self.apellido}"
    
    """
        CONSIDERACIONES PARA LA CREACIÓN DE USUARIOS PARA REALIZAR PRUEBAS EN POSTMAN

        Debemos crear un "superuser" para tener un rol de administrador y poder hacer pruebas:
        python manage.py createsuperuser

        En POSTMAN realizamos un POST a http://127.0.0.1:8000/api/token/ con el JSON
        {
            "username": "superusuarioCreado",
            "password": "contraseñaCreada"
        }

        Esto retorna un "refresh" y un "access", el access se usará para realizar las demás peticiones.

        Luego, si queremos crear un Médico o un Secretario hacemos POST a http://127.0.0.1:8000/api/usuarios/ y en
        Headers agregamos:
            Authorization: Bearer "access que obtuvimos"
            Content-Type: application/json
        y en el JSON creamos el usuario:
        {
            "username": "medicoUser",
            "password": "1231231",
            "rol": "MEDICO"
        }
    """
