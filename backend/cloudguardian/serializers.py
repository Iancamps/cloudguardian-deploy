# Los serializadores conviertes de datos de python en JSON y viceversa

from rest_framework import serializers
from django.contrib.auth.models import User

class UserRegisterSerializer(serializers.ModelSerializer): # Creamos una clase UserRegisterSerializer que hereda de serializers.ModelSerializer. Este tipo de serializador nos permite convertir modelos de Django en JSON y viceversa de manera sencilla
    password = serializers.CharField(write_only=True) # para que no se muestre en las respuestas JSON por seguridad

    class Meta:
        model = User # modelo a usar
        fields = ['username', 'password'] # campos del modelo a usar

    def create(self, validated_data): # metodo que se ejecuta cuando el serializador crea un usuario
        user = User.objects.create_user(**validated_data) # Llamamos al método create_user del modelo User, que automáticamente cifra la contraseña antes de guardarla
        return user
