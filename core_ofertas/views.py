from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Oferta
from .forms import OfertaForm

def index(request):
    """Página inicial - redireciona para minhas ofertas se logado, ou para admin"""
    if request.user.is_authenticated:
        return redirect('core_ofertas:minhas_ofertas')
    else:
        return redirect('admin:login')


@login_required
def minhas_ofertas(request):
    """Lista todas as ofertas do estabelecimento logado"""
    ofertas = Oferta.objects.filter(estabelecimento=request.user).order_by('-data_criacao')
    return render(request, 'core_ofertas/minhas_ofertas.html', {'ofertas': ofertas})

@login_required
def criar_oferta(request):
    """Cria uma nova oferta"""
    if request.method == 'POST':
        form = OfertaForm(request.POST, request.FILES)
        if form.is_valid():
            oferta = form.save(commit=False)
            oferta.estabelecimento = request.user
            oferta.save()
            messages.success(request, 'Oferta criada com sucesso!')
            return redirect('minhas_ofertas')
    else:
        form = OfertaForm()
    
    return render(request, 'core_ofertas/form_oferta.html', {
        'form': form,
        'titulo': 'Nova Oferta'
    })

@login_required
def editar_oferta(request, pk):
    """Edita uma oferta existente"""
    oferta = get_object_or_404(Oferta, pk=pk)
    
    # Verifica se o usuário é o dono da oferta
    if oferta.estabelecimento != request.user:
        messages.error(request, 'Você não tem permissão para editar esta oferta.')
        return redirect('minhas_ofertas')
    
    if request.method == 'POST':
        form = OfertaForm(request.POST, request.FILES, instance=oferta)
        if form.is_valid():
            form.save()
            messages.success(request, 'Oferta atualizada com sucesso!')
            return redirect('minhas_ofertas')
    else:
        form = OfertaForm(instance=oferta)
    
    return render(request, 'core_ofertas/form_oferta.html', {
        'form': form,
        'titulo': 'Editar Oferta',
        'oferta': oferta
    })

@login_required
def excluir_oferta(request, pk):
    """Exclui uma oferta"""
    oferta = get_object_or_404(Oferta, pk=pk)
    
    # Verifica se o usuário é o dono da oferta
    if oferta.estabelecimento != request.user:
        messages.error(request, 'Você não tem permissão para excluir esta oferta.')
        return redirect('minhas_ofertas')
    
    if request.method == 'POST':
        oferta.delete()
        messages.success(request, 'Oferta excluída com sucesso!')
        return redirect('minhas_ofertas')
    
    return render(request, 'core_ofertas/confirmar_exclusao.html', {'oferta': oferta})

def index(request):
    """Página inicial - redireciona para minhas ofertas se logado, ou para admin"""
    if request.user.is_authenticated:
        return redirect('minhas_ofertas')
    else:
        return redirect('admin:login')