from django.db import models
from categories.models import Category
from users.models import User

# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="posts"
    )  # Relación Uno a Muchos con User
    # Relación Muchos a Muchos con Category
    categories = models.ManyToManyField(Category, related_name="posts")

    # author se define como un campo Foreingkey que apunta al modelo User
    # onde_delete=models.CASCADE: Especifica que cuando se elimina un usuarios, todos los posts asociados también se eliminarán
    # related_name="posts": Permite acceder a los post asociados desde un usuario

    def __str__(self) -> str:
        return self.title
