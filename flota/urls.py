


from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

app_name = "flota"

# Rutas de la API REST
router = DefaultRouter()

router.register(
    "categorias",
    views.CategoriaViewSet,
    basename="categoria"
)

router.register(
    "vehiculos",
    views.VehiculoViewSet,
    basename="vehiculo"
)

router.register(
    "mantenimientos",
    views.MantenimientoViewSet,
    basename="mantenimiento"
)

# Rutas de la interfaz web
web_urlpatterns = [

    # CATEGORIAS
    path(
        "categorias/",
        views.lista_categorias,
        name="lista_categorias"
    ),
    path(
        "categorias/crear/",
        views.crear_categoria,
        name="crear_categoria"
    ),
    path(
        "categorias/editar/<int:pk>/",
        views.editar_categoria,
        name="editar_categoria"
    ),
    path(
        "categorias/eliminar/<int:pk>/",
        views.eliminar_categoria,
        name="eliminar_categoria"
    ),

    # VEHICULOS
    path(
        "vehiculos/",
        views.lista_vehiculos,
        name="lista_vehiculos"
    ),
    path(
        "vehiculos/crear/",
        views.crear_vehiculo,
        name="crear_vehiculo"
    ),
    path(
        "vehiculos/editar/<int:pk>/",
        views.editar_vehiculo,
        name="editar_vehiculo"
    ),
    path(
        "vehiculos/eliminar/<int:pk>/",
        views.eliminar_vehiculo,
        name="eliminar_vehiculo"
    ),
]

urlpatterns = web_urlpatterns + router.urls
