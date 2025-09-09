"""
Operações de FAQs em memória (cada FAQ contém pergunta, resposta, etc).
"""

import os

from .crud_memoria import (
    adicionar_faq_memoria,
    atualizar_faq_memoria,
    buscar_faq_memoria,
    listar_faqs_memoria,
    remover_faq_memoria,
)


class MenuMemoria:
    def __init__(self, faqs_memoria=None):
        self.faqs_memoria = faqs_memoria if faqs_memoria is not None else []
        pasta_memoria = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'memoria')
        )
        os.makedirs(pasta_memoria, exist_ok=True)
        self.caminho_json = os.path.join(pasta_memoria, 'faq_export.json')

    def listar_faqs_memoria(self):
        listar_faqs_memoria(self.faqs_memoria)

    def adicionar_faq_memoria(self):
        adicionar_faq_memoria(self.faqs_memoria)

    def atualizar_faq_memoria(self):
        atualizar_faq_memoria(self.faqs_memoria)

    def remover_faq_memoria(self):
        remover_faq_memoria(self.faqs_memoria)

    def buscar_faq_memoria(self):
        buscar_faq_memoria(self.faqs_memoria)
