// Validación y envío del formulario de registro
document.addEventListener('DOMContentLoaded', function() {
    const formulario = document.getElementById('formularioRegistro');
    const mensajeExito = document.getElementById('mensaje-exito');

    // Establecer fecha mínima para el campo de fecha (hoy)
    const fechaIngreso = document.getElementById('fecha_ingreso');
    const hoy = new Date().toISOString().split('T')[0];
    fechaIngreso.min = hoy;

    formulario.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Validar formulario
        if (validarFormulario()) {
            enviarDatos();
        }
    });

    function validarFormulario() {
        const campos = [
            { id: 'nombre', nombre: 'Nombre Completo' },
            { id: 'email', nombre: 'Correo Electrónico' },
            { id: 'telefono', nombre: 'Teléfono' },
            { id: 'departamento', nombre: 'Departamento' },
            { id: 'puesto', nombre: 'Puesto' },
            { id: 'fecha_ingreso', nombre: 'Fecha de Ingreso' }
        ];

        let formularioValido = true;
        let primerError = null;

        // Validar campos obligatorios
        campos.forEach(campo => {
            const elemento = document.getElementById(campo.id);
            if (!elemento.value.trim()) {
                formularioValido = false;
                resaltarError(elemento);
                if (!primerError) {
                    primerError = elemento;
                }
            } else {
                quitarError(elemento);
            }
        });

        // Validación específica para email
        const email = document.getElementById('email').value;
        if (email && !validarEmail(email)) {
            formularioValido = false;
            resaltarError(document.getElementById('email'));
            if (!primerError) {
                primerError = document.getElementById('email');
            }
            mostrarError('Por favor, ingrese un correo electrónico válido.');
        }

        // Validación específica para teléfono
        const telefono = document.getElementById('telefono').value;
        if (telefono && !validarTelefono(telefono)) {
            formularioValido = false;
            resaltarError(document.getElementById('telefono'));
            if (!primerError) {
                primerError = document.getElementById('telefono');
            }
            mostrarError('Por favor, ingrese un número de teléfono válido.');
        }

        if (!formularioValido && primerError) {
            primerError.focus();
            if (!document.querySelector('.error-message')) {
                mostrarError('Por favor, complete todos los campos obligatorios correctamente.');
            }
        }

        return formularioValido;
    }

    function validarEmail(email) {
        const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return regex.test(email);
    }

    function validarTelefono(telefono) {
        // Permite números, espacios, paréntesis, guiones y el signo +
        const regex = /^[\+]?[0-9\s\-\(\)]{10,}$/;
        return regex.test(telefono);
    }

    function resaltarError(elemento) {
        elemento.style.borderColor = '#e74c3c';
        elemento.style.boxShadow = '0 0 0 2px rgba(231, 76, 60, 0.2)';
    }

    function quitarError(elemento) {
        elemento.style.borderColor = '#ccc';
        elemento.style.boxShadow = 'none';
    }

    function mostrarError(mensaje) {
        // Remover mensaje de error anterior si existe
        const errorAnterior = document.querySelector('.error-message');
        if (errorAnterior) {
            errorAnterior.remove();
        }

        // Crear nuevo mensaje de error
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.style.cssText = `
            margin-top: 12px;
            color: #c62828;
            font-size: 13px;
            text-align: center;
            padding: 8px;
            background: #ffebee;
            border-radius: 6px;
            border: 1px solid #ffcdd2;
        `;
        errorDiv.textContent = mensaje;
        
        const boton = formulario.querySelector('.login-button');
        formulario.insertBefore(errorDiv, boton);
    }

    function enviarDatos() {
        // Remover mensaje de error si existe
        const errorAnterior = document.querySelector('.error-message');
        if (errorAnterior) {
            errorAnterior.remove();
        }

        const boton = formulario.querySelector('.login-button');
        const textoOriginal = boton.innerHTML;
        
        // Simular envío
        boton.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Enviando...';
        boton.disabled = true;

        // Simular delay de red
        setTimeout(() => {
            // Aquí iría la lógica real de envío al servidor
            console.log('Datos enviados:', obtenerDatosFormulario());
            
            // Mostrar mensaje de éxito
            mensajeExito.classList.add('mostrar');
            
            // Desplazar hacia el mensaje de éxito
            mensajeExito.scrollIntoView({ behavior: 'smooth', block: 'center' });
            
            // Restaurar botón
            boton.innerHTML = textoOriginal;
            boton.disabled = false;
            
            // Limpiar formulario
            setTimeout(() => {
                formulario.reset();
                mensajeExito.classList.remove('mostrar');
            }, 3000);
        }, 1500);
    }

    function obtenerDatosFormulario() {
        return {
            nombre: document.getElementById('nombre').value,
            email: document.getElementById('email').value,
            telefono: document.getElementById('telefono').value,
            departamento: document.getElementById('departamento').value,
            puesto: document.getElementById('puesto').value,
            fecha_ingreso: document.getElementById('fecha_ingreso').value,
            fecha_solicitud: new Date().toISOString()
        };
    }

    // Validación en tiempo real
    const campos = formulario.querySelectorAll('input');
    campos.forEach(campo => {
        campo.addEventListener('blur', function() {
            if (this.value.trim()) {
                quitarError(this);
                
                // Validación específica para email
                if (this.type === 'email' && this.value) {
                    if (!validarEmail(this.value)) {
                        resaltarError(this);
                    }
                }
                
                // Validación específica para teléfono
                if (this.id === 'telefono' && this.value) {
                    if (!validarTelefono(this.value)) {
                        resaltarError(this);
                    }
                }
            }
        });

        campo.addEventListener('input', function() {
            if (this.value.trim()) {
                quitarError(this);
                // Remover mensaje de error al empezar a escribir
                const errorAnterior = document.querySelector('.error-message');
                if (errorAnterior) {
                    errorAnterior.remove();
                }
            }
        });
    });
});