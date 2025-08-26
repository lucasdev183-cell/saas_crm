from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Cliente(models.Model):
    TIPOS_PESSOA = [
        ('PF', 'Pessoa Física'),
        ('PJ', 'Pessoa Jurídica'),
    ]
    
    STATUS_CHOICES = [
        ('ativo', 'Ativo'),
        ('inativo', 'Inativo'),
        ('potencial', 'Cliente Potencial'),
    ]
    
    # Informações básicas
    nome_completo = models.CharField('Nome Completo', max_length=200)
    nome_fantasia = models.CharField('Nome Fantasia', max_length=200, blank=True, null=True)
    tipo_pessoa = models.CharField('Tipo de Pessoa', max_length=2, choices=TIPOS_PESSOA, default='PF')
    cpf_cnpj = models.CharField('CPF/CNPJ', max_length=20, unique=True)
    rg_inscricao = models.CharField('RG/Inscrição Estadual', max_length=20, blank=True, null=True)
    
    # Contato
    email = models.EmailField('E-mail', blank=True, null=True)
    telefone = models.CharField('Telefone', max_length=20, blank=True, null=True)
    celular = models.CharField('Celular', max_length=20, blank=True, null=True)
    
    # Endereço
    cep = models.CharField('CEP', max_length=10, blank=True, null=True)
    endereco = models.CharField('Endereço', max_length=300, blank=True, null=True)
    numero = models.CharField('Número', max_length=10, blank=True, null=True)
    complemento = models.CharField('Complemento', max_length=100, blank=True, null=True)
    bairro = models.CharField('Bairro', max_length=100, blank=True, null=True)
    cidade = models.CharField('Cidade', max_length=100, blank=True, null=True)
    estado = models.CharField('Estado', max_length=2, blank=True, null=True)
    
    # Informações comerciais
    status = models.CharField('Status', max_length=10, choices=STATUS_CHOICES, default='potencial')
    segmento = models.CharField('Segmento', max_length=100, blank=True, null=True)
    origem = models.CharField('Origem do Contato', max_length=100, blank=True, null=True)
    observacoes = models.TextField('Observações', blank=True, null=True)
    
    # Controle
    responsavel = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Responsável')
    data_cadastro = models.DateTimeField('Data de Cadastro', auto_now_add=True)
    data_atualizacao = models.DateTimeField('Última Atualização', auto_now=True)
    ativo = models.BooleanField('Ativo', default=True)
    
    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['-data_cadastro']
    
    def __str__(self):
        return self.nome_completo
    
    def get_absolute_url(self):
        return reverse('clientes:detalhe', kwargs={'pk': self.pk})
    
    @property
    def nome_exibicao(self):
        if self.tipo_pessoa == 'PJ' and self.nome_fantasia:
            return self.nome_fantasia
        return self.nome_completo

class Contato(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='contatos', verbose_name='Cliente')
    nome = models.CharField('Nome', max_length=100)
    cargo = models.CharField('Cargo', max_length=100, blank=True, null=True)
    email = models.EmailField('E-mail', blank=True, null=True)
    telefone = models.CharField('Telefone', max_length=20, blank=True, null=True)
    celular = models.CharField('Celular', max_length=20, blank=True, null=True)
    observacoes = models.TextField('Observações', blank=True, null=True)
    principal = models.BooleanField('Contato Principal', default=False)
    ativo = models.BooleanField('Ativo', default=True)
    data_cadastro = models.DateTimeField('Data de Cadastro', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Contato'
        verbose_name_plural = 'Contatos'
        ordering = ['-principal', 'nome']
    
    def __str__(self):
        return f"{self.nome} - {self.cliente.nome_completo}"
