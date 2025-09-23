"""
Arquivo principal para execução do sistema FAQ (CRUD em memória).
"""

from config.settings import show_message
from menu_memoria import MenuMemoria

if __name__ == '__main__':
    show_message('Sistema FAQ (CRUD em memória) iniciado.', 'info')
    menu = MenuMemoria()
    menu.exibir_menu()
