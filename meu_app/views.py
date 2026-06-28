from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from decimal import Decimal
from .models import Ativo, Transacao, Corretora

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
# ==========================================
# ISSUE #8: Consolidação de Saldo e Preço Médio
# ==========================================
def carteira(request):
    ativos = Ativo.objects.all()
    ativos_da_carteira = []
    
    # Captura o que o usuário digitou na barra de busca (RF07)
    ticker_busca = request.GET.get('ticker', '').upper()

    for ativo in ativos:
        # Se houver uma busca e o ticker não bater, pula para o próximo
        if ticker_busca and ticker_busca not in ativo.ticker.upper():
            continue

        transacoes = ativo.transacoes.all().order_by('data_transacao')
        
        qtd_atual = Decimal('0.0')
        preco_medio = Decimal('0.0')
        
        # Algoritmo de Preço Médio e Saldo
        for t in transacoes:
            if t.tipo == 'C':  # Compra
                # Calcula o valor total do que eu já tinha + o que estou comprando agora
                valor_patrimonio_atual = qtd_atual * preco_medio
                valor_nova_compra = t.quantidade * t.preco_unitario
                
                qtd_atual += t.quantidade
                
                # Novo Preço Médio (Média Ponderada)
                if qtd_atual > 0:
                    preco_medio = (valor_patrimonio_atual + valor_nova_compra) / qtd_atual
                    
            elif t.tipo == 'V':  # Venda
                # Venda reduz a quantidade, mas NÃO altera o preço médio
                qtd_atual -= t.quantidade

        # Filtrar apenas ativos com saldo maior que zero
        if qtd_atual > 0:
            ativos_da_carteira.append({
                'ticker': ativo.ticker,
                'classe': ativo.classe.nome if ativo.classe else '-',
                'quantidade_total': round(qtd_atual, 4),
                'preco_medio': round(preco_medio, 2),
                'patrimonio': round(qtd_atual * preco_medio, 2)
            })

    # ATUALIZADO: Caminho apontando para a pasta meu_app
    return render(request, 'meu_app/carteira.html', {'ativos_da_carteira': ativos_da_carteira})

# ==========================================
# ISSUE #9: Inserção com Trava de Segurança
# ==========================================
def transacao_nova(request):
    if request.method == 'POST':
        # Pega os dados enviados pelo formulário HTML
        ativo_id = request.POST.get('ativo')
        corretora_id = request.POST.get('corretora')
        tipo = request.POST.get('tipo')
        quantidade = Decimal(request.POST.get('quantidade').replace(',', '.'))
        preco = Decimal(request.POST.get('preco_unitario').replace(',', '.'))
        data = request.POST.get('data_transacao')

        ativo = get_object_or_404(Ativo, id=ativo_id)
        
        # Validação - Impede Venda a Descoberto
        if tipo == 'V':
            # Calcula o saldo atual
            qtd_atual = sum(t.quantidade if t.tipo == 'C' else -t.quantidade for t in ativo.transacoes.all())
            
            if quantidade > qtd_atual:
                # Dispara a mensagem de erro e aborta o salvamento
                messages.error(request, f'Erro: Você não tem saldo suficiente de {ativo.ticker}. Saldo atual: {qtd_atual}')
                return redirect('transacao_nova')

        # Se passou na validação, salva no banco
        Transacao.objects.create(
            ativo_id=ativo_id,
            corretora_id=corretora_id,
            tipo=tipo,
            quantidade=quantidade,
            preco_unitario=preco,
            data_transacao=data
        )
        
        messages.success(request, 'Transação registrada com sucesso!')
        # Após salvar, manda o usuário de volta para a carteira
        return redirect('carteira') 

    # Se for um GET carrega o formulário vazio
    ativos = Ativo.objects.all()
    corretoras = Corretora.objects.all()
    
    # ATUALIZADO: Caminho apontando para a pasta meu_app
    return render(request, 'meu_app/criar_transacao.html', {'ativos': ativos, 'corretoras': corretoras})

# ==========================================
# ISSUE #11: Extrato de Transações (Histórico)
# ==========================================
def transacoes_lista(request):
    # Busca todas do banco, ordenando da mais nova para a mais antiga (sinal de menos no data_transacao)
    transacoes = Transacao.objects.all().order_by('-data_transacao')
    
    # ATUALIZADO: Caminho apontando para a pasta meu_app
    return render(request, 'meu_app/historico_transacoes.html', {'transacoes': transacoes})

# ==========================================
# Funções Auxiliares (Home e Excluir)
# ==========================================
def home(request):
    # ATUALIZADO: Caminho apontando para a pasta meu_app
    return render(request, 'meu_app/home.html')

def transacao_excluir(request, id):
    # Função placeholder para não dar erro na URL antes de implementarmos a exclusão
    pass


# meu_app/views.py
from django.shortcuts import redirect
from django.utils import timezone
from .models import Ativo
from .services import buscar_preco_atual

def sincronizar_cotacoes(request):
    ativos = Ativo.objects.all()
    
    for ativo in ativos:
        novo_preco = buscar_preco_atual(ativo.ticker)
        if novo_preco:
            ativo.preco_atual = novo_preco
            ativo.data_ultima_atualizacao = timezone.now()
            ativo.save()
            
    return redirect('nome_da_sua_view_da_carteira')




# Exemplo de trecho dentro da sua view principal da carteira
def ver_carteira(request):
    ativos = Ativo.objects.all()
    dados_carteira = []
    
    for ativo in ativos:
        # Evita quebras se a API ainda não tiver rodado nenhuma vez
        preco_atual = ativo.preco_atual if ativo.preco_atual else ativo.preco_medio
        
        patrimonio_atual = ativo.quantidade * preco_atual
        patrimonio_compra = ativo.quantidade * ativo.preco_medio
        
        # Cálculo da Rentabilidade % = ((Preço Atual - Preço Médio) / Preço Médio) * 100
        if ativo.preco_medio > 0:
            rentabilidade = ((preco_atual - ativo.preco_medio) / ativo.preco_medio) * 100
        else:
            rentabilidade = 0

        dados_carteira.append({
            'ativo': ativo,
            'patrimonio_atual': patrimonio_atual,
            'rentabilidade': rentabilidade,
        })
        
    return render(request, 'carteira.html', {'dados_carteira': dados_carteira})