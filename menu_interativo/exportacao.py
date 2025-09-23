"""
Módulo consolidado de exportação/importação de FAQs para o sistema FAQ.
Inclui funções para exportar FAQs do banco e da memória para JSON, importar da memória e o menu de exportação.
"""


# --- Menu de exportação ---
class MenuExportacao:
    def __init__(self, db):
        self.db = db

    def exportar_json(self):
        pass
