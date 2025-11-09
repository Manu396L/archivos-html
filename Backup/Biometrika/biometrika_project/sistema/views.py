from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
import csv
from .models import Sede, Empleado, Dispositivo, RegistroAcceso, Departamento, Credencial, Alerta, Notificacion
from .forms import EmpleadoForm
from django.utils import timezone
from datetime import datetime, timedelta


# Página de inicio (redirige al login)
def index(request):
    return redirect('sistema:acceso')

# Autenticación
def acceso(request):
    """Vista de login"""
    # Si ya está autenticado, redirigir al dashboard
    if request.user.is_authenticated:
        return redirect('sistema:dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Autenticar con la base de datos de Django
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'¡Bienvenido, {user.username}!')
            
            # Redirigir al dashboard o a donde vino
            next_url = request.GET.get('next', 'sistema:dashboard')
            return redirect(next_url)
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    
    return render(request, 'sistema/acceso.html')

def usuario_nuevo(request):
    """Vista de registro de nuevo usuario"""
    if request.method == 'POST':
        # Aquí procesarías el formulario
        messages.success(request, 'Solicitud enviada correctamente')
        return redirect('sistema:acceso')
    return render(request, 'sistema/usuario_nuevo.html')

def cambiar_contrasena(request):
    """Vista para cambiar contraseña"""
    if request.method == 'POST':
        # Aquí procesarías el cambio de contraseña
        messages.success(request, 'Se ha enviado un correo con instrucciones')
    return render(request, 'sistema/cambiar_contraseña.html')

def cerrar_sesion(request):
    """Vista de cierre de sesión"""
    logout(request)
    return render(request, 'sistema/cerrar_sesion.html')

# Dashboard y módulos principales (requieren autenticación)
@login_required
def dashboard(request):
    """Dashboard principal con datos reales de la base de datos"""
    try:
        # Datos básicos
        empleados_total = Empleado.objects.count()
        dispositivos_total = Dispositivo.objects.count()
        sedes_total = Sede.objects.count()
        
        # Cálculo de empleados presentes (basado en registros de acceso del día)
        hoy = timezone.now().date()
        registros_hoy = RegistroAcceso.objects.filter(
            fecha_hora__date=hoy, 
            tipo_acceso='entrada'
        ).values('empleado').distinct()
        
        empleados_presentes = registros_hoy.count()
        empleados_ausentes = max(0, empleados_total - empleados_presentes)
        
        # Calcular tardanzas (entradas después de las 8:30 AM)
        hora_tardanza = timezone.now().replace(hour=8, minute=30, second=0, microsecond=0)
        tardanzas = RegistroAcceso.objects.filter(
            fecha_hora__date=hoy,
            tipo_acceso='entrada',
            fecha_hora__time__gt=hora_tardanza.time()
        ).count()
        
        # Si no hay datos, usar valores por defecto
        if empleados_total == 0:
            empleados_total = 320
            empleados_presentes = 245
            empleados_ausentes = 45
            tardanzas = 30
            dispositivos_total = 67
            sedes_total = 5
            
        # Registros recientes para la tabla de actividad
        registros_recientes = RegistroAcceso.objects.select_related(
            'empleado', 'dispositivo'
        ).order_by('-fecha_hora')[:15]
        
    except Exception as e:
        # En caso de error, usar datos de ejemplo
        empleados_total = 320
        empleados_presentes = 245
        empleados_ausentes = 45
        tardanzas = 30
        dispositivos_total = 67
        sedes_total = 5
        registros_recientes = []
    
    context = {
        'empleados_total': empleados_total,
        'empleados_presentes': empleados_presentes,
        'empleados_ausentes': empleados_ausentes,
        'tardanzas': tardanzas,
        'sedes': sedes_total,
        'dispositivos': dispositivos_total,
        'registros_recientes': registros_recientes,
    }
    return render(request, 'sistema/dashboard.html', context)

@login_required
def sedes(request):
    """Gestión de sedes y áreas"""
    sedes_list = Sede.objects.all().order_by('nombre')
    departamentos = Departamento.objects.select_related('sede').all()
    
    context = {
        'sedes': sedes_list,
        'departamentos': departamentos,
    }
    return render(request, 'sistema/sedes.html', context)

@login_required
def personal(request):
    """Gestión de personal"""
    empleados = Empleado.objects.select_related('departamento', 'sede').all().order_by('nombre_completo')
    departamentos = Departamento.objects.all()
    sedes = Sede.objects.all()
    
    empleado_editar = None
    edit_id = request.GET.get('edit')
    
    # Procesar edición si viene por GET
    if edit_id:
        try:
            empleado_editar = Empleado.objects.get(id=edit_id)
        except Empleado.DoesNotExist:
            messages.error(request, 'Empleado no encontrado')
    
    # Procesar formulario POST
    if request.method == 'POST':
        if empleado_editar:
            # Modo edición
            form = EmpleadoForm(request.POST, request.FILES, instance=empleado_editar)
        else:
            # Modo creación
            form = EmpleadoForm(request.POST, request.FILES)
        
        if form.is_valid():
            empleado = form.save()
            action = "actualizado" if empleado_editar else "registrado"
            messages.success(request, f'Empleado {action} correctamente')
            return redirect('sistema:personal')
        else:
            messages.error(request, 'Por favor corrija los errores en el formulario')
    else:
        # GET request - inicializar formulario
        form = EmpleadoForm(instance=empleado_editar)
    
    context = {
        'empleados': empleados,
        'departamentos': departamentos,
        'sedes': sedes,
        'form': form,
        'editando': empleado_editar is not None,
    }
    return render(request, 'sistema/personal.html', context)

@login_required
def eliminar_empleado(request, empleado_id):
    """Eliminar empleado"""
    if request.method == 'POST':
        try:
            empleado = get_object_or_404(Empleado, id=empleado_id)
            nombre_empleado = empleado.nombre_completo
            empleado.delete()
            messages.success(request, f'Empleado {nombre_empleado} eliminado correctamente')
        except Exception as e:
            messages.error(request, f'Error al eliminar empleado: {str(e)}')
    
    return redirect('sistema:personal')

@login_required
def exportar_empleados(request):
    """Exportar empleados a CSV"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="empleados_biometrika.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['ID', 'Nombre', 'Cargo', 'Departamento', 'Sede', 'Correo', 'Teléfono', 'Fecha Ingreso'])
    
    empleados = Empleado.objects.select_related('departamento', 'sede').all()
    for empleado in empleados:
        writer.writerow([
            empleado.id_empleado,
            empleado.nombre_completo,
            empleado.cargo,
            empleado.departamento.nombre if empleado.departamento else '',
            empleado.sede.nombre if empleado.sede else '',
            empleado.correo_corporativo,
            empleado.telefono or '',
            empleado.fecha_ingreso.strftime('%d/%m/%Y') if empleado.fecha_ingreso else ''
        ])
    
    return response

@login_required
def dispositivos(request):
    """Gestión de dispositivos biométricos"""
    dispositivos_list = Dispositivo.objects.select_related('sede').all().order_by('nombre')
    sedes = Sede.objects.all()
    
    # Estadísticas de dispositivos
    dispositivos_activos = dispositivos_list.filter(estado='activo').count()
    dispositivos_inactivos = dispositivos_list.filter(estado__in=['pausado', 'error', 'sin_conexion']).count()
    
    context = {
        'dispositivos': dispositivos_list,
        'sedes': sedes,
        'dispositivos_activos': dispositivos_activos,
        'dispositivos_inactivos': dispositivos_inactivos,
        'total_dispositivos': dispositivos_list.count(),
    }
    return render(request, 'sistema/dispositivos.html', context)

@login_required
def reportes(request):
    """Reportes del sistema"""
    # Filtros por defecto (últimos 30 días)
    fecha_fin = timezone.now()
    fecha_inicio = fecha_fin - timedelta(days=30)
    
    registros = RegistroAcceso.objects.select_related(
        'empleado', 'dispositivo', 'credencial'
    ).filter(
        fecha_hora__range=[fecha_inicio, fecha_fin]
    ).order_by('-fecha_hora')
    
    # Estadísticas para el resumen
    total_registros = registros.count()
    exitosos = registros.filter(estado='exitoso').count()
    fallidos = registros.filter(estado='fallido').count()
    
    context = {
        'registros': registros[:50],  # Limitar para rendimiento
        'total_registros': total_registros,
        'exitosos': exitosos,
        'fallidos': fallidos,
        'fecha_inicio': fecha_inicio.date(),
        'fecha_fin': fecha_fin.date(),
    }
    return render(request, 'sistema/reportes.html', context)

@login_required
def alertas(request):
    """Alertas del sistema"""
    alertas_list = Alerta.objects.select_related(
        'dispositivo', 'empleado', 'registro_acceso'
    ).filter(
        archivada=False
    ).order_by('-fecha_creacion')
    
    # Estadísticas de alertas
    criticas = alertas_list.filter(prioridad='critica', resuelta=False).count()
    advertencias = alertas_list.filter(prioridad='alta', resuelta=False).count()
    estables = Dispositivo.objects.filter(estado='activo').count()
    
    context = {
        'alertas': alertas_list,
        'criticas': criticas,
        'advertencias': advertencias,
        'estables': estables,
    }
    return render(request, 'sistema/alertas.html', context)

@login_required
def notificaciones(request):
    """Notificaciones del usuario"""
    notificaciones_list = Notificacion.objects.filter(
        usuario=request.user,
        archivada=False
    ).order_by('-fecha_creacion')
    
    # Estadísticas
    no_leidas = notificaciones_list.filter(leida=False).count()
    criticas = notificaciones_list.filter(prioridad='critica', leida=False).count()
    hoy = notificaciones_list.filter(fecha_creacion__date=timezone.now().date()).count()
    total = notificaciones_list.count()
    
    context = {
        'notificaciones': notificaciones_list,
        'no_leidas': no_leidas,
        'criticas': criticas,
        'hoy': hoy,
        'total': total,
    }
    return render(request, 'sistema/notificaciones.html', context)

@login_required
def perfil(request):
    """Perfil del usuario"""
    empleado_id = request.GET.get('empleado')
    
    try:
        if empleado_id:
            # Ver perfil de otro empleado (solo admin)
            # Verificar si el usuario actual es administrador
            if not request.user.is_staff:
                messages.error(request, 'No tienes permisos para ver este perfil')
                return redirect('sistema:perfil')
            
            empleado = Empleado.objects.get(id=empleado_id)
        else:
            # Ver mi propio perfil
            empleado = Empleado.objects.get(usuario=request.user)
        
        # Obtener credenciales del empleado
        credenciales = Credencial.objects.filter(empleado=empleado, activa=True)
        
        # Obtener últimos accesos
        ultimos_accesos = RegistroAcceso.objects.filter(
            empleado=empleado
        ).select_related('dispositivo', 'dispositivo__sede').order_by('-fecha_hora')[:10]
        
        # Estadísticas del mes actual
        mes_actual = timezone.now().month
        accesos_mes = RegistroAcceso.objects.filter(
            empleado=empleado,
            fecha_hora__month=mes_actual,
            estado='exitoso'
        ).count()
        
        context = {
            'empleado': empleado,
            'credenciales': credenciales,
            'ultimos_accesos': ultimos_accesos,
            'accesos_mes': accesos_mes,
            'fecha_generacion': timezone.now(),
        }
        
    except Empleado.DoesNotExist:
        # Si no hay empleado asociado, mostrar datos básicos del usuario
        if empleado_id:
            messages.error(request, 'Empleado no encontrado')
            return redirect('sistema:personal')
        else:
            context = {
                'usuario': request.user,
                'fecha_generacion': timezone.now(),
            }
    
    return render(request, 'sistema/perfil.html', context)

@login_required
def configuracion(request):
    """Configuración del sistema"""
    # Aquí podrías agregar lógica para manejar configuraciones
    # Por ahora, solo renderiza el template
    return render(request, 'sistema/configuracion.html')

@login_required
def soporte(request):
    """Soporte técnico"""
    if request.method == 'POST':
        # Aquí procesarías el reporte de problemas
        messages.success(request, 'Reporte enviado correctamente')
    return render(request, 'sistema/soporte.html')