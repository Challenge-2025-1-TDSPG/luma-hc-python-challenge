"""
Exportação de FAQs do banco para JSON.
"""

import json
import os

from colorama import Fore, Style


def exportar_faqs_banco(lista_dict):
    try:
        pasta_banco = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'banco')
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
