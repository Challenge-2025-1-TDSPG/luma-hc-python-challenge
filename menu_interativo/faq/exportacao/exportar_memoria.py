"""
Exportação de FAQs em memória para JSON.
"""

import json
import os


def exportar_faqs_memoria(faqs_memoria):
    try:
        pasta_memoria = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'memoria')
        )
        os.makedirs(pasta_memoria, exist_ok=True)
        caminho_json = os.path.join(pasta_memoria, 'faq_export.json')
        with open(caminho_json, 'w', encoding='utf-8') as f:
            json.dump(faqs_memoria, f, ensure_ascii=False, indent=4)
        print(f'Exportação realizada com sucesso para {caminho_json}!')
    except Exception as e:
        print(f'Erro ao exportar FAQs para JSON: {e}')
