"""
<<<<<<< HEAD
Arquivo principal para execução do sistema FAQ (CRUD em memória).
"""

from config.settings import show_message
from menu_memoria import MenuMemoria

if __name__ == '__main__':
    show_message('Sistema FAQ (CRUD em memória) iniciado.', 'info')
    menu = MenuMemoria()
    menu.menu_memoria()
    show_message('Obrigado por usar o sistema FAQ! Até a próxima.', 'info')
=======
Sistema FAQ com integração Oracle Database
Ponto de entrada principal do sistema de perguntas e respostas frequentes.
Suporta operações CRUD e exportação de dados para JSON.
"""

import logging
import os

from colorama import init
from config.settings import get_oracle_config, show_message
from dotenv import load_dotenv
from menu_crud import Menu

load_dotenv(
    dotenv_path=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.env'))
)

logging.basicConfig(level=logging.INFO, format='%(levelname)s %(message)s')
logger = logging.getLogger(__name__)

init(autoreset=True)


if __name__ == '__main__':
    oracle_config = get_oracle_config()

    show_message(
        'Sistema FAQ iniciado. Conexão com banco Oracle será feita quando necessária.',
        'info',
    )

    menu = Menu(oracle_config)
    menu.exibir_menu()
>>>>>>> SP4
