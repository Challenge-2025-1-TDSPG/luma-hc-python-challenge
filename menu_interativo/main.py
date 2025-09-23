"""
Arquivo principal para execução do sistema FAQ.
Este script inicializa a conexão com o banco de dados Oracle,
verifica sua disponibilidade e inicia o menu interativo do sistema.

Utiliza variáveis de ambiente para configuração do banco de dados,
que devem estar definidas em um arquivo .env na raiz do projeto.
"""

import logging

from banco import FaqDB
from colorama import init
from config.settings import get_oracle_config, show_message

from menu_interativo.menu_crud import Menu

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s %(message)s')
logger = logging.getLogger(__name__)

# Inicializa o colorama para formatação colorida no terminal (necessário para Windows)
init(autoreset=True)


if __name__ == '__main__':
    # Configura os parâmetros de conexão com o banco Oracle a partir do módulo de configuração
    oracle_config = get_oracle_config()

    try:
        # Inicializa a conexão com o banco de dados com silent=True para suprimir mensagens automáticas
        db = FaqDB(oracle_config, silent=True)
        show_message('Conexão com banco Oracle estabelecida com sucesso.', 'success')
    except Exception as e:
        # Em caso de falha na conexão, exibe mensagem de erro detalhada e encerra o programa
        show_message(
            'Não foi possível conectar ao banco Oracle. Verifique as credenciais e o DSN.',
            'error',
        )
        show_message(f'Detalhes: {e}', 'warning')
        exit(1)

    # Inicializa o menu principal passando a instância FaqDB já criada
    menu = Menu(db)
    # Exibe o menu interativo e inicia o fluxo do programa
    menu.exibir_menu()
