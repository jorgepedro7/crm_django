from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import AccountForm
from .models import Account


class AccountBaseMixin(LoginRequiredMixin):
    model = Account
    login_url = 'users:login'

    def get_queryset(self):
        return Account.objects.filter(owner=self.request.user)


class AccountListView(AccountBaseMixin, ListView):
    template_name = 'accounts/account_list.html'
    context_object_name = 'accounts'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(name__icontains=query)
        return queryset


class AccountFormMixin(AccountBaseMixin):
    form_class = AccountForm
    success_url = reverse_lazy('accounts:list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class AccountCreateView(SuccessMessageMixin, AccountFormMixin, CreateView):
    template_name = 'accounts/account_form.html'
    success_message = 'Conta criada com sucesso.'


class AccountUpdateView(SuccessMessageMixin, AccountFormMixin, UpdateView):
    template_name = 'accounts/account_form.html'
    success_message = 'Conta atualizada com sucesso.'


class AccountDeleteView(AccountBaseMixin, DeleteView):
    template_name = 'accounts/account_confirm_delete.html'
    success_url = reverse_lazy('accounts:list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Conta excluída com sucesso.')
        return super().delete(request, *args, **kwargs)
