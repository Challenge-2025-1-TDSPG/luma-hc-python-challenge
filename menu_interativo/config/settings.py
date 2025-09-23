"""
Configurações globais e utilitários para o sistema FAQ.
Centraliza variáveis de ambiente, caminhos e funções comuns.
"""

import os

from colorama import Fore, Style
from dotenv import load_dotenv

# --- Cores e estilos padronizados ---
COLOR_TITLE = Fore.CYAN + Style.BRIGHT
COLOR_OPTION = Fore.WHITE
COLOR_PROMPT = Fore.GREEN
COLOR_WARNING = Fore.YELLOW
COLOR_ERROR = Fore.RED
COLOR_SUCCESS = Fore.GREEN
COLOR_INFO = Fore.CYAN
COLOR_RESET = Style.RESET_ALL
COLOR_MAGENTA = Fore.MAGENTA

# --- Formato de data padrão ---
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'

# --- Prompts e mensagens padrão ---
PROMPT_ID = f'{COLOR_PROMPT}Digite o ID do FAQ: {COLOR_RESET}'
PROMPT_PERGUNTA = f'{COLOR_PROMPT}Digite a pergunta: {COLOR_RESET}'
PROMPT_RESPOSTA = f'{COLOR_PROMPT}Digite a resposta: {COLOR_RESET}'
PROMPT_CATEGORIA = f'{COLOR_PROMPT}Digite o nome da categoria: {COLOR_RESET}'
PROMPT_ATIVO = f'{COLOR_PROMPT}Ativo? (1-Sim, 0-Não): {COLOR_RESET}'
PROMPT_CONFIRMA_EXCLUSAO = f'{COLOR_WARNING}{Style.BRIGHT}Pressione Enter para confirmar a exclusão ou C para cancelar: {COLOR_RESET}'
PROMPT_FILTRAR_CATEGORIA = (
    f'{COLOR_PROMPT}Filtrar por categoria (deixe vazio para todas): {COLOR_RESET}'
)
PROMPT_CONFIRMA_SAIR = (
    f'{COLOR_WARNING}Tem certeza que deseja sair? (s/n): {COLOR_RESET}'
)

# --- Mensagens padrão de confirmação/cancelamento ---
MSG_CANCELADO = 'Operação cancelada. Nenhuma alteração foi feita.'
MSG_CONFIRMA_CANCELA_PERGUNTA = 'Operação cancelada. Pergunta não foi alterada.'
MSG_CONFIRMA_CANCELA_RESPOSTA = 'Atualização de resposta cancelada.'
MSG_CONFIRMA_CANCELA_CATEGORIA = 'Atualização de categoria cancelada.'
MSG_CONFIRMA_CANCELA_STATUS = 'Operação cancelada. Status não foi alterado.'
MSG_ID_INVALIDO = 'ID deve ser um número inteiro.'
MSG_FAQ_NAO_ENCONTRADO = 'FAQ não encontrado.'
MSG_FAQ_JA_EXISTE = 'Já existe um FAQ com esse ID.'
MSG_CAMPOS_OBRIGATORIOS = 'Todos os campos são obrigatórios!'
MSG_ATIVO_INVALIDO = 'Valor para "Ativo" deve ser 1 (Sim) ou 0 (Não).'
MSG_FAQ_REMOVIDO = 'FAQ removido em memória!'
MSG_FAQ_ADICIONADO = 'FAQ adicionado com sucesso!'
MSG_FAQ_ATUALIZADO = 'FAQ atualizado com sucesso!'
MSG_FAQ_STATUS_ATUALIZADO = 'Status de ativação atualizado com sucesso!'
MSG_FAQ_LISTA_VAZIA = 'Nenhum FAQ em memória.'

load_dotenv(
    dotenv_path=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.env'))
)


# --- Funções utilitárias de validação ---
def is_int(value):
    try:
        int(value)
        return True
    except (ValueError, TypeError):
        return False


def is_not_empty(value):
    return bool(value and str(value).strip())


# Caminhos padrão
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
JSON_MEMORIA_PATH = os.path.join(BASE_DIR, 'json', 'memoria', 'faq_export.json')


# Mensagens padrão
SUCCESS = f'{Fore.GREEN}Operação realizada com sucesso!{Style.RESET_ALL}'
ERROR = f'{Fore.RED}Ocorreu um erro!{Style.RESET_ALL}'
WARNING = f'{Fore.YELLOW}Atenção!{Style.RESET_ALL}'

# Mensagens de exportação/importação
MSG_EXPORT_MEMORIA_OK = 'Exportação realizada com sucesso para {path}!'
MSG_EXPORT_JSON_ERROR = 'Erro ao exportar para JSON: {erro}'
MSG_EXPORT_MEMORIA_ERROR = 'Erro ao exportar FAQs para JSON: {erro}'
MSG_IMPORT_MEMORIA_OK = 'FAQs importados do JSON com sucesso!'
MSG_IMPORT_MEMORIA_WARN = 'Nenhum arquivo JSON válido encontrado para importar.'
MSG_IMPORT_MEMORIA_ERROR = 'Erro ao importar FAQs do JSON: {erro}'

# Strings de navegação e atalhos de menus
MENU_BACK_KEYS = '0/v para voltar'
MENU_EXIT_KEYS = '0/s para sair'
MENU_CONFIRM_EXIT = 'Tem certeza que deseja sair? (s/n): '
MENU_INVALID_OPTION = 'Opção inválida! Digite o número ou atalho da opção desejada.'
MENU_EXITING = 'Saindo...'
MENU_EXIT_CANCEL = 'Operação de saída cancelada. Retornando ao menu.'


# Função utilitária para exibir mensagens padronizadas
def show_message(msg, tipo='info'):
    if tipo == 'success':
        print(f'{Fore.GREEN}{msg}{Style.RESET_ALL}')
    elif tipo == 'error':
        print(f'{Fore.RED}{msg}{Style.RESET_ALL}')
    elif tipo == 'warning':
        print(f'{Fore.YELLOW}{msg}{Style.RESET_ALL}')
    else:
        print(f'{Fore.CYAN}{msg}{Style.RESET_ALL}')


# --- Funções utilitárias para input e validação centralizada ---
def input_id(prompt=PROMPT_ID):
    """Solicita e valida um ID inteiro do usuário."""
    id_str = input(prompt).strip()
    while not is_int(id_str):
        show_message(MSG_ID_INVALIDO, 'error')
        id_str = input(prompt).strip()
    return int(id_str)


def confirmar_acao(msg=MENU_CONFIRM_EXIT):
    """Solicita confirmação do usuário para uma ação (retorna True para 's')."""
    confirm = input(f'{COLOR_WARNING}{msg}{COLOR_RESET}').strip().lower()
    return confirm == 's'


def validar_campos_obrigatorios(*args):
    """Valida se todos os campos obrigatórios foram preenchidos."""
    if not all(is_not_empty(arg) for arg in args):
        show_message(MSG_CAMPOS_OBRIGATORIOS, 'error')
        return False
    return True
