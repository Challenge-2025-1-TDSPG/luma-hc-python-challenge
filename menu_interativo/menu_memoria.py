"""
Módulo consolidado de operações CRUD de FAQs em memória para o sistema FAQ.
Inclui funções de adicionar, listar, atualizar, deletar, buscar e o menu interativo.
"""

from datetime import datetime

from config.settings import (
    COLOR_ERROR,
    COLOR_INFO,
    COLOR_MAGENTA,
    COLOR_OPTION,
    COLOR_PROMPT,
    COLOR_RESET,
    COLOR_SUCCESS,
    COLOR_TITLE,
    COLOR_WARNING,
    DATETIME_FORMAT,
    MENU_BACK_KEYS,
    MENU_INVALID_OPTION,
    MSG_ATIVO_INVALIDO,
    MSG_CANCELADO,
    MSG_CONFIRMA_CANCELA_CATEGORIA,
    MSG_CONFIRMA_CANCELA_PERGUNTA,
    MSG_CONFIRMA_CANCELA_RESPOSTA,
    MSG_CONFIRMA_CANCELA_STATUS,
    MSG_FAQ_ADICIONADO,
    MSG_FAQ_JA_EXISTE,
    MSG_FAQ_LISTA_VAZIA,
    MSG_FAQ_NAO_ENCONTRADO,
    MSG_FAQ_REMOVIDO,
    MSG_FAQ_STATUS_ATUALIZADO,
    PROMPT_ATIVO,
    PROMPT_CATEGORIA,
    PROMPT_CONFIRMA_EXCLUSAO,
    PROMPT_FILTRAR_CATEGORIA,
    PROMPT_PERGUNTA,
    PROMPT_RESPOSTA,
    input_id,
    is_not_empty,
    show_message,
    validar_campos_obrigatorios,
)
from exportacao import exportar_faqs_memoria, importar_faqs_memoria
from models import FAQ


# --- Funções CRUD em memória ---
def adicionar_faq_memoria(lista):
    """
    Adiciona um novo FAQ à lista em memória.
    Args:
        lista (list): Lista de objetos FAQ.
    """
    # operacao_iniciada removida
    try:
        id = input_id()
        pergunta = input(PROMPT_PERGUNTA).strip()
        resposta = input(PROMPT_RESPOSTA).strip()
        categoria = input(PROMPT_CATEGORIA).strip()
        if categoria:
            show_message(f'Categoria será salva como: {categoria.upper()}', 'info')
        ativo_str = input(PROMPT_ATIVO).strip()
        if not validar_campos_obrigatorios(pergunta, resposta, categoria):
            return
        while ativo_str not in ['0', '1']:
            show_message(MSG_ATIVO_INVALIDO, 'error')
            ativo_str = input(PROMPT_ATIVO).strip()
        if any(item.id == id for item in lista):
            show_message(MSG_FAQ_JA_EXISTE, 'warning')
            return
        operacao_iniciada = True
        ativo = int(ativo_str)
        atualizado_em = datetime.now().strftime(DATETIME_FORMAT)
        novo_faq = FAQ(id, pergunta, resposta, ativo, atualizado_em, categoria.upper())
        lista.append(novo_faq)
    except Exception as e:
        show_message(f'Erro ao adicionar FAQ em memória: {e}', 'error')
    else:
        show_message(MSG_FAQ_ADICIONADO, 'success')
        print(novo_faq)
    # Log removido para não poluir interface


def listar_faqs_memoria(lista):
    """
    Lista todos os FAQs em memória, com opção de filtrar por categoria.
    Args:
        lista (list): Lista de objetos FAQ.
    """
    # operacao_iniciada removida
    try:
        categoria = input(PROMPT_FILTRAR_CATEGORIA).strip()
        operacao_iniciada = True
        if categoria:
            faqs_filtrados = [
                faq for faq in lista if faq.categoria.lower() == categoria.lower()
            ]
        else:
            faqs_filtrados = lista
    except Exception as e:
        show_message(f'Erro ao listar FAQs em memória: {e}', 'error')
    else:
        if not faqs_filtrados:
            show_message(
                f'{MSG_FAQ_LISTA_VAZIA + (" com esta categoria" if categoria else "")}',
                'warning',
            )
        else:
            for faq in faqs_filtrados:
                print(faq)
                print('-' * 40)
            show_message(
                f'Total de FAQs em memória{" nesta categoria" if categoria else ""}: {len(faqs_filtrados)}',
                'success',
            )
    # Log removido para não poluir interface


def atualizar_faq_memoria(lista):
    """
    Atualiza um FAQ existente em memória, permitindo alterar pergunta, resposta, categoria ou status.
    Args:
        lista (list): Lista de objetos FAQ.
    """
    # operacao_iniciada removida
    try:
        id = input_id(f'{COLOR_PROMPT}Digite o ID do FAQ a atualizar: {COLOR_RESET}')
        if not any(item.id == id for item in lista):
            show_message(MSG_FAQ_NAO_ENCONTRADO, 'warning')
            return
        operacao_iniciada = True
    except Exception as e:
        show_message(f'Erro ao iniciar atualização do FAQ em memória: {e}', 'error')
        return
    else:
        try:
            while True:
                print(f'\n{COLOR_TITLE}--- Atualizar FAQ ---{COLOR_RESET}')
                print(f'{COLOR_OPTION}1. Atualizar Pergunta')
                print(f'{COLOR_OPTION}2. Atualizar Resposta')
                print(f'{COLOR_OPTION}3. Atualizar Categoria')
                print(f'{COLOR_OPTION}4. Ativar/Desativar FAQ')
                print(f'{COLOR_WARNING}0. Voltar{COLOR_RESET}')
                opcao = input(
                    f'{COLOR_PROMPT}Escolha uma opção ({MENU_BACK_KEYS}): {COLOR_RESET}'
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
                    show_message(MENU_INVALID_OPTION, 'error')
        except Exception as e:
            show_message(f'Erro ao atualizar FAQ em memória: {e}', 'error')
    # Log removido para não poluir interface


def atualizar_pergunta_memoria(lista, id):
    """
    Atualiza a pergunta de um FAQ específico.
    Args:
        lista (list): Lista de objetos FAQ.
        id (int): ID do FAQ a ser atualizado.
    """
    nova_pergunta = input(
        f'{COLOR_PROMPT}Digite a nova pergunta (ou 0 para cancelar): {COLOR_RESET}'
    ).strip()
    if nova_pergunta == '0':
        show_message(MSG_CONFIRMA_CANCELA_PERGUNTA, 'warning')
        return
    if is_not_empty(nova_pergunta):
        for item in lista:
            if item.id == id:
                item.pergunta = nova_pergunta
                item.atualizado_em = datetime.now().strftime(DATETIME_FORMAT)
                show_message('Pergunta atualizada com sucesso!', 'success')
                break
    else:
        show_message('Pergunta não pode ser vazia.', 'error')


def atualizar_resposta_memoria(lista, id):
    """
    Atualiza a resposta de um FAQ específico.
    Args:
        lista (list): Lista de objetos FAQ.
        id (int): ID do FAQ a ser atualizado.
    """
    nova_resposta = input(
        f'{COLOR_PROMPT}Digite a nova resposta (ou 0 para cancelar): {COLOR_RESET}'
    ).strip()
    if nova_resposta == '0':
        show_message(MSG_CONFIRMA_CANCELA_RESPOSTA, 'warning')
        return
    if is_not_empty(nova_resposta):
        for item in lista:
            if item.id == id:
                item.resposta = nova_resposta
                item.atualizado_em = datetime.now().strftime(DATETIME_FORMAT)
                show_message('Resposta atualizada com sucesso!', 'success')
                break
    else:
        show_message('Resposta não pode ser vazia.', 'error')


def atualizar_categoria_memoria(lista, id):
    """
    Atualiza a categoria de um FAQ específico.
    Args:
        lista (list): Lista de objetos FAQ.
        id (int): ID do FAQ a ser atualizado.
    """
    nova_categoria = input(
        f'{COLOR_PROMPT}Digite a nova categoria (ou 0 para cancelar): {COLOR_RESET}'
    ).strip()
    if nova_categoria == '0':
        show_message(MSG_CONFIRMA_CANCELA_CATEGORIA, 'warning')
        return
    if is_not_empty(nova_categoria):
        show_message(f'Categoria será salva como: {nova_categoria.upper()}', 'info')
        for item in lista:
            if item.id == id:
                item.categoria = nova_categoria.upper()
                item.atualizado_em = datetime.now().strftime(DATETIME_FORMAT)
                show_message('Categoria atualizada com sucesso!', 'success')
                break
    else:
        show_message('Categoria não pode ser vazia.', 'error')


def ativar_desativar_faq_memoria(lista, id):
    """
    Ativa ou desativa um FAQ em memória.
    Args:
        lista (list): Lista de objetos FAQ.
        id (int): ID do FAQ a ser alterado.
    """
    faq = None
    for item in lista:
        if item.id == id:
            faq = item
            break
    if not faq:
        show_message(f'Erro: FAQ com ID {id} não está mais disponível.', 'error')
        return
    status_atual = 'ativado' if faq.ativo == 1 else 'desativado'
    status_cor = COLOR_SUCCESS if faq.ativo == 1 else COLOR_ERROR
    print(f'\n{COLOR_INFO}Status atual do FAQ: {status_cor}{status_atual}{COLOR_RESET}')
    print(
        f'{COLOR_OPTION}Opções: {COLOR_SUCCESS}1-Ativar FAQ | {COLOR_ERROR}0-Desativar FAQ | {COLOR_WARNING}C-Cancelar{COLOR_RESET}'
    )
    escolha = input(f'{COLOR_PROMPT}Escolha: {COLOR_RESET}').strip().upper()
    if escolha == 'C':
        show_message(MSG_CONFIRMA_CANCELA_STATUS, 'warning')
        return
    if escolha not in ['0', '1']:
        show_message('Opção inválida. Status não foi alterado.', 'error')
        return
    novo_status = int(escolha)
    if faq.ativo == novo_status:
        show_message('O FAQ já está com este status.', 'warning')
        return
    faq.ativo = novo_status
    faq.atualizado_em = datetime.now().strftime(DATETIME_FORMAT)
    show_message(MSG_FAQ_STATUS_ATUALIZADO, 'success')


def remover_faq_memoria(lista):
    """
    Remove um FAQ da lista em memória pelo ID informado.
    Args:
        lista (list): Lista de objetos FAQ.
    """
    # operacao_iniciada removida
    try:
        id = input_id(f'{COLOR_PROMPT}Digite o ID do FAQ a deletar: {COLOR_RESET}')
        if not any(item.id == id for item in lista):
            show_message(MSG_FAQ_NAO_ENCONTRADO, 'warning')
            return
        operacao_iniciada = True
        confirmacao = input(PROMPT_CONFIRMA_EXCLUSAO).strip().upper()
        if confirmacao == 'C':
            show_message(MSG_CANCELADO, 'success')
            return
        lista_original = lista.copy()
        lista[:] = [item for item in lista if item.id != id]
        if len(lista) == len(lista_original):
            raise ValueError(f'Não foi possível remover o FAQ com ID {id}')
    except Exception as e:
        show_message(f'Erro ao remover FAQ da memória: {e}', 'error')
    else:
        show_message(MSG_FAQ_REMOVIDO, 'success')
    # Log removido para não poluir interface


def buscar_faq_memoria(lista):
    """
    Busca e exibe um FAQ pelo ID informado.
    Args:
        lista (list): Lista de objetos FAQ.
    """
    # operacao_iniciada removida
    try:
        id = input_id()
        operacao_iniciada = True
        encontrados = [item for item in lista if item.id == id]
    except Exception as e:
        show_message(f'Erro ao buscar FAQ em memória: {e}', 'error')
    else:
        if encontrados:
            for faq in encontrados:
                print(faq)
        else:
            show_message(f'FAQ com ID {id} não encontrado em memória.', 'error')
    # Log removido para não poluir interface


# --- Menu interativo de memória ---
class MenuMemoria:
    """
    Classe para o menu interativo do CRUD de FAQs em memória.
    Permite executar operações de adicionar, listar, atualizar, remover e buscar FAQs.
    """

    def __init__(self, faqs_memoria=None):
        """
        Inicializa o menu de memória com uma lista de FAQs.
        Carrega do JSON se existir, senão inicia vazia.
        """
        if faqs_memoria is not None:
            self.faqs_memoria = faqs_memoria
        else:
            self.faqs_memoria = importar_faqs_memoria()

    def menu_memoria(self):
        """
        Exibe o menu interativo para operações CRUD em memória.
        """
        while True:
            print(
                f'\n{COLOR_MAGENTA}{COLOR_TITLE}--- CRUD FAQ EM MEMÓRIA ---{COLOR_RESET}'
            )
            print(f'{COLOR_OPTION}1. Adicionar FAQ')
            print(f'{COLOR_OPTION}2. Listar FAQs')
            print(f'{COLOR_OPTION}3. Atualizar FAQ')
            print(f'{COLOR_OPTION}4. Deletar FAQ')
            print(f'{COLOR_OPTION}5. Buscar FAQ por ID')
            # print(f'{COLOR_WARNING}{MENU_BACK_KEYS}{COLOR_RESET}')
            opcao = (
                input(
                    f'{COLOR_PROMPT}Escolha uma opção ({MENU_BACK_KEYS}): {COLOR_RESET}'
                )
                .strip()
                .lower()
            )
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
            elif opcao in ['0', 'v']:
                break
            else:
                show_message(MENU_INVALID_OPTION, 'error')

    def sync_from_json(self):
        self.faqs_memoria = importar_faqs_memoria()

    def sync_to_json(self):
        exportar_faqs_memoria(self.faqs_memoria)

    def listar_faqs_memoria(self):
        """
        Lista todos os FAQs em memória (sempre recarrega do JSON).
        """
        self.sync_from_json()
        listar_faqs_memoria(self.faqs_memoria)

    def adicionar_faq_memoria(self):
        """
        Adiciona um novo FAQ em memória (recarrega do JSON antes, exporta depois).
        """
        self.sync_from_json()
        adicionar_faq_memoria(self.faqs_memoria)
        self.sync_to_json()

    def atualizar_faq_memoria(self):
        """
        Atualiza um FAQ existente em memória (recarrega do JSON antes, exporta depois).
        """
        self.sync_from_json()
        atualizar_faq_memoria(self.faqs_memoria)
        self.sync_to_json()

    def remover_faq_memoria(self):
        """
        Remove um FAQ em memória (recarrega do JSON antes, exporta depois).
        """
        self.sync_from_json()
        remover_faq_memoria(self.faqs_memoria)
        self.sync_to_json()

    def buscar_faq_memoria(self):
        """
        Busca um FAQ em memória pelo ID (recarrega do JSON antes).
        """
        self.sync_from_json()
        buscar_faq_memoria(self.faqs_memoria)
