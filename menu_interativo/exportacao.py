"""
Módulo consolidado de exportação/importação de FAQs para o sistema FAQ.
Inclui funções para exportar FAQs do banco e da memória para JSON, importar da memória e o menu de exportação.
"""

import json
import os

from config.settings import JSON_BANCO_PATH, JSON_MEMORIA_PATH, show_message


# --- Exportação do banco para JSON ---
def exportar_faqs_banco(lista_dict):
    try:
        os.makedirs(os.path.dirname(JSON_BANCO_PATH), exist_ok=True)
        with open(JSON_BANCO_PATH, 'w', encoding='utf-8') as f:
            json.dump(lista_dict, f, ensure_ascii=False, indent=4)
        show_message(
            f'Exportação realizada com sucesso para {JSON_BANCO_PATH}!', 'success'
        )
    except Exception as e:
        show_message(f'Erro ao exportar para JSON: {e}', 'error')


# --- Exportação da memória para JSON ---
def exportar_faqs_memoria(faqs_memoria):
    try:
        os.makedirs(os.path.dirname(JSON_MEMORIA_PATH), exist_ok=True)
        with open(JSON_MEMORIA_PATH, 'w', encoding='utf-8') as f:
            json.dump(faqs_memoria, f, ensure_ascii=False, indent=4)
        show_message(
            f'Exportação realizada com sucesso para {JSON_MEMORIA_PATH}!', 'success'
        )
    except Exception as e:
        show_message(f'Erro ao exportar FAQs para JSON: {e}', 'error')


# --- Importação da memória a partir de JSON ---
def importar_faqs_memoria():
    try:
        if os.path.exists(JSON_MEMORIA_PATH):
            with open(JSON_MEMORIA_PATH, 'r', encoding='utf-8') as f:
                faqs = json.load(f)
                if isinstance(faqs, list):
                    show_message('FAQs importados do JSON com sucesso!', 'success')
                    return faqs
        show_message('Nenhum arquivo JSON válido encontrado para importar.', 'warning')
        return []
    except Exception as e:
        show_message(f'Erro ao importar FAQs do JSON: {e}', 'error')
        return []


# --- Menu de exportação ---
class MenuExportacao:
    def __init__(self, db):
        self.db = db

    def exportar_json(self):
        perguntas = self.db.listar()
        lista_dict = [vars(p) for p in perguntas]
        exportar_faqs_banco(lista_dict)
