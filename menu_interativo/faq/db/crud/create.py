"""
Operações de criação (Create) para FAQ.
"""

import logging

from ..queries import MAX_CATEGORIA_LEN, MAX_PERGUNTA_LEN, MAX_RESPOSTA_LEN, SQL_INSERT

# Configuração de logging
logger = logging.getLogger(__name__)


def adicionar(conn, pergunta, resposta, ativo, categoria):
    """Adiciona um novo registro FAQ na tabela.

    Args:
        conn: Conexão com o banco de dados
        pergunta (str): Pergunta do FAQ
        resposta (str): Resposta do FAQ
        ativo (int): Status de ativação (1 para ativo, 0 para inativo)
        categoria (str): Categoria do FAQ

    Returns:
        bool: True se a operação foi bem-sucedida, False caso contrário
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
        # Executa o INSERT com os parâmetros validados
        conn.cursor.execute(SQL_INSERT, (pergunta, resposta, ativo, categoria))
        # Confirma a transação no banco
        conn.conn.commit()
        logger.info('FAQ adicionada com sucesso!')
        return True
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
            logger.error(f'Erro ao adicionar FAQ: {e}')
        return False
