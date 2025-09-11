"""
Módulo para verificação e validação do schema do banco de dados FAQ.
"""

import logging

from colorama import Fore, Style

from .queries import FAQ_TABLE_NAME

# Configuração de logging
logger = logging.getLogger(__name__)


def check_faq_schema(cursor):
    """Valida presença de constraints/índice essenciais da FAQ. Não altera o banco.

    Este método realiza um health check para verificar se:
    1. A tabela FAQ existe no schema atual
    2. As constraints necessárias (CHECK, UNIQUE) estão presentes
    3. O índice para busca case-insensitive por categoria está criado

    Se algo estiver faltando, apenas registra um aviso no log, sem tentar corrigir.

    Args:
        cursor: Oracle cursor conectado ao banco
    """
    try:
        # Verifica se a tabela FAQ existe no dicionário de dados Oracle
        cursor.execute(
            'SELECT 1 FROM USER_TABLES WHERE TABLE_NAME = :t',
            {'t': FAQ_TABLE_NAME.upper()},
        )
        if not cursor.fetchone():
            logger.error('Tabela %s não encontrada no schema.', FAQ_TABLE_NAME)
            return

        # Helper function: verifica se uma constraint específica existe na tabela
        def exists_constraint(name: str) -> bool:
            cursor.execute(
                """
                SELECT 1 FROM USER_CONSTRAINTS
                WHERE TABLE_NAME = :t AND CONSTRAINT_NAME = :c
            """,
                {'t': FAQ_TABLE_NAME.upper(), 'c': name},
            )
            return bool(cursor.fetchone())

        # Helper function: verifica se um índice específico existe no schema
        def exists_index(name: str) -> bool:
            cursor.execute(
                """
                SELECT 1 FROM USER_INDEXES WHERE INDEX_NAME = :i
            """,
                {'i': name},
            )
            return bool(cursor.fetchone())

        # Coleta itens do modelo físico que estão faltando
        missing = []
        if not exists_constraint('FAQ_PERGUNTA_UN'):
            missing.append('UNIQUE( PERGUNTA ) -> FAQ_PERGUNTA_UN')
        if not exists_constraint('CK_FAQ_ATIVO'):
            missing.append('CHECK ATIVO IN (0,1) -> CK_FAQ_ATIVO')
        if not exists_index('IDX_FAQ_CATEG_UP'):
            missing.append('INDEX UPPER(CATEGORIA) -> IDX_FAQ_CATEG_UP')

        # Reporta resultado da verificação
        if missing:
            logger.warning(
                f'{Fore.YELLOW}FAQ: itens ausentes: {"; ".join(missing)}{Style.RESET_ALL}'
            )
        else:
            logger.info(
                f'{Fore.GREEN}FAQ: schema OK (UNIQUE, CHECK, índice).{Style.RESET_ALL}'
            )
    except Exception as e:
        logger.warning(
            f'{Fore.RED}Falha ao checar schema da FAQ: {str(e)}{Style.RESET_ALL}'
        )
