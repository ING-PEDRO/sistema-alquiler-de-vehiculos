
from django.urls import path
from . import views

app_name = "accesorios"

urlpatterns = [
    path(
        "",
        views.lista_accesorios,
        name="lista_accesorios"
    ),

    path(
        "crear/",
        views.crear_accesorio,
        name="crear_accesorio"
    ),

    path(
        "editar/<int:pk>/",
        views.editar_accesorio,
        name="editar_accesorio"
    ),

    path(
        "eliminar/<int:pk>/",
        views.eliminar_accesorio,
        name="eliminar_accesorio"
    ),
]
