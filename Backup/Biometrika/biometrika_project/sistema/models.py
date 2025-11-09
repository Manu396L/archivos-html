from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

class Sede(models.Model):
    TIPO_SEDE_CHOICES = [
        ('sede', 'Sede Principal'),
        ('oficina', 'Oficina'),
        ('area', 'Área Específica'),
        ('almacen', 'Almacén'),
    ]
    
    nombre = models.CharField(max_length=200)
    tipo = models.CharField(max_length=20, choices=TIPO_SEDE_CHOICES)
    codigo_unico = models.CharField(max_length=50, unique=True)
    direccion = models.TextField(blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    # Configuración de seguridad biométrica
    dispositivo_biometrico = models.CharField(max_length=20, choices=[
        ('huella', 'Lector de Huella Dactilar'),
        ('tarjeta', 'Tarjeta de Acceso'),
        ('pin', 'PIN'),
    ], default='huella')
    nivel_seguridad = models.CharField(max_length=10, choices=[
        ('bajo', 'Bajo'),
        ('medio', 'Medio'),
        ('alto', 'Alto'),
    ], default='medio')
    
    def __str__(self):
        return f"{self.nombre} ({self.get_tipo_display()})"

class Departamento(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    sede = models.ForeignKey(Sede, on_delete=models.CASCADE, related_name='departamentos')
    
    def __str__(self):
        return f"{self.nombre} - {self.sede.nombre}"

class Empleado(models.Model):
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
        ('suspendido', 'Suspendido'),
        ('vacaciones', 'Vacaciones'),
        ('licencia', 'Licencia'),
    ]
    
    NIVEL_SEGURIDAD_CHOICES = [
        ('bajo', 'Bajo'),
        ('medio', 'Medio'),
        ('alto', 'Alto'),
    ]
    
    # Información personal
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    id_empleado = models.CharField(max_length=50, unique=True)
    nombre_completo = models.CharField(max_length=200)
    foto = models.ImageField(upload_to='empleados/', blank=True, null=True)
    correo_corporativo = models.EmailField()
    telefono = models.CharField(max_length=20, blank=True, null=True)
    dni = models.CharField(max_length=20, blank=True, null=True)
    
    # Información laboral
    cargo = models.CharField(max_length=100)
    departamento = models.ForeignKey(Departamento, on_delete=models.SET_NULL, null=True)
    superior = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subordinados')
    fecha_ingreso = models.DateField()
    sede = models.ForeignKey(Sede, on_delete=models.SET_NULL, null=True)
    
    # Credenciales de seguridad
    nivel_seguridad = models.CharField(max_length=10, choices=NIVEL_SEGURIDAD_CHOICES, default='medio')
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='activo')
    
    # Auditoría
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Empleado"
        verbose_name_plural = "Empleados"
        ordering = ['nombre_completo']
    
    def __str__(self):
        return f"{self.nombre_completo} - {self.id_empleado}"

class Dispositivo(models.Model):
    TIPO_DISPOSITIVO_CHOICES = [
        ('huella', 'Lector de Huella'),
        ('tarjeta', 'Lector de Tarjeta'),
        ('facial', 'Reconocimiento Facial'),
        ('iris', 'Escáner de Iris'),
        ('multi', 'Multibiométrico'),
        ('pin', 'PIN'),
    ]
    
    ESTADO_DISPOSITIVO_CHOICES = [
        ('activo', 'Activo'),
        ('pausado', 'Pausado'),
        ('error', 'Error'),
        ('sin_conexion', 'Sin Conexión'),
        ('apagado', 'Apagado'),
        ('mantenimiento', 'En Mantenimiento'),
    ]
    
    # Información básica
    nombre = models.CharField(max_length=200)
    numero_serie = models.CharField(max_length=100, unique=True)
    tipo_dispositivo = models.CharField(max_length=20, choices=TIPO_DISPOSITIVO_CHOICES)
    
    # Ubicación
    sede = models.ForeignKey(Sede, on_delete=models.CASCADE)
    area_ubicacion = models.CharField(max_length=200)
    direccion_fisica = models.TextField(blank=True, null=True)
    
    # Configuración de red
    direccion_ip = models.GenericIPAddressField()
    zona_horaria = models.CharField(max_length=50, default='America/Buenos_Aires')
    intervalo_solicitud = models.IntegerField(default=5, validators=[MinValueValidator(1), MaxValueValidator(60)])
    
    # Estado
    estado = models.CharField(max_length=15, choices=ESTADO_DISPOSITIVO_CHOICES, default='activo')
    ultima_conexion = models.DateTimeField(null=True, blank=True)
    ultima_sincronizacion = models.DateTimeField(null=True, blank=True)
    
    # Observaciones
    observaciones = models.TextField(blank=True, null=True)
    
    # Auditoría
    fecha_instalacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Dispositivo"
        verbose_name_plural = "Dispositivos"
        ordering = ['sede', 'nombre']
    
    def __str__(self):
        return f"{self.nombre} ({self.numero_serie})"

class Credencial(models.Model):
    TIPO_CREDENCIAL_CHOICES = [
        ('huella', 'Huella Dactilar'),
        ('tarjeta', 'Tarjeta de Acceso'),
        ('pin', 'PIN'),
        ('facial', 'Reconocimiento Facial'),
        ('iris', 'Escaneo de Iris'),
        ('voz', 'Reconocimiento de Voz'),
    ]
    
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, related_name='credenciales')
    tipo_credencial = models.CharField(max_length=20, choices=TIPO_CREDENCIAL_CHOICES)
    
    # Dependiendo del tipo de credencial
    hash_huella = models.TextField(blank=True, null=True)
    numero_tarjeta = models.CharField(max_length=100, blank=True, null=True, unique=True)
    pin = models.CharField(max_length=50, blank=True, null=True)
    template_facial = models.TextField(blank=True, null=True)
    template_iris = models.TextField(blank=True, null=True)
    template_voz = models.TextField(blank=True, null=True)
    
    # Configuración
    activa = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_expiracion = models.DateTimeField(null=True, blank=True)
    fecha_ultimo_uso = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Credencial"
        verbose_name_plural = "Credenciales"
        unique_together = ['empleado', 'tipo_credencial']
    
    def __str__(self):
        return f"{self.empleado.nombre_completo} - {self.get_tipo_credencial_display()}"

class RegistroAcceso(models.Model):
    ESTADO_ACCESO_CHOICES = [
        ('exitoso', 'Exitoso'),
        ('fallido', 'Fallido'),
        ('pendiente', 'Pendiente'),
    ]
    
    TIPO_ACCESO_CHOICES = [
        ('entrada', 'Entrada'),
        ('salida', 'Salida'),
    ]
    
    # Información principal
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    dispositivo = models.ForeignKey(Dispositivo, on_delete=models.CASCADE)
    credencial = models.ForeignKey(Credencial, on_delete=models.CASCADE)
    
    # Detalles del acceso
    fecha_hora = models.DateTimeField(default=timezone.now)
    estado = models.CharField(max_length=15, choices=ESTADO_ACCESO_CHOICES)
    tipo_acceso = models.CharField(max_length=10, choices=TIPO_ACCESO_CHOICES, default='entrada')
    nivel_confianza = models.FloatField(
        null=True, 
        blank=True, 
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)]
    )
    
    # Información contextual
    sede = models.ForeignKey(Sede, on_delete=models.CASCADE)
    observaciones = models.TextField(blank=True, null=True)
    intento = models.IntegerField(default=1)
    
    # Auditoría
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Registro de Acceso"
        verbose_name_plural = "Registros de Acceso"
        ordering = ['-fecha_hora']
        indexes = [
            models.Index(fields=['fecha_hora', 'empleado']),
            models.Index(fields=['estado', 'dispositivo']),
        ]
    
    def __str__(self):
        return f"{self.empleado.nombre_completo} - {self.dispositivo.nombre} - {self.fecha_hora}"

class Alerta(models.Model):
    TIPO_ALERTA_CHOICES = [
        ('dispositivo', 'Estado de Dispositivo'),
        ('seguridad', 'Evento de Seguridad'),
        ('sistema', 'Actualización del Sistema'),
        ('usuario', 'Actividad de Usuarios'),
        ('mantenimiento', 'Mantenimiento del Sistema'),
        ('acceso', 'Evento de Acceso'),
        ('red', 'Problema de Red'),
    ]
    
    PRIORIDAD_CHOICES = [
        ('critica', 'Crítica'),
        ('alta', 'Alta'),
        ('media', 'Media'),
        ('baja', 'Baja'),
        ('informativa', 'Informativa'),
    ]
    
    titulo = models.CharField(max_length=200)
    mensaje = models.TextField()
    tipo_alerta = models.CharField(max_length=20, choices=TIPO_ALERTA_CHOICES)
    prioridad = models.CharField(max_length=15, choices=PRIORIDAD_CHOICES)
    
    # Relaciones opcionales
    dispositivo = models.ForeignKey(Dispositivo, on_delete=models.CASCADE, null=True, blank=True)
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, null=True, blank=True)
    registro_acceso = models.ForeignKey(RegistroAcceso, on_delete=models.CASCADE, null=True, blank=True)
    
    # Estado
    leida = models.BooleanField(default=False)
    archivada = models.BooleanField(default=False)
    resuelta = models.BooleanField(default=False)
    
    # Auditoría
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_leida = models.DateTimeField(null=True, blank=True)
    fecha_resuelta = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Alerta"
        verbose_name_plural = "Alertas"
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"{self.titulo} ({self.get_prioridad_display()})"

class Notificacion(models.Model):
    TIPO_NOTIFICACION_CHOICES = [
        ('alerta', 'Alertas del Sistema'),
        ('dispositivo', 'Estado de Dispositivos'),
        ('seguridad', 'Eventos de Seguridad'),
        ('sistema', 'Actualizaciones del Sistema'),
        ('usuario', 'Actividad de Usuarios'),
        ('acceso', 'Registro de Acceso'),
        ('reporte', 'Reporte Generado'),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notificaciones')
    titulo = models.CharField(max_length=200)
    mensaje = models.TextField()
    tipo_notificacion = models.CharField(max_length=20, choices=TIPO_NOTIFICACION_CHOICES)
    prioridad = models.CharField(max_length=15, choices=Alerta.PRIORIDAD_CHOICES)
    
    # Estado
    leida = models.BooleanField(default=False)
    archivada = models.BooleanField(default=False)
    
    # Enlace a recursos relacionados
    url_accion = models.CharField(max_length=500, blank=True, null=True)
    recurso_id = models.IntegerField(null=True, blank=True)
    
    # Auditoría
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_leida = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Notificación"
        verbose_name_plural = "Notificaciones"
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"{self.titulo} - {self.usuario.username}"

class SolicitudSoporte(models.Model):
    CATEGORIA_CHOICES = [
        ('tecnico', 'Problema Técnico'),
        ('cuenta', 'Problema con la Cuenta'),
        ('biometrico', 'Problema con el biométrico'),
        ('funcionalidad', 'Error de Funcionalidad'),
        ('dispositivo', 'Falla de Dispositivo'),
        ('acceso', 'Problema de Acceso'),
        ('otro', 'Otro'),
    ]
    
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('en_proceso', 'En Proceso'),
        ('resuelto', 'Resuelto'),
        ('cerrado', 'Cerrado'),
    ]
    
    # Información del solicitante
    nombre_completo = models.CharField(max_length=200)
    email = models.EmailField()
    telefono = models.CharField(max_length=20, blank=True, null=True)
    
    # Información del problema
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES)
    asunto = models.CharField(max_length=200)
    descripcion = models.TextField()
    
    # Relaciones opcionales
    empleado = models.ForeignKey(Empleado, on_delete=models.SET_NULL, null=True, blank=True)
    dispositivo = models.ForeignKey(Dispositivo, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Estado
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    prioridad = models.CharField(max_length=15, choices=Alerta.PRIORIDAD_CHOICES, default='media')
    
    # Seguimiento
    respuesta = models.TextField(blank=True, null=True)
    tecnico_asignado = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Auditoría
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    fecha_cierre = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Solicitud de Soporte"
        verbose_name_plural = "Solicitudes de Soporte"
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"{self.asunto} - {self.nombre_completo}"

class ConfiguracionSistema(models.Model):
    TIPO_CONFIG_CHOICES = [
        ('string', 'Texto'),
        ('integer', 'Número'),
        ('boolean', 'Booleano'),
        ('json', 'JSON'),
        ('float', 'Decimal'),
        ('time', 'Hora'),
        ('date', 'Fecha'),
    ]
    
    clave = models.CharField(max_length=100, unique=True)
    valor = models.TextField()
    tipo = models.CharField(max_length=50, choices=TIPO_CONFIG_CHOICES)
    descripcion = models.TextField(blank=True, null=True)
    categoria = models.CharField(max_length=50, default='general', choices=[
        ('general', 'General'),
        ('seguridad', 'Seguridad'),
        ('notificaciones', 'Notificaciones'),
        ('backup', 'Backup'),
        ('horarios', 'Horarios'),
        ('red', 'Red'),
    ])
    editable = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Configuración del Sistema"
        verbose_name_plural = "Configuraciones del Sistema"
    
    def __str__(self):
        return self.clave

class Reporte(models.Model):
    TIPO_REPORTE_CHOICES = [
        ('asistencia', 'Reporte de Asistencia'),
        ('accesos', 'Reporte de Accesos'),
        ('dispositivos', 'Reporte de Dispositivos'),
        ('seguridad', 'Reporte de Seguridad'),
        ('empleados', 'Reporte de Empleados'),
        ('alertas', 'Reporte de Alertas'),
    ]
    
    FORMATO_CHOICES = [
        ('pdf', 'PDF'),
        ('excel', 'Excel'),
        ('csv', 'CSV'),
    ]
    
    nombre = models.CharField(max_length=200)
    tipo_reporte = models.CharField(max_length=20, choices=TIPO_REPORTE_CHOICES)
    parametros = models.JSONField(default=dict)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Configuración de ejecución
    programado = models.BooleanField(default=False)
    frecuencia = models.CharField(max_length=50, blank=True, null=True)
    formato = models.CharField(max_length=10, choices=FORMATO_CHOICES, default='pdf')
    
    # Secciones a incluir
    incluir_datos = models.BooleanField(default=True)
    incluir_resumen = models.BooleanField(default=True)
    incluir_graficos = models.BooleanField(default=False)
    incluir_filtros = models.BooleanField(default=False)
    
    # Auditoría
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    ultima_ejecucion = models.DateTimeField(null=True, blank=True)
    ejecuciones_completadas = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = "Reporte"
        verbose_name_plural = "Reportes"
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return self.nombre

class HorarioLaboral(models.Model):
    DIA_SEMANA_CHOICES = [
        (1, 'Lunes'),
        (2, 'Martes'),
        (3, 'Miércoles'),
        (4, 'Jueves'),
        (5, 'Viernes'),
        (6, 'Sábado'),
        (7, 'Domingo'),
    ]
    
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, related_name='horarios')
    dia_semana = models.IntegerField(choices=DIA_SEMANA_CHOICES)
    hora_entrada = models.TimeField()
    hora_salida = models.TimeField()
    tolerancia_entrada = models.IntegerField(default=15)  # minutos
    tolerancia_salida = models.IntegerField(default=15)  # minutos
    activo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Horario Laboral"
        verbose_name_plural = "Horarios Laborales"
        unique_together = ['empleado', 'dia_semana']
    
    def __str__(self):
        return f"{self.empleado.nombre_completo} - {self.get_dia_semana_display()}"

class Auditoria(models.Model):
    TIPO_ACCION_CHOICES = [
        ('login', 'Inicio de Sesión'),
        ('logout', 'Cierre de Sesión'),
        ('crear', 'Creación'),
        ('modificar', 'Modificación'),
        ('eliminar', 'Eliminación'),
        ('acceso', 'Acceso a Recurso'),
        ('exportar', 'Exportación'),
        ('importar', 'Importación'),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    accion = models.CharField(max_length=20, choices=TIPO_ACCION_CHOICES)
    modelo = models.CharField(max_length=100)
    objeto_id = models.IntegerField(null=True, blank=True)
    descripcion = models.TextField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True, null=True)
    
    fecha_accion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Auditoría"
        verbose_name_plural = "Auditorías"
        ordering = ['-fecha_accion']
    
    def __str__(self):
        return f"{self.usuario.username} - {self.accion} - {self.modelo}"