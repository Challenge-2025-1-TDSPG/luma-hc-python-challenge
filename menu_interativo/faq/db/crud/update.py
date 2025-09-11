"""
Operações de atualização (Update) para FAQ.
"""

import logging

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
    categoria = categoria.strip()

    # Validações básicas
    if ativo not in (0, 1):
        raise ValueError('ativo deve ser 0 ou 1')
    if len(pergunta) > MAX_PERGUNTA_LEN:
        raise ValueError(f'pergunta excede {MAX_PERGUNTA_LEN} caracteres')
    if len(resposta) > MAX_RESPOSTA_LEN:
        raise ValueError(f'resposta excede {MAX_RESPOSTA_LEN} caracteres')
    if len(categoria) > MAX_CATEGORIA_LEN:
        raise ValueError(f'categoria excede {MAX_CATEGORIA_LEN} caracteres')
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
            logger.info(f'FAQ ID {id} atualizada com sucesso.')
        return rows_affected > 0  # Retorna True se algum registro foi atualizado
    except Exception as e:
        if conn.conn:
            conn.conn.rollback()  # Desfaz a transação em caso de erro
        # Tratamento específico para erros comuns do Oracle
        msg = str(e)
        if 'ORA-00001' in msg:
            logger.warning('Pergunta já cadastrada (violação de UNIQUE).')
        elif 'ORA-12899' in msg:
            logger.warning(
                'Valor excede o tamanho permitido para a coluna (ORA-12899).'
            )
        else:
            logger.error(f'Erro ao atualizar FAQ: {e}')
        return False
