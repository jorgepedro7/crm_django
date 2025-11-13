from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import TaskForm
from .models import Task


class TaskBaseMixin(LoginRequiredMixin):
    model = Task
    login_url = 'users:login'

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user).select_related('lead', 'contact')


class TaskListView(TaskBaseMixin, ListView):
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.GET.get('status')
        query = self.request.GET.get('q')
        if status:
            queryset = queryset.filter(status=status)
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            )
        return queryset.order_by('due_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.localdate()
        base_qs = Task.objects.filter(owner=self.request.user)
        context.update(
            {
                'selected_status': self.request.GET.get('status', ''),
                'status_choices': Task.Status.choices,
                'overdue_tasks': base_qs.filter(
                    status=Task.Status.PENDING, due_date__lt=today
                ).order_by('due_date')[:5],
                'upcoming_tasks': base_qs.filter(
                    status=Task.Status.PENDING, due_date__gte=today
                ).order_by('due_date')[:5],
            }
        )
        return context


class TaskFormMixin(TaskBaseMixin):
    form_class = TaskForm
    success_url = reverse_lazy('tasks:list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class TaskCreateView(SuccessMessageMixin, TaskFormMixin, CreateView):
    template_name = 'tasks/task_form.html'
    success_message = 'Tarefa criada com sucesso.'


class TaskUpdateView(SuccessMessageMixin, TaskFormMixin, UpdateView):
    template_name = 'tasks/task_form.html'
    success_message = 'Tarefa atualizada com sucesso.'


class TaskDeleteView(TaskBaseMixin, DeleteView):
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('tasks:list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Tarefa excluída com sucesso.')
        return super().delete(request, *args, **kwargs)
