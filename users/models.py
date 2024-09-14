# Models
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

# Create your models here.


# CustomerUserManager es un administrador personalizado que define cómo crear usuarios y superusuarios
class CustomUserManager(BaseUserManager):
    # Método para crear un usuariok estándar
    def create_user(self, email, password, **extra_fields):
        # Valida que el email esté presente
        if not email:
            raise ValueError("The Email field must be set")

        # Normaliza el email para mantener consistencia (e.g., convierte a minúsculas)
        email = self.normalize_email(email)
        # Crea una instancia de usuario utilizando el modelo definido y los campos adicionales
        user = self.model(email=email, **extra_fields)

        # Establece la contraseña del usuario de forma segura
        user.set_password(password)
        # Guarda el usuario en la base de datos especificando el uso del alias de la base de datos actual
        user.save(using=self._db)
        return user

    # Método para crear un superusuario (administrador)
    def create_superuser(self, email, password, **extra_fields):
        # Asegura que los campos is_staff y is_superuser estén establecidos en True para un superusuario
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        # Verifica que is_staff sea True, de lo contrario lanza una excepción
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")

        # Verifica que is_superuser sea True, de lo contrario lanza una excepción
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        # Llama el método create_user para crear el superusuario con los campos extra necesario
        return self.create_user(email=email, password=password, **extra_fields)


# Clase personalizada de usuario que hereda de AbstracBaseUser y PermissionMixin
class User(AbstractBaseUser, PermissionsMixin):

    # Definición de los campos del usuario
    email = models.EmailField(max_length=50, unique=True)
    username = models.CharField(max_length=45)
    date_of_birth = models.DateField(null=True)

    # Campos adicionales necesarios para la autenticación y permisos
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    # Define el administrador de usuarios personalizado para el modelo
    objects = CustomUserManager()

    # Campos requeridos por Django para la autenticación
    USERNAME_FIELD = (
        "email"  # Campo que se utilizará como identificador único para la autenticación
    )
    REQUIRED_FIELDS = ["username"]  # Campos adicionales requeridos al crear un usuario

    # Método para representar al usuario con una cadena de texto
    def __str__(self) -> str:
        return self.username
