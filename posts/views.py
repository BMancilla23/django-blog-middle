from rest_framework.request import Request

# from django.http import HttpRequest, JsonResponse
from rest_framework.response import Response
from rest_framework import status, generics, mixins
from rest_framework.decorators import api_view, APIView, permission_classes
from .models import Post
from .serializers import PostSerializer
from django.shortcuts import get_object_or_404
from .permissions import ReadOnly, AuthorOrReadOnly
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination
from drf_yasg.utils import swagger_auto_schema


class CustomPaginator(PageNumberPagination):
    page_size = 3  # Número de elementos por página por defecto
    page_query_param = (
        "page"  # Nombre del parámetro de consulta para el número de página
    )

    page_size_query_param = (
        "page_size"  # Nombre del parámetro para ajustar el tamaño de la página
    )


""" posts=[
    {
     "id": 1,
     "title": "Why is it difficult to learn Programmning",
     "content": "This is to give reasons why it is hard"
        
    },
    {
     "id": 2,
     "title": "Learn Javascript",
     "content": "This is a course on JS"
    },
    {
        "id": 3,
        "title": "Why is it difficult to learn Programming",
        "content": "This is to give reasons why it is hard"
    }
] """

# Create your views here.
""" def homepage(request:HttpRequest):
    response={"message": "Hellow World"}
    return JsonResponse(data=response) """

# Ejemplo de uso de vista basadas en funciones con el decorador @api_view


# Vista para manejar solicituded GET y POST
@api_view(http_method_names=["GET", "POST"])
@permission_classes([AllowAny])
def homepage(request: Request):

    # Maneja la solicitud POST
    if request.method == "POST":
        data = request.data  # Obtiene los datos enviados en el cuerpo de la solicitud
        response = {"message": "Hello world", "data": data}
        return Response(data=response, status=status.HTTP_201_CREATED)

    # Maneja la solicitud GET
    response = {"message": "Hello world!"}
    return Response(data=response, status=status.HTTP_200_OK)


# Vista para manejar todas las publicaciones (GET para listar, POST para crear)
@api_view(http_method_names=["GET", "POST"])
def all_posts(request: Request):
    posts = Post.objects.all()  # Obtiene todas las publicaciones del modelo Post

    if request.method == "POST":
        data = request.data
        serializer = PostSerializer(data=data)  # Serializa los datos entrantes

        if serializer.is_valid():
            serializer.save()  # Guarda la nueva publicación si los datos son válidos

            response = {"message": "Post created successfully", "data": serializer.data}

            return Response(data=response, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Maneja la solicitud GET para listar todas las publicaciones
    serializer = PostSerializer(
        instance=posts, many=True
    )  # Serializa todas las publicaciones
    # response={"message": "List of posts", "data": posts}

    response = {"message": "List of posts", "data": serializer.data}

    return Response(data=response, status=status.HTTP_200_OK)


# Ejemplo de uso de vistas basadas en clases (Class-Based Views) con APIView


""" # Vista para listar y crear publicaciones (GET para listar, POST para crear)
class PostListCreateView(APIView):

    serializer_class = PostSerializer  # Define el serializer que se usará en la vista

    def get(self, request: Request, *args, **kwargs):
        posts = Post.objects.all()

        serializer = self.serializer_class(
            instance=posts, many=True
        )  # Serializa todas las publicaciones

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request, *args, **kwargs):
        data = request.data

        serializer = self.serializer_class(data=data)  # Serializa los datos entrantes

        if serializer.is_valid():
            serializer.save()  # Guarda la nueva publicación si los datos son válidos

            response = {"message": "Post created successfully", "data": serializer.data}

            return Response(data=response, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Vista para recuperar, actualizar y eliminar una publicación específica (GET, PUT, DELETE)
class PostRetrieveUpdateDeleteView(APIView):
    serializer_class = PostSerializer

    def get(self, request: Request, post_id: int):
        post = get_object_or_404(
            Post, pk=post_id
        )  # Obtiene la publicación específica o lanza un error 404 si no se encuentra

        serializer = self.serializer_class(
            instance=post
        )  # Serializa la publicación específica

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request: Request, post_id: int):
        post = get_object_or_404(Post, pk=post_id)

        data = request.data

        serializer = self.serializer_class(
            instance=post, data=data
        )  # Serializa los datos entrantes para la actualización

        if serializer.is_valid():
            serializer.save()  # Guarda la publicación actualizada si los datos son válidos
            response = {"message": "Post updated successfully", "data": serializer.data}
            return Response(data=response, status=status.HTTP_200_OK)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, post_id: int):
        post = get_object_or_404(Post, pk=post_id)
        post.delete()  # Elimina la publicación

        response = {"message": "Post deleted successfully"}
        return Response(data=response, status=status.HTTP_204_NO_CONTENT)
 """


class PostListCreateView(
    generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin
):

    serializer_class = PostSerializer
    permission_classes = [AuthorOrReadOnly]
    pagination_class = CustomPaginator
    queryset = Post.objects.all().order_by("created_at")

    @swagger_auto_schema(
        operation_summary="List all posts",
        operation_description="This returns a list of all posts",
    )
    def get(self, request: Request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create a post",
        operation_description="Create a post",
    )
    def post(self, request: Request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class PostRetrieveUpdateDeleteView(
    generics.GenericAPIView,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    @swagger_auto_schema(
        operation_summary="Retrieve a post by id",
        operation_description="This retrieves a post by an id",
    )
    def get(self, request: Request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Updates a post by id",
        operation_description="This updates a post given this id",
    )
    def put(self, request: Request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete a post",
        operation_description="This deletes a post by an id",
    )
    def delete(self, request: Request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ListPostsForAuthor(
    generics.GenericAPIView,
    mixins.ListModelMixin,
):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # username = self.kwargs["username"]
        # Obtiene el parámetro de consulta 'username'
        username = self.request.query_params.get("username") or None

        queryset = Post.objects.all()

        if username is not None:
            # Filtra las publicaciones por el nombre de usuario
            return Post.objects.filter(author__username=username)

        return queryset

    @swagger_auto_schema(
        operation_summary="List posts for an author (user)",
        operation_description="List post for author",
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


# Vistas basadas en funciones para manejar acciones específicas sobre una publicación


# Vista para obtener los detalles de una publicación específica
@api_view(http_method_names=["GET"])
def get_post(request: Request, post_id: int):
    post = get_object_or_404(Post, pk=post_id)

    serializer = PostSerializer(instance=post)

    response = {"message": "Post details", "data": serializer.data}

    return Response(data=response, status=status.HTTP_200_OK)


# Vista para actualizar una publicación específica
@api_view(http_method_names=["PUT"])
def update_post(request: Request, post_id: int):
    post = get_object_or_404(Post, pk=post_id)

    data = request.data

    serializer = PostSerializer(instance=post, data=data)

    if serializer.is_valid():
        serializer.save()

        response = {"message": "Post updated successfully", "data": serializer.data}

        return Response(data=response, status=status.HTTP_200_OK)

    return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Vista para eliminar una publicación específica
@api_view(http_method_names=["DELETE"])
def delete_post(request: Request, post_id: int):
    post = get_object_or_404(Post, pk=post_id)
    post.delete()

    response = {"message": "Post deleted successfully"}

    return Response(data=response, status=status.HTTP_204_NO_CONTENT)
