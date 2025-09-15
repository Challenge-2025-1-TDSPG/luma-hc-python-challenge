"""
Arquivo principal para execução do sistema FAQ.
Este script inicializa a conexão com o banco de dados Oracle,
verifica sua disponibilidade e inicia o menu interativo do sistema.

Utiliza variáveis de ambiente para configuração do banco de dados,
que devem estar definidas em um arquivo .env na raiz do projeto.
"""

import logging
import os

from banco import FaqDB
from colorama import Fore, Style, init
from dotenv import load_dotenv
from menu import Menu

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s %(message)s')
logger = logging.getLogger(__name__)

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
        # Inicializa a conexão com o banco de dados com silent=True para suprimir mensagens automáticas
        db = FaqDB(oracle_config, silent=True)
        logger.info(
            f'{Fore.BLUE}Conexão com banco Oracle estabelecida com sucesso.{Style.RESET_ALL}'
        )
    except Exception as e:
        # Em caso de falha na conexão, exibe mensagem de erro detalhada e encerra o programa
        logger.error(
            f'{Fore.RED}Não foi possível conectar ao banco Oracle. Verifique as credenciais e o DSN.{Style.RESET_ALL}'
        )
        logger.warning(f'{Fore.YELLOW}Detalhes: {e}{Style.RESET_ALL}')
        exit(1)

    # Inicializa o menu principal passando a instância FaqDB já criada
    menu = Menu(db)
    # Exibe o menu interativo e inicia o fluxo do programa
    menu.exibir_menu()
