from django import forms

from .models import Account


class AccountForm(forms.ModelForm):
    website = forms.URLField(
        label='Site',
        required=False,
        assume_scheme='https',
    )

    class Meta:
        model = Account
        fields = ['name', 'industry', 'city', 'website']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        field_styles = {
            'class': 'w-full rounded-xl border border-slate-700 bg-slate-900/60 px-4 py-3 text-slate-100 placeholder-slate-500 focus:border-indigo-400 focus:outline-none focus:ring-2 focus:ring-indigo-400/30',
        }
        placeholders = {
            'name': 'Nome da empresa',
            'industry': 'Segmento (SaaS, Educação, Varejo...)',
            'city': 'Cidade / Estado',
            'website': 'https://empresa.com.br',
        }
        for field_name, field in self.fields.items():
            field.label = field.label or field_name.title()
            field.widget.attrs.update(field_styles)
            field.widget.attrs.update({'placeholder': placeholders.get(field_name, field.label)})
        if 'website' in self.fields:
            self.fields['website'].assume_scheme = 'https'

    def clean_name(self):
        name = self.cleaned_data['name'].strip()
        if self.user:
            qs = Account.objects.filter(owner=self.user, name__iexact=name)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError('Você já possui uma conta com este nome.')
        return name
