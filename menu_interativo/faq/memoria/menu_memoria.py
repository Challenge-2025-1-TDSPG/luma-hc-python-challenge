"""
Operações de FAQs em memória (cada FAQ contém pergunta, resposta, etc).
"""

import os

from colorama import Fore, Style

from .crud_memoria import (
    adicionar_faq_memoria,
    atualizar_faq_memoria,
    buscar_faq_memoria,
    listar_faqs_memoria,
    remover_faq_memoria,
)


class MenuMemoria:
    def __init__(self, faqs_memoria=None):
        self.faqs_memoria = faqs_memoria if faqs_memoria is not None else []
        pasta_memoria = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'memoria')
        )
        os.makedirs(pasta_memoria, exist_ok=True)
        self.caminho_json = os.path.join(pasta_memoria, 'faq_export.json')

    def menu_memoria(self):
        """Menu para operações em memória."""
        while True:
            print(
                f'\n{Fore.MAGENTA}{Style.BRIGHT}--- CRUD FAQ EM MEMÓRIA ---{Style.RESET_ALL}'
            )
            print(f'{Fore.WHITE}1. Adicionar FAQ')
            print(f'{Fore.WHITE}2. Listar FAQs')
            print(f'{Fore.WHITE}3. Atualizar FAQ')
            print(f'{Fore.WHITE}4. Deletar FAQ')
            print(f'{Fore.WHITE}5. Buscar FAQ por ID')
            print(f'{Fore.YELLOW}0. Voltar{Style.RESET_ALL}')
            opcao = input(f'{Fore.GREEN}Escolha uma opção: {Style.RESET_ALL}').strip()
            if opcao == '1':
                self.adicionar_faq_memoria()
            elif opcao == '2':
                self.listar_faqs_memoria()
            elif opcao == '3':
                self.atualizar_faq_memoria()
            elif opcao == '4':
                self.remover_faq_memoria()
            elif opcao == '5':
                self.buscar_faq_memoria()
            elif opcao == '0':
                break
            else:
                print(
                    f'{Fore.RED}Opção inválida! Digite o número da opção desejada.{Style.RESET_ALL}'
                )

    def listar_faqs_memoria(self):
        listar_faqs_memoria(self.faqs_memoria)

    def adicionar_faq_memoria(self):
        adicionar_faq_memoria(self.faqs_memoria)

    def atualizar_faq_memoria(self):
        atualizar_faq_memoria(self.faqs_memoria)

    def remover_faq_memoria(self):
        remover_faq_memoria(self.faqs_memoria)

    def buscar_faq_memoria(self):
        buscar_faq_memoria(self.faqs_memoria)
