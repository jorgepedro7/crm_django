from django.urls import path

from .views import (
    KanbanView,
    LeadConvertView,
    LeadCreateView,
    LeadDeleteView,
    LeadListView,
    LeadUpdateView,
    UpdateLeadPositionView,
)

app_name = 'leads'


urlpatterns = [
    path('', LeadListView.as_view(), name='list'),
    path('novo/', LeadCreateView.as_view(), name='create'),
    path('<int:pk>/editar/', LeadUpdateView.as_view(), name='update'),
    path('<int:pk>/excluir/', LeadDeleteView.as_view(), name='delete'),
    path('<int:pk>/converter/', LeadConvertView.as_view(), name='convert'),
    path('kanban/', KanbanView.as_view(), name='kanban'),
    path('kanban/update/', UpdateLeadPositionView.as_view(), name='kanban_update'),
]
