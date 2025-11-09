// Esperar a que el DOM esté completamente cargado
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('formularioProblema');
    const mensajeExito = document.getElementById('mensaje-exito');
    const btnVolver = document.getElementById('btnVolver'); // <- faltaba esto

    // --- Envío del formulario ---
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Obtener los datos del formulario
        const datos = {
            nombre: document.getElementById('nombre').value,
            email: document.getElementById('email').value,
            categoria: document.getElementById('categoria').value,
            asunto: document.getElementById('asunto').value,
            descripcion: document.getElementById('descripcion').value
        };
        
        console.log('Datos del formulario:', datos);

        // Mostrar mensaje de éxito
        mensajeExito.classList.add('mostrar');
        mensajeExito.scrollIntoView({ behavior: 'smooth', block: 'center' });

        // Limpiar formulario
        form.reset();

        // Ocultar mensaje después de 5 segundos
        setTimeout(() => {
            mensajeExito.classList.remove('mostrar');
        }, 5000);
    });

    // --- Botón de volver ---
    if (btnVolver) {
        const params = new URLSearchParams(window.location.search);
        const from = params.get("from");

        btnVolver.addEventListener("click", () => {
            if (from === "login") {
                window.location.href = "/acceso/";
            } else if (from === "dashboard") {
                window.location.href = "/dashboard/";
            } else {
                window.history.back(); // Fallback si no hay "from"
            }
        });
    }
});
