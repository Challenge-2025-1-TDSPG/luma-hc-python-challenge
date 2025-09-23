"""
Módulo de menu principal do sistema FAQ.
Oferece interface de CRUD, exportação para JSON e consumo de API pública.
"""

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


class Menu:
    """
    Classe responsável pelo menu principal e submenus do sistema FAQ.
    """

    def __init__(self, oracle_config):
        """Inicializa o menu principal e os submenus do sistema.

        Args:
            oracle_config: Dicionário de configuração Oracle com as chaves
                          'user', 'password' e 'dsn'
        """
        self.oracle_config = oracle_config
        self.db = None  # Conexão será criada sob demanda
        # faqs_memoria = []  # Removed
        # self.menu_memoria = MenuMemoria(faqs_memoria)  # Removed

    def _conectar_banco_se_necessario(self):
        """Conecta ao banco Oracle sob demanda, apenas quando necessário."""
        if self.db is None:
            try:
                from banco import FaqDB

                show_message('Conectando ao banco Oracle...', 'info')
                self.db = FaqDB(self.oracle_config, silent=True)
                show_message(
                    'Conexão com banco Oracle estabelecida com sucesso.', 'success'
                )
                return True
            except Exception as e:
                show_message(
                    'Não foi possível conectar ao banco Oracle. Verifique as credenciais e o DSN.',
                    'error',
                )
                show_message(f'Detalhes: {e}', 'warning')
                return False
        return True

    def _exportar_banco_json(self):
        """Exporta dados do banco para JSON, conectando se necessário."""
        if self._conectar_banco_se_necessario():
            try:
                from exportacao import MenuExportacao

                menu_exportacao = MenuExportacao(self.db)
                menu_exportacao.exportar_json()
            except Exception as e:
                show_message(f'Erro na exportação: {e}', 'error')

    def exibir_menu(self):
        while True:
            print(f'\n{COLOR_TITLE}--- MENU FAQ ---{COLOR_RESET}')
            print(f'{COLOR_OPTION}1. CRUD de FAQs (Banco Oracle)')
            print(f'{COLOR_OPTION}2. Exportar FAQs do banco para JSON')
            print(f'{COLOR_WARNING}{MENU_EXIT_KEYS}{COLOR_RESET}')
            opcao = (
                input(
                    f'{COLOR_PROMPT}Escolha uma opção ({MENU_EXIT_KEYS}): {COLOR_RESET}'
                )
                .strip()
                .lower()
            )
            if opcao == '1':
                # Conecta ao banco sob demanda antes de usar o CRUD
                if self._conectar_banco_se_necessario():
                    if hasattr(self.db, 'menu_crud'):
                        self.db.menu_crud()
                    else:
                        show_message(
                            'CRUD do banco não implementado diretamente aqui. Use as funções de banco.py.',
                            'warning',
                        )
            elif opcao == '2':
                # Conecta ao banco sob demanda antes de exportar
                self._exportar_banco_json()
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
