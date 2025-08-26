"""
URLs principais do CRM Profissional
Todas as rotas em português brasileiro
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

# Função para redirecionar a página inicial para o painel
def redirecionar_para_painel(request):
    return redirect('dashboard:painel')

urlpatterns = [
    # Administração
    path('admin/', admin.site.urls),
    
    # Página inicial redireciona para o painel
    path('', redirecionar_para_painel, name='inicio'),
    
    # Apps do CRM
    path('painel/', include('dashboard.urls')),
    path('clientes/', include('clientes.urls')),
    path('vendas/', include('vendas.urls')),
    path('tarefas/', include('tarefas.urls')),
    
    # Autenticação
    path('autenticacao/', include('django.contrib.auth.urls')),
]

# Configuração para servir arquivos de mídia durante o desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Configurações do admin
admin.site.site_header = 'CRM Profissional - Administração'
admin.site.site_title = 'CRM Profissional'
admin.site.index_title = 'Painel Administrativo'
