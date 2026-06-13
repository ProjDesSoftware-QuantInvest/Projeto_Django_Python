
# Register your models here.

from django.contrib import admin
from .models import Produto 
from .models import Tarefa, Categoria
# Importe seu Model

# Registre seu Model aqui
admin.site.register(Produto)
admin.site.register(Tarefa)
admin.site.register(Categoria)

