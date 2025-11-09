#!/usr/bin/env python3
"""
Script para verificar y corregir configuración de URLs
"""

import os

def check_main_urls():
    """Verificar URLs principales"""
    print("=" * 60)
    print("VERIFICANDO biometrika_project/urls.py")
    print("=" * 60)
    print()
    
    urls_path = os.path.join('biometrika_project', 'urls.py')
    
    if not os.path.exists(urls_path):
        print("❌ Archivo no encontrado")
        return False
    
    with open(urls_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("Contenido actual:")
    print("-" * 60)
    print(content)
    print("-" * 60)
    print()
    
    # Verificaciones
    issues = []
    
    if "include('sistema.urls')" not in content:
        issues.append("No incluye sistema.urls")
    
    if "path('', include('sistema.urls'))" not in content:
        issues.append("El include debe estar en path('', ...)")
    
    if issues:
        print("⚠️  Problemas encontrados:")
        for issue in issues:
            print(f"   - {issue}")
        return False
    else:
        print("✓ Configuración correcta")
        return True

def fix_main_urls():
    """Corregir URLs principales"""
    print()
    print("=" * 60)
    print("CORRIGIENDO biometrika_project/urls.py")
    print("=" * 60)
    print()
    
    urls_path = os.path.join('biometrika_project', 'urls.py')
    
    correct_content = '''"""
URLs principales del proyecto Biometrika
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('sistema.urls')),  # Rutas de la aplicación
]

# Servir archivos estáticos y media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0] if settings.STATICFILES_DIRS else None)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
'''
    
    # Backup
    backup_path = urls_path + '.backup'
    if os.path.exists(urls_path):
        with open(urls_path, 'r', encoding='utf-8') as f:
            with open(backup_path, 'w', encoding='utf-8') as fb:
                fb.write(f.read())
        print(f"✓ Backup creado: {backup_path}")
    
    # Escribir corrección
    with open(urls_path, 'w', encoding='utf-8') as f:
        f.write(correct_content)
    
    print("✓ Archivo actualizado")
    return True

def check_app_urls():
    """Verificar URLs de la aplicación"""
    print()
    print("=" * 60)
    print("VERIFICANDO sistema/urls.py")
    print("=" * 60)
    print()
    
    urls_path = os.path.join('sistema', 'urls.py')
    
    if not os.path.exists(urls_path):
        print("❌ Archivo no encontrado")
        return False
    
    with open(urls_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("Rutas definidas:")
    print("-" * 60)
    
    # Extraer paths
    import re
    paths = re.findall(r"path\('([^']*)'[^)]*name='([^']*)'", content)
    
    for url, name in paths:
        print(f"  ✓ /{url:<25} → {name}")
    
    print("-" * 60)
    print()
    
    if len(paths) < 10:
        print("⚠️  Parece que faltan rutas")
        return False
    
    print(f"✓ {len(paths)} rutas encontradas")
    return True

def create_app_urls():
    """Crear URLs de la aplicación"""
    print()
    print("=" * 60)
    print("CREANDO sistema/urls.py")
    print("=" * 60)
    print()
    
    urls_path = os.path.join('sistema', 'urls.py')
    
    correct_content = '''"""
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
    
    # Backup
    if os.path.exists(urls_path):
        backup_path = urls_path + '.backup'
        with open(urls_path, 'r', encoding='utf-8') as f:
            with open(backup_path, 'w', encoding='utf-8') as fb:
                fb.write(f.read())
        print(f"✓ Backup creado: {backup_path}")
    
    # Escribir
    with open(urls_path, 'w', encoding='utf-8') as f:
        f.write(correct_content)
    
    print("✓ Archivo creado/actualizado")
    return True

def test_urls():
    """Probar que Django puede cargar las URLs"""
    print()
    print("=" * 60)
    print("PROBANDO CONFIGURACIÓN DE URLS")
    print("=" * 60)
    print()
    
    try:
        import django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'biometrika_project.settings')
        django.setup()
        
        from django.urls import get_resolver
        
        resolver = get_resolver()
        url_patterns = resolver.url_patterns
        
        print(f"✓ Django cargó {len(url_patterns)} patrones de URL principales")
        print()
        print("URLs disponibles:")
        print("-" * 60)
        
        # Obtener URLs de sistema
        for pattern in url_patterns:
            if hasattr(pattern, 'url_patterns'):  # Es un include
                print(f"\n  Rutas de '{pattern.namespace or 'sistema'}':")
                for sub_pattern in pattern.url_patterns:
                    route = str(sub_pattern.pattern)
                    name = sub_pattern.name if hasattr(sub_pattern, 'name') else ''
                    if name:
                        print(f"    ✓ /{route:<25} → {pattern.namespace}:{name}")
        
        print("-" * 60)
        print()
        print("✅ Configuración de URLs correcta")
        return True
        
    except Exception as e:
        print(f"❌ Error al cargar URLs: {e}")
        return False

def show_available_urls():
    """Mostrar URLs disponibles para acceder"""
    print()
    print("=" * 60)
    print("URLS DISPONIBLES PARA ACCEDER")
    print("=" * 60)
    print()
    
    urls = [
        ('http://127.0.0.1:8000/', 'Página principal (redirige a login)'),
        ('http://127.0.0.1:8000/acceso/', 'Login'),
        ('http://127.0.0.1:8000/dashboard/', 'Dashboard (requiere login)'),
        ('http://127.0.0.1:8000/admin/', 'Admin de Django'),
    ]
    
    for url, description in urls:
        print(f"  {url:<40} → {description}")
    
    print()

def main():
    """Función principal"""
    
    if not os.path.exists('manage.py'):
        print("❌ Ejecuta este script desde la raíz del proyecto")
        return
    
    print("\n🔍 DIAGNÓSTICO DE URLs\n")
    
    # Verificar URLs principales
    main_ok = check_main_urls()
    
    if not main_ok:
        print("\n⚠️  Se necesita corregir biometrika_project/urls.py")
        respuesta = input("¿Deseas corregirlo automáticamente? (s/n): ")
        if respuesta.lower() == 's':
            fix_main_urls()
            main_ok = True
    
    # Verificar URLs de la app
    app_ok = check_app_urls()
    
    if not app_ok:
        print("\n⚠️  Se necesita corregir sistema/urls.py")
        respuesta = input("¿Deseas corregirlo automáticamente? (s/n): ")
        if respuesta.lower() == 's':
            create_app_urls()
            app_ok = True
    
    # Probar configuración
    if main_ok and app_ok:
        test_urls()
        show_available_urls()
        
        print("=" * 60)
        print("✅ CONFIGURACIÓN LISTA")
        print("=" * 60)
        print()
        print("Ahora ejecuta:")
        print("  python manage.py runserver")
        print()
        print("Y accede a:")
        print("  http://127.0.0.1:8000/")
        print()

if __name__ == '__main__':
    main()