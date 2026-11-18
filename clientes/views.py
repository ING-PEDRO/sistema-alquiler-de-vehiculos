
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q

from rest_framework import viewsets
from config.permissions import ASESOR, CLIENTE, grupos

from .models import Cliente
from .serializers import ClienteSerializer
from .forms import ClienteForm
from config.decorators import roles_requeridos

# ==========================================
# API REST DE CLIENTES
# ==========================================

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

    roles_read = [ASESOR, CLIENTE]
    roles_write = [ASESOR]

    search_fields = [
        "nombres",
        "apellidos",
        "numero_documento",
        "correo"
    ]

    ordering_fields = ["apellidos", "nombres"]

    def get_queryset(self):
        qs = super().get_queryset()
        u = self.request.user

        if not u.is_superuser and grupos(u) == {CLIENTE}:
            return qs.filter(usuario=u)

        return qs


# ==========================================
# LISTAR CLIENTES
# ==========================================
@roles_requeridos(ASESOR)
def lista_clientes(request):

    clientes = Cliente.objects.all().order_by("apellidos", "nombres")

    busqueda = request.GET.get("buscar", "").strip()

    if busqueda:
        clientes = clientes.filter(
            Q(numero_documento__icontains=busqueda) |
            Q(nombres__icontains=busqueda) |
            Q(apellidos__icontains=busqueda) |
            Q(telefono__icontains=busqueda) |
            Q(correo__icontains=busqueda)
        )

    return render(
        request,
        "clientes/lista.html",
        {
            "clientes": clientes,
            "busqueda": busqueda
        }
    )


# ==========================================
# REGISTRAR CLIENTE
# ==========================================
@roles_requeridos(ASESOR)
def crear_cliente(request):

    if request.method == "POST":

        form = ClienteForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "El cliente se registró correctamente."
            )

            return redirect("clientes:lista_clientes")

    else:
        form = ClienteForm()

    return render(
        request,
        "clientes/formulario.html",
        {
            "form": form,
            "titulo": "Registrar cliente"
        }
    )


# ==========================================
# EDITAR CLIENTE
# ==========================================
@roles_requeridos(ASESOR)
def editar_cliente(request, pk):

    cliente = get_object_or_404(Cliente, pk=pk)

    if request.method == "POST":

        form = ClienteForm(request.POST, instance=cliente)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Los datos del cliente se actualizaron correctamente."
            )

            return redirect("clientes:lista_clientes")

    else:
        form = ClienteForm(instance=cliente)

    return render(
        request,
        "clientes/formulario.html",
        {
            "form": form,
            "titulo": "Editar cliente",
            "cliente": cliente
        }
    )


# ==========================================
# ELIMINAR CLIENTE
# ==========================================
@roles_requeridos(ASESOR)
def eliminar_cliente(request, pk):

    cliente = get_object_or_404(Cliente, pk=pk)

    if request.method == "POST":

        try:
            cliente.delete()

            messages.success(
                request,
                "El cliente se eliminó correctamente."
            )

        except Exception:
            messages.error(
                request,
                "No se puede eliminar este cliente porque tiene registros asociados."
            )

        return redirect("clientes:lista_clientes")

    return render(
        request,
        "clientes/confirmar_eliminar.html",
        {
            "cliente": cliente
        }
    )

# ==========================================
# PERFIL PERSONAL DEL CLIENTE
# ==========================================

@roles_requeridos(CLIENTE)
def mi_perfil(request):

    cliente = get_object_or_404(
        Cliente,
        usuario=request.user
    )

    return render(
        request,
        "clientes/mi_perfil.html",
        {
            "cliente": cliente
        }
    )
