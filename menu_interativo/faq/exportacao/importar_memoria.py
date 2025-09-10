"""
Módulo para importação de FAQs a partir de arquivos JSON para memória.
Permite carregar dados previamente exportados de volta para o sistema.
"""

import json
import os

from colorama import Fore, Style


def importar_faqs_memoria():
    """Importa FAQs de um arquivo JSON para a memória.

    Esta função carrega os dados de FAQs a partir de um arquivo JSON localizado
    no diretório data/memoria do projeto e os converte em uma lista de dicionários
    para uso no sistema.

    Returns:
        list: Lista de dicionários com os FAQs importados, ou lista vazia se
              o arquivo não existir ou ocorrer algum erro na importação.
    """
    try:
        # Determina o caminho para o diretório onde está o arquivo JSON
        pasta_memoria = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'memoria')
        )
        # Define o caminho completo para o arquivo JSON
        caminho_json = os.path.join(pasta_memoria, 'faq_export.json')

        # Verifica se o arquivo existe
        if os.path.exists(caminho_json):
            # Abre o arquivo para leitura com codificação UTF-8
            with open(caminho_json, 'r', encoding='utf-8') as f:
                # Carrega os dados do JSON
                faqs = json.load(f)
                # Verifica se o conteúdo é uma lista (formato esperado)
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
