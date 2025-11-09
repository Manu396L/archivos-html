# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import *

# Extender el UserAdmin para incluir información del empleado
class EmpleadoInline(admin.StackedInline):
    model = Empleado
    can_delete = False
    verbose_name_plural = 'Información de Empleado'

class CustomUserAdmin(UserAdmin):
    inlines = (EmpleadoInline,)

# Reregistrar UserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

@admin.register(Sede)
class SedeAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'tipo', 'codigo_unico', 'dispositivo_biometrico', 'nivel_seguridad', 'fecha_creacion']
    list_filter = ['tipo', 'dispositivo_biometrico', 'nivel_seguridad']
    search_fields = ['nombre', 'codigo_unico', 'direccion']
    readonly_fields = ['fecha_creacion']

@admin.register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'sede', 'descripcion']
    list_filter = ['sede']
    search_fields = ['nombre', 'descripcion']

@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ['nombre_completo', 'id_empleado', 'cargo', 'departamento', 'sede', 'estado', 'nivel_seguridad']
    list_filter = ['estado', 'departamento', 'nivel_seguridad', 'sede']
    search_fields = ['nombre_completo', 'id_empleado', 'correo_corporativo', 'dni']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']

@admin.register(Dispositivo)
class DispositivoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'numero_serie', 'tipo_dispositivo', 'sede', 'estado', 'ultima_conexion']
    list_filter = ['tipo_dispositivo', 'estado', 'sede']
    search_fields = ['nombre', 'numero_serie', 'direccion_ip', 'area_ubicacion']
    readonly_fields = ['fecha_instalacion', 'fecha_actualizacion']

@admin.register(Credencial)
class CredencialAdmin(admin.ModelAdmin):
    list_display = ['empleado', 'tipo_credencial', 'activa', 'fecha_creacion', 'fecha_ultimo_uso']
    list_filter = ['tipo_credencial', 'activa']
    search_fields = ['empleado__nombre_completo', 'numero_tarjeta']
    readonly_fields = ['fecha_creacion']

@admin.register(RegistroAcceso)
class RegistroAccesoAdmin(admin.ModelAdmin):
    list_display = ['empleado', 'dispositivo', 'fecha_hora', 'estado', 'tipo_acceso', 'nivel_confianza']
    list_filter = ['estado', 'tipo_acceso', 'dispositivo', 'sede', 'fecha_hora']
    search_fields = ['empleado__nombre_completo', 'dispositivo__nombre']
    readonly_fields = ['fecha_registro']
    date_hierarchy = 'fecha_hora'

@admin.register(Alerta)
class AlertaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'tipo_alerta', 'prioridad', 'leida', 'resuelta', 'fecha_creacion']
    list_filter = ['tipo_alerta', 'prioridad', 'leida', 'resuelta', 'fecha_creacion']
    search_fields = ['titulo', 'mensaje']
    readonly_fields = ['fecha_creacion']

@admin.register(Notificacion)
class NotificacionAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'usuario', 'tipo_notificacion', 'prioridad', 'leida', 'fecha_creacion']
    list_filter = ['tipo_notificacion', 'prioridad', 'leida', 'fecha_creacion']
    search_fields = ['titulo', 'mensaje', 'usuario__username']
    readonly_fields = ['fecha_creacion']

@admin.register(SolicitudSoporte)
class SolicitudSoporteAdmin(admin.ModelAdmin):
    list_display = ['asunto', 'nombre_completo', 'categoria', 'estado', 'prioridad', 'fecha_creacion']
    list_filter = ['categoria', 'estado', 'prioridad', 'fecha_creacion']
    search_fields = ['asunto', 'nombre_completo', 'email', 'descripcion']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']

@admin.register(ConfiguracionSistema)
class ConfiguracionSistemaAdmin(admin.ModelAdmin):
    list_display = ['clave', 'valor', 'tipo', 'categoria', 'editable']
    list_filter = ['tipo', 'categoria', 'editable']
    search_fields = ['clave', 'descripcion']

@admin.register(Reporte)
class ReporteAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'tipo_reporte', 'usuario', 'programado', 'ultima_ejecucion']
    list_filter = ['tipo_reporte', 'programado', 'formato']
    search_fields = ['nombre', 'usuario__username']
    readonly_fields = ['fecha_creacion', 'ultima_ejecucion']

@admin.register(HorarioLaboral)
class HorarioLaboralAdmin(admin.ModelAdmin):
    list_display = ['empleado', 'dia_semana', 'hora_entrada', 'hora_salida', 'activo']
    list_filter = ['dia_semana', 'activo']
    search_fields = ['empleado__nombre_completo']

@admin.register(Auditoria)
class AuditoriaAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'accion', 'modelo', 'fecha_accion', 'ip_address']
    list_filter = ['accion', 'modelo', 'fecha_accion']
    search_fields = ['usuario__username', 'descripcion', 'ip_address']
    readonly_fields = ['fecha_accion']
    date_hierarchy = 'fecha_accion'

# Configuración del sitio admin
admin.site.site_header = "Sistema Biometrika - Administración"
admin.site.site_title = "Biometrika Admin"
admin.site.index_title = "Panel de Administración"