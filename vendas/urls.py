from django.urls import path
from . import views

app_name = 'vendas'

urlpatterns = [
    # Produtos
    path('produtos/', views.ProdutoListView.as_view(), name='produtos_lista'),
    path('produtos/adicionar/', views.ProdutoCreateView.as_view(), name='produtos_adicionar'),
    path('produtos/<int:pk>/', views.ProdutoDetailView.as_view(), name='produtos_detalhe'),
    path('produtos/<int:pk>/editar/', views.ProdutoUpdateView.as_view(), name='produtos_editar'),
    
    # Oportunidades
    path('oportunidades/', views.OportunidadeListView.as_view(), name='oportunidades_lista'),
    path('oportunidades/adicionar/', views.OportunidadeCreateView.as_view(), name='oportunidades_adicionar'),
    path('oportunidades/<int:pk>/', views.OportunidadeDetailView.as_view(), name='oportunidade_detalhe'),
    path('oportunidades/<int:pk>/editar/', views.OportunidadeUpdateView.as_view(), name='oportunidades_editar'),
    
    # Vendas
    path('', views.VendaListView.as_view(), name='lista'),
    path('adicionar/', views.VendaCreateView.as_view(), name='adicionar'),
    path('<int:pk>/', views.VendaDetailView.as_view(), name='venda_detalhe'),
    path('<int:pk>/editar/', views.VendaUpdateView.as_view(), name='editar'),
    
    # Funil de vendas
    path('funil/', views.FunilVendasView.as_view(), name='funil'),
]