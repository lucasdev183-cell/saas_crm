from django.urls import path
from . import views

app_name = 'tarefas'

urlpatterns = [
    # Tarefas
    path('', views.TarefaListView.as_view(), name='lista'),
    path('adicionar/', views.TarefaCreateView.as_view(), name='adicionar'),
    path('<int:pk>/', views.TarefaDetailView.as_view(), name='detalhe'),
    path('<int:pk>/editar/', views.TarefaUpdateView.as_view(), name='editar'),
    path('<int:pk>/concluir/', views.TarefaConcluirView.as_view(), name='concluir'),
    
    # Agenda
    path('agenda/', views.AgendaListView.as_view(), name='agenda_lista'),
    path('agenda/adicionar/', views.AgendaCreateView.as_view(), name='agenda_adicionar'),
    path('agenda/<int:pk>/', views.AgendaDetailView.as_view(), name='agenda_detalhe'),
    path('agenda/<int:pk>/editar/', views.AgendaUpdateView.as_view(), name='agenda_editar'),
    
    # Atividades
    path('atividades/', views.AtividadeListView.as_view(), name='atividades_lista'),
    path('atividades/adicionar/', views.AtividadeCreateView.as_view(), name='atividades_adicionar'),
    
    # Minhas tarefas
    path('minhas/', views.MinhasTarefasView.as_view(), name='minhas'),
]