from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class RegistroForm(UserCreationForm):
    first_name = forms.CharField(
        label='Nombre',
        max_length=50,
        widget=forms.TextInput(attrs={'id': 'id_first_name', 'autocomplete': 'given-name'}),
    )
    last_name = forms.CharField(
        label='Apellido',
        max_length=50,
        widget=forms.TextInput(attrs={'id': 'id_last_name', 'autocomplete': 'family-name'}),
    )
    email = forms.EmailField(
        label='Correo electrónico',
        widget=forms.EmailInput(attrs={'id': 'id_email', 'autocomplete': 'email'}),
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Traducir labels al español
        self.fields['password1'].label = 'Contraseña'
        self.fields['password1'].help_text = (
            'La contraseña debe tener al menos 8 caracteres, '
            'no puede ser completamente numérica.'
        )
        self.fields['password2'].label = 'Confirmar contraseña'
        self.fields['password2'].help_text = 'Ingresá la misma contraseña para verificarla.'
        self.fields['password1'].widget.attrs['id'] = 'id_password1'
        self.fields['password2'].widget.attrs['id'] = 'id_password2'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Este correo ya está registrado.')
        return email


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Correo electrónico'
        self.fields['username'].widget.attrs.update({
            'id': 'id_username',
            'autocomplete': 'email',
            'placeholder': '',
        })
        self.fields['password'].label = 'Contraseña'
        self.fields['password'].widget.attrs.update({
            'id': 'id_password',
            'autocomplete': 'current-password',
        })


class ValidacionForm(forms.Form):
    email = forms.EmailField(
        label='Correo electrónico',
        widget=forms.EmailInput(attrs={'id': 'id_email_val'}),
    )
    codigo = forms.CharField(
        label='Código de validación',
        max_length=50,
        widget=forms.TextInput(attrs={'id': 'id_codigo'}),
    )
