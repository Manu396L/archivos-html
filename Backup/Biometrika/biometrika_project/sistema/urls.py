#urls.py


# sistema/urls.py

from django.urls import path
from . import views

app_name = 'sistema'

urlpatterns = [
    # Página principal (redirige)
    path('', views.index, name='index'),
    # Dashboard principal
    path('dashboard/', views.dashboard, name='dashboard'),
    # Gestion
    path('sedes/', views.sedes, name='sedes'),
    path('personal/', views.personal, name='personal'),
    path('dispositivos/', views.dispositivos, name='dispositivos'),
    # Reportes y alertas
    path('reportes/', views.reportes, name='reportes'),
    path('alertas/', views.alertas, name='alertas'),
    
    # Usuario
    path('notificaciones/', views.notificaciones, name='notificaciones'),
    path('perfil/', views.perfil, name='perfil'),
    path('configuracion/', views.configuracion, name='configuracion'),
    # Soporte
    path('soporte/', views.soporte, name='soporte'),
    # Autenticación
    path('acceso/', views.acceso, name='acceso'),
    path('usuario-nuevo/', views.usuario_nuevo, name='usuario_nuevo'),
    path('cambiar-contrasena/', views.cambiar_contrasena, name='cambiar_contrasena'),
    path('cerrar-sesion/', views.cerrar_sesion, name='cerrar_sesion'),
]