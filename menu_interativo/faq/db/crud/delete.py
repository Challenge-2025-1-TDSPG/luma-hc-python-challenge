"""
Operações de exclusão (Delete) para FAQ.
"""

import logging

from colorama import Fore, Style

from ..queries import SQL_DELETE

# Configuração de logging
logger = logging.getLogger(__name__)


def deletar(conn, id):
    """Remove um FAQ pelo seu ID.

    Args:
        conn: Conexão com o banco de dados
        id (int): ID do FAQ a ser removido

    Returns:
        bool: True se a remoção foi bem-sucedida, False caso contrário
    """
    try:
        conn.cursor.execute(SQL_DELETE, (id,))
        rows_affected = conn.cursor.rowcount
        conn.conn.commit()
        if rows_affected > 0:
            logger.info(
                f'{Fore.GREEN}FAQ ID {id} deletada com sucesso.{Style.RESET_ALL}'
            )
        else:
            logger.warning(
                f'{Fore.YELLOW}FAQ ID {id} não encontrada para exclusão.{Style.RESET_ALL}'
            )
        return rows_affected > 0  # Retorna True se algum registro foi excluído
    except Exception as e:
        if conn.conn:
            conn.conn.rollback()  # Desfaz a transação em caso de erro
        logger.error(f'{Fore.RED}Erro ao deletar FAQ: {e}{Style.RESET_ALL}')
        return False
