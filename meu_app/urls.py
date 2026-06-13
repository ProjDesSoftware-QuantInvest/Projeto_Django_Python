
from django.urls import path
from meu_app import views



urlpatterns = [
    
    path('', views.home),
    path('tarefas/', views.listar_tarefas, name='listar_tarefas'),
    path('tarefas/criar/', views.criar_tarefa,name='criar_tarefa'),
    path('tarefas/<int:id>/', views.detalhe_tarefa, name='detalhe_tarefa'),
    path('tarefas/<int:id>/editar/', views.editar_tarefa,name='editar_tarefa'),
    path('tarefas/<int:id>/excluir/', views.excluir_tarefa,name='excluir_tarefa'),
    path('tarefas/<int:id>/concluir/',views.concluir_tarefa,name='concluir_tarefa'),


]