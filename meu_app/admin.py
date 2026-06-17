
from django.contrib import admin
from .models import Produto, Categoria, Tarefa, ClasseAtivo, Corretora, Ativo, Transacao

# Registrando os modelos originais
admin.site.register(Produto)
admin.site.register(Tarefa)
admin.site.register(Categoria)

# Registrando os novos modelos de Investimentos
admin.site.register(ClasseAtivo)
admin.site.register(Corretora)
admin.site.register(Ativo)
admin.site.register(Transacao)