"""
Operações CRUD do FAQ.
"""

from ..db import FaqDB


class MenuCRUD:
    def __init__(self, db: FaqDB):
        self.db = db

    def menu_crud(self):
        while True:
            print('\n--- CRUD FAQ ---')
            print('1. Adicionar Pergunta')
            print('2. Listar Perguntas')
            print('3. Atualizar Pergunta')
            print('4. Deletar Pergunta')
            print('5. Buscar Pergunta por ID')
            print('6. Listar Categorias')
            print('0. Voltar')
            opcao = input('Escolha uma opção: ').strip()
            if opcao == '1':
                self._adicionar_pergunta()
            elif opcao == '2':
                self._listar_perguntas()
            elif opcao == '3':
                self._atualizar_pergunta()
            elif opcao == '4':
                self._deletar_pergunta()
            elif opcao == '5':
                self._buscar_pergunta()
            elif opcao == '6':
                self._listar_categorias()
            elif opcao == '0':
                break
            else:
                print('Opção inválida! Digite o número da opção desejada.')

    def _adicionar_pergunta(self):
        try:
            pergunta = input('Digite a pergunta: ').strip()
            resposta = input('Digite a resposta: ').strip()
            pasta = input('Digite o nome da categoria: ').strip()
            ativo_str = input('Ativo? (1-Sim, 0-Não): ').strip()
            if not (pergunta and resposta and pasta):
                print('Todos os campos são obrigatórios!')
                return
            if ativo_str not in ['0', '1']:
                print('Valor para "Ativo" deve ser 1 (Sim) ou 0 (Não).')
                return
            ativo = int(ativo_str)
            self.db.adicionar(pergunta, resposta, ativo, pasta)
        except Exception as e:
            print(f'Erro ao adicionar pergunta: {e}')
        else:
            print('Pergunta adicionada com sucesso!')
        finally:
            print('[LOG] Operação de inserção finalizada.')

    def _listar_perguntas(self):
        categoria = input('Filtrar por categoria (deixe vazio para todas): ').strip()
        perguntas = self.db.listar(categoria if categoria else None)
        if perguntas:
            for p in perguntas:
                print(p)
                print('-' * 30)
        else:
            print('Nenhuma pergunta cadastrada.')

    def _atualizar_pergunta(self):
        try:
            id_str = input('Digite o ID da pergunta a atualizar: ').strip()
            if not id_str.isdigit():
                print('ID deve ser um número inteiro.')
                return
            id = int(id_str)
            pergunta = input('Nova pergunta: ').strip()
            resposta = input('Nova resposta: ').strip()
            pasta = input('Nova categoria: ').strip()
            ativo_str = input('Ativo? (1-Sim, 0-Não): ').strip()
            if not (pergunta and resposta and pasta):
                print('Todos os campos são obrigatórios!')
                return
            if ativo_str not in ['0', '1']:
                print('Valor para "Ativo" deve ser 1 (Sim) ou 0 (Não).')
                return
            ativo = int(ativo_str)
            self.db.atualizar(id, pergunta, resposta, ativo, pasta)
        except Exception as e:
            print(f'Erro ao atualizar pergunta: {e}')
        else:
            print('Pergunta atualizada com sucesso!')
        finally:
            print('[LOG] Operação de atualização finalizada.')

    def _deletar_pergunta(self):
        try:
            id_str = input('Digite o ID da pergunta a deletar: ').strip()
            if not id_str.isdigit():
                print('ID deve ser um número inteiro.')
                return
            id = int(id_str)
            self.db.deletar(id)
        except Exception as e:
            print(f'Erro ao deletar pergunta: {e}')
        else:
            print('Pergunta deletada com sucesso!')
        finally:
            print('[LOG] Operação de exclusão finalizada.')

    def _buscar_pergunta(self):
        try:
            id_str = input('Digite o ID da pergunta: ').strip()
            if not id_str.isdigit():
                print('ID deve ser um número inteiro.')
                return
            id = int(id_str)
            pergunta = self.db.buscar_por_id(id)
            if pergunta:
                print(pergunta)
        except Exception as e:
            print(f'Erro ao buscar pergunta: {e}')

    def _listar_categorias(self):
        categorias = self.db.listar_pastas()
        if categorias:
            print('Categorias disponíveis:')
            for categoria in categorias:
                print(f'- {categoria}')
        else:
            print('Nenhuma categoria cadastrada.')
