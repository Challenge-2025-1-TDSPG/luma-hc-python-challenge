"""
Módulo de menu principal do sistema FAQ.
Oferece interface de CRUD, exportação para JSON e consumo de API pública.
"""

from banco import FaqDB
from colorama import Fore, Style
from exportacao import MenuExportacao
from memoria import MenuMemoria


class Menu:
    """
    Classe responsável pelo menu principal e submenus do sistema FAQ.
    """

    def __init__(self, db_or_config):
        """Inicializa o menu principal e os submenus do sistema.

        Args:
            db_or_config: Pode ser uma instância de FaqDB já inicializada ou
                         um dicionário de configuração Oracle com as chaves
                         'user', 'password' e 'dsn'
        """
        if isinstance(db_or_config, FaqDB):
            self.db = db_or_config
        else:
            self.db = FaqDB(db_or_config)
        faqs_memoria = []
        self.menu_exportacao = MenuExportacao(self.db)
        self.menu_memoria = MenuMemoria(faqs_memoria)

    def exibir_menu(self):
        while True:
            print(f'\n{Fore.CYAN}{Style.BRIGHT}--- MENU FAQ ---{Style.RESET_ALL}')
            print(f'{Fore.WHITE}1. CRUD de FAQs (Banco Oracle)')
            print(f'{Fore.WHITE}2. CRUD de FAQs em memória')
            print(f'{Fore.WHITE}3. Exportar FAQs do banco para JSON')
            print(f'{Fore.YELLOW}0. Sair{Style.RESET_ALL}')
            opcao = input(f'{Fore.GREEN}Escolha uma opção: {Style.RESET_ALL}').strip()
            if opcao == '1':
                # O menu CRUD do banco pode ser implementado como função ou classe em banco.py
                if hasattr(self.db, 'menu_crud'):
                    self.db.menu_crud()
                else:
                    print(
                        f'{Fore.YELLOW}CRUD do banco não implementado diretamente aqui. Use as funções de banco.py.{Style.RESET_ALL}'
                    )
            elif opcao == '2':
                self.menu_memoria.menu_memoria()
            elif opcao == '3':
                self.menu_exportacao.exportar_json()
            elif opcao == '0':
                print(f'{Fore.YELLOW}Saindo...{Style.RESET_ALL}')
                if self.db:
                    self.db.close(silent=False)
                break
            else:
                print(
                    f'{Fore.RED}Opção inválida! Digite o número da opção desejada.{Style.RESET_ALL}'
                )
