# Serializers
from rest_framework import serializers
from rest_framework.validators import ValidationError
from rest_framework.authtoken.models import Token
from .models import User


class SignUpSerializer(serializers.ModelSerializer):
    # email = models.EmailField(unique=True)
    # username = models.CharField(max_length=45)

    # Define un campo para el email que debe ser único
    email = serializers.EmailField(max_length=50)
    # Define un campo para la contraseña que solo se puede escribir y es obligatorio
    password = serializers.CharField(write_only=True, required=True, min_length=8)

    class Meta:
        # Especifica el modelo al que se refiere este serializador
        model = User
        # Define los campos que deben ser incluidos en la representación del modelo
        fields = ["username", "email", "password"]

    def validate(self, attrs):
        # Verifica si ya existe un usuario con el mismo email
        email_exists = User.objects.filter(email=attrs["email"]).exists()

        # Si el email ya está registrado, lanza un error de validación
        if email_exists:
            raise ValidationError("Email has already been used")

        # Llama al método de validación de la clase base para realizar cualquier otra validación
        return super().validate(attrs)

    def create(self, validated_data):
        # Extrae la contraseña del conjunto de datos válidos
        password = validated_data.pop("password")

        # Crea un nuevo usuario usando el método 'create' de la clase base
        user = super().create(validated_data)

        # Establece la contraseña del usuario de manera segura
        user.set_password(password)  # Cambia la contraseña del usuario

        # Guarda el usuario en la base de datos
        user.save()

        # Crea un nuevo token para el usuario
        Token.objects.create(user=user)

        # Devuelve el usuario creado
        return user
