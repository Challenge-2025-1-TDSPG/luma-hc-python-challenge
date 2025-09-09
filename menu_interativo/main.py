"""
Arquivo principal para execução do sistema FAQ.
"""

import os

from colorama import Fore, Style, init
from dotenv import load_dotenv
from faq import FaqDB, Menu

# Inicializa o colorama (necessário para Windows)
init(autoreset=True)

if __name__ == '__main__':
    load_dotenv()
    oracle_config = {
        'user': os.environ.get('DB_USER'),
        'password': os.environ.get('DB_PASS'),
        'dsn': os.environ.get('DB_URL'),
    }

    try:
        # Usando o protocolo de contexto para testar a conexão
        with FaqDB(oracle_config) as test_db:
            print(
                f'{Fore.BLUE}[INFO] Conexão com banco Oracle estabelecida com sucesso.{Style.RESET_ALL}'
            )
    except Exception as e:
        print(
            f'\n{Fore.RED}[ERRO] Não foi possível conectar ao banco Oracle. Verifique as credenciais e o DSN.{Style.RESET_ALL}'
        )
        print(f'{Fore.YELLOW}Detalhes: {e}{Style.RESET_ALL}')
        exit(1)

    menu = Menu(oracle_config)
    menu.exibir_menu()
