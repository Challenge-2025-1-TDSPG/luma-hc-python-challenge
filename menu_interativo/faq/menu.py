"""
Módulo de menu principal do sistema FAQ.
Oferece interface de CRUD, exportação para JSON e consumo de API pública.
"""

from colorama import Fore, Style

from .banco_oracle import MenuCRUD
from .db import FaqDB
from .exportacao import MenuExportacao
from .memoria import MenuMemoria


class Menu:
    """
    Classe responsável pelo menu principal e submenus do sistema FAQ.
    """

    def __init__(self, oracle_config):
        """Inicializa o menu e as operações modulares."""
        self.oracle_config = oracle_config
        self.db = FaqDB(oracle_config)
        faqs_memoria = []
        self.menu_crud = MenuCRUD(self.db)
        self.menu_exportacao = MenuExportacao(self.db)
        self.menu_memoria = MenuMemoria(faqs_memoria)

    def exibir_menu(self):
        """
        Exibe o menu principal e gerencia a navegação entre submenus.
        """
        while True:
            print(f'\n{Fore.CYAN}{Style.BRIGHT}--- MENU FAQ ---{Style.RESET_ALL}')
            print(f'{Fore.WHITE}1. CRUD de FAQs (Banco Oracle)')
            print(f'{Fore.WHITE}2. CRUD de FAQs em memória')
            print(f'{Fore.WHITE}3. Exportar FAQs do banco para JSON')
            print(f'{Fore.YELLOW}0. Sair{Style.RESET_ALL}')
            opcao = input(f'{Fore.GREEN}Escolha uma opção: {Style.RESET_ALL}').strip()
            if opcao == '1':
                self.menu_crud.menu_crud()
            elif opcao == '2':
                self.menu_memoria.menu_memoria()
            elif opcao == '3':
                self.menu_exportacao.exportar_json()
            elif opcao == '0':
                if self.db:
                    self.db.close()
                print(f'{Fore.YELLOW}Saindo...{Style.RESET_ALL}')
                break
            else:
                print(
                    f'{Fore.RED}Opção inválida! Digite o número da opção desejada.{Style.RESET_ALL}'
                )


if __name__ == '__main__':
    menu = Menu()
    menu.exibir_menu()
