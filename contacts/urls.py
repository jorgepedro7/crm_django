from django.urls import path

from .views import (
    ContactCreateView,
    ContactDeleteView,
    ContactListView,
    ContactUpdateView,
)

app_name = 'contacts'


urlpatterns = [
    path('', ContactListView.as_view(), name='list'),
    path('novo/', ContactCreateView.as_view(), name='create'),
    path('<int:pk>/editar/', ContactUpdateView.as_view(), name='update'),
    path('<int:pk>/excluir/', ContactDeleteView.as_view(), name='delete'),
]
