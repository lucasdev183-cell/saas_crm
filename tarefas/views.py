from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Tarefa, Atividade, Agenda

class TarefaListView(LoginRequiredMixin, ListView):
    model = Tarefa
    template_name = 'tarefas/lista.html'
    context_object_name = 'tarefas'
    paginate_by = 20

class TarefaDetailView(LoginRequiredMixin, DetailView):
    model = Tarefa
    template_name = 'tarefas/detalhe.html'
    context_object_name = 'tarefa'

class TarefaCreateView(LoginRequiredMixin, CreateView):
    model = Tarefa
    template_name = 'tarefas/form.html'
    fields = ['titulo', 'descricao', 'tipo', 'prioridade', 'data_vencimento']
    success_url = reverse_lazy('tarefas:lista')

class TarefaUpdateView(LoginRequiredMixin, UpdateView):
    model = Tarefa
    template_name = 'tarefas/form.html'
    fields = ['titulo', 'descricao', 'tipo', 'prioridade', 'status', 'data_vencimento']

class TarefaConcluirView(LoginRequiredMixin, UpdateView):
    model = Tarefa
    template_name = 'tarefas/concluir.html'
    fields = []
    
    def form_valid(self, form):
        form.instance.status = 'concluida'
        return super().form_valid(form)

class AgendaListView(LoginRequiredMixin, ListView):
    model = Agenda
    template_name = 'tarefas/agenda_lista.html'
    context_object_name = 'eventos'
    paginate_by = 20

class AgendaDetailView(LoginRequiredMixin, DetailView):
    model = Agenda
    template_name = 'tarefas/agenda_detalhe.html'
    context_object_name = 'evento'

class AgendaCreateView(LoginRequiredMixin, CreateView):
    model = Agenda
    template_name = 'tarefas/agenda_form.html'
    fields = ['titulo', 'descricao', 'tipo', 'data_inicio', 'data_fim', 'local']
    success_url = reverse_lazy('tarefas:agenda_lista')

class AgendaUpdateView(LoginRequiredMixin, UpdateView):
    model = Agenda
    template_name = 'tarefas/agenda_form.html'
    fields = ['titulo', 'descricao', 'tipo', 'data_inicio', 'data_fim', 'local']

class AtividadeListView(LoginRequiredMixin, ListView):
    model = Atividade
    template_name = 'tarefas/atividades_lista.html'
    context_object_name = 'atividades'
    paginate_by = 20

class AtividadeCreateView(LoginRequiredMixin, CreateView):
    model = Atividade
    template_name = 'tarefas/atividades_form.html'
    fields = ['titulo', 'descricao', 'tipo', 'data_atividade']
    success_url = reverse_lazy('tarefas:atividades_lista')

class MinhasTarefasView(LoginRequiredMixin, TemplateView):
    template_name = 'tarefas/minhas.html'
