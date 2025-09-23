"""
Módulo de menu principal do sistema FAQ.
Oferece interface de CRUD, exportação para JSON e consumo de API pública.
"""

from banco import FaqDB
from config.settings import (
    COLOR_OPTION,
    COLOR_PROMPT,
    COLOR_RESET,
    COLOR_TITLE,
    COLOR_WARNING,
    MENU_CONFIRM_EXIT,
    MENU_EXIT_CANCEL,
    MENU_EXIT_KEYS,
    MENU_EXITING,
    MENU_INVALID_OPTION,
    show_message,
)
from exportacao import MenuExportacao

from menu_interativo.menu_memoria import MenuMemoria


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
            print(f'\n{COLOR_TITLE}--- MENU FAQ ---{COLOR_RESET}')
            print(f'{COLOR_OPTION}1. CRUD de FAQs (Banco Oracle)')
            print(f'{COLOR_OPTION}2. CRUD de FAQs em memória')
            print(f'{COLOR_OPTION}3. Exportar FAQs do banco para JSON')
            print(f'{COLOR_WARNING}{MENU_EXIT_KEYS}{COLOR_RESET}')
            opcao = (
                input(
                    f'{COLOR_PROMPT}Escolha uma opção ({MENU_EXIT_KEYS}): {COLOR_RESET}'
                )
                .strip()
                .lower()
            )
            if opcao == '1':
                # O menu CRUD do banco pode ser implementado como função ou classe em banco.py
                if hasattr(self.db, 'menu_crud'):
                    self.db.menu_crud()
                else:
                    show_message(
                        'CRUD do banco não implementado diretamente aqui. Use as funções de banco.py.',
                        'warning',
                    )
            elif opcao == '2':
                self.menu_memoria.menu_memoria()
            elif opcao == '3':
                self.menu_exportacao.exportar_json()
            elif opcao in ['0', 's']:
                confirm = (
                    input(f'{COLOR_WARNING}{MENU_CONFIRM_EXIT}{COLOR_RESET}')
                    .strip()
                    .lower()
                )
                if confirm == 's':
                    show_message(MENU_EXITING, 'warning')
                    if self.db:
                        self.db.close(silent=False)
                    break
                else:
                    show_message(MENU_EXIT_CANCEL, 'success')
            else:
                show_message(MENU_INVALID_OPTION, 'error')
