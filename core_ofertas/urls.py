from django.urls import path
from . import views

#app_name = 'core_ofertas'

urlpatterns = [
    path('', views.index, name='index'),  # Página inicial
    path('minhas-ofertas/', views.minhas_ofertas, name='minhas_ofertas'),
    path('criar-oferta/', views.criar_oferta, name='criar_oferta'),
    path('editar-oferta/<int:pk>/', views.editar_oferta, name='editar_oferta'),
    path('excluir-oferta/<int:pk>/', views.excluir_oferta, name='excluir_oferta'),
]