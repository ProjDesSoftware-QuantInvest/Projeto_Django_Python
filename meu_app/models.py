from django.db import models

# ==============================================================================
# Modelos Antigos (Mantidos do seu código original)
# ==============================================================================


class Produto(models.Model):
    nome = models.CharField(max_length=200)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    estoque = models.IntegerField(default=0)
    data_criacao = models.DateTimeField(auto_now_add=True)

    # isso faz com que um objeto Produto seja exibido pelo valor do campo nome.
    # Sem esse método, o Django mostraria algo pouco útil, como: Produto object (1). com o __str__ ele retorna algo como Notebook
    def __str__(self):
        return self.nome


class Categoria(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome


class Tarefa(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    concluida = models.BooleanField(default=False)
    data_criacao = models.DateTimeField(auto_now_add=True)
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.titulo


# ==============================================================================
# Novos Modelos (Novas Ações Solicitadas)
# ==============================================================================

class ClasseAtivo(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class Corretora(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class Ativo(models.Model):
    ticker = models.CharField(max_length=10, unique=True)
    # Relacionamento Foreign Key com ClasseAtivo
    classe = models.ForeignKey(
        ClasseAtivo,
        on_delete=models.PROTECT,
        related_name='ativos'
    )

    def __str__(self):
        return self.ticker


class Transacao(models.Model):
    # Opções para limitar o campo 'tipo' no banco e no painel do Django
    TIPO_CHOICES = [
        ('C', 'Compra'),
        ('V', 'Venda'),
    ]

    # Relacionamentos Foreign Key com Ativo e Corretora
    ativo = models.ForeignKey(
        Ativo,
        on_delete=models.CASCADE,
        related_name='transacoes'
    )
    corretora = models.ForeignKey(
        Corretora,
        on_delete=models.CASCADE,
        related_name='transacoes'
    )

    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES)

    # Quantidade configurada para aceitar até 4 casas decimais (ex: criptoativos ou frações)
    quantidade = models.DecimalField(max_digits=18, decimal_places=4)

    # Preço unitário configurado para aceitar 2 casas decimais
    preco_unitario = models.DecimalField(max_digits=12, decimal_places=2)

    data_transacao = models.DateTimeField()

    def __str__(self):
        # Exibe uma string limpa identificando a transação, ex: "Compra de WEGE3 - 10.0000 un"
        tipo_extenso = "Compra" if self.tipo == 'C' else "Venda"
        return f"{tipo_extenso} de {self.ativo.ticker} - {self.quantidade} un"
