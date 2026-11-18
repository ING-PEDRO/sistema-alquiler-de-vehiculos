
from functools import wraps

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from config.permissions import (
    ADMINISTRADOR,
    ASESOR,
    JEFE_FLOTA,
    CLIENTE,
    grupos,
)


def roles_requeridos(*roles_permitidos):
    """
    Permite acceder a una vista únicamente a usuarios
    autenticados que tengan alguno de los roles indicados.
    """

    def decorador(vista):
        @wraps(vista)
        @login_required
        def vista_protegida(request, *args, **kwargs):

            usuario = request.user

            # El superusuario siempre tiene acceso.
            if usuario.is_superuser:
                return vista(request, *args, **kwargs)

            roles_usuario = grupos(usuario)

            # El administrador tiene acceso total.
            if ADMINISTRADOR in roles_usuario:
                return vista(request, *args, **kwargs)

            # Comprobar los roles autorizados.
            if roles_usuario.intersection(roles_permitidos):
                return vista(request, *args, **kwargs)

            raise PermissionDenied(
                "No tienes permisos para acceder a esta sección."
            )

        return vista_protegida

    return decorador


# Constantes disponibles para proteger las vistas.
ROL_ADMINISTRADOR = ADMINISTRADOR
ROL_ASESOR = ASESOR
ROL_JEFE_FLOTA = JEFE_FLOTA
ROL_CLIENTE = CLIENTE
