from django import forms

from accounts.models import Account
from contacts.models import Contact
from .models import Lead


class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = [
            'name',
            'email',
            'phone',
            'source',
            'status',
            'account',
            'contact',
            'notes',
        ]
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        field_styles = {
            'class': 'w-full rounded-xl border border-slate-700 bg-slate-900/60 px-4 py-3 text-slate-100 placeholder-slate-500 focus:border-indigo-400 focus:outline-none focus:ring-2 focus:ring-indigo-400/30',
        }
        placeholders = {
            'name': 'Nome completo ou empresa',
            'email': 'lead@empresa.com',
            'phone': '(11) 98888-0000',
            'notes': 'Resumo da necessidade, próximos passos...',
        }
        for field_name, field in self.fields.items():
            field.label = field.label or field_name.title()
            widget = field.widget
            widget.attrs.update(field_styles)
            if placeholder := placeholders.get(field_name):
                widget.attrs.setdefault('placeholder', placeholder)
        if self.user:
            self.fields['account'].queryset = Account.objects.filter(owner=self.user)
            self.fields['contact'].queryset = Contact.objects.filter(owner=self.user)
        self.fields['account'].required = False
        self.fields['contact'].required = False
        self.fields['account'].empty_label = 'Selecione uma conta (opcional)'
        self.fields['contact'].empty_label = 'Selecione um contato (opcional)'
        self.fields['contact'].help_text = 'Opcional — será criado automaticamente ao converter se vazio.'

    def clean_email(self):
        email = self.cleaned_data['email'].strip()
        if self.user:
            qs = Lead.objects.filter(owner=self.user, email__iexact=email)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError('Você já possui um lead com este e-mail.')
        return email

    def clean_contact(self):
        contact = self.cleaned_data.get('contact')
        account = self.cleaned_data.get('account')
        if contact:
            if self.user and contact.owner != self.user:
                raise forms.ValidationError('Selecione um contato pertencente à sua carteira.')
            if account and contact.account != account:
                raise forms.ValidationError('O contato precisa estar associado à mesma conta.')
        return contact
