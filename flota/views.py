from config.decorators import roles_requeridos
from config.permissions import ASESOR, JEFE_FLOTA
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q

from rest_framework import viewsets

from .models import Categoria, Vehiculo, Mantenimiento
from .serializers import (
    CategoriaSerializer,
    VehiculoSerializer,
    MantenimientoSerializer,
)
from .forms import VehiculoForm, CategoriaForm


# ==========================================
# API REST: CATEGORIAS
# ==========================================

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer


# ==========================================
# API REST: VEHICULOS
# ==========================================

class VehiculoViewSet(viewsets.ModelViewSet):
    queryset = Vehiculo.objects.select_related("categoria").all()
    serializer_class = VehiculoSerializer


# ==========================================
# API REST: MANTENIMIENTOS
# ==========================================

class MantenimientoViewSet(viewsets.ModelViewSet):
    queryset = Mantenimiento.objects.select_related("vehiculo").all()
    serializer_class = MantenimientoSerializer


# ==========================================
# INTERFAZ WEB: LISTAR VEHICULOS
# ==========================================
@roles_requeridos(ASESOR, JEFE_FLOTA)
def lista_vehiculos(request):

    vehiculos = Vehiculo.objects.select_related(
        "categoria"
    ).order_by("-id")

    busqueda = request.GET.get("buscar", "").strip()

    if busqueda:
        vehiculos = vehiculos.filter(
            Q(placa__icontains=busqueda) |
            Q(marca__icontains=busqueda) |
            Q(modelo__icontains=busqueda) |
            Q(categoria__nombre__icontains=busqueda)
        )

    return render(
        request,
        "flota/vehiculos/lista.html",
        {
            "vehiculos": vehiculos,
            "busqueda": busqueda,
        }
    )


# ==========================================
# INTERFAZ WEB: REGISTRAR VEHICULO
# ==========================================
@roles_requeridos( JEFE_FLOTA)
def crear_vehiculo(request):

    if request.method == "POST":

        form = VehiculoForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "El vehículo se registró correctamente."
            )

            return redirect("flota:lista_vehiculos")

    else:
        form = VehiculoForm()

    return render(
        request,
        "flota/vehiculos/formulario.html",
        {
            "form": form,
            "titulo": "Registrar vehículo",
        }
    )


# ==========================================
# INTERFAZ WEB: EDITAR VEHICULO
# ==========================================
@roles_requeridos( JEFE_FLOTA)
def editar_vehiculo(request, pk):

    vehiculo = get_object_or_404(Vehiculo, pk=pk)

    if request.method == "POST":

        form = VehiculoForm(
            request.POST,
            request.FILES,
            instance=vehiculo
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "El vehículo se actualizó correctamente."
            )

            return redirect("flota:lista_vehiculos")

    else:
        form = VehiculoForm(instance=vehiculo)

    return render(
        request,
        "flota/vehiculos/formulario.html",
        {
            "form": form,
            "titulo": "Editar vehículo",
            "vehiculo": vehiculo,
        }
    )


# ==========================================
# INTERFAZ WEB: ELIMINAR VEHICULO
# ==========================================
@roles_requeridos( JEFE_FLOTA)
def eliminar_vehiculo(request, pk):

    vehiculo = get_object_or_404(Vehiculo, pk=pk)

    if request.method == "POST":

        vehiculo.delete()

        messages.success(
            request,
            "El vehículo se eliminó correctamente."
        )

        return redirect("flota:lista_vehiculos")

    return render(
        request,
        "flota/vehiculos/confirmar_eliminar.html",
        {
            "vehiculo": vehiculo,
        }
    )

# ==========================================
# INTERFAZ WEB: LISTAR CATEGORIAS
# ==========================================
@roles_requeridos(ASESOR, JEFE_FLOTA)
def lista_categorias(request):

    categorias = Categoria.objects.all().order_by("nombre")

    busqueda = request.GET.get("buscar", "").strip()

    if busqueda:
        categorias = categorias.filter(
            Q(nombre__icontains=busqueda) |
            Q(descripcion__icontains=busqueda)
        )

    return render(
        request,
        "flota/categorias/lista.html",
        {
            "categorias": categorias,
            "busqueda": busqueda,
        }
    )


# ==========================================
# INTERFAZ WEB: CREAR CATEGORIA
# ==========================================
@roles_requeridos(JEFE_FLOTA)
def crear_categoria(request):

    if request.method == "POST":

        form = CategoriaForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "La categoría se registró correctamente."
            )

            return redirect("flota:lista_categorias")

    else:
        form = CategoriaForm()

    return render(
        request,
        "flota/categorias/formulario.html",
        {
            "form": form,
            "titulo": "Registrar categoría",
        }
    )


# ==========================================
# INTERFAZ WEB: EDITAR CATEGORIA
# ==========================================
@roles_requeridos(JEFE_FLOTA)
def editar_categoria(request, pk):

    categoria = get_object_or_404(Categoria, pk=pk)

    if request.method == "POST":

        form = CategoriaForm(
            request.POST,
            instance=categoria
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "La categoría se actualizó correctamente."
            )

            return redirect("flota:lista_categorias")

    else:
        form = CategoriaForm(instance=categoria)

    return render(
        request,
        "flota/categorias/formulario.html",
        {
            "form": form,
            "titulo": "Editar categoría",
            "categoria": categoria,
        }
    )


# ==========================================
# INTERFAZ WEB: ELIMINAR CATEGORIA
# ==========================================
@roles_requeridos(JEFE_FLOTA)
def eliminar_categoria(request, pk):

    categoria = get_object_or_404(Categoria, pk=pk)

    if request.method == "POST":

        try:
            categoria.delete()

            messages.success(
                request,
                "La categoría se eliminó correctamente."
            )

        except Exception as error:
            from django.db.models.deletion import ProtectedError

            if isinstance(error, ProtectedError):
                messages.error(
                    request,
                    "No se puede eliminar esta categoría porque tiene vehículos asociados."
                )
            else:
                raise

        return redirect("flota:lista_categorias")

    return render(
        request,
        "flota/categorias/confirmar_eliminar.html",
        {
            "categoria": categoria,
        }
    )
