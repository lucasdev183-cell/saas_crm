from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from decimal import Decimal
from clientes.models import Cliente

class Produto(models.Model):
    nome = models.CharField('Nome do Produto', max_length=200)
    descricao = models.TextField('Descrição', blank=True, null=True)
    codigo = models.CharField('Código', max_length=50, unique=True)
    preco_unitario = models.DecimalField('Preço Unitário', max_digits=10, decimal_places=2)
    categoria = models.CharField('Categoria', max_length=100, blank=True, null=True)
    unidade_medida = models.CharField('Unidade de Medida', max_length=10, default='UN')
    estoque_atual = models.IntegerField('Estoque Atual', default=0)
    estoque_minimo = models.IntegerField('Estoque Mínimo', default=0)
    ativo = models.BooleanField('Ativo', default=True)
    data_cadastro = models.DateTimeField('Data de Cadastro', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        ordering = ['nome']
    
    def __str__(self):
        return self.nome
    
    @property
    def precisa_reposicao(self):
        return self.estoque_atual <= self.estoque_minimo

class Oportunidade(models.Model):
    STATUS_CHOICES = [
        ('prospectando', 'Prospectando'),
        ('qualificada', 'Qualificada'),
        ('proposta', 'Proposta Enviada'),
        ('negociacao', 'Em Negociação'),
        ('fechada_ganha', 'Fechada - Ganha'),
        ('fechada_perdida', 'Fechada - Perdida'),
    ]
    
    FASES_FUNIL = [
        ('inicial', 'Contato Inicial'),
        ('interesse', 'Demonstrou Interesse'),
        ('necessidade', 'Identificou Necessidade'),
        ('orcamento', 'Solicitou Orçamento'),
        ('decisao', 'Em Decisão'),
        ('fechamento', 'Fechamento'),
    ]
    
    titulo = models.CharField('Título da Oportunidade', max_length=200)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, verbose_name='Cliente')
    valor_estimado = models.DecimalField('Valor Estimado', max_digits=12, decimal_places=2)
    probabilidade = models.IntegerField('Probabilidade (%)', default=50)
    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES, default='prospectando')
    fase_funil = models.CharField('Fase do Funil', max_length=20, choices=FASES_FUNIL, default='inicial')
    data_inicio = models.DateField('Data de Início')
    data_fechamento_prevista = models.DateField('Data de Fechamento Prevista')
    data_fechamento_real = models.DateField('Data de Fechamento Real', blank=True, null=True)
    responsavel = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Responsável')
    descricao = models.TextField('Descrição', blank=True, null=True)
    origem = models.CharField('Origem', max_length=100, blank=True, null=True)
    concorrentes = models.TextField('Concorrentes', blank=True, null=True)
    observacoes = models.TextField('Observações', blank=True, null=True)
    data_cadastro = models.DateTimeField('Data de Cadastro', auto_now_add=True)
    data_atualizacao = models.DateTimeField('Última Atualização', auto_now=True)
    
    class Meta:
        verbose_name = 'Oportunidade'
        verbose_name_plural = 'Oportunidades'
        ordering = ['-data_cadastro']
    
    def __str__(self):
        return f"{self.titulo} - {self.cliente.nome_completo}"
    
    def get_absolute_url(self):
        return reverse('vendas:oportunidade_detalhe', kwargs={'pk': self.pk})
    
    @property
    def valor_ponderado(self):
        return self.valor_estimado * (self.probabilidade / 100)

class Venda(models.Model):
    STATUS_CHOICES = [
        ('orcamento', 'Orçamento'),
        ('pedido', 'Pedido'),
        ('aprovada', 'Aprovada'),
        ('faturada', 'Faturada'),
        ('entregue', 'Entregue'),
        ('cancelada', 'Cancelada'),
    ]
    
    numero = models.CharField('Número da Venda', max_length=20, unique=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, verbose_name='Cliente')
    oportunidade = models.ForeignKey(Oportunidade, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Oportunidade')
    data_venda = models.DateField('Data da Venda')
    status = models.CharField('Status', max_length=15, choices=STATUS_CHOICES, default='orcamento')
    valor_total = models.DecimalField('Valor Total', max_digits=12, decimal_places=2, default=0)
    desconto = models.DecimalField('Desconto', max_digits=10, decimal_places=2, default=0)
    observacoes = models.TextField('Observações', blank=True, null=True)
    vendedor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Vendedor')
    data_cadastro = models.DateTimeField('Data de Cadastro', auto_now_add=True)
    data_atualizacao = models.DateTimeField('Última Atualização', auto_now=True)
    
    class Meta:
        verbose_name = 'Venda'
        verbose_name_plural = 'Vendas'
        ordering = ['-data_venda']
    
    def __str__(self):
        return f"Venda {self.numero} - {self.cliente.nome_completo}"
    
    def get_absolute_url(self):
        return reverse('vendas:venda_detalhe', kwargs={'pk': self.pk})
    
    def calcular_total(self):
        total_itens = sum(item.valor_total for item in self.itens.all())
        return total_itens - self.desconto
    
    def save(self, *args, **kwargs):
        if not self.numero:
            # Gerar número automático
            ultimo_numero = Venda.objects.filter(numero__startswith='VN').count()
            self.numero = f'VN{(ultimo_numero + 1):06d}'
        super().save(*args, **kwargs)

class ItemVenda(models.Model):
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE, related_name='itens', verbose_name='Venda')
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, verbose_name='Produto')
    quantidade = models.DecimalField('Quantidade', max_digits=10, decimal_places=2)
    preco_unitario = models.DecimalField('Preço Unitário', max_digits=10, decimal_places=2)
    desconto_item = models.DecimalField('Desconto do Item', max_digits=10, decimal_places=2, default=0)
    observacoes = models.CharField('Observações', max_length=300, blank=True, null=True)
    
    class Meta:
        verbose_name = 'Item da Venda'
        verbose_name_plural = 'Itens da Venda'
    
    def __str__(self):
        return f"{self.produto.nome} - {self.quantidade}"
    
    @property
    def valor_total(self):
        return (self.quantidade * self.preco_unitario) - self.desconto_item
