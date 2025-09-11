"""
Módulo de acesso ao banco de dados FAQ.
Esta é uma camada de compatibilidade que usa a implementação modular.
"""

# Reexportando a classe FaqDB da implementação modular
from .db.facade import FaqDB

__all__ = ['FaqDB']
