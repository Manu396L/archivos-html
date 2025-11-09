// Datos del empleado (en un caso real, estos datos vendrían de una API o base de datos)
class Empleado(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre_completo = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100)
    departamento = models.ForeignKey(Departamento, on_delete=models.SET_NULL, null=True)
    sede = models.ForeignKey(Sede, on_delete=models.SET_NULL, null=True)
    correo = models.EmailField()
    telefono = models.CharField(max_length=20, blank=True)
    oficina = models.CharField(max_length=50, blank=True)
    fecha_ingreso = models.DateField()
    estado = models.CharField(max_length=20, choices=[('activo', 'Activo'), ('inactivo', 'Inactivo')])

// Función para cargar los datos del empleado
function cargarDatosEmpleado() {
    // Información principal
    document.getElementById('empleado-nombre').textContent = empleado.nombre;
    document.getElementById('empleado-cargo').textContent = empleado.cargo;
    document.getElementById('empleado-id').textContent = `ID: ${empleado.id}`;
    
    // Badges de estado
    document.getElementById('nivel-seguridad-badge').innerHTML = 
        `<i class="fa-solid fa-shield-halved"></i> Nivel: ${empleado.nivelSeguridad}`;

    // Información personal
    document.getElementById('info-id').textContent = empleado.id;
    document.getElementById('info-nombre').textContent = empleado.nombre;
    document.getElementById('info-cargo').textContent = empleado.cargo;
    document.getElementById('info-area').textContent = empleado.area;
    document.getElementById('info-correo').textContent = empleado.correo;
    document.getElementById('info-fecha-ingreso').textContent = empleado.fechaIngreso;

    // Información de ubicación
    document.getElementById('info-tipo-sede').textContent = empleado.tipoSede;
    document.getElementById('info-nombre-sede').textContent = empleado.nombreSede;
    document.getElementById('info-direccion').textContent = empleado.direccion;
    document.getElementById('info-accesos').textContent = empleado.accesos;

    // Credenciales de seguridad
    document.getElementById('info-dispositivo').textContent = empleado.dispositivo;
    document.getElementById('info-nivel-seguridad').textContent = empleado.nivelSeguridad;
    document.getElementById('info-credencial').textContent = empleado.credencial;
    document.getElementById('info-ultimo-acceso').textContent = empleado.ultimoAcceso;

    // Tarjeta de credencial
    document.getElementById('credential-nombre').textContent = empleado.nombre;
    document.getElementById('credential-id').textContent = `ID: ${empleado.id}`;
    document.getElementById('credential-cargo').textContent = empleado.cargo;
    document.getElementById('credential-area').textContent = empleado.area;
    document.getElementById('credential-tipo').textContent = empleado.dispositivo;

    // Información de contacto
    document.getElementById('contact-correo').textContent = empleado.correo;
    document.getElementById('contact-telefono').textContent = empleado.telefono;
    document.getElementById('contact-oficina').textContent = empleado.oficina;

    // Estadísticas
    document.getElementById('stat-accesos-mes').textContent = empleado.accesosMes;
    document.getElementById('stat-promedio-diario').textContent = empleado.promedioDiario;
    document.getElementById('stat-ultima-actividad').textContent = empleado.ultimaActividad;

    // Fecha de generación
    const fechaActual = new Date().toLocaleDateString('es-ES', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
    document.getElementById('fecha-generacion').textContent = fechaActual;
}

// Función para editar el perfil - REDIRIGE AL ARCHIVO DE EMPLEADO
function editarPerfil() {
    // Redirigir al archivo de personal.html con el ID del empleado para edición
    window.location.href = `personal.html?editar=${empleado.id}`;
}

// Función para imprimir el perfil
function imprimirPerfil() {
    window.print();
}

// Función para cargar foto (simulación)
function cargarFoto() {
    // En una implementación real, esto cargaría la foto desde una base de datos
    const fotoUrl = ''; // URL de la foto del empleado
    
    const profilePhoto = document.getElementById('profile-photo');
    const credentialPhoto = document.getElementById('credential-photo');
    
    if (fotoUrl) {
        profilePhoto.innerHTML = `<img src="${fotoUrl}" alt="Foto del empleado">`;
        credentialPhoto.innerHTML = `<img src="${fotoUrl}" alt="Foto del empleado">`;
    } else {
        // Si no hay foto, mantener el icono por defecto
        profilePhoto.innerHTML = '<i class="fa-solid fa-user"></i>';
        credentialPhoto.innerHTML = '<i class="fa-solid fa-user"></i>';
    }
}

// Función para obtener parámetros de la URL
function obtenerParametrosURL() {
    const parametros = new URLSearchParams(window.location.search);
    return Object.fromEntries(parametros.entries());
}

// Función para cargar empleado específico si viene de personal.html
function cargarEmpleadoDesdeURL() {
    const parametros = obtenerParametrosURL();
    
    if (parametros.id) {
        // En una implementación real, aquí harías una llamada a la API
        // para obtener los datos del empleado específico
        console.log('Cargando empleado con ID:', parametros.id);
        
        // Simular carga de datos específicos
        // empleado = obtenerEmpleadoPorID(parametros.id);
    }
}

// Función para actualizar fecha de generación (función adicional de respaldo)
function actualizarFechaGeneracion() {
    const fechaElement = document.getElementById('fecha-generacion');
    if (fechaElement && (fechaElement.textContent === '-' || !fechaElement.textContent)) {
        const ahora = new Date();
        fechaElement.textContent = ahora.toLocaleDateString('es-AR');
    }
}

// Inicializar la página cuando se cargue
document.addEventListener('DOMContentLoaded', function() {
    cargarEmpleadoDesdeURL();
    cargarDatosEmpleado();
    cargarFoto();
    
    // Ejecutar la actualización de fecha como respaldo
    actualizarFechaGeneracion();
    
    console.log('Perfil del empleado cargado correctamente');
});

// Hacer las funciones globales para que estén disponibles en los botones HTML
window.editarPerfil = editarPerfil;
window.imprimirPerfil = imprimirPerfil;