from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from usuarios.views import UsuarioViewSet, AdministradorViewSet, SecretarioViewSet, CambiarPasswordView
from pacientes.views import PacienteViewSet, ResponsableViewSet
from medicos.views import MedicoViewSet
from historiales.views import HistorialMedicoViewSet, RegistroHistorialViewSet
from pacientes.views import RegistroPacienteView
from medicos.views import RegistroMedicoView
from turnos.views import TurnoViewSet
from turnos.views import RegistroTurnoView
from turnos.views import PagoViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)
router.register(r'administradores', AdministradorViewSet)
router.register(r'secretarios', SecretarioViewSet)
router.register(r'pacientes', PacienteViewSet)
router.register(r'responsables', ResponsableViewSet)
router.register(r'medicos', MedicoViewSet)
router.register(r'historiales', HistorialMedicoViewSet)
router.register(r'registros-historial', RegistroHistorialViewSet)
router.register(r'turnos', TurnoViewSet, basename="turnos")
router.register(r'pagos', PagoViewSet, basename="pagos")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),

    # Endpoint para registrar paciente
    path('api/registro-paciente/', RegistroPacienteView.as_view(), name='registro-paciente'),

    # Endpoint para registrar médico
    path('api/registro-medico/', RegistroMedicoView.as_view(), name='registro-medico'),

    # Endpoint para registrar turno
    path('api/registro-turno/', RegistroTurnoView.as_view(), name='registro-turno'),

    #Seguridad de token Autenticación para login (Se usa para loguearse), luego api/usuarios/ lo usaremos para crear los usuarios
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    #URL cambio de contraseña
    path("api/change-password/", CambiarPasswordView.as_view(), name="change-password"),
]
