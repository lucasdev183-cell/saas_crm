from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Sum, Avg
from django.utils import timezone
from datetime import datetime, timedelta
from clientes.models import Cliente
from vendas.models import Venda, Oportunidade, Produto
from tarefas.models import Tarefa, Atividade

class PainelView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/painel.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        hoje = timezone.now().date()
        inicio_mes = hoje.replace(day=1)
        mes_passado = (inicio_mes - timedelta(days=1)).replace(day=1)
        
        # Métricas gerais
        context['total_clientes'] = Cliente.objects.filter(ativo=True).count()
        context['clientes_ativos'] = Cliente.objects.filter(status='ativo', ativo=True).count()
        context['clientes_potenciais'] = Cliente.objects.filter(status='potencial', ativo=True).count()
        
        # Vendas
        vendas_mes = Venda.objects.filter(data_venda__gte=inicio_mes, data_venda__lte=hoje)
        context['vendas_mes'] = vendas_mes.count()
        context['faturamento_mes'] = vendas_mes.aggregate(total=Sum('valor_total'))['total'] or 0
        
        vendas_mes_passado = Venda.objects.filter(data_venda__gte=mes_passado, data_venda__lt=inicio_mes)
        faturamento_mes_passado = vendas_mes_passado.aggregate(total=Sum('valor_total'))['total'] or 0
        
        # Cálculo do crescimento
        if faturamento_mes_passado > 0:
            crescimento = ((context['faturamento_mes'] - faturamento_mes_passado) / faturamento_mes_passado) * 100
            context['crescimento_faturamento'] = round(crescimento, 1)
        else:
            context['crescimento_faturamento'] = 0
        
        # Oportunidades
        oportunidades_abertas = Oportunidade.objects.exclude(status__in=['fechada_ganha', 'fechada_perdida'])
        context['oportunidades_abertas'] = oportunidades_abertas.count()
        context['valor_pipeline'] = oportunidades_abertas.aggregate(total=Sum('valor_estimado'))['total'] or 0
        
        # Tarefas
        context['tarefas_pendentes'] = Tarefa.objects.filter(
            responsavel=self.request.user,
            status__in=['pendente', 'em_andamento']
        ).count()
        
        context['tarefas_vencendo_hoje'] = Tarefa.objects.filter(
            responsavel=self.request.user,
            data_vencimento__date=hoje,
            status__in=['pendente', 'em_andamento']
        ).count()
        
        context['tarefas_atrasadas'] = Tarefa.objects.filter(
            responsavel=self.request.user,
            data_vencimento__lt=timezone.now(),
            status__in=['pendente', 'em_andamento']
        ).count()
        
        # Gráfico de vendas dos últimos 7 dias
        ultimos_7_dias = []
        vendas_7_dias = []
        for i in range(6, -1, -1):
            data = hoje - timedelta(days=i)
            vendas_dia = Venda.objects.filter(data_venda=data).aggregate(total=Sum('valor_total'))['total'] or 0
            ultimos_7_dias.append(data.strftime('%d/%m'))
            vendas_7_dias.append(float(vendas_dia))
        
        context['grafico_vendas_labels'] = ultimos_7_dias
        context['grafico_vendas_data'] = vendas_7_dias
        
        # Produtos com estoque baixo
        from django.db import models
        context['produtos_estoque_baixo'] = Produto.objects.filter(
            estoque_atual__lte=models.F('estoque_minimo'),
            ativo=True
        )[:5]
        
        # Últimas atividades
        context['ultimas_atividades'] = Atividade.objects.filter(
            usuario=self.request.user
        ).select_related('cliente', 'oportunidade')[:10]
        
        # Top clientes do mês
        context['top_clientes'] = Cliente.objects.filter(
            venda__data_venda__gte=inicio_mes,
            venda__data_venda__lte=hoje
        ).annotate(
            total_compras=Sum('venda__valor_total')
        ).order_by('-total_compras')[:5]
        
        return context

class MetricasView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/metricas.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        hoje = timezone.now().date()
        
        # Métricas de conversão
        total_oportunidades = Oportunidade.objects.count()
        oportunidades_ganhas = Oportunidade.objects.filter(status='fechada_ganha').count()
        
        if total_oportunidades > 0:
            context['taxa_conversao'] = round((oportunidades_ganhas / total_oportunidades) * 100, 1)
        else:
            context['taxa_conversao'] = 0
        
        # Tempo médio de fechamento
        oportunidades_fechadas = Oportunidade.objects.filter(
            status__in=['fechada_ganha', 'fechada_perdida'],
            data_fechamento_real__isnull=False
        )
        
        if oportunidades_fechadas.exists():
            tempos_fechamento = []
            for op in oportunidades_fechadas:
                tempo = (op.data_fechamento_real - op.data_inicio).days
                tempos_fechamento.append(tempo)
            context['tempo_medio_fechamento'] = round(sum(tempos_fechamento) / len(tempos_fechamento), 1)
        else:
            context['tempo_medio_fechamento'] = 0
        
        # Ticket médio
        vendas_com_valor = Venda.objects.filter(valor_total__gt=0)
        if vendas_com_valor.exists():
            context['ticket_medio'] = vendas_com_valor.aggregate(media=Avg('valor_total'))['media']
        else:
            context['ticket_medio'] = 0
        
        return context

class RelatoriosView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/relatorios.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Relatórios disponíveis
        context['relatorios'] = [
            {
                'titulo': 'Relatório de Vendas',
                'descricao': 'Análise detalhada das vendas por período',
                'url': '#',
                'icone': 'fas fa-chart-line'
            },
            {
                'titulo': 'Relatório de Clientes',
                'descricao': 'Análise do cadastro e comportamento dos clientes',
                'url': '#',
                'icone': 'fas fa-users'
            },
            {
                'titulo': 'Pipeline de Vendas',
                'descricao': 'Análise do funil de vendas e oportunidades',
                'url': '#',
                'icone': 'fas fa-funnel-dollar'
            },
            {
                'titulo': 'Relatório de Produtos',
                'descricao': 'Análise de performance e estoque de produtos',
                'url': '#',
                'icone': 'fas fa-box'
            },
        ]
        
        return context
