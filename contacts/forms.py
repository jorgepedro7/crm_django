from django import forms

from accounts.models import Account
from .models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['account', 'name', 'email', 'phone', 'position']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        field_styles = {
            'class': 'w-full rounded-xl border border-slate-700 bg-slate-900/60 px-4 py-3 text-slate-100 placeholder-slate-500 focus:border-indigo-400 focus:outline-none focus:ring-2 focus:ring-indigo-400/30',
        }
        placeholders = {
            'account': 'Selecione a conta responsável',
            'name': 'Nome completo',
            'email': 'email@empresa.com',
            'phone': '(11) 99999-0000',
            'position': 'Cargo / Função',
        }
        for field_name, field in self.fields.items():
            field.label = field.label or field_name.title()
            field.widget.attrs.update(field_styles)
            if placeholder := placeholders.get(field_name):
                field.widget.attrs.update({'placeholder': placeholder})
        if self.user:
            self.fields['account'].queryset = Account.objects.filter(owner=self.user)
        self.fields['account'].empty_label = 'Selecione uma conta'

    def clean_email(self):
        email = self.cleaned_data['email'].strip()
        if self.user:
            qs = Contact.objects.filter(owner=self.user, email__iexact=email)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError('Você já possui um contato com este e-mail.')
        return email
