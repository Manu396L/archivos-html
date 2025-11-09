// Datos de ejemplo para los reportes
const datosReportes = [
    { id: 'BIO-2024-001', usuario: 'Juan Carlos Rodríguez', tipo: 'huella', fecha: '15/03/2024 08:30:25', dispositivo: 'Terminal 1 - Recepción', estado: 'exitoso', confianza: 98 },
    { id: 'BIO-2024-002', usuario: 'María Elena González', tipo: 'facial', fecha: '15/03/2024 08:32:10', dispositivo: 'Terminal 2 - Oficinas', estado: 'exitoso', confianza: 94 },
    { id: 'BIO-2024-003', usuario: 'Carlos Alberto Méndez', tipo: 'huella', fecha: '15/03/2024 08:35:42', dispositivo: 'Terminal 3 - Laboratorio', estado: 'fallido', confianza: 45 },
    { id: 'BIO-2024-004', usuario: 'Ana Patricia Silva', tipo: 'voz', fecha: '15/03/2024 08:40:15', dispositivo: 'Dispositivo Móvil', estado: 'exitoso', confianza: 87 },
    { id: 'BIO-2024-005', usuario: 'Roberto José Hernández', tipo: 'iris', fecha: '15/03/2024 08:45:33', dispositivo: 'Terminal 1 - Recepción', estado: 'exitoso', confianza: 96 },
    { id: 'BIO-2024-006', usuario: 'Laura Isabel Fernández', tipo: 'huella', fecha: '15/03/2024 08:50:22', dispositivo: 'Terminal 2 - Oficinas', estado: 'pendiente', confianza: 0 },
    { id: 'BIO-2024-007', usuario: 'Miguel Ángel Torres', tipo: 'facial', fecha: '15/03/2024 08:55:47', dispositivo: 'Terminal 3 - Laboratorio', estado: 'exitoso', confianza: 91 },
    { id: 'BIO-2024-008', usuario: 'Sofía Alejandra Ramírez', tipo: 'huella', fecha: '15/03/2024 09:02:18', dispositivo: 'Terminal 1 - Recepción', estado: 'fallido', confianza: 32 },
    { id: 'BIO-2024-009', usuario: 'David Eduardo Castro', tipo: 'facial', fecha: '15/03/2024 09:08:33', dispositivo: 'Terminal 2 - Oficinas', estado: 'exitoso', confianza: 89 },
    { id: 'BIO-2024-010', usuario: 'Carmen Rosa Vargas', tipo: 'iris', fecha: '15/03/2024 09:15:47', dispositivo: 'Terminal 3 - Laboratorio', estado: 'exitoso', confianza: 97 }
];

// Variables globales
let datosFiltrados = [...datosReportes];
let paginaActual = 1;
const registrosPorPagina = 8;
let totalRegistros = 1247;

// Funcionalidad para la página de reportes
document.addEventListener('DOMContentLoaded', function() {
    // Inicializar eventos
    inicializarEventos();
    
    // Inicializar filtros con valores por defecto
    inicializarFiltros();
    
    // Cargar datos iniciales
    cargarDatosTabla();
    actualizarPaginacion();
});

function inicializarEventos() {
    // Botones de filtro
    document.getElementById('btnAplicar').addEventListener('click', aplicarFiltros);
    document.getElementById('btnLimpiar').addEventListener('click', limpiarFiltros);
    document.getElementById('btnExportar').addEventListener('click', mostrarModalExportar);
    
    // Modal de exportación
    document.querySelector('.close').addEventListener('click', cerrarModal);
    document.getElementById('btnExportarAhora').addEventListener('click', exportarReporte);
    document.getElementById('btnProgramar').addEventListener('click', programarExportacion);
    
    // Cerrar modal al hacer clic fuera
    window.addEventListener('click', function(event) {
        const modal = document.getElementById('modalExportar');
        if (event.target === modal) {
            cerrarModal();
        }
    });
}

function inicializarFiltros() {
    // Establecer fechas por defecto (últimos 7 días)
    const hoy = new Date();
    const hace7Dias = new Date();
    hace7Dias.setDate(hoy.getDate() - 7);
    
    document.getElementById('filtro-fecha-inicio').value = formatearFechaInput(hace7Dias);
    document.getElementById('filtro-fecha-fin').value = formatearFechaInput(hoy);
}

function formatearFechaInput(fecha) {
    const año = fecha.getFullYear();
    const mes = String(fecha.getMonth() + 1).padStart(2, '0');
    const dia = String(fecha.getDate()).padStart(2, '0');
    return `${año}-${mes}-${dia}`;
}

function aplicarFiltros() {
    // Obtener valores de los filtros
    const fechaInicio = document.getElementById('filtro-fecha-inicio').value;
    const fechaFin = document.getElementById('filtro-fecha-fin').value;
    const tipo = document.getElementById('filtro-tipo').value;
    const estado = document.getElementById('filtro-estado').value;
    const dispositivo = document.getElementById('filtro-dispositivo').value;
    const usuario = document.getElementById('filtro-usuario').value.toLowerCase();
    
    // Validar fechas
    if (fechaInicio && fechaFin && fechaInicio > fechaFin) {
        mostrarNotificacion('La fecha de inicio no puede ser mayor a la fecha de fin', 'error');
        return;
    }
    
    // Filtrar datos (simulación)
    datosFiltrados = datosReportes.filter(registro => {
        // Aquí iría la lógica real de filtrado
        // Por ahora simulamos algunos filtros básicos
        
        if (tipo && registro.tipo !== tipo) return false;
        if (estado && registro.estado !== estado) return false;
        if (usuario && !registro.usuario.toLowerCase().includes(usuario)) return false;
        
        return true;
    });
    
    paginaActual = 1;
    cargarDatosTabla();
    actualizarPaginacion();
    
    mostrarNotificacion('Filtros aplicados correctamente', 'success');
}

function limpiarFiltros() {
    // Restablecer valores por defecto
    document.getElementById('filtro-tipo').value = '';
    document.getElementById('filtro-estado').value = '';
    document.getElementById('filtro-dispositivo').value = '';
    document.getElementById('filtro-usuario').value = '';
    
    // Restablecer fechas a los últimos 7 días
    inicializarFiltros();
    
    // Restablecer datos
    datosFiltrados = [...datosReportes];
    paginaActual = 1;
    cargarDatosTabla();
    actualizarPaginacion();
    
    mostrarNotificacion('Filtros limpiados', 'info');
}

function cargarDatosTabla() {
    const tbody = document.getElementById('tbodyReportes');
    tbody.innerHTML = '';
    
    const inicio = (paginaActual - 1) * registrosPorPagina;
    const fin = inicio + registrosPorPagina;
    const registrosPagina = datosFiltrados.slice(inicio, fin);
    
    registrosPagina.forEach(registro => {
        const fila = document.createElement('tr');
        
        // Determinar icono y texto del tipo biométrico
        let iconoTipo = '';
        let textoTipo = '';
        switch(registro.tipo) {
            case 'huella':
                iconoTipo = 'fa-fingerprint';
                textoTipo = 'Huella Dactilar';
                break;
            case 'facial':
                iconoTipo = 'fa-face-smile';
                textoTipo = 'Reconocimiento Facial';
                break;
            case 'voz':
                iconoTipo = 'fa-microphone';
                textoTipo = 'Reconocimiento de Voz';
                break;
            case 'iris':
                iconoTipo = 'fa-eye';
                textoTipo = 'Escaneo de Iris';
                break;
        }
        
        // Determinar clase y texto del estado
        let claseEstado = '';
        let textoEstado = '';
        switch(registro.estado) {
            case 'exitoso':
                claseEstado = 'estado-exitoso';
                textoEstado = 'Exitoso';
                break;
            case 'fallido':
                claseEstado = 'estado-fallido';
                textoEstado = 'Fallido';
                break;
            case 'pendiente':
                claseEstado = 'estado-pendiente';
                textoEstado = 'Pendiente';
                break;
        }
        
        fila.innerHTML = `
            <td><strong>${registro.id}</strong></td>
            <td>${registro.usuario}</td>
            <td><span class="tipo-biometrico"><i class="fa-solid ${iconoTipo}"></i>${textoTipo}</span></td>
            <td>${registro.fecha}</td>
            <td>${registro.dispositivo}</td>
            <td><span class="estado-registro ${claseEstado}">${textoEstado}</span></td>
            <td>${registro.confianza}%</td>
            <td><button class="btn-detalle" onclick="mostrarDetalleRegistro('${registro.id}')"><i class="fa-solid fa-eye"></i> Detalles</button></td>
        `;
        
        tbody.appendChild(fila);
    });
    
    actualizarInfoPaginacion();
}

function actualizarPaginacion() {
    const totalPaginas = Math.ceil(datosFiltrados.length / registrosPorPagina);
    const controles = document.getElementById('controlesPaginacion');
    controles.innerHTML = '';
    
    // Botón anterior
    const btnAnterior = document.createElement('button');
    btnAnterior.className = `btn-pagina anterior ${paginaActual === 1 ? 'disabled' : ''}`;
    btnAnterior.innerHTML = '<i class="fa-solid fa-chevron-left"></i> Anterior';
    btnAnterior.disabled = paginaActual === 1;
    btnAnterior.addEventListener('click', () => {
        if (paginaActual > 1) {
            paginaActual--;
            cargarDatosTabla();
            actualizarPaginacion();
        }
    });
    controles.appendChild(btnAnterior);
    
    // Páginas
    const maxPaginasVisibles = 5;
    let inicioPagina = Math.max(1, paginaActual - Math.floor(maxPaginasVisibles / 2));
    let finPagina = Math.min(totalPaginas, inicioPagina + maxPaginasVisibles - 1);
    
    // Ajustar si estamos cerca del final
    if (finPagina - inicioPagina + 1 < maxPaginasVisibles) {
        inicioPagina = Math.max(1, finPagina - maxPaginasVisibles + 1);
    }
    
    // Puntos suspensivos iniciales
    if (inicioPagina > 1) {
        const btnPuntosInicio = document.createElement('button');
        btnPuntosInicio.className = 'btn-pagina';
        btnPuntosInicio.textContent = '...';
        btnPuntosInicio.disabled = true;
        controles.appendChild(btnPuntosInicio);
    }
    
    // Botones de páginas
    for (let i = inicioPagina; i <= finPagina; i++) {
        const btnPagina = document.createElement('button');
        btnPagina.className = `btn-pagina ${i === paginaActual ? 'activa' : ''}`;
        btnPagina.textContent = i;
        btnPagina.addEventListener('click', () => {
            paginaActual = i;
            cargarDatosTabla();
            actualizarPaginacion();
        });
        controles.appendChild(btnPagina);
    }
    
    // Puntos suspensivos finales
    if (finPagina < totalPaginas) {
        const btnPuntosFin = document.createElement('button');
        btnPuntosFin.className = 'btn-pagina';
        btnPuntosFin.textContent = '...';
        btnPuntosFin.disabled = true;
        controles.appendChild(btnPuntosFin);
    }
    
    // Botón siguiente
    const btnSiguiente = document.createElement('button');
    btnSiguiente.className = `btn-pagina siguiente ${paginaActual === totalPaginas ? 'disabled' : ''}`;
    btnSiguiente.innerHTML = 'Siguiente <i class="fa-solid fa-chevron-right"></i>';
    btnSiguiente.disabled = paginaActual === totalPaginas;
    btnSiguiente.addEventListener('click', () => {
        if (paginaActual < totalPaginas) {
            paginaActual++;
            cargarDatosTabla();
            actualizarPaginacion();
        }
    });
    controles.appendChild(btnSiguiente);
}

function actualizarInfoPaginacion() {
    const inicio = (paginaActual - 1) * registrosPorPagina + 1;
    const fin = Math.min(paginaActual * registrosPorPagina, datosFiltrados.length);
    const total = datosFiltrados.length;
    
    document.getElementById('infoPaginacion').textContent = 
        `Mostrando ${inicio}-${fin} de ${total} registros`;
}

function mostrarModalExportar() {
    document.getElementById('modalExportar').style.display = 'block';
}

function cerrarModal() {
    document.getElementById('modalExportar').style.display = 'none';
}

function exportarReporte() {
    const formato = document.querySelector('input[name="export-format"]:checked').value;
    const incluirDatos = document.getElementById('section-datos').checked;
    const incluirResumen = document.getElementById('section-resumen').checked;
    const incluirGraficos = document.getElementById('section-graficos').checked;
    const incluirFiltros = document.getElementById('section-filtros').checked;
    
    // Simular proceso de exportación
    mostrarNotificacion(`Exportando reporte en formato ${formato.toUpperCase()}...`, 'info');
    
    setTimeout(() => {
        mostrarNotificacion(`Reporte exportado en formato ${formato.toUpperCase()}`, 'success');
        cerrarModal();
    }, 2000);
}

function programarExportacion() {
    mostrarNotificacion('Funcionalidad de programación de exportaciones próximamente', 'info');
}

function mostrarDetalleRegistro(idRegistro) {
    const registro = datosReportes.find(r => r.id === idRegistro);
    if (registro) {
        // Aquí podrías mostrar un modal con los detalles
        alert(`Detalles del registro: ${idRegistro}\n\nUsuario: ${registro.usuario}\nTipo: ${registro.tipo}\nFecha: ${registro.fecha}\nDispositivo: ${registro.dispositivo}\nEstado: ${registro.estado}\nNivel de confianza: ${registro.confianza}%`);
    }
}

function mostrarNotificacion(mensaje, tipo) {
    const notificacion = document.getElementById('notificacion');
    notificacion.textContent = mensaje;
    notificacion.className = `notificacion notificacion-${tipo}`;
    notificacion.style.display = 'block';
    
    // Ocultar después de 3 segundos
    setTimeout(() => {
        notificacion.style.display = 'none';
    }, 3000);
}