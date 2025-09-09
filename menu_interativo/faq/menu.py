"""
Módulo de menu principal do sistema FAQ.
Oferece interface de CRUD, exportação para JSON e consumo de API pública.
"""

import json

from .api import CuriosidadeAPI
from .db import FaqDB


class Menu:
    """
    Classe responsável pelo menu principal e submenus do sistema FAQ.
    """

    def __init__(self):
        """Inicializa o menu e a conexão com o banco de dados."""
        self.db = FaqDB()

    def exibir_menu(self):
        """
        Exibe o menu principal e gerencia a navegação entre submenus.
        """
        while True:
            print('\n--- MENU FAQ ---')
            print('1. CRUD de Perguntas')
            print('2. Exportar perguntas para JSON')
            print('3. Buscar curiosidade (API pública)')
            print('0. Sair')
            opcao = input('Escolha uma opção: ')
            if opcao == '1':
                self.menu_crud()
            elif opcao == '2':
                self.exportar_json()
            elif opcao == '3':
                self.menu_api()
            elif opcao == '0':
                self.db.close()
                print('Saindo...')
                break
            else:
                print('Opção inválida!')

    def menu_crud(self):
        """
        Exibe submenu de operações CRUD.
        """
        while True:
            print('\n--- CRUD FAQ ---')
            print('1. Adicionar Pergunta')
            print('2. Listar Perguntas')
            print('3. Atualizar Pergunta')
            print('4. Deletar Pergunta')
            print('5. Buscar Pergunta por ID')
            print('6. Listar Pastas')
            print('0. Voltar')
            opcao = input('Escolha uma opção: ')
            if opcao == '1':
                self.adicionar_pergunta()
            elif opcao == '2':
                self.listar_perguntas()
            elif opcao == '3':
                self.atualizar_pergunta()
            elif opcao == '4':
                self.deletar_pergunta()
            elif opcao == '5':
                self.buscar_pergunta()
            elif opcao == '6':
                self.listar_pastas()
            elif opcao == '0':
                break
            else:
                print('Opção inválida!')

    def adicionar_pergunta(self):
        """
        Adiciona uma nova pergunta ao FAQ.
        """
        try:
            pergunta = input('Digite a pergunta: ').strip()
            resposta = input('Digite a resposta: ').strip()
            ativo = int(input('Ativo? (1-Sim, 0-Não): '))
            pasta = input('Digite o nome da pasta (categoria): ').strip()
            if pergunta and resposta and pasta and ativo in [0, 1]:
                self.db.adicionar(pergunta, resposta, ativo, pasta)
            else:
                print('Dados inválidos!')
        except Exception as e:
            print(f'Erro: {e}')

    def listar_perguntas(self):
        """
        Lista perguntas do FAQ, com opção de filtrar por pasta.
        """
        pasta = input('Filtrar por pasta (deixe vazio para todas): ').strip()
        perguntas = self.db.listar(pasta if pasta else None)
        if perguntas:
            for p in perguntas:
                print(p)
                print('-' * 30)
        else:
            print('Nenhuma pergunta cadastrada.')

    def atualizar_pergunta(self):
        """
        Atualiza uma pergunta existente no FAQ.
        """
        try:
            id = int(input('Digite o ID da pergunta a atualizar: '))
            pergunta = input('Nova pergunta: ').strip()
            resposta = input('Nova resposta: ').strip()
            ativo = int(input('Ativo? (1-Sim, 0-Não): '))
            pasta = input('Nova pasta (categoria): ').strip()
            if pergunta and resposta and pasta and ativo in [0, 1]:
                self.db.atualizar(id, pergunta, resposta, ativo, pasta)
            else:
                print('Dados inválidos!')
        except Exception as e:
            print(f'Erro: {e}')

    def deletar_pergunta(self):
        """
        Deleta uma pergunta do FAQ.
        """
        try:
            id = int(input('Digite o ID da pergunta a deletar: '))
            self.db.deletar(id)
        except Exception as e:
            print(f'Erro: {e}')

    def buscar_pergunta(self):
        """
        Busca uma pergunta pelo ID.
        """
        try:
            id = int(input('Digite o ID da pergunta: '))
            pergunta = self.db.buscar_por_id(id)
            if pergunta:
                print(pergunta)
        except Exception as e:
            print(f'Erro: {e}')

    def listar_pastas(self):
        """
        Lista todas as pastas (categorias) cadastradas.
        """
        pastas = self.db.listar_pastas()
        if pastas:
            print('Pastas disponíveis:')
            for pasta in pastas:
                print(f'- {pasta}')
        else:
            print('Nenhuma pasta cadastrada.')

    def exportar_json(self):
        """
        Exporta todas as perguntas do FAQ para um arquivo JSON na pasta data/.
        """
        perguntas = self.db.listar()
        lista_dict = [vars(p) for p in perguntas]
        try:
            caminho = '../data/faq_export.json'
            with open(caminho, 'w', encoding='utf-8') as f:
                json.dump(lista_dict, f, ensure_ascii=False, indent=4)
            print(f'Exportação realizada com sucesso para {caminho}!')
        except Exception as e:
            print(f'Erro ao exportar para JSON: {e}')

    def menu_api(self):
        """
        Consome uma API pública e exibe uma curiosidade.
        """
        print('\n--- Curiosidade (API Pública) ---')
        curiosidade = CuriosidadeAPI.buscar_curiosidade()
        print(curiosidade)


if __name__ == '__main__':
    menu = Menu()
    menu.exibir_menu()
