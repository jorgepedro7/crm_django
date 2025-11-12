from django.urls import path

from .views import (
    LeadConvertView,
    LeadCreateView,
    LeadDeleteView,
    LeadListView,
    LeadUpdateView,
)

app_name = 'leads'


urlpatterns = [
    path('', LeadListView.as_view(), name='list'),
    path('novo/', LeadCreateView.as_view(), name='create'),
    path('<int:pk>/editar/', LeadUpdateView.as_view(), name='update'),
    path('<int:pk>/excluir/', LeadDeleteView.as_view(), name='delete'),
    path('<int:pk>/converter/', LeadConvertView.as_view(), name='convert'),
]
