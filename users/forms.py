from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        field_configs = {
            'email': {
                'label': 'E-mail corporativo',
                'placeholder': 'nome@empresa.com.br',
            },
            'password1': {
                'label': 'Senha',
                'placeholder': 'Crie uma senha segura',
            },
            'password2': {
                'label': 'Confirme a senha',
                'placeholder': 'Repita a senha',
            },
        }
        for name, field in self.fields.items():
            config = field_configs.get(name, {})
            if 'label' in config:
                field.label = config['label']
            field.widget.attrs.update(
                {
                    'class': 'w-full rounded-lg border border-slate-600 bg-slate-800/50 px-4 py-3 text-slate-100 placeholder-slate-400 focus:border-indigo-400 focus:outline-none focus:ring-2 focus:ring-indigo-400/40',
                    'placeholder': config.get('placeholder', field.label),
                }
            )


class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label='E-mail',
        widget=forms.EmailInput(
            attrs={
                'class': 'w-full rounded-lg border border-slate-600 bg-slate-800/50 px-4 py-3 text-slate-100 placeholder-slate-400 focus:border-indigo-400 focus:outline-none focus:ring-2 focus:ring-indigo-400/40',
                'placeholder': 'seuemail@empresa.com.br',
                'autocomplete': 'email',
            }
        ),
    )
    password = forms.CharField(
        label='Senha',
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'class': 'w-full rounded-lg border border-slate-600 bg-slate-800/50 px-4 py-3 text-slate-100 placeholder-slate-400 focus:border-indigo-400 focus:outline-none focus:ring-2 focus:ring-indigo-400/40',
                'placeholder': 'Digite sua senha',
                'autocomplete': 'current-password',
            }
        ),
    )
