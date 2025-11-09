// Datos de ejemplo para las notificaciones
const notificaciones = [
    {
        id: 1,
        titulo: "Dispositivo BIO-001 Caído",
        mensaje: "El dispositivo de huella dactilar en Recepción Principal ha dejado de responder. No se están registrando accesos desde las 08:45 AM.",
        tipo: "Alerta de Dispositivo",
        prioridad: "critica",
        estado: "no-leida",
        fecha: "Hace 15 minutos",
        origen: "Sistema de Monitoreo",
        usuario: "Sistema Automático",
        dispositivo: "BIO-001 - Recepción Principal"
    },
    {
        id: 2,
        titulo: "Intento de Acceso No Autorizado",
        mensaje: "Múltiples intentos fallidos de autenticación en el dispositivo BIO-045. Usuario: Carlos Mendoza. Se ha bloqueado temporalmente el acceso.",
        tipo: "Evento de Seguridad",
        prioridad: "alta",
        estado: "no-leida",
        fecha: "Hace 2 horas",
        origen: "Sistema de Seguridad",
        usuario: "Carlos Mendoza",
        dispositivo: "BIO-045 - RH Piso 3"
    },
    {
        id: 3,
        titulo: "Backup Completado Exitosamente",
        mensaje: "El backup automático de la base de datos se ha completado correctamente. Tamaño del archivo: 2.4 GB. Duración: 15 minutos.",
        tipo: "Mantenimiento del Sistema",
        prioridad: "media",
        estado: "leida",
        fecha: "Hoy, 02:30 AM",
        origen: "Sistema de Backup",
        usuario: "Sistema Automático",
        dispositivo: "Servidor Central"
    },
    {
        id: 4,
        titulo: "Nuevo Usuario Registrado",
        mensaje: "Se ha registrado un nuevo usuario en el sistema: Laura Martínez. Departamento: Ventas. Dispositivo asignado: BIO-201.",
        tipo: "Gestión de Usuarios",
        prioridad: "baja",
        estado: "no-leida",
        fecha: "Ayer, 04:15 PM",
        origen: "Sistema de Usuarios",
        usuario: "Administrador",
        dispositivo: "BIO-201 - Ventas Piso 2"
    },
    {
        id: 5,
        titulo: "Actualización de Software Disponible",
        mensaje: "Nueva versión 2.1.5 del sistema Biometrika disponible. Incluye mejoras en el rendimiento y corrección de errores menores.",
        tipo: "Actualización del Sistema",
        prioridad: "informativa",
        estado: "leida",
        fecha: "Ayer, 10:20 AM",
        origen: "Sistema de Actualizaciones",
        usuario: "Sistema Automático",
        dispositivo: "Todos los dispositivos"
    },
    {
        id: 6,
        titulo: "Problema de Conectividad en Sede Norte",
        mensaje: "Se detectó pérdida de conectividad con los dispositivos biométricos en la Sede Norte. Verificando estado de la red.",
        tipo: "Problema de Red",
        prioridad: "critica",
        estado: "no-leida",
        fecha: "15/03/2024, 09:30 AM",
        origen: "Sistema de Red",
        usuario: "Sistema Automático",
        dispositivo: "Sede Norte - Todos"
    }
];

// Variables globales
let notificacionesFiltradas = [...notificaciones];
let notificacionesFiltroActual = 'todas';

// Funcionalidad para la página de notificaciones
document.addEventListener('DOMContentLoaded', function() {
    // Inicializar eventos
    inicializarEventos();
    
    // Cargar notificaciones
    actualizarResumen();
});

function inicializarEventos() {
    // Botones de filtro
    document.getElementById('btnAplicar').addEventListener('click', aplicarFiltros);
    document.getElementById('btnLimpiar').addEventListener('click', limpiarFiltros);
    document.getElementById('btnMarcarTodas').addEventListener('click', marcarTodasComoLeidas);
    
    // Modal de detalles
    document.querySelector('.close').addEventListener('click', cerrarModal);
    document.getElementById('btnCerrarDetalle').addEventListener('click', cerrarModal);
    document.getElementById('btnAccionDetalle').addEventListener('click', tomarAccion);
    
    // Cerrar modal al hacer clic fuera
    window.addEventListener('click', function(event) {
        const modal = document.getElementById('modalDetalle');
        if (event.target === modal) {
            cerrarModal();
        }
    });
    
    // Eventos de las tarjetas de resumen
    document.querySelectorAll('.resumen-item').forEach(item => {
        item.addEventListener('click', function() {
            const tipo = this.classList[1]; // no-leidas, criticas, hoy, total
            filtrarPorTipo(tipo);
        });
    });
    
    // Inicializar botones de acción de notificaciones
    inicializarBotonesNotificaciones();
}

function inicializarBotonesNotificaciones() {
    // Botones de marcar como leída
    document.querySelectorAll('.btn-marcar').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.stopPropagation();
            const notificacionItem = this.closest('.notificacion-item');
            marcarComoLeida(notificacionItem);
        });
    });
    
    // Botones de archivar
    document.querySelectorAll('.btn-archivar').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.stopPropagation();
            const notificacionItem = this.closest('.notificacion-item');
            archivarNotificacion(notificacionItem);
        });
    });
    
    // Botones de detalle
    document.querySelectorAll('.btn-detalle').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.stopPropagation();
            const notificacionItem = this.closest('.notificacion-item');
            mostrarDetalles(notificacionItem);
        });
    });
    
    // Click en toda la notificación para mostrar detalles
    document.querySelectorAll('.notificacion-item').forEach(item => {
        item.addEventListener('click', function() {
            mostrarDetalles(this);
        });
    });
}

function aplicarFiltros() {
    const tipo = document.getElementById('filtro-tipo').value;
    const prioridad = document.getElementById('filtro-prioridad').value;
    const estado = document.getElementById('filtro-estado').value;
    const fecha = document.getElementById('filtro-fecha').value;
    
    notificacionesFiltradas = notificaciones.filter(notif => {
        if (tipo && notif.tipo !== tipo) return false;
        if (prioridad && notif.prioridad !== prioridad) return false;
        if (estado && notif.estado !== estado) return false;
        // Aquí iría la lógica de filtrado por fecha
        return true;
    });
    
    mostrarNotificacionesFiltradas();
    mostrarNotificacionSistema('Filtros aplicados correctamente', 'success');
}

function limpiarFiltros() {
    document.getElementById('filtro-tipo').value = '';
    document.getElementById('filtro-prioridad').value = '';
    document.getElementById('filtro-estado').value = '';
    document.getElementById('filtro-fecha').value = '';
    
    notificacionesFiltradas = [...notificaciones];
    mostrarNotificacionesFiltradas();
    mostrarNotificacionSistema('Filtros limpiados', 'info');
}

function filtrarPorTipo(tipo) {
    switch(tipo) {
        case 'no-leidas':
            notificacionesFiltradas = notificaciones.filter(n => n.estado === 'no-leida');
            break;
        case 'criticas':
            notificacionesFiltradas = notificaciones.filter(n => n.prioridad === 'critica');
            break;
        case 'hoy':
            // Simular filtro de hoy
            notificacionesFiltradas = notificaciones.filter(n => n.fecha.includes('Hoy') || n.fecha.includes('Hace'));
            break;
        case 'total':
            notificacionesFiltradas = [...notificaciones];
            break;
    }
    
    notificacionesFiltroActual = tipo;
    mostrarNotificacionesFiltradas();
    
    // Actualizar clases activas en resumen
    document.querySelectorAll('.resumen-item').forEach(item => {
        item.classList.remove('activa');
    });
    document.querySelector(`.resumen-item.${tipo}`).classList.add('activa');
}

function mostrarNotificacionesFiltradas() {
    const container = document.querySelector('.notificaciones-container');
    container.innerHTML = '';
    
    notificacionesFiltradas.forEach(notif => {
        const notificacionElement = crearElementoNotificacion(notif);
        container.appendChild(notificacionElement);
    });
    
    // Re-inicializar eventos de los nuevos botones
    inicializarBotonesNotificaciones();
    actualizarResumen();
}

function crearElementoNotificacion(notif) {
    const div = document.createElement('div');
    div.className = `notificacion-item ${notif.estado} ${notif.prioridad}`;
    div.setAttribute('data-id', notif.id);
    
    // Determinar icono según tipo
    let icono = 'fa-bell';
    switch(notif.tipo) {
        case 'Alerta de Dispositivo':
            icono = 'fa-triangle-exclamation';
            break;
        case 'Evento de Seguridad':
            icono = 'fa-shield-halved';
            break;
        case 'Mantenimiento del Sistema':
            icono = 'fa-database';
            break;
        case 'Gestión de Usuarios':
            icono = 'fa-user-plus';
            break;
        case 'Actualización del Sistema':
            icono = 'fa-cloud-arrow-down';
            break;
        case 'Problema de Red':
            icono = 'fa-network-wired';
            break;
    }
    
    div.innerHTML = `
        <div class="notificacion-icono">
            <i class="fa-solid ${icono}"></i>
        </div>
        <div class="notificacion-contenido">
            <div class="notificacion-header">
                <h4>${notif.titulo}</h4>
                <span class="notificacion-fecha">${notif.fecha}</span>
            </div>
            <p class="notificacion-mensaje">${notif.mensaje}</p>
            <div class="notificacion-detalles">
                <span class="notificacion-tipo">${notif.tipo}</span>
                <span class="notificacion-prioridad ${notif.prioridad}">${notif.prioridad}</span>
            </div>
        </div>
        <div class="notificacion-acciones">
            <button class="btn-notificacion btn-marcar" title="Marcar como leída">
                <i class="fa-solid fa-check"></i>
            </button>
            <button class="btn-notificacion btn-archivar" title="Archivar">
                <i class="fa-solid fa-box-archive"></i>
            </button>
            <button class="btn-notificacion btn-detalle" title="Ver detalles">
                <i class="fa-solid fa-ellipsis-vertical"></i>
            </button>
        </div>
    `;
    
    return div;
}

function marcarComoLeida(notificacionElement) {
    const id = parseInt(notificacionElement.getAttribute('data-id'));
    const notificacion = notificaciones.find(n => n.id === id);
    
    if (notificacion && notificacion.estado === 'no-leida') {
        notificacion.estado = 'leida';
        notificacionElement.classList.remove('no-leida');
        notificacionElement.classList.add('leida');
        
        // Quitar el fondo especial de no leída
        notificacionElement.style.backgroundColor = '';
        
        mostrarNotificacionSistema('Notificación marcada como leída', 'success');
        actualizarResumen();
    }
}

function archivarNotificacion(notificacionElement) {
    const id = parseInt(notificacionElement.getAttribute('data-id'));
    
    // En una implementación real, aquí se enviaría una solicitud al servidor
    notificacionElement.style.opacity = '0.5';
    notificacionElement.style.pointerEvents = 'none';
    
    setTimeout(() => {
        notificacionElement.remove();
        mostrarNotificacionSistema('Notificación archivada', 'info');
        actualizarResumen();
    }, 300);
}

function mostrarDetalles(notificacionElement) {
    const id = parseInt(notificacionElement.getAttribute('data-id'));
    const notificacion = notificaciones.find(n => n.id === id);
    
    if (notificacion) {
        // Llenar el modal con los detalles
        document.getElementById('detalle-titulo').textContent = notificacion.titulo;
        document.getElementById('detalle-mensaje').textContent = notificacion.mensaje;
        document.getElementById('detalle-fecha').textContent = notificacion.fecha;
        document.getElementById('detalle-prioridad').textContent = notificacion.prioridad;
        document.getElementById('detalle-tipo').textContent = notificacion.tipo;
        document.getElementById('detalle-origen').textContent = notificacion.origen;
        document.getElementById('detalle-usuario').textContent = notificacion.usuario;
        document.getElementById('detalle-dispositivo').textContent = notificacion.dispositivo;
        
        // Estilizar la prioridad
        const prioridadElement = document.getElementById('detalle-prioridad');
        prioridadElement.className = 'detalle-prioridad';
        prioridadElement.classList.add(notificacion.prioridad);
        
        // Mostrar el modal
        document.getElementById('modalDetalle').style.display = 'block';
        
        // Marcar como leída si no lo está
        if (notificacion.estado === 'no-leida') {
            marcarComoLeida(notificacionElement);
        }
    }
}

function cerrarModal() {
    document.getElementById('modalDetalle').style.display = 'none';
}

function tomarAccion() {
    // Aquí iría la lógica para tomar acción específica según el tipo de notificación
    mostrarNotificacionSistema('Acción ejecutada correctamente', 'success');
    cerrarModal();
}

function marcarTodasComoLeidas() {
    notificaciones.forEach(notif => {
        notif.estado = 'leida';
    });
    
    // Actualizar la interfaz
    document.querySelectorAll('.notificacion-item').forEach(item => {
        item.classList.remove('no-leida');
        item.classList.add('leida');
        item.style.backgroundColor = '';
    });
    
    mostrarNotificacionSistema('Todas las notificaciones marcadas como leídas', 'success');
    actualizarResumen();
}

function actualizarResumen() {
    const noLeidas = notificaciones.filter(n => n.estado === 'no-leida').length;
    const criticas = notificaciones.filter(n => n.prioridad === 'critica').length;
    const hoy = notificaciones.filter(n => n.fecha.includes('Hoy') || n.fecha.includes('Hace')).length;
    const total = notificaciones.length;
    
    document.querySelector('.resumen-item.no-leidas .resumen-valor').textContent = noLeidas;
    document.querySelector('.resumen-item.criticas .resumen-valor').textContent = criticas;
    document.querySelector('.resumen-item.hoy .resumen-valor').textContent = hoy;
    document.querySelector('.resumen-item.total .resumen-valor').textContent = total;
    
    // Actualizar información de paginación
    document.querySelector('.paginacion-info').textContent = 
        `Mostrando 1-${notificacionesFiltradas.length} de ${notificaciones.length} notificaciones`;
}

function mostrarNotificacionSistema(mensaje, tipo) {
    const notificacion = document.getElementById('notificacionSistema');
    notificacion.textContent = mensaje;
    notificacion.className = `notificacion-sistema ${tipo}`;
    notificacion.style.display = 'block';
    
    // Ocultar después de 3 segundos
    setTimeout(() => {
        notificacion.style.display = 'none';
    }, 3000);
}