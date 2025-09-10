"""
Módulo de menu para operações CRUD de FAQs em memória.
Fornece interface para adicionar, listar, atualizar, deletar e buscar FAQs
armazenados em estruturas de dados em memória.
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
    """Classe que gerencia o menu de operações CRUD para FAQs em memória.

    Esta classe fornece uma interface interativa para realizar operações
    Create, Read, Update e Delete (CRUD) nas FAQs armazenadas em memória,
    sem persistência em banco de dados.
    """

    def __init__(self, faqs_memoria=None):
        """Inicializa o menu de operações em memória.

        Args:
            faqs_memoria (list, optional): Lista inicial de FAQs em memória.
                                          Se não fornecida, inicia com lista vazia.
        """
        # Inicializa a lista de FAQs, usando a fornecida ou uma lista vazia
        self.faqs_memoria = faqs_memoria if faqs_memoria is not None else []

        # Configura o diretório para possível exportação/importação de dados
        pasta_memoria = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'memoria')
        )
        os.makedirs(pasta_memoria, exist_ok=True)
        self.caminho_json = os.path.join(pasta_memoria, 'faq_export.json')

    def menu_memoria(self):
        """Exibe o menu de operações em memória e processa as escolhas do usuário.

        Este método entra em um loop até que o usuário escolha voltar ao menu principal.
        Cada opção do menu direciona para a função correspondente para realizar a operação CRUD.
        """
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
        """Exibe todos os FAQs armazenados em memória."""
        listar_faqs_memoria(self.faqs_memoria)

    def adicionar_faq_memoria(self):
        """Adiciona um novo FAQ à lista em memória."""
        adicionar_faq_memoria(self.faqs_memoria)

    def atualizar_faq_memoria(self):
        """Atualiza um FAQ existente na lista em memória."""
        atualizar_faq_memoria(self.faqs_memoria)

    def remover_faq_memoria(self):
        """Remove um FAQ da lista em memória pelo ID."""
        remover_faq_memoria(self.faqs_memoria)

    def buscar_faq_memoria(self):
        """Busca um FAQ na lista em memória pelo ID."""
        buscar_faq_memoria(self.faqs_memoria)
