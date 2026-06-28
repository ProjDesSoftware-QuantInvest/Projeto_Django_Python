
from django.urls import path
from meu_app import views


urlpatterns = [

    path('', views.home, name='home'),
    path('carteira/', views.carteira, name='carteira'),
    path('transacoes/', views.transacoes_lista, name='transacoes_lista'),
    path('transacoes/nova/', views.transacao_nova, name='transacao_nova'),
    path('transacoes/<int:id>/excluir/', views.transacao_excluir, name='transacao_excluir'),
    path('tarefas/', views.listar_tarefas, name='listar_tarefas'),
    path('tarefas/criar/', views.criar_tarefa,name='criar_tarefa'),
    path('tarefas/<int:id>/', views.detalhe_tarefa, name='detalhe_tarefa'),
    path('tarefas/<int:id>/editar/', views.editar_tarefa,name='editar_tarefa'),
    path('tarefas/<int:id>/excluir/', views.excluir_tarefa,name='excluir_tarefa'),
    path('tarefas/<int:id>/concluir/',views.concluir_tarefa,name='concluir_tarefa'),
    path('carteira/atualizar/', views.sincronizar_cotacoes, name='sincronizar_cotacoes'),

]
