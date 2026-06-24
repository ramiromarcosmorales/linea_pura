from django import forms

from .models import Consulta


class ContactoForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = ['nombre', 'email', 'mensaje']
        labels = {
            'nombre': 'Nombre',
            'email': 'Email',
            'mensaje': 'Mensaje',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={
                'autocomplete': 'name',
                'id': 'id_nombre',
            }),
            'email': forms.EmailInput(attrs={
                'autocomplete': 'email',
                'id': 'id_email',
            }),
            'mensaje': forms.Textarea(attrs={
                'rows': 5,
                'autocomplete': 'off',
                'id': 'id_mensaje',
            }),
        }

    def clean_mensaje(self):
        mensaje = self.cleaned_data.get('mensaje', '')
        if len(mensaje) < 10:
            raise forms.ValidationError('El mensaje debe tener al menos 10 caracteres.')
        return mensaje
