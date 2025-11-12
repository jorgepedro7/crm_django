from django.urls import path

from .views import (
    TaskCreateView,
    TaskDeleteView,
    TaskListView,
    TaskUpdateView,
)

app_name = 'tasks'


urlpatterns = [
    path('', TaskListView.as_view(), name='list'),
    path('nova/', TaskCreateView.as_view(), name='create'),
    path('<int:pk>/editar/', TaskUpdateView.as_view(), name='update'),
    path('<int:pk>/excluir/', TaskDeleteView.as_view(), name='delete'),
]
