"""
Operações de FAQs em memória (cada FAQ contém pergunta, resposta, etc).
"""

import json
import os

from .faq_memoria import adicionar_faq, atualizar_faq, buscar_faq, remover_faq


class MenuMemoria:
    def __init__(self, faqs_memoria=None):
        self.faqs_memoria = faqs_memoria if faqs_memoria is not None else []
        self.caminho_json = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..', 'data', 'faq_export.json')
        )
        self.carregar_json()

    def carregar_json(self):
        if os.path.exists(self.caminho_json):
            try:
                with open(self.caminho_json, 'r', encoding='utf-8') as f:
                    faqs = json.load(f)
                    if isinstance(faqs, list):
                        self.faqs_memoria = faqs
            except Exception as e:
                print(f'[LOG] Erro ao carregar FAQs do JSON: {e}')

    def exportar_json(self):
        try:
            with open(self.caminho_json, 'w', encoding='utf-8') as f:
                json.dump(self.faqs_memoria, f, ensure_ascii=False, indent=4)
            print(f'Exportação realizada com sucesso para {self.caminho_json}!')
        except Exception as e:
            print(f'Erro ao exportar FAQs para JSON: {e}')

    def menu_memoria(self):
        while True:
            print('\n--- CRUD de FAQs em Memória ---')
            print('1. Listar FAQs em memória')
            print('2. Adicionar FAQ em memória')
            print('3. Atualizar FAQ em memória')
            print('4. Remover FAQ em memória')
            print('5. Buscar FAQ por ID em memória')
            print('6. Importar FAQs do JSON')
            print('7. Exportar FAQs para JSON')
            print('0. Voltar')
            opcao = input('Escolha uma opção: ').strip()
            if opcao == '1':
                self.listar_faqs_memoria()
            elif opcao == '2':
                self.adicionar_faq_memoria()
            elif opcao == '3':
                self.atualizar_faq_memoria()
            elif opcao == '4':
                self.remover_faq_memoria()
            elif opcao == '5':
                self.buscar_faq_memoria()
            elif opcao == '6':
                self.carregar_json()
                print('FAQs importados do JSON!')
            elif opcao == '7':
                self.exportar_json()
            elif opcao == '0':
                break
            else:
                print('Opção inválida! Digite o número da opção desejada.')

    def listar_faqs_memoria(self):
        if not self.faqs_memoria:
            print('Nenhum FAQ em memória.')
        else:
            for faq in self.faqs_memoria:
                print(f'ID: {faq["id"]} | Pergunta: {faq["pergunta"]}')
            print(f'Total de FAQs em memória: {len(self.faqs_memoria)}')

    def adicionar_faq_memoria(self):
        try:
            id_str = input('ID do FAQ: ').strip()
            pergunta = input('Pergunta do FAQ: ').strip()
            if not (id_str.isdigit() and pergunta):
                print('ID deve ser número e a pergunta não pode ser vazia.')
                return
            id = int(id_str)
            adicionar_faq(self.faqs_memoria, id, pergunta)
            print('FAQ adicionado em memória!')
        except Exception as e:
            print(f'Erro ao adicionar FAQ: {e}')

    def atualizar_faq_memoria(self):
        try:
            id_str = input('ID do FAQ a atualizar: ').strip()
            nova_pergunta = input('Nova pergunta do FAQ: ').strip()
            if not (id_str.isdigit() and nova_pergunta):
                print('ID deve ser número e a pergunta não pode ser vazia.')
                return
            id = int(id_str)
            atualizar_faq(self.faqs_memoria, id, nova_pergunta)
            print('FAQ atualizado em memória!')
        except Exception as e:
            print(f'Erro ao atualizar FAQ: {e}')

    def remover_faq_memoria(self):
        try:
            id_str = input('ID do FAQ a remover: ').strip()
            if not id_str.isdigit():
                print('ID deve ser número.')
                return
            id = int(id_str)
            self.faqs_memoria[:] = remover_faq(self.faqs_memoria, id)
            print('FAQ removido em memória!')
        except Exception as e:
            print(f'Erro ao remover FAQ: {e}')

    def buscar_faq_memoria(self):
        try:
            id_str = input('ID do FAQ a buscar: ').strip()
            if not id_str.isdigit():
                print('ID deve ser número.')
                return
            id = int(id_str)
            encontrados = buscar_faq(self.faqs_memoria, id)
            if encontrados:
                for faq in encontrados:
                    print(f'ID: {faq["id"]} | Pergunta: {faq["pergunta"]}')
            else:
                print('Nenhum FAQ encontrado com esse ID.')
        except Exception as e:
            print(f'Erro ao buscar FAQ: {e}')
