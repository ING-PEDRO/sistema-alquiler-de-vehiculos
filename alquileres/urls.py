

from django.urls import path

from . import views


app_name = "alquileres"

urlpatterns = [
    path(
        "",
        views.lista_alquileres,
        name="lista"
    ),

    path(
        "crear/",
        views.crear_alquiler,
        name="crear"
    ),

    path(
        "editar/<int:pk>/",
        views.editar_alquiler,
        name="editar"
    ),

    path(
        "eliminar/<int:pk>/",
        views.eliminar_alquiler,
        name="eliminar"
    ),
]

