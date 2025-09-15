"""
Módulo consolidado de exportação/importação de FAQs para o sistema FAQ.
Inclui funções para exportar FAQs do banco e da memória para JSON, importar da memória e o menu de exportação.
"""

import json
import os

from colorama import Fore, Style


# --- Exportação do banco para JSON ---
def exportar_faqs_banco(lista_dict):
    try:
        pasta_banco = os.path.abspath(
            os.path.join(os.path.dirname(__file__), 'json', 'banco')
        )
        os.makedirs(pasta_banco, exist_ok=True)
        caminho = os.path.join(pasta_banco, 'faq_export.json')
        with open(caminho, 'w', encoding='utf-8') as f:
            json.dump(lista_dict, f, ensure_ascii=False, indent=4)
        print(
            f'{Fore.GREEN}Exportação realizada com sucesso para {caminho}!{Style.RESET_ALL}'
        )
    except Exception as e:
        print(f'{Fore.RED}Erro ao exportar para JSON: {e}{Style.RESET_ALL}')


# --- Exportação da memória para JSON ---
def exportar_faqs_memoria(faqs_memoria):
    try:
        pasta_memoria = os.path.abspath(
            os.path.join(os.path.dirname(__file__), 'json', 'memoria')
        )
        os.makedirs(pasta_memoria, exist_ok=True)
        caminho_json = os.path.join(pasta_memoria, 'faq_export.json')
        with open(caminho_json, 'w', encoding='utf-8') as f:
            json.dump(faqs_memoria, f, ensure_ascii=False, indent=4)
        print(
            f'{Fore.GREEN}Exportação realizada com sucesso para {caminho_json}!{Style.RESET_ALL}'
        )
    except Exception as e:
        print(f'{Fore.RED}Erro ao exportar FAQs para JSON: {e}{Style.RESET_ALL}')


# --- Importação da memória a partir de JSON ---
def importar_faqs_memoria():
    try:
        pasta_memoria = os.path.abspath(
            os.path.join(os.path.dirname(__file__), 'json', 'memoria')
        )
        caminho_json = os.path.join(pasta_memoria, 'faq_export.json')
        if os.path.exists(caminho_json):
            with open(caminho_json, 'r', encoding='utf-8') as f:
                faqs = json.load(f)
                if isinstance(faqs, list):
                    print(
                        f'{Fore.GREEN}FAQs importados do JSON com sucesso!{Style.RESET_ALL}'
                    )
                    return faqs
        print(
            f'{Fore.YELLOW}Nenhum arquivo JSON válido encontrado para importar.{Style.RESET_ALL}'
        )
        return []
    except Exception as e:
        print(f'{Fore.RED}Erro ao importar FAQs do JSON: {e}{Style.RESET_ALL}')
        return []


# --- Menu de exportação ---
class MenuExportacao:
    def __init__(self, db):
        self.db = db

    def exportar_json(self):
        perguntas = self.db.listar()
        lista_dict = [vars(p) for p in perguntas]
        exportar_faqs_banco(lista_dict)
