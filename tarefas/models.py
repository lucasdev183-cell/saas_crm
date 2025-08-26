from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from clientes.models import Cliente
from vendas.models import Oportunidade

class Tarefa(models.Model):
    TIPOS_TAREFA = [
        ('ligacao', 'Ligação'),
        ('email', 'E-mail'),
        ('reuniao', 'Reunião'),
        ('visita', 'Visita'),
        ('proposta', 'Elaborar Proposta'),
        ('follow_up', 'Follow-up'),
        ('apresentacao', 'Apresentação'),
        ('outro', 'Outro'),
    ]
    
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('em_andamento', 'Em Andamento'),
        ('concluida', 'Concluída'),
        ('cancelada', 'Cancelada'),
        ('adiada', 'Adiada'),
    ]
    
    PRIORIDADES = [
        ('baixa', 'Baixa'),
        ('media', 'Média'),
        ('alta', 'Alta'),
        ('urgente', 'Urgente'),
    ]
    
    titulo = models.CharField('Título', max_length=200)
    descricao = models.TextField('Descrição', blank=True, null=True)
    tipo = models.CharField('Tipo', max_length=15, choices=TIPOS_TAREFA, default='outro')
    status = models.CharField('Status', max_length=15, choices=STATUS_CHOICES, default='pendente')
    prioridade = models.CharField('Prioridade', max_length=10, choices=PRIORIDADES, default='media')
    
    # Relacionamentos
    responsavel = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Responsável')
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Cliente')
    oportunidade = models.ForeignKey(Oportunidade, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Oportunidade')
    
    # Datas
    data_vencimento = models.DateTimeField('Data de Vencimento')
    data_conclusao = models.DateTimeField('Data de Conclusão', null=True, blank=True)
    tempo_estimado = models.IntegerField('Tempo Estimado (minutos)', null=True, blank=True)
    
    # Controle
    criado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='tarefas_criadas', verbose_name='Criado por')
    data_cadastro = models.DateTimeField('Data de Cadastro', auto_now_add=True)
    data_atualizacao = models.DateTimeField('Última Atualização', auto_now=True)
    
    # Lembrete
    lembrete = models.BooleanField('Criar Lembrete', default=False)
    data_lembrete = models.DateTimeField('Data do Lembrete', null=True, blank=True)
    
    class Meta:
        verbose_name = 'Tarefa'
        verbose_name_plural = 'Tarefas'
        ordering = ['data_vencimento', '-prioridade']
    
    def __str__(self):
        return self.titulo
    
    def get_absolute_url(self):
        return reverse('tarefas:detalhe', kwargs={'pk': self.pk})
    
    @property
    def atrasada(self):
        from django.utils import timezone
        return self.status != 'concluida' and self.data_vencimento < timezone.now()
    
    @property
    def vence_hoje(self):
        from django.utils import timezone
        hoje = timezone.now().date()
        return self.data_vencimento.date() == hoje

class Anotacao(models.Model):
    tarefa = models.ForeignKey(Tarefa, on_delete=models.CASCADE, related_name='anotacoes', verbose_name='Tarefa')
    conteudo = models.TextField('Conteúdo')
    autor = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Autor')
    data_criacao = models.DateTimeField('Data de Criação', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Anotação'
        verbose_name_plural = 'Anotações'
        ordering = ['-data_criacao']
    
    def __str__(self):
        return f"Anotação - {self.tarefa.titulo}"

class Atividade(models.Model):
    TIPOS_ATIVIDADE = [
        ('ligacao', 'Ligação Realizada'),
        ('email_enviado', 'E-mail Enviado'),
        ('email_recebido', 'E-mail Recebido'),
        ('reuniao', 'Reunião'),
        ('visita', 'Visita'),
        ('proposta_enviada', 'Proposta Enviada'),
        ('contrato_assinado', 'Contrato Assinado'),
        ('pagamento_recebido', 'Pagamento Recebido'),
        ('outro', 'Outro'),
    ]
    
    titulo = models.CharField('Título', max_length=200)
    descricao = models.TextField('Descrição', blank=True, null=True)
    tipo = models.CharField('Tipo', max_length=20, choices=TIPOS_ATIVIDADE, default='outro')
    
    # Relacionamentos
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuário')
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Cliente')
    oportunidade = models.ForeignKey(Oportunidade, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Oportunidade')
    tarefa = models.ForeignKey(Tarefa, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Tarefa')
    
    # Controle
    data_atividade = models.DateTimeField('Data da Atividade')
    data_cadastro = models.DateTimeField('Data de Cadastro', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Atividade'
        verbose_name_plural = 'Atividades'
        ordering = ['-data_atividade']
    
    def __str__(self):
        return f"{self.titulo} - {self.data_atividade.strftime('%d/%m/%Y %H:%M')}"

class Agenda(models.Model):
    TIPOS_EVENTO = [
        ('reuniao', 'Reunião'),
        ('ligacao', 'Ligação'),
        ('visita', 'Visita'),
        ('apresentacao', 'Apresentação'),
        ('evento', 'Evento'),
        ('outro', 'Outro'),
    ]
    
    titulo = models.CharField('Título', max_length=200)
    descricao = models.TextField('Descrição', blank=True, null=True)
    tipo = models.CharField('Tipo', max_length=15, choices=TIPOS_EVENTO, default='reuniao')
    
    # Datas e horários
    data_inicio = models.DateTimeField('Data/Hora de Início')
    data_fim = models.DateTimeField('Data/Hora de Fim')
    dia_inteiro = models.BooleanField('Dia Inteiro', default=False)
    
    # Relacionamentos
    organizador = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Organizador')
    participantes = models.ManyToManyField(User, related_name='eventos_participando', blank=True, verbose_name='Participantes')
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Cliente')
    oportunidade = models.ForeignKey(Oportunidade, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Oportunidade')
    
    # Localização
    local = models.CharField('Local', max_length=300, blank=True, null=True)
    endereco = models.TextField('Endereço', blank=True, null=True)
    
    # Lembrete
    lembrete = models.BooleanField('Criar Lembrete', default=True)
    minutos_lembrete = models.IntegerField('Minutos antes do lembrete', default=15)
    
    # Controle
    data_cadastro = models.DateTimeField('Data de Cadastro', auto_now_add=True)
    data_atualizacao = models.DateTimeField('Última Atualização', auto_now=True)
    
    class Meta:
        verbose_name = 'Evento da Agenda'
        verbose_name_plural = 'Eventos da Agenda'
        ordering = ['data_inicio']
    
    def __str__(self):
        return f"{self.titulo} - {self.data_inicio.strftime('%d/%m/%Y %H:%M')}"
    
    def get_absolute_url(self):
        return reverse('tarefas:agenda_detalhe', kwargs={'pk': self.pk})
