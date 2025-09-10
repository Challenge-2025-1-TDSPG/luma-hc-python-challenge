"""
Arquivo principal para execução do sistema FAQ.
Este script inicializa a conexão com o banco de dados Oracle,
verifica sua disponibilidade e inicia o menu interativo do sistema.

Utiliza variáveis de ambiente para configuração do banco de dados,
que devem estar definidas em um arquivo .env na raiz do projeto.
"""

import os

from colorama import Fore, Style, init
from dotenv import load_dotenv
from faq import FaqDB, Menu

# Inicializa o colorama para formatação colorida no terminal (necessário para Windows)
init(autoreset=True)

if __name__ == '__main__':
    # Carrega as variáveis de ambiente do arquivo .env
    load_dotenv()

    # Configura os parâmetros de conexão com o banco Oracle a partir das variáveis de ambiente
    oracle_config = {
        'user': os.environ.get('DB_USER'),
        'password': os.environ.get('DB_PASS'),
        'dsn': os.environ.get('DB_URL'),
    }

    try:
        # Testa a conexão com o banco de dados utilizando o gerenciador de contexto
        # O bloco with garante que a conexão será fechada corretamente após o teste
        with FaqDB(oracle_config) as test_db:
            print(
                f'{Fore.BLUE}[INFO] Conexão com banco Oracle estabelecida com sucesso.{Style.RESET_ALL}'
            )
    except Exception as e:
        # Em caso de falha na conexão, exibe mensagem de erro detalhada e encerra o programa
        print(
            f'\n{Fore.RED}[ERRO] Não foi possível conectar ao banco Oracle. Verifique as credenciais e o DSN.{Style.RESET_ALL}'
        )
        print(f'{Fore.YELLOW}Detalhes: {e}{Style.RESET_ALL}')
        exit(1)

    # Inicializa o menu principal passando a configuração do banco de dados
    menu = Menu(oracle_config)
    # Exibe o menu interativo e inicia o fluxo do programa
    menu.exibir_menu()
