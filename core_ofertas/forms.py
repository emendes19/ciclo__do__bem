from django import forms
from .models import Oferta
from django.utils import timezone

class OfertaForm(forms.ModelForm):
    class Meta:
        model = Oferta
        fields = ['titulo', 'descricao', 'quantidade', 'unidade', 'data_expiracao', 'foto']
        widgets = {
            'data_expiracao': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'descricao': forms.Textarea(attrs={'rows': 4}),
        }
    
    def clean_data_expiracao(self):
        data_expiracao = self.cleaned_data.get('data_expiracao')
        if data_expiracao and data_expiracao <= timezone.now():
            raise forms.ValidationError("A data de expiração deve ser futura.")
        return data_expiracao