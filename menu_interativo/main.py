"""
Arquivo principal para execução do sistema FAQ.
"""

import os

from dotenv import load_dotenv
from faq import FaqDB, Menu

if __name__ == '__main__':
    load_dotenv()
    oracle_config = {
        'user': os.environ.get('DB_USER'),
        'password': os.environ.get('DB_PASS'),
        'dsn': os.environ.get('DB_URL'),
    }

    try:
        test_db = FaqDB(oracle_config)
        test_db.close()
    except Exception as e:
        print(
            '\n[ERRO] Não foi possível conectar ao banco Oracle. Verifique as credenciais e o DSN.'
        )
        print(f'Detalhes: {e}')
        exit(1)

    menu = Menu(oracle_config)
    menu.exibir_menu()
