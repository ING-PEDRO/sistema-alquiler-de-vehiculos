"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""




from django.contrib import admin
from django.urls import path, include

from . import views


urlpatterns = [
    # Página principal
    path("", views.inicio, name="inicio"),

    # Administración
    path("admin/", admin.site.urls),

    # Interfaz web de alquileres
    path(
        "alquileres/",
        include("alquileres.urls")
    ),

    # API REST
    path("api/", include("flota.urls")),
    path("api/", include("clientes.urls")),
    path("api/", include("accesorios.urls")),
    path("api/", include("alquileres.api_urls")),
]

