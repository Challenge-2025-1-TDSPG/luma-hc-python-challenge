"""
Arquivo principal para execução do sistema FAQ.
Este script inicializa a conexão com o banco de dados Oracle,
verifica sua disponibilidade e inicia o menu interativo do sistema.

Utiliza variáveis de ambiente para configuração do banco de dados,
que devem estar definidas em um arquivo .env na raiz do projeto.
"""

# Força o carregamento do .env ao iniciar, independente do contexto
import logging
import os

from colorama import init
from config.settings import get_oracle_config, show_message
from dotenv import load_dotenv
from menu_crud import Menu

load_dotenv(
    dotenv_path=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.env'))
)

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s %(message)s')
logger = logging.getLogger(__name__)

# Inicializa o colorama para formatação colorida no terminal
init(autoreset=True)


if __name__ == '__main__':
    # Configura os parâmetros de conexão com o banco Oracle a partir do módulo de configuração
    oracle_config = get_oracle_config()

    # Não conecta ao banco na inicialização - conexão será feita sob demanda
    show_message(
        'Sistema FAQ iniciado. Conexão com banco Oracle será feita quando necessária.',
        'info',
    )

    # Inicializa o menu principal passando a configuração Oracle
    menu = Menu(oracle_config)
    # Exibe o menu interativo e inicia o fluxo do programa
    menu.exibir_menu()
