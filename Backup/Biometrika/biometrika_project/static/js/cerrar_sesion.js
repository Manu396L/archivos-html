// Ejecutar inmediatamente al cargar la página
(function() {
    // Limpiar toda la sesión
    sessionStorage.clear();
    
    // Limpiar datos específicos de localStorage
    localStorage.removeItem('usuario');
    localStorage.removeItem('token');
    localStorage.removeItem('sesion_activa');
    
    // O limpiar todo el localStorage:
    // localStorage.clear();

    console.log('Sesión cerrada correctamente');

    // Redirigir al login después de 1 segundo
    setTimeout(() => {
        window.location.href = '/acceso/';
        
        // Ajusta la ruta según tu estructura:
        // window.location.href = '/index.html';
        // window.location.href = '/auth/login.html';
        // window.location.href = '../index.html';
    }, 1000);
})();