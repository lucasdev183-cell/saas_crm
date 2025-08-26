from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Produto, Oportunidade, Venda

class ProdutoListView(LoginRequiredMixin, ListView):
    model = Produto
    template_name = 'vendas/produtos_lista.html'
    context_object_name = 'produtos'
    paginate_by = 20

class ProdutoDetailView(LoginRequiredMixin, DetailView):
    model = Produto
    template_name = 'vendas/produtos_detalhe.html'
    context_object_name = 'produto'

class ProdutoCreateView(LoginRequiredMixin, CreateView):
    model = Produto
    template_name = 'vendas/produtos_form.html'
    fields = ['nome', 'codigo', 'preco_unitario', 'categoria', 'estoque_atual']
    success_url = reverse_lazy('vendas:produtos_lista')

class ProdutoUpdateView(LoginRequiredMixin, UpdateView):
    model = Produto
    template_name = 'vendas/produtos_form.html'
    fields = ['nome', 'codigo', 'preco_unitario', 'categoria', 'estoque_atual']

class OportunidadeListView(LoginRequiredMixin, ListView):
    model = Oportunidade
    template_name = 'vendas/oportunidades_lista.html'
    context_object_name = 'oportunidades'
    paginate_by = 20

class OportunidadeDetailView(LoginRequiredMixin, DetailView):
    model = Oportunidade
    template_name = 'vendas/oportunidades_detalhe.html'
    context_object_name = 'oportunidade'

class OportunidadeCreateView(LoginRequiredMixin, CreateView):
    model = Oportunidade
    template_name = 'vendas/oportunidades_form.html'
    fields = ['titulo', 'cliente', 'valor_estimado', 'probabilidade', 'data_inicio', 'data_fechamento_prevista']
    success_url = reverse_lazy('vendas:oportunidades_lista')

class OportunidadeUpdateView(LoginRequiredMixin, UpdateView):
    model = Oportunidade
    template_name = 'vendas/oportunidades_form.html'
    fields = ['titulo', 'cliente', 'valor_estimado', 'probabilidade', 'status', 'fase_funil']

class VendaListView(LoginRequiredMixin, ListView):
    model = Venda
    template_name = 'vendas/lista.html'
    context_object_name = 'vendas'
    paginate_by = 20

class VendaDetailView(LoginRequiredMixin, DetailView):
    model = Venda
    template_name = 'vendas/detalhe.html'
    context_object_name = 'venda'

class VendaCreateView(LoginRequiredMixin, CreateView):
    model = Venda
    template_name = 'vendas/form.html'
    fields = ['cliente', 'data_venda', 'status']
    success_url = reverse_lazy('vendas:lista')

class VendaUpdateView(LoginRequiredMixin, UpdateView):
    model = Venda
    template_name = 'vendas/form.html'
    fields = ['cliente', 'data_venda', 'status']

class FunilVendasView(LoginRequiredMixin, TemplateView):
    template_name = 'vendas/funil.html'
