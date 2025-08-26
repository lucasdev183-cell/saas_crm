from django.contrib import admin
from .models import Tarefa, Anotacao, Atividade, Agenda

class AnotacaoInline(admin.TabularInline):
    model = Anotacao
    extra = 1
    fields = ['conteudo', 'autor']

@admin.register(Tarefa)
class TarefaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'tipo', 'status', 'prioridade', 'responsavel', 'cliente', 'data_vencimento', 'atrasada']
    list_filter = ['tipo', 'status', 'prioridade', 'responsavel', 'data_vencimento']
    search_fields = ['titulo', 'descricao', 'cliente__nome_completo']
    list_editable = ['status', 'prioridade']
    ordering = ['data_vencimento', '-prioridade']
    date_hierarchy = 'data_vencimento'
    inlines = [AnotacaoInline]
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('titulo', 'descricao', 'tipo', 'responsavel')
        }),
        ('Status e Prioridade', {
            'fields': ('status', 'prioridade', 'tempo_estimado')
        }),
        ('Relacionamentos', {
            'fields': ('cliente', 'oportunidade'),
            'classes': ('collapse',)
        }),
        ('Datas', {
            'fields': ('data_vencimento', 'data_conclusao')
        }),
        ('Lembrete', {
            'fields': ('lembrete', 'data_lembrete'),
            'classes': ('collapse',)
        })
    )
    
    def atrasada(self, obj):
        return obj.atrasada
    atrasada.boolean = True
    atrasada.short_description = 'Atrasada'

@admin.register(Atividade)
class AtividadeAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'tipo', 'usuario', 'cliente', 'data_atividade']
    list_filter = ['tipo', 'usuario', 'data_atividade']
    search_fields = ['titulo', 'descricao', 'cliente__nome_completo']
    ordering = ['-data_atividade']
    date_hierarchy = 'data_atividade'
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('titulo', 'descricao', 'tipo', 'usuario')
        }),
        ('Relacionamentos', {
            'fields': ('cliente', 'oportunidade', 'tarefa')
        }),
        ('Data', {
            'fields': ('data_atividade',)
        })
    )

@admin.register(Agenda)
class AgendaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'tipo', 'organizador', 'data_inicio', 'data_fim', 'cliente']
    list_filter = ['tipo', 'organizador', 'data_inicio']
    search_fields = ['titulo', 'descricao', 'local', 'cliente__nome_completo']
    ordering = ['data_inicio']
    date_hierarchy = 'data_inicio'
    filter_horizontal = ['participantes']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('titulo', 'descricao', 'tipo', 'organizador')
        }),
        ('Data e Horário', {
            'fields': ('data_inicio', 'data_fim', 'dia_inteiro')
        }),
        ('Participantes', {
            'fields': ('participantes',)
        }),
        ('Relacionamentos', {
            'fields': ('cliente', 'oportunidade'),
            'classes': ('collapse',)
        }),
        ('Localização', {
            'fields': ('local', 'endereco'),
            'classes': ('collapse',)
        }),
        ('Lembrete', {
            'fields': ('lembrete', 'minutos_lembrete'),
            'classes': ('collapse',)
        })
    )
