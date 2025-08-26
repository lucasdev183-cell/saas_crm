from django.contrib import admin
from .models import Produto, Oportunidade, Venda, ItemVenda

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'codigo', 'preco_unitario', 'categoria', 'estoque_atual', 'estoque_minimo', 'ativo']
    list_filter = ['categoria', 'ativo', 'data_cadastro']
    search_fields = ['nome', 'codigo', 'descricao']
    list_editable = ['preco_unitario', 'estoque_atual', 'ativo']
    ordering = ['nome']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'descricao', 'codigo', 'categoria')
        }),
        ('Preço e Estoque', {
            'fields': ('preco_unitario', 'unidade_medida', 'estoque_atual', 'estoque_minimo')
        }),
        ('Controle', {
            'fields': ('ativo',)
        })
    )

@admin.register(Oportunidade)
class OportunidadeAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'cliente', 'valor_estimado', 'probabilidade', 'status', 'fase_funil', 'responsavel', 'data_fechamento_prevista']
    list_filter = ['status', 'fase_funil', 'responsavel', 'data_inicio', 'data_fechamento_prevista']
    search_fields = ['titulo', 'cliente__nome_completo', 'descricao']
    list_editable = ['status', 'fase_funil', 'probabilidade']
    ordering = ['-data_cadastro']
    date_hierarchy = 'data_fechamento_prevista'
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('titulo', 'cliente', 'responsavel', 'origem')
        }),
        ('Valor e Probabilidade', {
            'fields': ('valor_estimado', 'probabilidade', 'status', 'fase_funil')
        }),
        ('Datas', {
            'fields': ('data_inicio', 'data_fechamento_prevista', 'data_fechamento_real')
        }),
        ('Detalhes', {
            'fields': ('descricao', 'concorrentes', 'observacoes'),
            'classes': ('collapse',)
        })
    )

class ItemVendaInline(admin.TabularInline):
    model = ItemVenda
    extra = 1
    fields = ['produto', 'quantidade', 'preco_unitario', 'desconto_item']

@admin.register(Venda)
class VendaAdmin(admin.ModelAdmin):
    list_display = ['numero', 'cliente', 'data_venda', 'status', 'valor_total', 'vendedor']
    list_filter = ['status', 'vendedor', 'data_venda']
    search_fields = ['numero', 'cliente__nome_completo']
    list_editable = ['status']
    ordering = ['-data_venda']
    date_hierarchy = 'data_venda'
    inlines = [ItemVendaInline]
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('numero', 'cliente', 'oportunidade', 'vendedor')
        }),
        ('Valores', {
            'fields': ('data_venda', 'status', 'valor_total', 'desconto')
        }),
        ('Observações', {
            'fields': ('observacoes',),
            'classes': ('collapse',)
        })
    )
