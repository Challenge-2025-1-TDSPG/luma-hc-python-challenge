"""
Módulo para exportação de FAQs do banco de dados para arquivo JSON.
Permite persistir os dados do banco em um arquivo para backup ou transferência.
"""

import json
import os

from colorama import Fore, Style


def exportar_faqs_banco(lista_dict):
    """Exporta uma lista de FAQs para um arquivo JSON.

    Esta função recebe uma lista de dicionários representando FAQs e os salva
    em um arquivo JSON formatado no diretório data/banco do projeto.

    Args:
        lista_dict (list): Lista de dicionários contendo os dados dos FAQs
                          Cada dicionário deve ter as chaves correspondentes
                          aos atributos de um FAQ (id, pergunta, resposta, etc.)
    """
    try:
        # Determina o caminho para o diretório de exportação
        pasta_banco = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'banco')
        )
        # Cria o diretório se não existir
        os.makedirs(pasta_banco, exist_ok=True)
        # Define o caminho completo para o arquivo JSON
        caminho = os.path.join(pasta_banco, 'faq_export.json')
        # Abre o arquivo para escrita com codificação UTF-8 para suporte a caracteres especiais
        with open(caminho, 'w', encoding='utf-8') as f:
            # Salva os dados em formato JSON com indentação para melhor legibilidade
            # ensure_ascii=False permite caracteres não-ASCII no arquivo
            json.dump(lista_dict, f, ensure_ascii=False, indent=4)

        # Informa ao usuário que a exportação foi bem-sucedida
        print(
            f'{Fore.GREEN}Exportação realizada com sucesso para {caminho}!{Style.RESET_ALL}'
        )
    except Exception as e:
        # Exibe mensagem de erro detalhada em caso de falha
        print(f'{Fore.RED}Erro ao exportar para JSON: {e}{Style.RESET_ALL}')
