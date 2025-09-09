"""
Operações CRUD do FAQ.
"""

from .adicionar import adicionar_faq
from .atualizar import atualizar_faq
from .buscar import buscar_faq
from .categorias import listar_categorias
from .deletar import deletar_faq
from .listar import listar_faqs


class MenuCRUD:
    def __init__(self, db):
        self.db = db

    def menu_crud(self):
        while True:
            print('\n--- CRUD FAQ ---')
            print('1. Adicionar FAQ')
            print('2. Listar FAQs')
            print('3. Atualizar FAQ')
            print('4. Deletar FAQ')
            print('5. Buscar FAQ por ID')
            print('6. Listar Categorias')
            print('0. Voltar')
            opcao = input('Escolha uma opção: ').strip()
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
                print('Opção inválida! Digite o número da opção desejada.')
