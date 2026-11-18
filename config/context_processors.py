
from config.permissions import (
    ADMINISTRADOR,
    ASESOR,
    JEFE_FLOTA,
    CLIENTE,
    grupos,
)


def datos_usuario(request):

    if not request.user.is_authenticated:
        return {
            "es_administrador": False,
            "es_asesor": False,
            "es_jefe_flota": False,
            "es_cliente": False,
        }

    roles = grupos(request.user)

    return {
        "es_administrador": (
            request.user.is_superuser
            or ADMINISTRADOR in roles
        ),
        "es_asesor": ASESOR in roles,
        "es_jefe_flota": JEFE_FLOTA in roles,
        "es_cliente": CLIENTE in roles,
    }
