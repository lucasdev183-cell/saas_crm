"""
URLs principais do CRM Profissional
Todas as rotas em português brasileiro
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views

# Função para redirecionar a página inicial para o painel
def redirecionar_para_painel(request):
    if request.user.is_authenticated:
        return redirect('dashboard:painel')
    else:
        return redirect('login')

urlpatterns = [
    # Administração
    path('admin/', admin.site.urls),
    
    # Página inicial redireciona para o painel ou login
    path('', redirecionar_para_painel, name='inicio'),
    
    # Autenticação
    path('entrar/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('sair/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Apps do CRM (protegidos por autenticação)
    path('painel/', include('dashboard.urls')),
    path('clientes/', include('clientes.urls')),
    path('vendas/', include('vendas.urls')),
    path('tarefas/', include('tarefas.urls')),
]

# Configuração para servir arquivos de mídia durante o desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Configurações do admin
admin.site.site_header = 'CRM Profissional - Administração'
admin.site.site_title = 'CRM Profissional'
admin.site.index_title = 'Painel Administrativo'
