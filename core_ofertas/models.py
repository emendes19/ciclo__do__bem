from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

class Oferta(models.Model):
    STATUS_CHOICES = [
        ('disponivel', 'Disponível'),
        ('reservado', 'Reservado'),
        ('expirado', 'Expirado'),
    ]
    
    UNIDADE_CHOICES = [
        ('unidade', 'Unidade'),
        ('kg', 'Quilograma'),
        ('g', 'Grama'),
        ('l', 'Litro'),
        ('ml', 'Mililitro'),
        ('pacote', 'Pacote'),
        ('caixa', 'Caixa'),
    ]
    
    estabelecimento = models.ForeignKey(
        get_user_model(), 
        on_delete=models.CASCADE,
        related_name='ofertas'
    )
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    quantidade = models.DecimalField(max_digits=10, decimal_places=2)
    unidade = models.CharField(max_length=20, choices=UNIDADE_CHOICES, default='unidade')
    data_expiracao = models.DateTimeField()
    foto = models.ImageField(upload_to='ofertas/', blank=True, null=True)
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='disponivel'
    )
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-data_criacao']
        verbose_name = 'Oferta'
        verbose_name_plural = 'Ofertas'
    
    def __str__(self):
        return f"{self.titulo} - {self.estabelecimento}"
    
    def verificar_expiracao(self):
        """Verifica se a oferta expirou e atualiza o status automaticamente"""
        if timezone.now() > self.data_expiracao and self.status != 'expirado':
            self.status = 'expirado'
            self.save()
            return True
        return False
    
    def save(self, *args, **kwargs):
        """Override do save para verificar expiração automaticamente"""
        # Verifica se é uma nova instância ou se a data de expiração foi alterada
        if self.pk:
            try:
                original = Oferta.objects.get(pk=self.pk)
                if original.data_expiracao != self.data_expiracao:
                    self.verificar_expiracao()
            except Oferta.DoesNotExist:
                pass
        else:
            # Para novas instâncias, verifica se já está expirada
            if timezone.now() > self.data_expiracao:
                self.status = 'expirado'
        
        super().save(*args, **kwargs)