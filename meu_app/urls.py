
from django.urls import path
from meu_app import views


urlpatterns = [

    path('', views.home, name='home'),
    path('carteira/', views.carteira, name='carteira'),
    path('transacoes/', views.transacoes_lista, name='transacoes_lista'),
    path('transacoes/nova/', views.transacao_nova, name='transacao_nova'),
    path('transacoes/<int:id>/excluir/',
         views.transacao_excluir, name='transacao_excluir'),


]
