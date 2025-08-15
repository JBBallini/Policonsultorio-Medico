from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from usuarios.views import UsuarioViewSet, AdministradorViewSet, SecretarioViewSet
from pacientes.views import PacienteViewSet, ResponsableViewSet
from medicos.views import MedicoViewSet
from historiales.views import HistorialMedicoViewSet, RegistroHistorialViewSet

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)
router.register(r'administradores', AdministradorViewSet)
router.register(r'secretarios', SecretarioViewSet)
router.register(r'pacientes', PacienteViewSet)
router.register(r'responsables', ResponsableViewSet)
router.register(r'medicos', MedicoViewSet)
router.register(r'historiales', HistorialMedicoViewSet)
router.register(r'registros-historial', RegistroHistorialViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
