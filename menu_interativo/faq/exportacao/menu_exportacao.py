"""
Operações de exportação do FAQ.
"""

from .exportar_banco import exportar_faqs_banco


class MenuExportacao:
    def __init__(self, db):
        self.db = db

    def exportar_json(self):
        perguntas = self.db.listar()
        lista_dict = [vars(p) for p in perguntas]
        exportar_faqs_banco(lista_dict)
