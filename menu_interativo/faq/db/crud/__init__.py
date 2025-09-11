"""
Importações e exports para o pacote CRUD.
"""

from .create import adicionar
from .delete import deletar
from .read import buscar_por_id, listar, listar_categorias
from .update import atualizar

__all__ = [
    'adicionar',
    'listar',
    'buscar_por_id',
    'listar_categorias',
    'atualizar',
    'deletar',
]
