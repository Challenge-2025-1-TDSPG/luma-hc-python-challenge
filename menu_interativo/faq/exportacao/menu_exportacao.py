"""
Operações de exportação do FAQ.
"""

import json
import os


class MenuExportacao:
    def __init__(self, db):
        self.db = db

    def exportar_json(self):
        perguntas = self.db.listar()
        lista_dict = [vars(p) for p in perguntas]
        try:
            pasta_banco = os.path.abspath(
                os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'banco')
            )
            os.makedirs(pasta_banco, exist_ok=True)
            caminho = os.path.join(pasta_banco, 'faq_export.json')
            with open(caminho, 'w', encoding='utf-8') as f:
                json.dump(lista_dict, f, ensure_ascii=False, indent=4)
            print(f'Exportação realizada com sucesso para {caminho}!')
        except Exception as e:
            print(f'Erro ao exportar para JSON: {e}')
