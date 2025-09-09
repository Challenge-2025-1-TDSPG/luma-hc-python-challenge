"""
Importação de FAQs em memória a partir de JSON.
"""
import json
import os

def importar_faqs_memoria():
    try:
        pasta_memoria = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'memoria')
        )
        caminho_json = os.path.join(pasta_memoria, 'faq_export.json')
        if os.path.exists(caminho_json):
            with open(caminho_json, 'r', encoding='utf-8') as f:
                faqs = json.load(f)
                if isinstance(faqs, list):
                    print('FAQs importados do JSON!')
                    return faqs
        print('Nenhum arquivo JSON encontrado para importar.')
        return []
    except Exception as e:
        print(f'Erro ao importar FAQs do JSON: {e}')
        return []
