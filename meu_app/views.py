

# Create your views here.



from django.shortcuts import render, redirect, get_object_or_404

from .models import Tarefa, Categoria
from datetime import datetime

def home(request):
    return render(request, 'meu_app/home.html', {'hoje': datetime.today()})





def listar_tarefas(request):
    tarefas = Tarefa.objects.all().order_by('-data_criacao')
    busca = request.GET.get('busca')
    status = request.GET.get('status')
    ordem = request.GET.get('ordem')

    if busca:
        tarefas = tarefas.filter(titulo__icontains=busca)

    if status == 'pendentes':
        tarefas = tarefas.filter(concluida=False)
    elif status == 'concluidas':
        tarefas = tarefas.filter(concluida=True)

    if ordem == 'antigas':
        tarefas = tarefas.order_by('data_criacao')
    elif ordem == 'titulo_az':
        tarefas = tarefas.order_by('titulo')
    elif ordem == 'titulo_za':
        tarefas = tarefas.order_by('-titulo')
    else:
        tarefas = tarefas.order_by('-data_criacao')
    return render(
        request,
        'meu_app/listar_tarefas.html',
        {'tarefas': tarefas}
    )


def criar_tarefa(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descricao = request.POST.get('descricao')
        concluida = request.POST.get('concluida') == 'on'

        categoria_id = request.POST.get('categoria')

        categoria = None

        if categoria_id:
            categoria = get_object_or_404(Categoria, id=categoria_id)

        Tarefa.objects.create(
            titulo=titulo,
            descricao=descricao,
            concluida=concluida,
            categoria=categoria
        )

        return redirect('listar_tarefas')

    return render(
        request,
        'meu_app/criar_tarefa.html',
        {'categorias': categoria}
    )


def detalhe_tarefa(request, id):
    tarefa = get_object_or_404(Tarefa, id=id)

    return render(
        request,
        'meu_app/detalhe_tarefa.html',
        {'tarefa': tarefa}
    )



def editar_tarefa(request, id):
    tarefa = get_object_or_404(Tarefa, id=id)

    if request.method == 'POST':
        tarefa.titulo = request.POST.get('titulo')
        tarefa.descricao = request.POST.get('descricao')
        tarefa.concluida = request.POST.get('concluida') == 'on'
        tarefa.save()

        return redirect('listar_tarefas')

    return render(
        request,
        'meu_app/editar_tarefa.html',
        {'tarefa': tarefa}
    )



def excluir_tarefa(request, id):
    tarefa = get_object_or_404(Tarefa, id=id)

    if request.method == 'POST':
        tarefa.delete()
        return redirect('listar_tarefas')

    return render(
        request,
        'meu_app/confirmar_exclusao.html',
        {'tarefa': tarefa}
    )

def concluir_tarefa(request, id):
    tarefa = get_object_or_404(Tarefa, id=id)
    tarefa.concluida = True
    tarefa.save()

    return redirect('listar_tarefas')

