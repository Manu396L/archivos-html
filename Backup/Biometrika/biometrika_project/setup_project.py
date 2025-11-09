#!/usr/bin/env python3
"""
Script de configuración completa para el proyecto Biometrika
Ejecutar después de crear el proyecto Django
"""

import os
import shutil

def create_directories():
    """Crear estructura de directorios"""
    print("📁 Creando estructura de directorios...")
    
    directories = [
        'sistema/templates/sistema',
        'static/css',
        'static/js',
        'static/images',
        'media',
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"  ✓ {directory}")
    
    print()

def create_settings():
    """Crear archivo settings.py configurado"""
    print("⚙️  Creando settings.py...")
    
    settings_content = '''"""
Configuración de Django para el proyecto Biometrika
"""

from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-tu-clave-secreta-cambiar-en-produccion'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'sistema',  # Nuestra aplicación
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'biometrika_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'sistema' / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'biometrika_project.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'es-ar'
TIME_ZONE = 'America/Argentina/Buenos_Aires'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Login configuration
LOGIN_URL = 'sistema:acceso'
LOGIN_REDIRECT_URL = 'sistema:dashboard'
LOGOUT_REDIRECT_URL = 'sistema:acceso'

# Messages
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.DEBUG: 'debug',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'error',
}
'''
    
    with open('biometrika_project/settings.py', 'w', encoding='utf-8') as f:
        f.write(settings_content)
    
    print("  ✓ settings.py configurado")
    print()

def create_main_urls():
    """Crear URLs principales"""
    print("🔗 Creando URLs principales...")
    
    urls_content = '''"""
URLs principales del proyecto Biometrika
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('sistema.urls')),
]

# Servir archivos estáticos y media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
'''
    
    with open('biometrika_project/urls.py', 'w', encoding='utf-8') as f:
        f.write(urls_content)
    
    print("  ✓ biometrika_project/urls.py")
    print()

def create_app_urls():
    """Crear URLs de la aplicación"""
    print("🔗 Creando URLs de la aplicación...")
    
    urls_content = '''"""
URLs de la aplicación Sistema
"""

from django.urls import path
from . import views

app_name = 'sistema'

urlpatterns = [
    # Página principal
    path('', views.index, name='index'),
    
    # Autenticación
    path('acceso/', views.acceso, name='acceso'),
    path('usuario-nuevo/', views.usuario_nuevo, name='usuario_nuevo'),
    path('cambiar-contrasena/', views.cambiar_contrasena, name='cambiar_contrasena'),
    path('cerrar-sesion/', views.cerrar_sesion, name='cerrar_sesion'),
    
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Gestión
    path('sedes/', views.sedes, name='sedes'),
    path('personal/', views.personal, name='personal'),
    path('dispositivos/', views.dispositivos, name='dispositivos'),
    
    # Reportes y alertas
    path('reportes/', views.reportes, name='reportes'),
    path('alertas/', views.alertas, name='alertas'),
    
    # Usuario
    path('notificaciones/', views.notificaciones, name='notificaciones'),
    path('perfil/', views.perfil, name='perfil'),
    path('configuracion/', views.configuracion, name='configuracion'),
    
    # Soporte
    path('soporte/', views.soporte, name='soporte'),
]
'''
    
    with open('sistema/urls.py', 'w', encoding='utf-8') as f:
        f.write(urls_content)
    
    print("  ✓ sistema/urls.py")
    print()

def create_views():
    """Crear vistas"""
    print("👁️  Creando vistas...")
    
    views_content = '''"""
Vistas del sistema biométrico
"""

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages

def index(request):
    """Página de inicio - redirige al login"""
    return redirect('sistema:acceso')

def acceso(request):
    """Vista de login"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('sistema:dashboard')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    
    return render(request, 'sistema/acceso.html')

def usuario_nuevo(request):
    """Registro de nuevo usuario"""
    if request.method == 'POST':
        messages.success(request, 'Solicitud enviada correctamente. El administrador la revisará.')
        return redirect('sistema:acceso')
    
    return render(request, 'sistema/usuario_nuevo.html')

def cambiar_contrasena(request):
    """Recuperación de contraseña"""
    if request.method == 'POST':
        messages.success(request, 'Se ha enviado un correo con las instrucciones.')
        return redirect('sistema:acceso')
    
    return render(request, 'sistema/cambiar_contraseña.html')

def cerrar_sesion(request):
    """Cierre de sesión"""
    logout(request)
    return render(request, 'sistema/cerrar_sesion.html')

@login_required
def dashboard(request):
    """Dashboard principal"""
    context = {
        'empleados_total': 320,
        'empleados_presentes': 245,
        'empleados_ausentes': 45,
        'tardanzas': 30,
        'sedes': 5,
        'dispositivos': 67,
    }
    return render(request, 'sistema/dashboard.html', context)

@login_required
def sedes(request):
    """Gestión de sedes y áreas"""
    return render(request, 'sistema/sedes.html')

@login_required
def personal(request):
    """Gestión de personal"""
    return render(request, 'sistema/personal.html')

@login_required
def dispositivos(request):
    """Gestión de dispositivos"""
    return render(request, 'sistema/dispositivos.html')

@login_required
def reportes(request):
    """Reportes del sistema"""
    return render(request, 'sistema/reportes.html')

@login_required
def alertas(request):
    """Alertas del sistema"""
    return render(request, 'sistema/alertas.html')

@login_required
def notificaciones(request):
    """Notificaciones del usuario"""
    return render(request, 'sistema/notificaciones.html')

@login_required
def perfil(request):
    """Perfil del usuario"""
    return render(request, 'sistema/perfil.html')

@login_required
def configuracion(request):
    """Configuración del sistema"""
    return render(request, 'sistema/configuracion.html')

@login_required
def soporte(request):
    """Soporte técnico"""
    if request.method == 'POST':
        messages.success(request, 'Su reporte ha sido enviado. Nos pondremos en contacto pronto.')
    
    return render(request, 'sistema/soporte.html')
'''
    
    with open('sistema/views.py', 'w', encoding='utf-8') as f:
        f.write(views_content)
    
    print("  ✓ sistema/views.py")
    print()

def create_migration_script():
    """Crear script para migrar HTML"""
    print("🔄 Creando script de migración de templates...")
    
    script_content = '''#!/usr/bin/env python3
"""
Script para migrar archivos HTML a templates Django
"""

import os
import re

URL_MAPPING = {
    'dashboard.html': "{% url 'sistema:dashboard' %}",
    'acceso.html': "{% url 'sistema:acceso' %}",
    'sedes.html': "{% url 'sistema:sedes' %}",
    'personal.html': "{% url 'sistema:personal' %}",
    'dispositivos.html': "{% url 'sistema:dispositivos' %}",
    'soporte.html': "{% url 'sistema:soporte' %}",
    'reportes.html': "{% url 'sistema:reportes' %}",
    'alertas.html': "{% url 'sistema:alertas' %}",
    'notificaciones.html': "{% url 'sistema:notificaciones' %}",
    'perfil.html': "{% url 'sistema:perfil' %}",
    'configuracion.html': "{% url 'sistema:configuracion' %}",
    'cambiar_contraseña.html': "{% url 'sistema:cambiar_contrasena' %}",
    'cerrar_sesion.html': "{% url 'sistema:cerrar_sesion' %}",
    'usuario_nuevo.html': "{% url 'sistema:usuario_nuevo' %}",
}

def convert_template(content):
    """Convierte contenido HTML a template Django"""
    
    # Agregar {% load static %} al inicio
    if '{% load static %}' not in content:
        content = '{% load static %}\\n' + content
    
    # Convertir CSS
    content = re.sub(
        r'href=["\']\.\.\/(?:proyecto\/)?assets\/css\/([^"\']+)["\']',
        r'href="{% static \'css/\\1\' %}"',
        content
    )
    
    # Convertir JavaScript
    content = re.sub(
        r'src=["\']\.\.\/(?:proyecto\/)?assets\/js\/([^"\']+)["\']',
        r'src="{% static \'js/\\1\' %}"',
        content
    )
    
    # Convertir imágenes
    content = re.sub(
        r'src=["\']\.\.\/(?:projeto\/)?assets\/images\/([^"\']+)["\']',
        r'src="{% static \'images/\\1\' %}"',
        content
    )
    
    # Convertir enlaces internos
    for html_file, url_tag in URL_MAPPING.items():
        patterns = [
            rf'href=["\']\.\.\/admin\/{html_file}["\']',
            rf'href=["\'][^"\']*{html_file}["\']',
        ]
        for pattern in patterns:
            content = re.sub(pattern, f'href="{url_tag}"', content)
    
    # Agregar CSRF token en formularios POST
    content = re.sub(
        r'(<form[^>]*method=["\']post["\'][^>]*>)',
        r'\\1\\n            {% csrf_token %}',
        content,
        flags=re.IGNORECASE
    )
    
    return content

def migrate_html_files(source_dir, dest_dir):
    """Migrar archivos HTML"""
    
    if not os.path.exists(source_dir):
        print(f"❌ Directorio no encontrado: {source_dir}")
        print("Por favor, coloca tus archivos HTML en este directorio primero.")
        return False
    
    html_files = [f for f in os.listdir(source_dir) if f.endswith('.html')]
    
    if not html_files:
        print(f"❌ No se encontraron archivos HTML en {source_dir}")
        return False
    
    print(f"\\n📄 Migrando {len(html_files)} archivos HTML...\\n")
    
    for html_file in html_files:
        source_path = os.path.join(source_dir, html_file)
        dest_path = os.path.join(dest_dir, html_file)
        
        try:
            with open(source_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            converted = convert_template(content)
            
            with open(dest_path, 'w', encoding='utf-8') as f:
                f.write(converted)
            
            print(f"  ✓ {html_file}")
        
        except Exception as e:
            print(f"  ✗ {html_file}: {e}")
    
    return True

if __name__ == '__main__':
    print("=" * 50)
    print("MIGRACIÓN DE TEMPLATES HTML A DJANGO")
    print("=" * 50)
    
    # Directorios
    source_dir = 'html_originales'  # Coloca tus HTML aquí
    dest_dir = 'sistema/templates/sistema'
    
    if migrate_html_files(source_dir, dest_dir):
        print("\\n✅ Migración completada!")
        print("\\n📋 Pasos siguientes:")
        print("1. Copiar carpeta 'assets' a 'static/'")
        print("2. Ejecutar: python manage.py migrate")
        print("3. Ejecutar: python manage.py createsuperuser")
        print("4. Ejecutar: python manage.py runserver")
    else:
        print("\\n⚠️  Instrucciones:")
        print(f"1. Crear carpeta: mkdir {source_dir}")
        print(f"2. Copiar tus archivos HTML a {source_dir}/")
        print("3. Ejecutar este script nuevamente")
'''
    
    with open('migrate_templates.py', 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    os.chmod('migrate_templates.py', 0o755)
    
    print("  ✓ migrate_templates.py")
    print()

def create_readme():
    """Crear README con instrucciones"""
    print("📝 Creando README...")
    
    readme_content = '''# Sistema Biométrico - Biometrika S.A

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
'''
    
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("  ✓ README.md")
    print()

def main():
    """Función principal"""
    print("=" * 60)
    print(" CONFIGURACIÓN DEL PROYECTO BIOMETRIKA")
    print("=" * 60)
    print()
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists('manage.py'):
        print("❌ ERROR: Este script debe ejecutarse desde el directorio raíz del proyecto Django")
        print("   (donde está el archivo manage.py)")
        return
    
    create_directories()
    create_settings()
    create_main_urls()
    create_app_urls()
    create_views()
    create_migration_script()
    create_readme()
    
    print("=" * 60)
    print("✅ CONFIGURACIÓN COMPLETADA")
    print("=" * 60)
    print()
    print("📋 PASOS SIGUIENTES:")
    print()
    print("1. Crear carpeta para HTML originales:")
    print("   mkdir html_originales")
    print()
    print("2. Copiar tus archivos HTML a html_originales/")
    print()
    print("3. Copiar archivos CSS/JS:")
    print("   cp -r /ruta/proyecto/assets/css/* static/css/")
    print("   cp -r /ruta/proyecto/assets/js/* static/js/")
    print()
    print("4. Migrar templates:")
    print("   python migrate_templates.py")
    print()
    print("5. Configurar base de datos:")
    print("   python manage.py migrate")
    print()
    print("6. Crear superusuario:")
    print("   python manage.py createsuperuser")
    print()
    print("7. Ejecutar servidor:")
    print("   python manage.py runserver")
    print()
    print("=" * 60)

if __name__ == '__main__':
    main()