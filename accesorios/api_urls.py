
from rest_framework.routers import DefaultRouter
from .views import AccesorioViewSet

router = DefaultRouter()

router.register(
    "accesorios",
    AccesorioViewSet,
    basename="accesorio"
)

urlpatterns = router.urls
