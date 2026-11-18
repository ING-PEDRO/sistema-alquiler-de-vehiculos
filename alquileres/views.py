

from rest_framework import viewsets

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction

from .models import Alquiler, AlquilerAccesorio
from .serializers import (
    AlquilerSerializer,
    AlquilerAccesorioSerializer,
)
from .forms import AlquilerForm, AccesoriosFormSet


# ==========================================
# API REST: ALQUILERES
# ==========================================

class AlquilerViewSet(viewsets.ModelViewSet):
    queryset = Alquiler.objects.select_related(
        "cliente", "vehiculo"
    ).all()
    serializer_class = AlquilerSerializer


# ==========================================
# API REST: ACCESORIOS DE ALQUILER
# ==========================================

class AlquilerAccesorioViewSet(viewsets.ModelViewSet):
    queryset = AlquilerAccesorio.objects.select_related(
        "alquiler", "accesorio"
    ).all()
    serializer_class = AlquilerAccesorioSerializer


# ==========================================
# INTERFAZ WEB: LISTAR ALQUILERES
# ==========================================

def lista_alquileres(request):

    alquileres = Alquiler.objects.select_related(
        "cliente", "vehiculo"
    ).prefetch_related(
        "accesorios_alquilados__accesorio"
    ).order_by("-id")

    return render(
        request,
        "alquileres/lista.html",
        {"alquileres": alquileres}
    )


# ==========================================
# INTERFAZ WEB: CREAR ALQUILER
# ==========================================

def crear_alquiler(request):

    alquiler = Alquiler()

    if request.method == "POST":

        form = AlquilerForm(request.POST)
        formset = AccesoriosFormSet(
            request.POST,
            instance=alquiler
        )

        if form.is_valid() and formset.is_valid():

            with transaction.atomic():

                alquiler = form.save()
                formset.instance = alquiler
                formset.save()

            messages.success(
                request,
                "El alquiler se registró correctamente."
            )

            return redirect("alquileres:lista")

    else:
        form = AlquilerForm()
        formset = AccesoriosFormSet(instance=alquiler)

    return render(
        request,
        "alquileres/formulario.html",
        {
            "form": form,
            "formset": formset,
            "titulo": "Registrar alquiler"
        }
    )


# ==========================================
# INTERFAZ WEB: EDITAR ALQUILER
# ==========================================

def editar_alquiler(request, pk):

    alquiler = get_object_or_404(Alquiler, pk=pk)

    if request.method == "POST":

        form = AlquilerForm(
            request.POST,
            instance=alquiler
        )

        formset = AccesoriosFormSet(
            request.POST,
            instance=alquiler
        )

        if form.is_valid() and formset.is_valid():

            with transaction.atomic():

                form.save()
                formset.save()

            messages.success(
                request,
                "El alquiler se actualizó correctamente."
            )

            return redirect("alquileres:lista")

    else:
        form = AlquilerForm(instance=alquiler)
        formset = AccesoriosFormSet(instance=alquiler)

    return render(
        request,
        "alquileres/formulario.html",
        {
            "form": form,
            "formset": formset,
            "titulo": "Editar alquiler"
        }
    )


# ==========================================
# INTERFAZ WEB: ELIMINAR ALQUILER
# ==========================================

def eliminar_alquiler(request, pk):

    alquiler = get_object_or_404(Alquiler, pk=pk)

    if request.method == "POST":

        alquiler.delete()

        messages.success(
            request,
            "El alquiler se eliminó correctamente."
        )

        return redirect("alquileres:lista")

    return render(
        request,
        "alquileres/confirmar_eliminar.html",
        {"alquiler": alquiler}
    )

