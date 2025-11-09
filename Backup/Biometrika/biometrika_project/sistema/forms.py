#forms.py

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *


class SedeForm(forms.ModelForm):
    class Meta:
        model = Sede
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'codigo_unico': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'dispositivo_biometrico': forms.Select(attrs={'class': 'form-control'}),
            'nivel_seguridad': forms.Select(attrs={'class': 'form-control'}),
        }

class DepartamentoForm(forms.ModelForm):
    class Meta:
        model = Departamento
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'sede': forms.Select(attrs={'class': 'form-control'}),
        }

class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        exclude = ['usuario', 'fecha_creacion', 'fecha_actualizacion']
        widgets = {
            'id_empleado': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre_completo': forms.TextInput(attrs={'class': 'form-control'}),
            'foto': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'correo_corporativo': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'dni': forms.TextInput(attrs={'class': 'form-control'}),
            'cargo': forms.TextInput(attrs={'class': 'form-control'}),
            'departamento': forms.Select(attrs={'class': 'form-control'}),
            'superior': forms.Select(attrs={'class': 'form-control'}),
            'fecha_ingreso': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'sede': forms.Select(attrs={'class': 'form-control'}),
            'nivel_seguridad': forms.Select(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
        }

class DispositivoForm(forms.ModelForm):
    class Meta:
        model = Dispositivo
        exclude = ['fecha_instalacion', 'fecha_actualizacion', 'ultima_conexion', 'ultima_sincronizacion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_serie': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_dispositivo': forms.Select(attrs={'class': 'form-control'}),
            'sede': forms.Select(attrs={'class': 'form-control'}),
            'area_ubicacion': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion_fisica': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'direccion_ip': forms.TextInput(attrs={'class': 'form-control'}),
            'zona_horaria': forms.TextInput(attrs={'class': 'form-control'}),
            'intervalo_solicitud': forms.NumberInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class CredencialForm(forms.ModelForm):
    class Meta:
        model = Credencial
        exclude = ['fecha_creacion', 'fecha_ultimo_uso']
        widgets = {
            'empleado': forms.Select(attrs={'class': 'form-control'}),
            'tipo_credencial': forms.Select(attrs={'class': 'form-control'}),
            'hash_huella': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'numero_tarjeta': forms.TextInput(attrs={'class': 'form-control'}),
            'pin': forms.TextInput(attrs={'class': 'form-control'}),
            'template_facial': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'template_iris': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'template_voz': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'activa': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'fecha_expiracion': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        tipo_credencial = cleaned_data.get('tipo_credencial')
        
        # Validaciones específicas por tipo de credencial
        if tipo_credencial == 'huella' and not cleaned_data.get('hash_huella'):
            raise forms.ValidationError("Para credencial de huella, debe proporcionar el hash de huella.")
        
        if tipo_credencial == 'tarjeta' and not cleaned_data.get('numero_tarjeta'):
            raise forms.ValidationError("Para credencial de tarjeta, debe proporcionar el número de tarjeta.")
        
        if tipo_credencial == 'pin' and not cleaned_data.get('pin'):
            raise forms.ValidationError("Para credencial PIN, debe proporcionar el PIN.")
        
        if tipo_credencial == 'facial' and not cleaned_data.get('template_facial'):
            raise forms.ValidationError("Para credencial facial, debe proporcionar el template facial.")
        
        return cleaned_data

class RegistroAccesoForm(forms.ModelForm):
    class Meta:
        model = RegistroAcceso
        exclude = ['fecha_registro']
        widgets = {
            'empleado': forms.Select(attrs={'class': 'form-control'}),
            'dispositivo': forms.Select(attrs={'class': 'form-control'}),
            'credencial': forms.Select(attrs={'class': 'form-control'}),
            'fecha_hora': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'tipo_acceso': forms.Select(attrs={'class': 'form-control'}),
            'nivel_confianza': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'max': '1'}),
            'sede': forms.Select(attrs={'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'intento': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class AlertaForm(forms.ModelForm):
    class Meta:
        model = Alerta
        exclude = ['fecha_creacion', 'fecha_leida', 'fecha_resuelta']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'mensaje': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'tipo_alerta': forms.Select(attrs={'class': 'form-control'}),
            'prioridad': forms.Select(attrs={'class': 'form-control'}),
            'dispositivo': forms.Select(attrs={'class': 'form-control'}),
            'empleado': forms.Select(attrs={'class': 'form-control'}),
            'registro_acceso': forms.Select(attrs={'class': 'form-control'}),
            'leida': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'archivada': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'resuelta': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class NotificacionForm(forms.ModelForm):
    class Meta:
        model = Notificacion
        exclude = ['fecha_creacion', 'fecha_leida']
        widgets = {
            'usuario': forms.Select(attrs={'class': 'form-control'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'mensaje': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'tipo_notificacion': forms.Select(attrs={'class': 'form-control'}),
            'prioridad': forms.Select(attrs={'class': 'form-control'}),
            'leida': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'archivada': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'url_accion': forms.TextInput(attrs={'class': 'form-control'}),
            'recurso_id': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class SolicitudSoporteForm(forms.ModelForm):
    class Meta:
        model = SolicitudSoporte
        exclude = ['fecha_creacion', 'fecha_actualizacion', 'fecha_cierre', 'tecnico_asignado']
        widgets = {
            'nombre_completo': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'asunto': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'empleado': forms.Select(attrs={'class': 'form-control'}),
            'dispositivo': forms.Select(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'prioridad': forms.Select(attrs={'class': 'form-control'}),
            'respuesta': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

class ConfiguracionSistemaForm(forms.ModelForm):
    class Meta:
        model = ConfiguracionSistema
        fields = '__all__'
        widgets = {
            'clave': forms.TextInput(attrs={'class': 'form-control'}),
            'valor': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'editable': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ReporteForm(forms.ModelForm):
    class Meta:
        model = Reporte
        exclude = ['fecha_creacion', 'ultima_ejecucion', 'ejecuciones_completadas']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_reporte': forms.Select(attrs={'class': 'form-control'}),
            'parametros': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'usuario': forms.Select(attrs={'class': 'form-control'}),
            'programado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'frecuencia': forms.TextInput(attrs={'class': 'form-control'}),
            'formato': forms.Select(attrs={'class': 'form-control'}),
            'incluir_datos': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'incluir_resumen': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'incluir_graficos': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'incluir_filtros': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class HorarioLaboralForm(forms.ModelForm):
    class Meta:
        model = HorarioLaboral
        fields = '__all__'
        widgets = {
            'empleado': forms.Select(attrs={'class': 'form-control'}),
            'dia_semana': forms.Select(attrs={'class': 'form-control'}),
            'hora_entrada': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'hora_salida': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'tolerancia_entrada': forms.NumberInput(attrs={'class': 'form-control'}),
            'tolerancia_salida': forms.NumberInput(attrs={'class': 'form-control'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class AuditoriaForm(forms.ModelForm):
    class Meta:
        model = Auditoria
        exclude = ['fecha_accion']
        widgets = {
            'usuario': forms.Select(attrs={'class': 'form-control'}),
            'accion': forms.Select(attrs={'class': 'form-control'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control'}),
            'objeto_id': forms.NumberInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'ip_address': forms.TextInput(attrs={'class': 'form-control'}),
            'user_agent': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

# Formularios personalizados adicionales

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }

class FiltroRegistroAccesoForm(forms.Form):
    fecha_inicio = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    fecha_fin = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    empleado = forms.ModelChoiceField(
        queryset=Empleado.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    estado = forms.ChoiceField(
        choices=[('', 'Todos')] + RegistroAcceso.ESTADO_ACCESO_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    sede = forms.ModelChoiceField(
        queryset=Sede.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

class FiltroReporteForm(forms.Form):
    TIPO_REPORTE_CHOICES = [
        ('', 'Seleccionar tipo de reporte'),
        ('asistencia', 'Reporte de Asistencia'),
        ('accesos', 'Reporte de Accesos'),
        ('dispositivos', 'Reporte de Dispositivos'),
        ('seguridad', 'Reporte de Seguridad'),
        ('empleados', 'Reporte de Empleados'),
        ('alertas', 'Reporte de Alertas'),
    ]
    
    tipo_reporte = forms.ChoiceField(
        choices=TIPO_REPORTE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    fecha_inicio = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    fecha_fin = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    formato = forms.ChoiceField(
        choices=Reporte.FORMATO_CHOICES,
        initial='pdf',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

class BusquedaEmpleadoForm(forms.Form):
    query = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por nombre, ID o cargo...'
        })
    )
    departamento = forms.ModelChoiceField(
        queryset=Departamento.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    sede = forms.ModelChoiceField(
        queryset=Sede.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    estado = forms.ChoiceField(
        choices=[('', 'Todos')] + Empleado.ESTADO_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )