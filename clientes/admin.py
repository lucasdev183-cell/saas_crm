from django.contrib import admin
from .models import Cliente, Contato

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nome_completo', 'tipo_pessoa', 'cpf_cnpj', 'email', 'status', 'responsavel', 'data_cadastro']
    list_filter = ['tipo_pessoa', 'status', 'segmento', 'responsavel', 'data_cadastro']
    search_fields = ['nome_completo', 'nome_fantasia', 'cpf_cnpj', 'email']
    list_editable = ['status']
    ordering = ['-data_cadastro']
    date_hierarchy = 'data_cadastro'
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome_completo', 'nome_fantasia', 'tipo_pessoa', 'cpf_cnpj', 'rg_inscricao')
        }),
        ('Contato', {
            'fields': ('email', 'telefone', 'celular')
        }),
        ('Endereço', {
            'fields': ('cep', 'endereco', 'numero', 'complemento', 'bairro', 'cidade', 'estado'),
            'classes': ('collapse',)
        }),
        ('Informações Comerciais', {
            'fields': ('status', 'segmento', 'origem', 'responsavel', 'observacoes')
        }),
        ('Controle', {
            'fields': ('ativo',),
            'classes': ('collapse',)
        })
    )

@admin.register(Contato)
class ContatoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'cliente', 'cargo', 'email', 'telefone', 'principal', 'ativo']
    list_filter = ['principal', 'ativo', 'data_cadastro']
    search_fields = ['nome', 'email', 'cliente__nome_completo']
    list_editable = ['principal', 'ativo']
    ordering = ['cliente__nome_completo', '-principal', 'nome']
