// dashboard-charts.js
// Inicializar gráficos cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    // Gráfico de Asistencia (Doughnut) - DATOS DE PRESENTISMO
    const asistenciaCtx = document.getElementById('asistenciaChart').getContext('2d');
    const asistenciaChart = new Chart(asistenciaCtx, {
        type: 'doughnut',
        data: {
            labels: ['Asistencia', 'Ausencia', 'Tardanzas'],
            datasets: [{
                data: [245, 45, 30], // 245 Presentes, 45 Ausentes, 30 Tardanzas
                backgroundColor: ['#2ecc71', '#e74c3c', '#f39c12'],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 15,
                        usePointStyle: true
                    }
                }
            },
            cutout: '70%'
        }
    });
    
    // Gráfico de Estado de Dispositivos (Doughnut)
    const dispositivosCtx = document.getElementById('dispositivosChart').getContext('2d');
    const dispositivosChart = new Chart(dispositivosCtx, {
        type: 'doughnut',
        data: {
            labels: ['Online', 'Offline', 'No Autorizado'],
            datasets: [{
                data: [57, 8, 2], // 57 Online, 8 Offline, 2 No Autorizado
                backgroundColor: ['#2ecc71', '#e74c3c', '#f39c12'],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 15,
                        usePointStyle: true
                    }
                }
            },
            cutout: '70%'
        }
    });
    
    // Gráfico de Presentismo (Doughnut) - DATOS COHERENTES
    const presentismoCtx = document.getElementById('presentismoChart').getContext('2d');
    const presentismoChart = new Chart(presentismoCtx, {
        type: 'doughnut',
        data: {
            labels: ['Presentes', 'Ausentes', 'Tardanzas'],
            datasets: [{
                data: [245, 45, 30], // Mismos datos que asistencia pero enfocado en presentismo
                backgroundColor: ['#2ecc71', '#e74c3c', '#3498db'],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 15,
                        usePointStyle: true
                    }
                }
            },
            cutout: '70%'
        }
    });
    
    // Gráfico de Excepciones de Asistencia (Bar) - DATOS RELACIONADOS
    const excepcionesCtx = document.getElementById('excepcionesChart').getContext('2d');
    const excepcionesChart = new Chart(excepcionesCtx, {
        type: 'bar',
        data: {
            labels: ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom'],
            datasets: [
                {
                    label: 'Llegadas tarde',
                    data: [8, 6, 7, 5, 4, 0, 0], // Total 30 tardanzas semanales
                    backgroundColor: '#3498db',
                    borderRadius: 4
                },
                {
                    label: 'Salidas temprano',
                    data: [3, 4, 2, 5, 6, 0, 0], // Total 20 salidas temprano
                    backgroundColor: '#e74c3c',
                    borderRadius: 4
                },
                {
                    label: 'Ausencia',
                    data: [7, 6, 8, 9, 15, 0, 0], // Total 45 ausencias semanales
                    backgroundColor: '#f39c12',
                    borderRadius: 4
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                x: {
                    grid: {
                        display: false
                    }
                },
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 5
                    }
                }
            }
        }
    });
});