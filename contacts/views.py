from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import ContactForm
from .models import Contact


class ContactBaseMixin(LoginRequiredMixin):
    model = Contact
    login_url = 'users:login'

    def get_queryset(self):
        return Contact.objects.filter(owner=self.request.user).select_related('account')


class ContactListView(ContactBaseMixin, ListView):
    template_name = 'contacts/contact_list.html'
    context_object_name = 'contacts'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query)
                | Q(email__icontains=query)
                | Q(account__name__icontains=query)
            )
        return queryset


class ContactFormMixin(ContactBaseMixin):
    form_class = ContactForm
    success_url = reverse_lazy('contacts:list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ContactCreateView(ContactFormMixin, CreateView):
    template_name = 'contacts/contact_form.html'


class ContactUpdateView(ContactFormMixin, UpdateView):
    template_name = 'contacts/contact_form.html'


class ContactDeleteView(ContactBaseMixin, DeleteView):
    template_name = 'contacts/contact_confirm_delete.html'
    success_url = reverse_lazy('contacts:list')
