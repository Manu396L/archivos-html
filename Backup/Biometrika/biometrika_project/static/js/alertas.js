// alertas.js - Funcionalidad para la página de alertas de dispositivos

document.addEventListener('DOMContentLoaded', function() {
    // Referencias a elementos del DOM
    const btnAplicar = document.querySelector('.btn-aplicar');
    const btnLimpiar = document.querySelector('.btn-limpiar');
    const botonesReportar = document.querySelectorAll('.btn-reportar');
    const filtroSede = document.getElementById('filtro-sede');
    const filtroEstado = document.getElementById('filtro-estado');
    const filtroAutenticacion = document.getElementById('filtro-autenticacion');
    const filtroDispositivo = document.getElementById('filtro-dispositivo');
    const tabla = document.querySelector('.tabla-alertas tbody');
    const filasOriginales = Array.from(tabla.querySelectorAll('tr'));

    // Función para aplicar filtros
    function aplicarFiltros() {
        const sede = filtroSede.value.toLowerCase();
        const estado = filtroEstado.value.toLowerCase();
        const autenticacion = filtroAutenticacion.value.toLowerCase();
        const dispositivo = filtroDispositivo.value.toLowerCase();

        // Mostrar todas las filas primero
        filasOriginales.forEach(fila => {
            fila.style.display = '';
        });

        // Aplicar filtros
        filasOriginales.forEach(fila => {
            const celdas = fila.querySelectorAll('td');
            const textoDispositivo = celdas[0].textContent.toLowerCase();
            const textoSede = celdas[1].textContent.toLowerCase();
            const textoEstado = celdas[6].querySelector('.estado-dispositivo').textContent.toLowerCase();
            const textoAutenticacion = celdas[5].querySelector('.tipo-autenticacion').textContent.toLowerCase();

            let mostrar = true;

            // Filtro por sede
            if (sede && !textoSede.includes(sede)) {
                mostrar = false;
            }

            // Filtro por estado
            if (estado && textoEstado !== estado) {
                mostrar = false;
            }

            // Filtro por autenticación
            if (autenticacion && !textoAutenticacion.includes(autenticacion)) {
                mostrar = false;
            }

            // Filtro por dispositivo
            if (dispositivo && !textoDispositivo.includes(dispositivo)) {
                mostrar = false;
            }

            fila.style.display = mostrar ? '' : 'none';
        });

        // Mostrar mensaje si no hay resultados
        const filasVisibles = Array.from(tabla.querySelectorAll('tr')).filter(fila => 
            fila.style.display !== 'none'
        );

        if (filasVisibles.length === 0) {
            mostrarMensajeSinResultados();
        } else {
            ocultarMensajeSinResultados();
        }

        mostrarNotificacion('Filtros aplicados correctamente', 'success');
    }

    // Función para limpiar filtros
    function limpiarFiltros() {
        filtroSede.value = '';
        filtroEstado.value = '';
        filtroAutenticacion.value = '';
        filtroDispositivo.value = '';

        // Mostrar todas las filas
        filasOriginales.forEach(fila => {
            fila.style.display = '';
        });

        ocultarMensajeSinResultados();
        mostrarNotificacion('Filtros limpiados', 'info');
    }

    // Función para reportar dispositivo
    function reportarDispositivo(boton) {
        const fila = boton.closest('tr');
        const dispositivo = fila.querySelector('td:first-child strong').textContent;
        
        if(confirm(`¿Está seguro que desea reportar el dispositivo ${dispositivo}?`)) {
            // Simular envío de reporte
            boton.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Enviando...';
            boton.disabled = true;

            setTimeout(() => {
                boton.innerHTML = '<i class="fa-solid fa-check"></i> Reportado';
                boton.style.background = '#27ae60';
                boton.disabled = true;
                
                // Actualizar estado en la interfaz
                const estadoCell = fila.querySelector('.estado-dispositivo');
                estadoCell.textContent = 'Reportado';
                estadoCell.className = 'estado-dispositivo estado-online';
                
                mostrarNotificacion(`Dispositivo ${dispositivo} reportado correctamente`, 'success');
                
                // Actualizar contadores
                actualizarContadores();
            }, 1500);
        }
    }

    // Función para actualizar contadores
    function actualizarContadores() {
        const dispositivosCriticos = document.querySelectorAll('.estado-caido').length;
        const dispositivosProblemas = document.querySelectorAll('.estado-inestable').length;
        const dispositivosEstables = document.querySelectorAll('.estado-online').length;

        document.querySelector('.resumen-item.criticas .resumen-valor').textContent = dispositivosCriticos;
        document.querySelector('.resumen-item.advertencias .resumen-valor').textContent = dispositivosProblemas;
        document.querySelector('.resumen-item.estables .resumen-valor').textContent = dispositivosEstables;
    }

    // Función para mostrar mensaje cuando no hay resultados
    function mostrarMensajeSinResultados() {
        let mensaje = tabla.querySelector('.sin-resultados');
        if (!mensaje) {
            mensaje = document.createElement('tr');
            mensaje.className = 'sin-resultados';
            mensaje.innerHTML = `
                <td colspan="8" style="text-align: center; padding: 40px; color: #7f8c8d;">
                    <i class="fa-solid fa-search" style="font-size: 48px; margin-bottom: 15px; display: block;"></i>
                    <h3 style="margin-bottom: 10px;">No se encontraron dispositivos</h3>
                    <p>Intente ajustar los filtros de búsqueda</p>
                </td>
            `;
            tabla.appendChild(mensaje);
        }
        mensaje.style.display = '';
    }

    // Función para ocultar mensaje de no resultados
    function ocultarMensajeSinResultados() {
        const mensaje = tabla.querySelector('.sin-resultados');
        if (mensaje) {
            mensaje.style.display = 'none';
        }
    }

    // Función para mostrar notificaciones
    function mostrarNotificacion(mensaje, tipo = 'info') {
        // Crear elemento de notificación
        const notificacion = document.createElement('div');
        notificacion.className = `notificacion notificacion-${tipo}`;
        notificacion.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: ${tipo === 'success' ? '#d4edda' : tipo === 'error' ? '#f8d7da' : '#d1ecf1'};
            color: ${tipo === 'success' ? '#155724' : tipo === 'error' ? '#721c24' : '#0c5460'};
            padding: 15px 20px;
            border-radius: 8px;
            border: 1px solid ${tipo === 'success' ? '#c3e6cb' : tipo === 'error' ? '#f5c6cb' : '#bee5eb'};
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            z-index: 10000;
            max-width: 300px;
            animation: slideIn 0.3s ease;
        `;
        
        notificacion.innerHTML = `
            <div style="display: flex; align-items: center; gap: 10px;">
                <i class="fa-solid fa-${tipo === 'success' ? 'check' : tipo === 'error' ? 'exclamation' : 'info'}-circle"></i>
                <span>${mensaje}</span>
            </div>
        `;

        document.body.appendChild(notificacion);

        // Remover notificación después de 3 segundos
        setTimeout(() => {
            notificacion.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => {
                if (notificacion.parentNode) {
                    notificacion.parentNode.removeChild(notificacion);
                }
            }, 300);
        }, 3000);
    }

    // Event Listeners
    btnAplicar.addEventListener('click', aplicarFiltros);
    btnLimpiar.addEventListener('click', limpiarFiltros);

    botonesReportar.forEach(btn => {
        btn.addEventListener('click', function() {
            reportarDispositivo(this);
        });
    });

    // Eventos para filtros en tiempo real
    [filtroSede, filtroEstado, filtroAutenticacion].forEach(select => {
        select.addEventListener('change', aplicarFiltros);
    });

    filtroDispositivo.addEventListener('input', aplicarFiltros);

    // Inicializar contadores
    actualizarContadores();
});

// Estilos CSS para animaciones
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);