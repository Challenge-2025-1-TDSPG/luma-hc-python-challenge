"""
Operações de atualização (Update) para FAQ.
"""

import logging

from colorama import Fore, Style

from ..queries import MAX_CATEGORIA_LEN, MAX_PERGUNTA_LEN, MAX_RESPOSTA_LEN, SQL_UPDATE

# Configuração de logging
logger = logging.getLogger(__name__)


def atualizar(conn, id, pergunta, resposta, ativo, categoria):
    """Atualiza um FAQ existente pelo ID.

    Args:
        conn: Conexão com o banco de dados
        id (int): ID do FAQ a ser atualizado
        pergunta (str): Nova pergunta do FAQ
        resposta (str): Nova resposta do FAQ
        ativo (int): Novo status de ativação (1 para ativo, 0 para inativo)
        categoria (str): Nova categoria do FAQ

    Returns:
        bool: True se a atualização foi bem-sucedida, False caso contrário
    """
    # Normalização de entrada (remove espaços em branco extras)
    pergunta = pergunta.strip()
    resposta = resposta.strip()
    categoria = categoria.strip().upper()  # Converte para maiúsculo para consistência

    # Validações básicas
    if ativo not in (0, 1):
        error_msg = f'{Fore.RED}ativo deve ser 0 ou 1{Style.RESET_ALL}'
        raise ValueError(error_msg)
    if len(pergunta) > MAX_PERGUNTA_LEN:
        error_msg = (
            f'{Fore.RED}pergunta excede {MAX_PERGUNTA_LEN} caracteres{Style.RESET_ALL}'
        )
        raise ValueError(error_msg)
    if len(resposta) > MAX_RESPOSTA_LEN:
        error_msg = (
            f'{Fore.RED}resposta excede {MAX_RESPOSTA_LEN} caracteres{Style.RESET_ALL}'
        )
        raise ValueError(error_msg)
    if len(categoria) > MAX_CATEGORIA_LEN:
        error_msg = f'{Fore.RED}categoria excede {MAX_CATEGORIA_LEN} caracteres{Style.RESET_ALL}'
        raise ValueError(error_msg)
    try:
        # Executa o UPDATE com todos os parâmetros na ordem correta (:1, :2, ...)
        # A ordem é: pergunta, resposta, ativo, categoria, id
        conn.cursor.execute(
            SQL_UPDATE,
            (pergunta, resposta, ativo, categoria, id),
        )
        # rowcount indica quantas linhas foram afetadas (deve ser 1 para sucesso)
        rows_affected = conn.cursor.rowcount
        conn.conn.commit()
        if rows_affected > 0:
            logger.info(
                f'{Fore.GREEN}FAQ ID {id} atualizada com sucesso.{Style.RESET_ALL}'
            )
        return rows_affected > 0  # Retorna True se algum registro foi atualizado
    except Exception as e:
        if conn.conn:
            conn.conn.rollback()  # Desfaz a transação em caso de erro
        # Tratamento específico para erros comuns do Oracle
        msg = str(e)
        if 'ORA-00001' in msg:
            logger.warning(
                f'{Fore.YELLOW}Pergunta já cadastrada (violação de UNIQUE).{Style.RESET_ALL}'
            )
        elif 'ORA-12899' in msg:
            logger.warning(
                f'{Fore.YELLOW}Valor excede o tamanho permitido para a coluna (ORA-12899).{Style.RESET_ALL}'
            )
        else:
            logger.error(f'{Fore.RED}Erro ao atualizar FAQ: {e}{Style.RESET_ALL}')
        return False
