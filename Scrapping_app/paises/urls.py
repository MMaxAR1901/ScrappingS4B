from django.urls import path
from . import views

urlpatterns = [
    path("cargar/", views.cargarPaises, name="cargarPaises"),
    path("lista/", views.listaPaises, name="listaPaises"),
    path("borrar-logico/<int:pk>/", views.borradoLogicoPais, name="borradoLogicoPais"),
]