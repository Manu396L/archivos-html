document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('formularioProblema');
    const mensajeExito = document.getElementById('mensaje-exito');
    const btnVolver = document.getElementById('btnVolver'); // 👈 asegurate de tener este botón en el HTML

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
        
        mensajeExito.classList.add('mostrar');
        mensajeExito.scrollIntoView({ behavior: 'smooth', block: 'center' });
        form.reset();
        
        setTimeout(() => {
            mensajeExito.classList.remove('mostrar');
        }, 5000);
    });

    // 🔧 Redirección corregida
    if (btnVolver) {
        const params = new URLSearchParams(window.location.search);
        const from = params.get("from");

        btnVolver.addEventListener("click", () => {
            if (from === "login") {
                window.location.href = "/acceso/"; // ✅ vista Django
            } else if (from === "dashboard") {
                window.location.href = "/dashboard/"; // ✅ vista Django
            } else {
                window.history.back();
            }
        });
    }
});
