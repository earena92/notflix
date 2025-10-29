from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CreacionUsuario(UserCreationForm):
    # Formulario customizado a partir del UserCreationForm proporcionado por Django que ya incluye validación y errores entre otros
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(CreacionUsuario, self).__init__(*args, **kwargs)
        # Cambiamos los labels usuario y contraseña
        self.fields['username'].label = "Usuario: "
        self.fields['password1'].label = "Contraseña: "
        self.fields['password2'].label = "Confirme su contraseña: "
        
        # Borramos el texto de ayuda
        self.fields['username'].help_text = ""
        self.fields['password1'].help_text = ""
        self.fields['password2'].help_text = ""