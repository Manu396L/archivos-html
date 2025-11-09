#!/usr/bin/env python3
"""
Script para corregir templates con comillas mal escapadas
"""

import os
import re

def fix_template(file_path):
    """Corregir un archivo template"""
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 1. Corregir comillas escapadas incorrectamente en static
        content = re.sub(
            r"\{% static \\'([^']+)\\' %\}",
            r"{% static '\1' %}",
            content
        )
        
        # 2. Corregir comillas escapadas en url
        content = re.sub(
            r"\{% url \\'([^']+)\\' %\}",
            r"{% url '\1' %}",
            content
        )
        
        # 3. Convertir enlaces antiguos de HTML a Django URLs
        url_mappings = {
            r'href=["\']\.\.\/admin\/dashboard\.html["\']': 'href="{% url \'sistema:dashboard\' %}"',
            r'href=["\']\.\.\/admin\/acceso\.html["\']': 'href="{% url \'sistema:acceso\' %}"',
            r'href=["\']\.\.\/admin\/sedes\.html["\']': 'href="{% url \'sistema:sedes\' %}"',
            r'href=["\']\.\.\/admin\/personal\.html["\']': 'href="{% url \'sistema:personal\' %}"',
            r'href=["\']\.\.\/admin\/dispositivos\.html["\']': 'href="{% url \'sistema:dispositivos\' %}"',
            r'href=["\']\.\.\/admin\/soporte\.html["\']': 'href="{% url \'sistema:soporte\' %}"',
            r'href=["\']\.\.\/admin\/reportes\.html["\']': 'href="{% url \'sistema:reportes\' %}"',
            r'href=["\']\.\.\/admin\/alertas\.html["\']': 'href="{% url \'sistema:alertas\' %}"',
            r'href=["\']\.\.\/admin\/notificaciones\.html["\']': 'href="{% url \'sistema:notificaciones\' %}"',
            r'href=["\']\.\.\/admin\/perfil\.html["\']': 'href="{% url \'sistema:perfil\' %}"',
            r'href=["\']\.\.\/admin\/configuracion\.html["\']': 'href="{% url \'sistema:configuracion\' %}"',
            r'href=["\']\.\.\/admin\/cambiar_contraseña\.html["\']': 'href="{% url \'sistema:cambiar_contrasena\' %}"',
            r'href=["\']\.\.\/admin\/cerrar_sesion\.html["\']': 'href="{% url \'sistema:cerrar_sesion\' %}"',
            r'href=["\']\.\.\/admin\/usuario_nuevo\.html["\']': 'href="{% url \'sistema:usuario_nuevo\' %}"',
            
            # Sin ../admin/
            r'href=["\']dashboard\.html["\']': 'href="{% url \'sistema:dashboard\' %}"',
            r'href=["\']acceso\.html["\']': 'href="{% url \'sistema:acceso\' %}"',
            r'href=["\']sedes\.html["\']': 'href="{% url \'sistema:sedes\' %}"',
            r'href=["\']personal\.html["\']': 'href="{% url \'sistema:personal\' %}"',
            r'href=["\']dispositivos\.html["\']': 'href="{% url \'sistema:dispositivos\' %}"',
            r'href=["\']soporte\.html["\']': 'href="{% url \'sistema:soporte\' %}"',
            r'href=["\']reportes\.html["\']': 'href="{% url \'sistema:reportes\' %}"',
            r'href=["\']alertas\.html["\']': 'href="{% url \'sistema:alertas\' %}"',
            r'href=["\']notificaciones\.html["\']': 'href="{% url \'sistema:notificaciones\' %}"',
            r'href=["\']perfil\.html["\']': 'href="{% url \'sistema:perfil\' %}"',
            r'href=["\']configuracion\.html["\']': 'href="{% url \'sistema:configuracion\' %}"',
            r'href=["\']cambiar_contraseña\.html["\']': 'href="{% url \'sistema:cambiar_contrasena\' %}"',
            r'href=["\']cerrar_sesion\.html["\']': 'href="{% url \'sistema:cerrar_sesion\' %}"',
            r'href=["\']usuario_nuevo\.html["\']': 'href="{% url \'sistema:usuario_nuevo\' %}"',
        }
        
        for pattern, replacement in url_mappings.items():
            content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
        
        # 4. Agregar {% load static %} si no existe
        if '{% load static %}' not in content and '{% static' in content:
            content = '{% load static %}\n' + content
        
        # Si hubo cambios, guardar
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
        
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

def fix_all_templates(templates_dir):
    """Corregir todos los templates"""
    
    print("=" * 60)
    print("CORRIGIENDO TEMPLATES")
    print("=" * 60)
    print()
    
    if not os.path.exists(templates_dir):
        print(f"❌ Directorio no encontrado: {templates_dir}")
        return False
    
    html_files = []
    for file in os.listdir(templates_dir):
        if file.endswith('.html'):
            html_files.append(file)
    
    if not html_files:
        print(f"❌ No se encontraron archivos HTML en {templates_dir}")
        return False
    
    print(f"📄 Encontrados {len(html_files)} archivos HTML\n")
    
    fixed_count = 0
    
    for html_file in html_files:
        file_path = os.path.join(templates_dir, html_file)
        
        if fix_template(file_path):
            print(f"  ✓ {html_file} - Corregido")
            fixed_count += 1
        else:
            print(f"  · {html_file} - Sin cambios")
    
    print()
    print("=" * 60)
    print(f"✅ {fixed_count} archivos corregidos")
    print(f"   {len(html_files) - fixed_count} archivos sin cambios")
    print("=" * 60)
    
    return True

def show_example():
    """Mostrar ejemplo de corrección"""
    print()
    print("=" * 60)
    print("EJEMPLO DE CORRECCIÓN")
    print("=" * 60)
    print()
    print("ANTES (Incorrecto):")
    print("  {% static \\'css/style.css\\' %}")
    print("  {% url \\'sistema:dashboard\\' %}")
    print()
    print("DESPUÉS (Correcto):")
    print("  {% static 'css/style.css' %}")
    print("  {% url 'sistema:dashboard' %}")
    print()

def main():
    """Función principal"""
    
    if not os.path.exists('manage.py'):
        print("❌ Ejecuta este script desde la raíz del proyecto")
        return
    
    templates_dir = os.path.join('sistema', 'templates', 'sistema')
    
    show_example()
    
    if fix_all_templates(templates_dir):
        print()
        print("✅ Templates corregidos")
        print()
        print("Ahora ejecuta:")
        print("  python manage.py runserver")
        print()
        print("Y accede a:")
        print("  http://127.0.0.1:8000/acceso/")
    else:
        print()
        print("❌ No se pudieron corregir los templates")

if __name__ == '__main__':
    main()