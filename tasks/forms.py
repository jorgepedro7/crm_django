from django import forms

from contacts.models import Contact
from leads.models import Lead
from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            'title',
            'description',
            'due_date',
            'status',
            'lead',
            'contact',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        field_styles = {
            'class': 'w-full rounded-xl border border-slate-700 bg-slate-900/60 px-4 py-3 text-slate-100 placeholder-slate-500 focus:border-indigo-400 focus:outline-none focus:ring-2 focus:ring-indigo-400/30',
        }
        placeholders = {
            'title': 'Nome da atividade',
            'description': 'Contexto, próximos passos, links úteis...',
        }
        for name, field in self.fields.items():
            field.label = field.label or name.title()
            field.widget.attrs.update(field_styles)
            if placeholder := placeholders.get(name):
                field.widget.attrs.setdefault('placeholder', placeholder)
        if self.user:
            self.fields['lead'].queryset = Lead.objects.filter(owner=self.user)
            self.fields['contact'].queryset = Contact.objects.filter(owner=self.user)
        self.fields['lead'].required = False
        self.fields['contact'].required = False
        self.fields['lead'].empty_label = 'Vincular lead (opcional)'
        self.fields['contact'].empty_label = 'Vincular contato (opcional)'

    def clean(self):
        cleaned_data = super().clean()
        lead = cleaned_data.get('lead')
        contact = cleaned_data.get('contact')
        if self.user:
            if lead and lead.owner != self.user:
                self.add_error('lead', 'Selecione um lead da sua carteira.')
            if contact and contact.owner != self.user:
                self.add_error('contact', 'Selecione um contato da sua carteira.')
        if lead and contact and lead.contact and lead.contact != contact:
            self.add_error(
                'contact',
                'Se informar lead e contato, use o contato ligado ao lead selecionado.',
            )
        return cleaned_data
