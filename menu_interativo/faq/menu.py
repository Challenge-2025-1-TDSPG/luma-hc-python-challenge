"""
Módulo de menu principal do sistema FAQ.
Oferece interface de CRUD, exportação para JSON e consumo de API pública.
"""

from .crud.menu_crud import MenuCRUD
from .db import FaqDB
from .exportacao.menu_exportacao import MenuExportacao
from .memoria.menu_memoria import MenuMemoria


class Menu:
    """
    Classe responsável pelo menu principal e submenus do sistema FAQ.
    """

    def __init__(self, oracle_config):
        """Inicializa o menu e as operações modulares."""
        self.db = FaqDB(oracle_config)
        from .memoria.perguntas_memoria import adicionar_pergunta

        perguntas = []
        adicionar_pergunta(perguntas, 1, 'Pergunta 1')
        adicionar_pergunta(perguntas, 2, 'Pergunta 2')
        self.menu_crud = MenuCRUD(self.db)
        self.menu_exportacao = MenuExportacao(self.db)
        self.menu_memoria = MenuMemoria(perguntas)

    def exibir_menu(self):
        """
        Exibe o menu principal e gerencia a navegação entre submenus.
        """
        while True:
            print('\n--- MENU FAQ ---')
            print('1. CRUD de Perguntas')
            print('2. Listar perguntas em memória')
            print('3. Exportar perguntas para JSON')
            print('0. Sair')
            opcao = input('Escolha uma opção: ').strip()
            if opcao == '1':
                self.menu_crud.menu_crud()
            elif opcao == '2':
                self.menu_memoria.listar_perguntas_memoria()
            elif opcao == '3':
                self.menu_exportacao.exportar_json()
            elif opcao == '0':
                self.db.close()
                print('Saindo...')
                break
            else:
                print('Opção inválida! Digite o número da opção desejada.')


if __name__ == '__main__':
    menu = Menu()
    menu.exibir_menu()
