
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.db.models.deletion import ProtectedError
from config.decorators import roles_requeridos
from rest_framework import viewsets
from config.permissions import ASESOR, CLIENTE, JEFE_FLOTA

from .models import Accesorio
from .serializers import AccesorioSerializer
from .forms import AccesorioForm


# ==========================================
# API REST DE ACCESORIOS
# ==========================================

class AccesorioViewSet(viewsets.ModelViewSet):
    queryset = Accesorio.objects.all()
    serializer_class = AccesorioSerializer

    roles_read = [ASESOR, JEFE_FLOTA, CLIENTE]
    roles_write = [JEFE_FLOTA]

    search_fields = ["nombre", "descripcion"]
    ordering_fields = ["nombre", "precio_dia", "stock"]


# ==========================================
# LISTAR ACCESORIOS
# ==========================================
@roles_requeridos(ASESOR, JEFE_FLOTA)
def lista_accesorios(request):

    accesorios = Accesorio.objects.all().order_by("nombre")

    busqueda = request.GET.get("buscar", "").strip()

    if busqueda:
        accesorios = accesorios.filter(
            Q(nombre__icontains=busqueda) |
            Q(descripcion__icontains=busqueda)
        )

    return render(
        request,
        "accesorios/lista.html",
        {
            "accesorios": accesorios,
            "busqueda": busqueda
        }
    )


# ==========================================
# REGISTRAR ACCESORIO
# ==========================================
@roles_requeridos(JEFE_FLOTA)
def crear_accesorio(request):

    if request.method == "POST":

        form = AccesorioForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "El accesorio se registró correctamente."
            )

            return redirect("accesorios:lista_accesorios")

    else:
        form = AccesorioForm()

    return render(
        request,
        "accesorios/formulario.html",
        {
            "form": form,
            "titulo": "Registrar accesorio"
        }
    )


# ==========================================
# EDITAR ACCESORIO
# ==========================================
@roles_requeridos(JEFE_FLOTA)
def editar_accesorio(request, pk):

    accesorio = get_object_or_404(Accesorio, pk=pk)

    if request.method == "POST":

        form = AccesorioForm(
            request.POST,
            instance=accesorio
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "El accesorio se actualizó correctamente."
            )

            return redirect("accesorios:lista_accesorios")

    else:
        form = AccesorioForm(instance=accesorio)

    return render(
        request,
        "accesorios/formulario.html",
        {
            "form": form,
            "titulo": "Editar accesorio",
            "accesorio": accesorio
        }
    )


# ==========================================
# ELIMINAR ACCESORIO
# ==========================================

@roles_requeridos(JEFE_FLOTA)
def eliminar_accesorio(request, pk):

    accesorio = get_object_or_404(Accesorio, pk=pk)

    if request.method == "POST":

        try:
            cantidad = int(request.POST.get("cantidad", 0))

            if cantidad <= 0:
                messages.error(
                    request,
                    "Debes ingresar una cantidad mayor que cero."
                )

            elif cantidad > accesorio.stock:
                messages.error(
                    request,
                    f"Solo hay {accesorio.stock} unidades disponibles."
                )

            elif cantidad < accesorio.stock:
                accesorio.stock -= cantidad
                accesorio.save(update_fields=["stock"])

                messages.success(
                    request,
                    f"Se retiraron {cantidad} unidades de {accesorio.nombre}. "
                    f"Quedan {accesorio.stock} unidades disponibles."
                )

            else:
                accesorio.delete()

                messages.success(
                    request,
                    "El accesorio se eliminó completamente del inventario."
                )

        except ValueError:
            messages.error(
                request,
                "Ingresa una cantidad válida."
            )

        except ProtectedError:
            messages.error(
                request,
                "No se puede eliminar completamente este accesorio porque está asociado a uno o varios alquileres."
            )

        return redirect("accesorios:lista_accesorios")

    return render(
        request,
        "accesorios/confirmar_eliminar.html",
        {
            "accesorio": accesorio
        }
    )
