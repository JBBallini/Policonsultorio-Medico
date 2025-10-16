
from rest_framework import serializers
from .models import Usuario
from .models import Administrador, Secretario

#Registro de usuarios, no agregamos el campo id como parte del registro.
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ["username", "password", "rol"]
        #La contraseña es writeonly para no retornala en alguna response
        extra_kwargs = {
            "password": {"write_only": True}
        }

    #Hacemos un overwrite del create para validar los datos y encriptar las contraseñas
    def create(self, validated_data):
        password = validated_data.pop("password")
        usuario = Usuario(**validated_data)
        #Encripta contraseña
        usuario.set_password(password)
        usuario.save()
        return usuario

class AdministradorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Administrador
        fields = "__all__"

class SecretarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Secretario
        fields = "__all__"
