"""
Operações de FAQs em memória (cada FAQ contém pergunta, resposta, etc).
"""

import json
import os

from .crud_memoria.adicionar import adicionar_faq_memoria
from .crud_memoria.atualizar import atualizar_faq_memoria
from .crud_memoria.buscar import buscar_faq_memoria
from .crud_memoria.deletar import remover_faq_memoria
from .crud_memoria.listar import listar_faqs_memoria


class MenuMemoria:
    def __init__(self, faqs_memoria=None):
        self.faqs_memoria = faqs_memoria if faqs_memoria is not None else []
        pasta_memoria = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'memoria')
        )
        os.makedirs(pasta_memoria, exist_ok=True)
        self.caminho_json = os.path.join(pasta_memoria, 'faq_export.json')
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
        listar_faqs_memoria(self.faqs_memoria)

    def adicionar_faq_memoria(self):
        adicionar_faq_memoria(self.faqs_memoria)

    def atualizar_faq_memoria(self):
        atualizar_faq_memoria(self.faqs_memoria)

    def remover_faq_memoria(self):
        remover_faq_memoria(self.faqs_memoria)

    def buscar_faq_memoria(self):
        buscar_faq_memoria(self.faqs_memoria)
