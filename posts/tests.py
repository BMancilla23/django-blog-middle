# from django.test import TestCase
from rest_framework.test import APITestCase, APIRequestFactory
from .views import PostListCreateView
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from categories.models import Category

# Create your tests here.

User = get_user_model()


# Caso de prueba para una vista simple de "Hello World"
class HelloWorldTestCase(APITestCase):

    def test_hello_world(self):
        # Hacemos una petición GET a la ruta con nombre "post_home"
        response = self.client.get(reverse("post_home"))
        # Verificamos que la respuesta tenga el estado 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Verificamos que la respuesta contenga el mensaje esperado
        self.assertEqual(response.data["message"], "Hello world!")


# Caso de prueba para las vistas de listar y craer posts
class PostListCreateTestCase(APITestCase):
    # Método que se ejecuta antes de cada prueba. Se usa para configurar el estado inicial necesario para las pruebas
    def setUp(self):
        # self.factory = APIRequestFactory()
        # self.view = PostListCreateView.as_view()
        self.url = reverse(
            "list_posts"
        )  # Generamos la URL de la vista que vamos a probar

        # Creamos un usuario de prueba
        self.user = User.objects.create(
            email="test@example.com", username="test_user", password="test1234"
        )

        # Creamos dos categorías de prueba
        self.category1 = Category.objects.create(name="Category 1")

        self.category2 = Category.objects.create(name="Category 2")

    # Función que autentica al usuario para poder realizar peticiones protegidas por autenticación jWT
    def authenticate(self):

        # Primero creamos el usuario en la base de datos mediante el endpoint de signup
        self.client.post(
            reverse("signup"),
            {
                "username": "test_user",
                "password": "test1234",
                "email": "test@gmail.com",
            },
        )

        # Luego, obtenemos el token de acceso del endpoint de login
        response = self.client.post(
            reverse("login"),
            {
                "email": "test@gmail.com",
                "password": "test1234",
            },
        )

        # print(response.data)

        # Extraemos el token de la respuesta
        token = response.data["tokens"]["access"]

        # Añadimos el token en las cabeceras de autorización para las siguientes peticiones
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    # Prueba para la lista de posts cuando no hay ningún post creado
    def test_list_post(self):
        # request = self.factory.get(self.url)
        # response = self.view(request)
        # Realizamos una petición GET a la URL de list_posts
        response = self.client.get(self.url)

        # print(response.data)

        # Verificamos que la respuesta tenga el estado 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verificamos que la cantidad de posts sea 0
        self.assertEqual(response.data["count"], 0)

        # Verificamos que el resultado sea una lista vacía
        self.assertEqual(response.data["results"], [])

    # Prueba para la creación de un nuevo post
    def test_create_post(self):
        """sample_post = {
            "title": "Sample Post",
            "content": "This is a sample post",
            "author": self.user.id,
            "categories": [self.category1.id, self.category2.id],
        }
        request = self.factory.post(self.url, sample_post)

        request.user = self.user

        response = self.view(request)

        print(response.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)"""
        self.authenticate()  # Llamamos a la función que autentica al usuario

        # Definimos los datos del post de prueba
        sample_data = {
            "title": "Sample Post",
            "content": "This is a sample post",
            "author": self.user.id,
            "categories": [self.category1.id, self.category2.id],
        }

        # Realizamos una petición POST con los datos del post
        response = self.client.post(reverse("list_posts"), sample_data)

        # Verificamos que el post se haya creado correctamente y la respuesta tenga el estado 201 Created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Verificamos que el título del post en la respuesta sea el mismo que enviamos
        self.assertEqual(response.data["title"], "Sample Post")
