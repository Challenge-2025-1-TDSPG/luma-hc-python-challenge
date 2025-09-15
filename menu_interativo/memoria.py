"""
Módulo consolidado de operações CRUD de FAQs em memória para o sistema FAQ.
Inclui funções de adicionar, listar, atualizar, deletar, buscar e o menu interativo.
"""

import os
from datetime import datetime

from colorama import Fore, Style


# --- Funções CRUD em memória ---
def adicionar_faq_memoria(lista):
    operacao_iniciada = False
    try:
        id_str = input(f'{Fore.CYAN}Digite o ID do FAQ: {Style.RESET_ALL}').strip()
        pergunta = input(f'{Fore.CYAN}Digite a pergunta: {Style.RESET_ALL}').strip()
        resposta = input(f'{Fore.CYAN}Digite a resposta: {Style.RESET_ALL}').strip()
        categoria = input(
            f'{Fore.CYAN}Digite o nome da categoria: {Style.RESET_ALL}'
        ).strip()
        if categoria:
            print(
                f'{Fore.BLUE}Categoria será salva como: {categoria.upper()}{Style.RESET_ALL}'
            )
        ativo_str = input(
            f'{Fore.CYAN}Ativo? (1-Sim, 0-Não): {Style.RESET_ALL}'
        ).strip()
        if not (id_str.isdigit() and pergunta and resposta and categoria):
            print(f'{Fore.RED}Todos os campos são obrigatórios!{Style.RESET_ALL}')
            return
        while ativo_str not in ['0', '1']:
            print(
                f'{Fore.RED}Valor para "Ativo" deve ser 1 (Sim) ou 0 (Não).{Style.RESET_ALL}'
            )
            ativo_str = input(
                f'{Fore.CYAN}Ativo? (1-Sim, 0-Não): {Style.RESET_ALL}'
            ).strip()
        try:
            id = int(id_str)
        except ValueError:
            print(f'{Fore.RED}O ID deve ser um número inteiro válido.{Style.RESET_ALL}')
            return
        if any(item['id'] == id for item in lista):
            print(f'{Fore.YELLOW}Já existe um FAQ com esse ID.{Style.RESET_ALL}')
            return
        operacao_iniciada = True
        ativo = int(ativo_str)
        atualizado_em = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        novo_faq = {
            'id': id,
            'pergunta': pergunta,
            'resposta': resposta,
            'ativo': ativo,
            'atualizado_em': atualizado_em,
            'categoria': categoria.upper(),
        }
        lista.append(novo_faq)
    except Exception as e:
        print(f'{Fore.RED}Erro ao adicionar FAQ em memória: {e}{Style.RESET_ALL}')
    else:
        print(f'{Fore.GREEN}FAQ adicionado com sucesso!{Style.RESET_ALL}')
        ativo_texto = (
            f'{Fore.GREEN}Sim{Style.RESET_ALL}'
            if novo_faq['ativo'] == 1
            else f'{Fore.RED}Não{Style.RESET_ALL}'
        )
        print(
            f'{Fore.MAGENTA}ID:{Style.RESET_ALL} {novo_faq["id"]}\n'
            f'{Fore.MAGENTA}Pergunta:{Style.RESET_ALL} {novo_faq["pergunta"]}\n'
            f'{Fore.MAGENTA}Resposta:{Style.RESET_ALL} {novo_faq["resposta"]}\n'
            f'{Fore.MAGENTA}Ativo:{Style.RESET_ALL} {ativo_texto}\n'
            f'{Fore.MAGENTA}Atualizado em:{Style.RESET_ALL} {novo_faq["atualizado_em"]}\n'
            f'{Fore.MAGENTA}Categoria:{Style.RESET_ALL} {novo_faq["categoria"]}'
        )
    finally:
        if operacao_iniciada:
            print(
                f'{Fore.GREEN}[LOG] Operação de inserção em memória finalizada.{Style.RESET_ALL}'
            )


def listar_faqs_memoria(lista):
    operacao_iniciada = False
    try:
        categoria = input(
            f'{Fore.CYAN}Filtrar por categoria (deixe vazio para todas): {Style.RESET_ALL}'
        ).strip()
        operacao_iniciada = True
        if categoria:
            faqs_filtrados = [
                faq
                for faq in lista
                if faq.get('categoria', '').lower() == categoria.lower()
            ]
        else:
            faqs_filtrados = lista
    except Exception as e:
        print(f'{Fore.RED}Erro ao listar FAQs em memória: {e}{Style.RESET_ALL}')
    else:
        if not faqs_filtrados:
            print(
                f'{Fore.YELLOW}Nenhum FAQ em memória{" com esta categoria" if categoria else ""}.{Style.RESET_ALL}'
            )
        else:
            try:
                for faq in faqs_filtrados:
                    ativo_texto = (
                        f'{Fore.GREEN}Sim{Style.RESET_ALL}'
                        if faq.get('ativo') == 1
                        else f'{Fore.RED}Não{Style.RESET_ALL}'
                    )
                    print(
                        f'{Fore.MAGENTA}ID:{Style.RESET_ALL} {faq["id"]}\n'
                        f'{Fore.MAGENTA}Pergunta:{Style.RESET_ALL} {faq["pergunta"]}\n'
                        f'{Fore.MAGENTA}Resposta:{Style.RESET_ALL} {faq.get("resposta", "")}\n'
                        f'{Fore.MAGENTA}Ativo:{Style.RESET_ALL} {ativo_texto}\n'
                        f'{Fore.MAGENTA}Atualizado em:{Style.RESET_ALL} {faq.get("atualizado_em", "")}\n'
                        f'{Fore.MAGENTA}Categoria:{Style.RESET_ALL} {faq.get("categoria", "")}\n'
                        f'{Fore.CYAN}{"-" * 30}{Style.RESET_ALL}'
                    )
                print(
                    f'{Fore.GREEN}Total de FAQs em memória{" nesta categoria" if categoria else ""}: {len(faqs_filtrados)}{Style.RESET_ALL}'
                )
            except KeyError as e:
                print(
                    f'{Fore.RED}Erro ao exibir FAQ: chave ausente - {e}{Style.RESET_ALL}'
                )
    finally:
        if operacao_iniciada:
            print(
                f'{Fore.GREEN}[LOG] Operação de listagem em memória finalizada.{Style.RESET_ALL}'
            )


def atualizar_faq_memoria(lista):
    operacao_iniciada = False
    try:
        id_str = input(
            f'{Fore.CYAN}Digite o ID do FAQ a atualizar: {Style.RESET_ALL}'
        ).strip()
        if not id_str.isdigit():
            print(f'{Fore.RED}ID deve ser um número inteiro.{Style.RESET_ALL}')
            return
        id = int(id_str)
        if not any(item['id'] == id for item in lista):
            print(f'{Fore.YELLOW}FAQ não encontrado.{Style.RESET_ALL}')
            return
        operacao_iniciada = True
    except Exception as e:
        print(
            f'{Fore.RED}Erro ao iniciar atualização do FAQ em memória: {e}{Style.RESET_ALL}'
        )
        return
    else:
        try:
            while True:
                print(
                    f'\n{Fore.BLUE}{Style.BRIGHT}--- Atualizar FAQ ---{Style.RESET_ALL}'
                )
                print(f'{Fore.WHITE}1. Atualizar Pergunta')
                print(f'{Fore.WHITE}2. Atualizar Resposta')
                print(f'{Fore.WHITE}3. Atualizar Categoria')
                print(f'{Fore.WHITE}4. Ativar/Desativar FAQ')
                print(f'{Fore.YELLOW}0. Voltar{Style.RESET_ALL}')
                opcao = input(
                    f'{Fore.GREEN}Escolha uma opção: {Style.RESET_ALL}'
                ).strip()
                if opcao == '1':
                    atualizar_pergunta_memoria(lista, id)
                elif opcao == '2':
                    atualizar_resposta_memoria(lista, id)
                elif opcao == '3':
                    atualizar_categoria_memoria(lista, id)
                elif opcao == '4':
                    ativar_desativar_faq_memoria(lista, id)
                elif opcao == '0':
                    break
                else:
                    print(
                        f'{Fore.RED}Opção inválida! Digite o número da opção desejada.{Style.RESET_ALL}'
                    )
        except Exception as e:
            print(f'{Fore.RED}Erro ao atualizar FAQ em memória: {e}{Style.RESET_ALL}')
    finally:
        if operacao_iniciada:
            print(
                f'{Fore.GREEN}[LOG] Operação de atualização em memória finalizada.{Style.RESET_ALL}'
            )


def atualizar_pergunta_memoria(lista, id):
    nova_pergunta = input(
        f'{Fore.CYAN}Digite a nova pergunta (ou 0 para cancelar): {Style.RESET_ALL}'
    ).strip()
    if nova_pergunta == '0':
        print(
            f'{Fore.YELLOW}Operação cancelada. Pergunta não foi alterada.{Style.RESET_ALL}'
        )
        return
    if nova_pergunta:
        for item in lista:
            if item['id'] == id:
                item['pergunta'] = nova_pergunta
                item['atualizado_em'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(f'{Fore.GREEN}Pergunta atualizada com sucesso!{Style.RESET_ALL}')
                break
    else:
        print(f'{Fore.RED}Pergunta não pode ser vazia.{Style.RESET_ALL}')


def atualizar_resposta_memoria(lista, id):
    nova_resposta = input(
        f'{Fore.CYAN}Digite a nova resposta (ou 0 para cancelar): {Style.RESET_ALL}'
    ).strip()
    if nova_resposta == '0':
        print(f'{Fore.YELLOW}Atualização de resposta cancelada.{Style.RESET_ALL}')
        return
    if nova_resposta:
        for item in lista:
            if item['id'] == id:
                item['resposta'] = nova_resposta
                item['atualizado_em'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(f'{Fore.GREEN}Resposta atualizada com sucesso!{Style.RESET_ALL}')
                break
    else:
        print(f'{Fore.RED}Resposta não pode ser vazia.{Style.RESET_ALL}')


def atualizar_categoria_memoria(lista, id):
    nova_categoria = input(
        f'{Fore.CYAN}Digite a nova categoria (ou 0 para cancelar): {Style.RESET_ALL}'
    ).strip()
    if nova_categoria == '0':
        print(f'{Fore.YELLOW}Atualização de categoria cancelada.{Style.RESET_ALL}')
        return
    if nova_categoria:
        print(
            f'{Fore.BLUE}Categoria será salva como: {nova_categoria.upper()}{Style.RESET_ALL}'
        )
        for item in lista:
            if item['id'] == id:
                item['categoria'] = nova_categoria.upper()
                item['atualizado_em'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(f'{Fore.GREEN}Categoria atualizada com sucesso!{Style.RESET_ALL}')
                break
    else:
        print(f'{Fore.RED}Categoria não pode ser vazia.{Style.RESET_ALL}')


def ativar_desativar_faq_memoria(lista, id):
    faq = None
    for item in lista:
        if item['id'] == id:
            faq = item
            break
    if not faq:
        print(
            f'{Fore.RED}Erro: FAQ com ID {id} não está mais disponível.{Style.RESET_ALL}'
        )
        return
    status_atual = 'ativado' if faq['ativo'] == 1 else 'desativado'
    status_cor = Fore.GREEN if faq['ativo'] == 1 else Fore.RED
    print(
        f'\n{Fore.CYAN}Status atual do FAQ: {status_cor}{status_atual}{Style.RESET_ALL}'
    )
    print(
        f'{Fore.WHITE}Opções: {Fore.GREEN}1-Ativar FAQ | {Fore.RED}0-Desativar FAQ | {Fore.YELLOW}C-Cancelar{Style.RESET_ALL}'
    )
    escolha = input(f'{Fore.CYAN}Escolha: {Style.RESET_ALL}').strip().upper()
    if escolha == 'C':
        print(
            f'{Fore.YELLOW}Operação cancelada. Status não foi alterado.{Style.RESET_ALL}'
        )
        return
    if escolha not in ['0', '1']:
        print(f'{Fore.RED}Opção inválida. Status não foi alterado.{Style.RESET_ALL}')
        return
    novo_status = int(escolha)
    if faq['ativo'] == novo_status:
        print(f'{Fore.YELLOW}O FAQ já está com este status.{Style.RESET_ALL}')
        return
    faq['ativo'] = novo_status
    faq['atualizado_em'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f'{Fore.GREEN}Status de ativação atualizado com sucesso!{Style.RESET_ALL}')


def remover_faq_memoria(lista):
    operacao_iniciada = False
    try:
        id_str = input(
            f'{Fore.CYAN}Digite o ID do FAQ a deletar: {Style.RESET_ALL}'
        ).strip()
        if not id_str.isdigit():
            print(f'{Fore.RED}ID deve ser um número inteiro.{Style.RESET_ALL}')
            return
        id = int(id_str)
        if not any(item['id'] == id for item in lista):
            print(f'{Fore.YELLOW}FAQ não encontrado.{Style.RESET_ALL}')
            return
        operacao_iniciada = True
        confirmacao = (
            input(
                f'{Fore.YELLOW}{Style.BRIGHT}Pressione Enter para confirmar a exclusão ou C para cancelar: {Style.RESET_ALL}'
            )
            .strip()
            .upper()
        )
        if confirmacao == 'C':
            print(
                f'{Fore.GREEN}Operação cancelada. Nenhuma alteração foi feita.{Style.RESET_ALL}'
            )
            return
        lista_original = lista.copy()
        lista[:] = [item for item in lista if item['id'] != id]
        if len(lista) == len(lista_original):
            raise ValueError(f'Não foi possível remover o FAQ com ID {id}')
    except Exception as e:
        print(f'{Fore.RED}Erro ao remover FAQ da memória: {e}{Style.RESET_ALL}')
    else:
        print(f'{Fore.GREEN}FAQ removido em memória!{Style.RESET_ALL}')
    finally:
        if operacao_iniciada:
            print(
                f'{Fore.GREEN}[LOG] Operação de exclusão em memória finalizada.{Style.RESET_ALL}'
            )


def buscar_faq_memoria(lista):
    operacao_iniciada = False
    try:
        id_str = input(f'{Fore.CYAN}Digite o ID do FAQ: {Style.RESET_ALL}').strip()
        if not id_str.isdigit():
            print(f'{Fore.RED}ID deve ser um número inteiro.{Style.RESET_ALL}')
            return
        id = int(id_str)
        operacao_iniciada = True
        encontrados = [item for item in lista if item['id'] == id]
    except Exception as e:
        print(f'{Fore.RED}Erro ao buscar FAQ em memória: {e}{Style.RESET_ALL}')
    else:
        if encontrados:
            for faq in encontrados:
                try:
                    ativo_texto = (
                        f'{Fore.GREEN}Sim{Style.RESET_ALL}'
                        if faq.get('ativo') == 1
                        else f'{Fore.RED}Não{Style.RESET_ALL}'
                    )
                    print(
                        f'{Fore.MAGENTA}ID:{Style.RESET_ALL} {faq["id"]}\n'
                        f'{Fore.MAGENTA}Pergunta:{Style.RESET_ALL} {faq["pergunta"]}\n'
                        f'{Fore.MAGENTA}Resposta:{Style.RESET_ALL} {faq.get("resposta", "")}\n'
                        f'{Fore.MAGENTA}Ativo:{Style.RESET_ALL} {ativo_texto}\n'
                        f'{Fore.MAGENTA}Atualizado em:{Style.RESET_ALL} {faq.get("atualizado_em", "")}\n'
                        f'{Fore.MAGENTA}Categoria:{Style.RESET_ALL} {faq.get("categoria", "")}\n'
                        f'{Fore.CYAN}{"-" * 30}{Style.RESET_ALL}'
                    )
                except KeyError as e:
                    print(
                        f'{Fore.RED}Erro ao exibir FAQ: chave ausente - {e}{Style.RESET_ALL}'
                    )
        else:
            print(
                f'{Fore.RED}FAQ com ID {id} não encontrado em memória.{Style.RESET_ALL}'
            )
    finally:
        if operacao_iniciada:
            print(
                f'{Fore.GREEN}[LOG] Operação de busca em memória finalizada.{Style.RESET_ALL}'
            )


# --- Menu interativo de memória ---
class MenuMemoria:
    def __init__(self, faqs_memoria=None):
        self.faqs_memoria = faqs_memoria if faqs_memoria is not None else []
        pasta_memoria = os.path.abspath(
            os.path.join(os.path.dirname(__file__), 'data', 'memoria')
        )
        os.makedirs(pasta_memoria, exist_ok=True)
        self.caminho_json = os.path.join(pasta_memoria, 'faq_export.json')

    def menu_memoria(self):
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
