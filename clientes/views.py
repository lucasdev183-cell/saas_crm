from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Cliente, Contato

class ClienteListView(LoginRequiredMixin, ListView):
    model = Cliente
    template_name = 'clientes/lista.html'
    context_object_name = 'clientes'
    paginate_by = 20

class ClienteDetailView(LoginRequiredMixin, DetailView):
    model = Cliente
    template_name = 'clientes/detalhe.html'
    context_object_name = 'cliente'

class ClienteCreateView(LoginRequiredMixin, CreateView):
    model = Cliente
    template_name = 'clientes/form.html'
    fields = ['nome_completo', 'tipo_pessoa', 'cpf_cnpj', 'email', 'telefone', 'status']
    success_url = reverse_lazy('clientes:lista')

class ClienteUpdateView(LoginRequiredMixin, UpdateView):
    model = Cliente
    template_name = 'clientes/form.html'
    fields = ['nome_completo', 'tipo_pessoa', 'cpf_cnpj', 'email', 'telefone', 'status']

class ClienteDeleteView(LoginRequiredMixin, DeleteView):
    model = Cliente
    template_name = 'clientes/confirmar_exclusao.html'
    success_url = reverse_lazy('clientes:lista')

class ContatoCreateView(LoginRequiredMixin, CreateView):
    model = Contato
    template_name = 'clientes/contato_form.html'
    fields = ['nome', 'email', 'telefone', 'cargo']
    
    def form_valid(self, form):
        form.instance.cliente_id = self.kwargs['cliente_pk']
        return super().form_valid(form)

class ContatoUpdateView(LoginRequiredMixin, UpdateView):
    model = Contato
    template_name = 'clientes/contato_form.html'
    fields = ['nome', 'email', 'telefone', 'cargo']

class ContatoDeleteView(LoginRequiredMixin, DeleteView):
    model = Contato
    template_name = 'clientes/contato_confirmar_exclusao.html'
    
    def get_success_url(self):
        return reverse_lazy('clientes:detalhe', kwargs={'pk': self.object.cliente.pk})
