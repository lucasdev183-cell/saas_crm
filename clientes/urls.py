from django.urls import path
from . import views

app_name = 'clientes'

urlpatterns = [
    path('', views.ClienteListView.as_view(), name='lista'),
    path('adicionar/', views.ClienteCreateView.as_view(), name='adicionar'),
    path('<int:pk>/', views.ClienteDetailView.as_view(), name='detalhe'),
    path('<int:pk>/editar/', views.ClienteUpdateView.as_view(), name='editar'),
    path('<int:pk>/excluir/', views.ClienteDeleteView.as_view(), name='excluir'),
    path('<int:cliente_pk>/contatos/adicionar/', views.ContatoCreateView.as_view(), name='contato_adicionar'),
    path('contatos/<int:pk>/editar/', views.ContatoUpdateView.as_view(), name='contato_editar'),
    path('contatos/<int:pk>/excluir/', views.ContatoDeleteView.as_view(), name='contato_excluir'),
]