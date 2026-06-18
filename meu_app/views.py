from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from decimal import Decimal
from .models import Ativo, Transacao, Corretora

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