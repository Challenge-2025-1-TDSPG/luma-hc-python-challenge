"""
Módulo para exportação de FAQs em memória para arquivo JSON.
Permite persistir os dados que estão em memória em um arquivo para uso posterior.
"""

import json
import os

from colorama import Fore, Style


def exportar_faqs_memoria(faqs_memoria):
    """Exporta os FAQs em memória para um arquivo JSON.

    Esta função recebe uma lista de dicionários representando FAQs que estão
    armazenados em memória e os salva em um arquivo JSON formatado no diretório
    data/memoria do projeto.

    Args:
        faqs_memoria (list): Lista de dicionários com os FAQs em memória
                            Cada dicionário deve conter as chaves 'id', 'pergunta',
                            'resposta', 'ativo', 'atualizado_em' e 'categoria'
    """
    try:
        # Determina o caminho para o diretório de exportação da memória
        pasta_memoria = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'memoria')
        )
        # Cria o diretório se não existir
        os.makedirs(pasta_memoria, exist_ok=True)
        # Define o caminho completo para o arquivo JSON
        caminho_json = os.path.join(pasta_memoria, 'faq_export.json')
        # Abre o arquivo para escrita com codificação UTF-8
        with open(caminho_json, 'w', encoding='utf-8') as f:
            # Salva os dados em formato JSON com indentação
            json.dump(faqs_memoria, f, ensure_ascii=False, indent=4)

        # Informa ao usuário que a exportação foi bem-sucedida
        print(
            f'{Fore.GREEN}Exportação realizada com sucesso para {caminho_json}!{Style.RESET_ALL}'
        )
    except Exception as e:
        # Exibe mensagem de erro detalhada em caso de falha
        print(f'{Fore.RED}Erro ao exportar FAQs para JSON: {e}{Style.RESET_ALL}')
