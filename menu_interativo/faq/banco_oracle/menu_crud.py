"""
Operações CRUD do FAQ.
"""

from colorama import Fore, Style

from .crud import (
    adicionar_faq,
    atualizar_faq,
    buscar_faq,
    deletar_faq,
    listar_categorias,
    listar_faqs,
)


class MenuCRUD:
    def __init__(self, db):
        self.db = db

    def menu_crud(self):
        while True:
            print(f'\n{Fore.BLUE}{Style.BRIGHT}--- CRUD FAQ ---{Style.RESET_ALL}')
            print(f'{Fore.WHITE}1. Adicionar FAQ')
            print(f'{Fore.WHITE}2. Listar FAQs')
            print(f'{Fore.WHITE}3. Atualizar FAQ')
            print(f'{Fore.WHITE}4. Deletar FAQ')
            print(f'{Fore.WHITE}5. Buscar FAQ por ID')
            print(f'{Fore.WHITE}6. Listar Categorias')
            print(f'{Fore.YELLOW}0. Voltar{Style.RESET_ALL}')
            opcao = input(f'{Fore.GREEN}Escolha uma opção: \n{Style.RESET_ALL}').strip()
            if opcao == '1':
                adicionar_faq(self.db)
            elif opcao == '2':
                listar_faqs(self.db)
            elif opcao == '3':
                atualizar_faq(self.db)
            elif opcao == '4':
                deletar_faq(self.db)
            elif opcao == '5':
                buscar_faq(self.db)
            elif opcao == '6':
                listar_categorias(self.db)
            elif opcao == '0':
                break
            else:
                print(
                    f'{Fore.RED}Opção inválida! Digite o número da opção desejada.{Style.RESET_ALL}'
                )
