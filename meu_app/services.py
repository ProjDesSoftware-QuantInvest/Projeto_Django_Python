# meu_app/services.py
import yfinance as yf
from decimal import Decimal

def buscar_preco_atual(ticker: str) -> Decimal:
    """
    Busca a cotação atual de um ativo via Yahoo Finance.
    Se o ticker não terminar com .SA (comum na B3), o sufixo é adicionado.
    """
    try:
        # Garante o formato correto para a B3 se for o caso
        ticker_formatado = ticker if ticker.endswith('.SA') else f"{ticker}.SA"
        
        ticker_yf = yf.Ticker(ticker_formatado)
        
        # Obtém o preço de fechamento mais recente ou o preço atual
        # 'fast_info' é mais rápido que chamar 'info'
        preco = ticker_yf.fast_info['last_price']
        
        if preco:
            return Decimal(str(round(preco, 2)))
        return Decimal('0.00')
        
    except Exception as e:
        # Em produção, substitua por um logger adequado
        print(f"Erro ao buscar cotação para {ticker}: {e}")
        return None

