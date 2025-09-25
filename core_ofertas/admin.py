from django.contrib import admin
from .models import Oferta
from django.utils import timezone

@admin.register(Oferta)
class OfertaAdmin(admin.ModelAdmin):
    list_display = [
        'titulo', 
        'estabelecimento', 
        'quantidade', 
        'unidade',
        'data_expiracao', 
        'status', 
        'data_criacao'
    ]
    
    list_filter = [
        'status', 
        'unidade',
        'data_expiracao',
        'data_criacao',
        'estabelecimento'
    ]
    
    search_fields = [
        'titulo', 
        'descricao', 
        'estabelecimento__username',
        'estabelecimento__email'
    ]
    
    readonly_fields = ['data_criacao', 'data_atualizacao']
    
    fieldsets = [
        ('Informações Básicas', {
            'fields': [
                'estabelecimento', 
                'titulo', 
                'descricao'
            ]
        }),
        ('Detalhes da Oferta', {
            'fields': [
                'quantidade', 
                'unidade', 
                'data_expiracao',
                'foto'
            ]
        }),
        ('Status e Metadados', {
            'fields': [
                'status',
                'data_criacao',
                'data_atualizacao'
            ]
        }),
    ]
    
    def get_queryset(self, request):
        """Atualiza automaticamente o status das ofertas expiradas"""
        queryset = super().get_queryset(request)
        
        # Verifica ofertas que podem ter expirado
        ofertas_para_verificar = queryset.filter(
            status__in=['disponivel', 'reservado'],
            data_expiracao__lt=timezone.now()
        )
        
        for oferta in ofertas_para_verificar:
            oferta.verificar_expiracao()
        
        return queryset