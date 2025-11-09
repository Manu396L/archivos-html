document.addEventListener('DOMContentLoaded', function() {
    const formulario = document.getElementById('formulario-recuperacion');
    const mensajeExito = document.getElementById('mensaje-exito');
    const dniInput = document.getElementById('dni');
    const emailInput = document.getElementById('email');

    // Envío del formulario
    formulario.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Obtener datos del formulario
        const dni = dniInput.value.trim();
        const email = emailInput.value.trim();
        
        // Validar que los campos no estén vacíos
        if (!dni || !email) {
            alert('Por favor, complete todos los campos requeridos');
            return;
        }

        // Validar DNI (solo números, entre 7 y 8 dígitos)
        if (!validarDNI(dni)) {
            alert('Por favor, ingrese un DNI válido (7 u 8 dígitos numéricos)');
            dniInput.focus();
            return;
        }

        // Validar formato de email
        if (!validarEmail(email)) {
            alert('Por favor, ingrese un correo electrónico válido');
            emailInput.focus();
            return;
        }
        
        const datos = {
            dni: dni,
            email: email,
            timestamp: new Date().toISOString()
        };
        
        console.log('Solicitud de recuperación:', datos);
        
        // Aquí enviarías los datos al servidor
        /*
        fetch('/api/recuperar-contrasena', {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json' 
            },
            body: JSON.stringify(datos)
        })
        .then(response => response.json())
        .then(data => {
            console.log('Respuesta del servidor:', data);
            if (data.success) {
                mostrarMensajeExito();
            } else {
                alert('Error: ' + (data.message || 'No se pudo procesar la solicitud'));
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Ocurrió un error al procesar la solicitud. Por favor, inténtelo de nuevo.');
        });
        */
        
        // Por ahora solo mostrar el mensaje de éxito
        mostrarMensajeExito();
    });

    // Función para mostrar mensaje de éxito
    function mostrarMensajeExito() {
        // Mostrar mensaje de éxito
        mensajeExito.classList.add('mostrar');
        
        // Scroll suave al mensaje
        mensajeExito.scrollIntoView({ 
            behavior: 'smooth', 
            block: 'center' 
        });
        
        // Limpiar formulario
        formulario.reset();
        
        // Ocultar mensaje después de 8 segundos
        setTimeout(() => {
            mensajeExito.classList.remove('mostrar');
        }, 8000);
    }

    // Función para validar DNI (7 u 8 dígitos numéricos)
    function validarDNI(dni) {
        const dniRegex = /^\d{7,8}$/;
        return dniRegex.test(dni);
    }

    // Función para validar email
    function validarEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    // Solo permitir números en el campo DNI
    dniInput.addEventListener('input', function() {
        // Eliminar cualquier caracter que no sea número
        this.value = this.value.replace(/[^0-9]/g, '');
        
        // Limitar a 8 dígitos
        if (this.value.length > 8) {
            this.value = this.value.slice(0, 8);
        }

        // Limpiar estilos de error
        this.style.borderColor = '';
        this.style.backgroundColor = '';
    });

    // Validación en tiempo real del DNI al perder el foco
    dniInput.addEventListener('blur', function() {
        const dni = this.value.trim();
        
        if (dni && !validarDNI(dni)) {
            this.style.borderColor = '#c62828';
            this.style.backgroundColor = '#ffebee';
        } else {
            this.style.borderColor = '';
            this.style.backgroundColor = '';
        }
    });

    // Validación en tiempo real del email
    emailInput.addEventListener('blur', function() {
        const email = this.value.trim();
        
        if (email && !validarEmail(email)) {
            this.style.borderColor = '#c62828';
            this.style.backgroundColor = '#ffebee';
        } else {
            this.style.borderColor = '';
            this.style.backgroundColor = '';
        }
    });

    // Limpiar error al empezar a escribir en email
    emailInput.addEventListener('input', function() {
        this.style.borderColor = '';
        this.style.backgroundColor = '';
    });

    // Limpiar espacios en blanco del DNI al perder foco
    dniInput.addEventListener('blur', function() {
        this.value = this.value.trim();
    });

    // Prevenir envío del formulario con Enter si los campos están vacíos
    formulario.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            const dni = dniInput.value.trim();
            const email = emailInput.value.trim();
            
            if (!dni || !email) {
                e.preventDefault();
                alert('Por favor, complete todos los campos requeridos');
            }
        }
    });
});
