
document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginform');
    const errorMessage = document.getElementById('errorMessage');
    
    // Ocultar mensaje de error inicialmente
    errorMessage.style.display = 'none';

    loginForm.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevenir envío del formulario
        
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        
        // Validar credenciales 
        if (validateCredentials(username, password)) {
            // Credenciales correctas
            window.location.href = "/dashboard/"; // Redirigir a la página del dashboard
        } else {
            // Credenciales incorrectas
            errorMessage.style.display = 'block';
        }
    });

    function validateCredentials(username, password) {
        const validUsers = {
            'admin': '1234',
            'usuario': 'clave123',
            'biometrika': 'admin2025'
        };
    
        return validUsers[username] === password;
            }

    // Opcional: Limpiar mensaje de error cuando el usuario empiece a escribir
    const inputs = document.querySelectorAll('input[type="text"], input[type="password"]');
    inputs.forEach(input => {
        input.addEventListener('input', function() {
            errorMessage.style.display = 'none';
        });
    });
});