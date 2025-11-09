# Sistema Biométrico - Biometrika S.A

## Configuración Inicial

### 1. Preparar archivos HTML

```bash
# Crear carpeta para archivos HTML originales
mkdir html_originales

# Copiar tus archivos HTML a esta carpeta
cp /ruta/a/tus/html/*.html html_originales/

# Copiar archivos CSS, JS e imágenes
cp -r /ruta/a/tu/proyecto/assets/css/* static/css/
cp -r /ruta/a/tu/proyecto/assets/js/* static/js/
cp -r /ruta/a/tu/proyecto/assets/images/* static/images/ 2>/dev/null || true
```

### 2. Migrar templates

```bash
python migrate_templates.py
```

### 3. Configurar base de datos

```bash
python manage.py migrate
```

### 4. Crear superusuario

```bash
python manage.py createsuperuser
```

### 5. Ejecutar servidor

```bash
python manage.py runserver
```

### 6. Acceder al sistema

- Aplicación: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

## Estructura del Proyecto

```
biometrika_project/
├── biometrika_project/     # Configuración del proyecto
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── sistema/                # Aplicación principal
│   ├── templates/
│   │   └── sistema/        # Templates HTML
│   ├── views.py
│   └── urls.py
├── static/                 # Archivos estáticos
│   ├── css/
│   ├── js/
│   └── images/
├── html_originales/        # HTML originales (temporal)
├── migrate_templates.py    # Script de migración
└── manage.py

```

## Credenciales por Defecto

Usuario: admin
Contraseña: (la que creaste con createsuperuser)

## Comandos Útiles

```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Ejecutar servidor
python manage.py runserver

# Ejecutar en otro puerto
python manage.py runserver 8080

# Colectar archivos estáticos (producción)
python manage.py collectstatic
```

## Solución de Problemas

### Los archivos CSS/JS no se cargan

1. Verifica que estén en la carpeta `static/`
2. Ejecuta: `python manage.py collectstatic`
3. Verifica que `DEBUG = True` en development

### Template no encontrado

Verifica que el archivo esté en: `sistema/templates/sistema/`

### Error de CSRF

Asegúrate de que todos los formularios POST tengan `{% csrf_token %}`



Lista completa de URLs disponibles:				
                
URL Django			                    Descripción	
http://127.0.0.1:8000/			        Inicio (redirige a login)	
http://127.0.0.1:8000/acceso/			Login	
http://127.0.0.1:8000/dashboard/		Dashboard (requiere login)	
http://127.0.0.1:8000/sedes/			Sedes y áreas	
http://127.0.0.1:8000/personal/			Gestión de personal	
http://127.0.0.1:8000/dispositivos/		Dispositivos	
http://127.0.0.1:8000/reportes/			Reportes	
http://127.0.0.1:8000/alertas/			Alertas	
http://127.0.0.1:8000/notificaciones/	Notificaciones	
http://127.0.0.1:8000/perfil/			Perfil	
http://127.0.0.1:8000/configuracion/	Configuración	
http://127.0.0.1:8000/soporte/			Soporte	
http://127.0.0.1:8000/usuario-nuevo/	Registro	


pip list

Package    Version
---------- -------
asgiref    3.10.0
Django     5.2.8
pillow     12.0.0
pip        25.3
setuptools 65.5.0
sqlparse   0.5.3
tzdata     2025.2




Solución:

Abrí la consola del navegador (F12 → pestaña “Network”).

Activá “Disable cache” (arriba).

Recargá la página con Ctrl + F5 o Shift + F5.

Verificá que esté cargando el archivo correcto desde:

http://127.0.0.1:8000/static/js/login.js



# Instalar todos los requirements
pip install -r requirements.txt

# Instalar solo para desarrollo
pip install -r requirements_dev.txt

# Instalar solo para producción
pip install -r requirements_prod.txt

# Congelar dependencias actuales
pip freeze > requirements.txt

# Verificar dependencias con seguridad
pip install safety
safety check

# Actualizar todas las dependencias
pip install -r requirements.txt --upgrade



# pip isntall 
pip uninstall Pillow
pip install Pillow

# verificar
python -c "import PIL; print(PIL.__version__)".

# pip upgrade
pip install --upgrade pip
pip install Pillow


# requierements.txt
# Incluye todos los requirements base
-r requirements.txt

# Herramientas específicas para desarrollo
django-debug-toolbar>=4.0.0
django-extensions>=3.2.0
ipython>=8.0.0
jupyter>=1.0.0

# Testing
pytest>=7.0.0
pytest-django>=4.5.0
pytest-cov>=4.0.0
factory-boy>=3.2.0

# Linting y formateo
flake8>=6.0.0
black>=23.0.0
isort>=5.12.0

# Seguridad
bandit>=1.7.0
safety>=2.0.0

# Documentación
sphinx>=7.0.0
sphinx-rtd-theme>=1.0.0



#pip para produccion
# Incluye solo lo necesario para producción
-r requirements.txt

# Producción específica
gunicorn>=21.0.0
whitenoise>=6.0.0
psycopg2-binary>=2.9.0  # Si usas PostgreSQL

# Monitoreo
sentry-sdk>=1.0.0








 ### Sistema Biometrika - Sistema de Control de Acceso Biométrico ###
# Descripción
Sistema Biometrika es una plataforma web completa para la gestión y control de acceso biométrico en organizaciones. Permite administrar empleados, dispositivos biométricos, sedes, y generar reportes detallados de accesos.

# Características Principales

# Gestión de Acceso
Autenticación multi-factor (huella, facial, tarjeta, PIN)

Control de acceso por niveles de seguridad

Registro detallado de entradas y salidas

Monitoreo en tiempo real

# Gestión de Personal
Registro completo de empleados

Fotos y credenciales digitales

Asignación de horarios laborales

Gestión de departamentos y sedes

# Dispositivos Biométricos
Configuración centralizada de dispositivos

Monitoreo de estado en tiempo real

Sincronización automática

Mantenimiento remoto

# Reportes y Analytics
Reportes de asistencia personalizados

Exportación en múltiples formatos (PDF, Excel, CSV)

Dashboard con métricas en tiempo real

Alertas y notificaciones automáticas

# Configuración
Parámetros configurables del sistema

Políticas de seguridad personalizables

Gestión de backups automáticos

Sistema de soporte integrado

### Instalación ###
Prerrequisitos
Python 3.8+
pip (gestor de paquetes de Python)
Git
Instalación Automática (Windows)
Clonar el repositorio:
bash
git clone <url-del-repositorio>
cd biometrika_project
Ejecutar instalación automática:

bash
install_requirements.bat
Activar entorno virtual:

bash
venv_biometrika\Scripts\activate
Configurar la base de datos:

bash
python manage.py makemigrations
python manage.py migrate
Crear superusuario:

bash
python manage.py createsuperuser
Ejecutar el servidor:

bash
python manage.py runserver
Instalación Manual
Crear entorno virtual:

bash
python -m venv venv_biometrika
venv_biometrika\Scripts\activate  # Windows
# source venv_biometrika/bin/activate  # Linux/Mac
Instalar dependencias:

bash
pip install -r requirements.txt
Seguir pasos 4-6 de la instalación automática

🗄️ Estructura del Proyecto
text
biometrika_project/
├── biometrika_project/          # Configuración del proyecto Django
│   ├── settings.py             # Configuración principal
│   ├── urls.py                 # URLs principales
│   └── wsgi.py                 # Configuración WSGI
├── sistema/                    # Aplicación principal
│   ├── models.py              # Modelos de base de datos
│   ├── views.py               # Vistas y lógica de negocio
│   ├── urls.py                # URLs de la aplicación
│   ├── admin.py               # Configuración del admin
│   └── templates/             # Plantillas HTML
├── static/                    # Archivos estáticos (CSS, JS, imágenes)
├── media/                     # Archivos multimedia (fotos de empleados)
├── requirements.txt           # Dependencias del proyecto
├── manage.py                  # Script de gestión de Django
└── README.md                  # Este archivo
🎯 Módulos del Sistema
1. Dashboard
Resumen general del sistema

Métricas en tiempo real

Actividad reciente

Estado de dispositivos

2. Gestión de Personal
Registro y edición de empleados

Asignación de credenciales

Gestión de horarios

Estados laborales

3. Sedes y Áreas
Configuración de ubicaciones

Niveles de seguridad por área

Dispositivos por sede

Control de accesos

4. Dispositivos
Configuración de lectores biométricos

Monitoreo de estado

Mantenimiento remoto

Sincronización de datos

5. Reportes
Asistencia por empleado

Accesos por período

Dispositivos activos/inactivos

Exportación personalizada

6. Alertas
Dispositivos desconectados

Intentos de acceso fallidos

Eventos de seguridad

Notificaciones del sistema

7. Soporte
Sistema de tickets

Seguimiento de problemas

Comunicación con técnicos

Historial de soporte

8. Configuración
Parámetros del sistema

Políticas de seguridad

Configuración de red

Backup y restauración

🔐 Seguridad
Autenticación multi-factor

Encriptación de datos biométricos

Registro de auditoría completo

Políticas de contraseñas

Control de acceso por roles

📈 Reportes Disponibles
Reporte de Asistencia

Horarios de entrada/salida

Tardanzas y ausencias

Horas extras

Por empleado o departamento

Reporte de Accesos

Registros exitosos/fallidos

Intentos por dispositivo

Patrones de acceso

Alertas de seguridad

Reporte de Dispositivos

Estado de conectividad

Uso por horarios

Mantenimiento requerido

Estadísticas de funcionamiento

🛠️ Desarrollo
Estructura de la Base de Datos
Los modelos principales incluyen:

Empleados: Información personal y laboral

Sedes: Ubicaciones físicas

Dispositivos: Equipos biométricos

Credenciales: Datos de autenticación

RegistrosAcceso: Trazabilidad de accesos

Alertas: Sistema de notificaciones

Personalización
El sistema es altamente configurable mediante:

Parámetros en ConfiguracionSistema

Plantillas modificables

Estilos CSS personalizables

Módulos extensibles

📞 Soporte
Soporte Técnico:

📞 Teléfono: 4666-1212

📧 Email: soporte@biometrika.com

🕒 Horario: Lunes a Viernes 8:00 - 18:00

🐛 Solución de Problemas
Problemas Comunes
Error al instalar Pillow:

bash
pip install --upgrade pip
pip install Pillow
Error de migraciones:

bash
python manage.py makemigrations sistema
python manage.py migrate
Problemas con archivos estáticos:

bash
python manage.py collectstatic
📄 Licencia
Copyright © Sistema Biométrico 2025
Versión 1.0

🔄 Actualizaciones
Para actualizar el sistema:

Activar entorno virtual:

bash
venv_biometrika\Scripts\activate
Actualizar dependencias:

bash
pip install -r requirements.txt --upgrade
Aplicar migraciones:

bash
python manage.py migrate
Reiniciar servidor

¡Listo para usar!

El sistema estará disponible en http://localhost:8000 después de la instalación.

