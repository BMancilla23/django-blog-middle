from django.urls import path, include
from rest_framework import routers
from categories import views

router = routers.DefaultRouter()

router.register(r"", views.CategoryViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
