from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.PainelView.as_view(), name='painel'),
    path('metricas/', views.MetricasView.as_view(), name='metricas'),
    path('relatorios/', views.RelatoriosView.as_view(), name='relatorios'),
]