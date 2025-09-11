"""
Operações de leitura (Read) para FAQ.
"""

import logging

from ...models import FAQ
from ..queries import (
    SQL_SELECT_ALL,
    SQL_SELECT_BY_CATEGORY,
    SQL_SELECT_BY_CATEGORY_WITH_LIMIT,
    SQL_SELECT_BY_ID,
    SQL_SELECT_DISTINCT_CATEGORIES,
    SQL_SELECT_WITH_LIMIT,
)

# Configuração de logging
logger = logging.getLogger(__name__)


def listar(conn, categoria=None, limit=None):
    """Lista todos os FAQs ou filtra por categoria, com opção de limitar o número de resultados.

    Args:
        conn: Conexão com o banco de dados
        categoria (str, optional): Categoria para filtrar.
                                   Se None, retorna todos os FAQs.
        limit (int, optional): Limita o número de resultados.
                              Se None, retorna todos os resultados.

    Returns:
        list: Lista de objetos FAQ encontrados
    """
    try:
        if categoria:
            if limit:
                conn.cursor.execute(
                    SQL_SELECT_BY_CATEGORY_WITH_LIMIT, (categoria, limit)
                )
            else:
                conn.cursor.execute(SQL_SELECT_BY_CATEGORY, (categoria,))
        else:
            if limit:
                conn.cursor.execute(SQL_SELECT_WITH_LIMIT, (limit,))
            else:
                conn.cursor.execute(SQL_SELECT_ALL)
        rows = conn.cursor.fetchall()
        perguntas = [FAQ(*row) for row in rows]
        return perguntas
    except Exception as e:
        logger.error(f'Erro ao listar FAQ: {e}')
        return []


def buscar_por_id(conn, id):
    """Busca um FAQ pelo seu ID.

    Args:
        conn: Conexão com o banco de dados
        id (int): ID do FAQ a ser buscado

    Returns:
        FAQ: Objeto FAQ encontrado, ou None se não encontrado
    """
    try:
        conn.cursor.execute(SQL_SELECT_BY_ID, (id,))
        row = conn.cursor.fetchone()
        if row:
            return FAQ(*row)
        else:
            return None
    except Exception as e:
        logger.error(f'Erro ao buscar FAQ: {e}')
        return None


def listar_categorias(conn):
    """Lista todas as categorias distintas de FAQs cadastradas.

    Args:
        conn: Conexão com o banco de dados

    Returns:
        list: Lista de strings com os nomes das categorias
    """
    try:
        conn.cursor.execute(SQL_SELECT_DISTINCT_CATEGORIES)
        rows = conn.cursor.fetchall()
        return [row[0] for row in rows]
    except Exception as e:
        logger.error(f'Erro ao listar categorias: {e}')
        return []
