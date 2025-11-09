#!/usr/bin/env python3
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
        content = '{% load static %}\n' + content
    
    # Convertir CSS - usando raw strings correctamente
    content = re.sub(
        r'href=["\']\.\.\/(?:proyecto\/)?assets\/css\/([^"\']+)["\']',
        r'href="{% static \'css/\1\' %}"',
        content
    )
    
    # Convertir JavaScript
    content = re.sub(
        r'src=["\']\.\.\/(?:proyecto\/)?assets\/js\/([^"\']+)["\']',
        r'src="{% static \'js/\1\' %}"',
        content
    )
    
    # Convertir imágenes
    content = re.sub(
        r'src=["\']\.\.\/(?:proyecto\/)?assets\/images\/([^"\']+)["\']',
        r'src="{% static \'images/\1\' %}"',
        content
    )
    
    # Convertir enlaces internos
    for html_file, url_tag in URL_MAPPING.items():
        # Patrón para enlaces con ../admin/
        pattern1 = r'href=["\']\.\.\/admin\/' + re.escape(html_file) + r'["\']'
        content = re.sub(pattern1, f'href="{url_tag}"', content)
        
        # Patrón para otros enlaces
        pattern2 = r'href=["\'][^"\']*\/' + re.escape(html_file) + r'["\']'
        content = re.sub(pattern2, f'href="{url_tag}"', content)
    
    # Agregar CSRF token en formularios POST
    def add_csrf(match):
        form_tag = match.group(1)
        return form_tag + '\n            {% csrf_token %}'
    
    content = re.sub(
        r'(<form[^>]*method=["\']post["\'][^>]*>)',
        add_csrf,
        content,
        flags=re.IGNORECASE
    )
    
    return content

def migrate_html_files(source_dir, dest_dir):
    """Migrar archivos HTML"""
    
    if not os.path.exists(source_dir):
        print(f"❌ Directorio no encontrado: {source_dir}")
        print("Por favor, coloca tus archivos HTML en este directorio primero.")
        print(f"\nPuedes crear el directorio con: mkdir {source_dir}")
        return False
    
    html_files = [f for f in os.listdir(source_dir) if f.endswith('.html')]
    
    if not html_files:
        print(f"❌ No se encontraron archivos HTML en {source_dir}")
        return False
    
    # Crear directorio destino si no existe
    os.makedirs(dest_dir, exist_ok=True)
    
    print(f"\n📄 Migrando {len(html_files)} archivos HTML...\n")
    
    success_count = 0
    error_count = 0
    
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
            success_count += 1
        
        except Exception as e:
            print(f"  ✗ {html_file}: {e}")
            error_count += 1
    
    print(f"\n{'='*50}")
    print(f"Exitosos: {success_count}")
    print(f"Errores: {error_count}")
    print(f"{'='*50}")
    
    return success_count > 0

def main():
    print("=" * 60)
    print(" MIGRACIÓN DE TEMPLATES HTML A DJANGO")
    print("=" * 60)
    
    # Directorios
    source_dir = 'html_originales'
    dest_dir = os.path.join('sistema', 'templates', 'sistema')
    
    print(f"\n📂 Directorio origen: {source_dir}")
    print(f"📂 Directorio destino: {dest_dir}\n")
    
    if migrate_html_files(source_dir, dest_dir):
        print("\n✅ Migración completada!")
        print("\n📋 Pasos siguientes:")
        print("1. Verificar que los archivos CSS/JS estén en static/")
        print("   - static/css/")
        print("   - static/js/")
        print("   - static/images/")
        print("\n2. Aplicar migraciones:")
        print("   python manage.py migrate")
        print("\n3. Crear superusuario:")
        print("   python manage.py createsuperuser")
        print("\n4. Ejecutar servidor:")
        print("   python manage.py runserver")
        print("\n5. Abrir en navegador:")
        print("   http://127.0.0.1:8000/")
    else:
        print("\n⚠️  Instrucciones:")
        print(f"1. Crear carpeta: mkdir {source_dir}")
        print(f"2. Copiar tus archivos HTML a {source_dir}/")
        print("   Ejemplo: cp ../proyecto/admin/*.html html_originales/")
        print("\n3. Copiar archivos estáticos:")
        print("   mkdir -p static/css static/js static/images")
        print("   cp -r ../proyecto/assets/css/* static/css/")
        print("   cp -r ../proyecto/assets/js/* static/js/")
        print("\n4. Ejecutar este script nuevamente")

if __name__ == '__main__':
    main()