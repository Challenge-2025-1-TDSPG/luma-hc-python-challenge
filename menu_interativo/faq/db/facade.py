"""
Facade para o banco de dados FAQ mantendo a mesma API pública.
Este módulo mantém compatibilidade com o código original, mas
utiliza os componentes modularizados internamente.
"""

import logging

from .connection import OracleConnection
from .crud import (
    adicionar,
    atualizar,
    buscar_por_id,
    deletar,
    listar,
    listar_categorias,
)

# Configuração de logging
logger = logging.getLogger(__name__)
if not logger.handlers:
    logging.basicConfig(level=logging.INFO, format='%(levelname)s %(message)s')


class FaqDB:
    """
    Classe responsável por gerenciar o banco de dados dos itens de FAQ (Oracle).
    Esta implementação mantém a mesma API pública que a versão original,
    mas usa internamente os componentes modularizados.
    """

    def __init__(self, oracle_config, silent=False):
        """Inicializa a conexão com o banco de dados Oracle.

        Args:
            oracle_config (dict): Configuração de conexão ao banco Oracle,
                                 contendo as chaves 'user', 'password' e 'dsn'
            silent (bool): Se True, suprime mensagens de log durante a inicialização

        Raises:
            ImportError: Se o módulo oracledb não estiver instalado
            Exception: Se oracle_config não for fornecido ou se a conexão falhar
        """
        from .connection import configurar_conexao

        configurar_conexao(oracle_config)
        self.conn = OracleConnection(oracle_config, silent)
        self.silent = silent

    # Implementando o protocolo de contexto para uso com 'with'
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Sempre fecha silenciosamente ao sair do contexto 'with'
        self.close(silent=True)
        return False  # Propaga exceções se houverem

    def adicionar(self, pergunta, resposta, ativo, categoria):
        """Adiciona um novo registro FAQ na tabela.

        Args:
            pergunta (str): Pergunta do FAQ
            resposta (str): Resposta do FAQ
            ativo (int): Status de ativação (1 para ativo, 0 para inativo)
            categoria (str): Categoria do FAQ

        Returns:
            bool: True se a operação foi bem-sucedida, False caso contrário
        """
        try:
            result = adicionar(self.conn, pergunta, resposta, ativo, categoria)
            return result
        except Exception as e:
            logger.error(f'Erro ao adicionar FAQ: {e}')
            return False

    def listar(self, categoria=None, limit=None):
        """Lista todos os FAQs ou filtra por categoria, com opção de limitar o número de resultados.

        Args:
            categoria (str, optional): Categoria para filtrar.
                                       Se None, retorna todos os FAQs.
            limit (int, optional): Limita o número de resultados.
                                  Se None, retorna todos os resultados.

        Returns:
            list: Lista de objetos FAQ encontrados
        """
        try:
            return listar(self.conn, categoria, limit)
        except Exception as e:
            logger.error(f'Erro ao listar FAQ: {e}')
            return []

    def atualizar(self, id, pergunta, resposta, ativo, categoria):
        """Atualiza um FAQ existente pelo ID.

        Args:
            id (int): ID do FAQ a ser atualizado
            pergunta (str): Nova pergunta do FAQ
            resposta (str): Nova resposta do FAQ
            ativo (int): Novo status de ativação (1 para ativo, 0 para inativo)
            categoria (str): Nova categoria do FAQ

        Returns:
            bool: True se a atualização foi bem-sucedida, False caso contrário
        """
        try:
            return atualizar(self.conn, id, pergunta, resposta, ativo, categoria)
        except Exception as e:
            logger.error(f'Erro ao atualizar FAQ: {e}')
            return False

    def deletar(self, id):
        """Remove um FAQ pelo seu ID.

        Args:
            id (int): ID do FAQ a ser removido

        Returns:
            bool: True se a remoção foi bem-sucedida, False caso contrário
        """
        try:
            return deletar(self.conn, id)
        except Exception as e:
            logger.error(f'Erro ao deletar FAQ: {e}')
            return False

    def buscar_por_id(self, id):
        """Busca um FAQ pelo seu ID.

        Args:
            id (int): ID do FAQ a ser buscado

        Returns:
            FAQ: Objeto FAQ encontrado, ou None se não encontrado
        """
        try:
            return buscar_por_id(self.conn, id)
        except Exception as e:
            logger.error(f'Erro ao buscar FAQ por ID: {e}')
            return None

    def listar_categorias(self):
        """Lista todas as categorias distintas de FAQs cadastradas.

        Returns:
            list: Lista de strings com os nomes das categorias
        """
        try:
            return listar_categorias(self.conn)
        except Exception as e:
            logger.error(f'Erro ao listar categorias: {e}')
            return []

    def close(self, silent=None):
        """Fecha a conexão com o banco de dados de forma segura.

        Args:
            silent (bool, optional): Se True, não exibe mensagens de log ao fechar a conexão.
                                    Se None, usa o valor definido no construtor.
        """
        if self.conn:
            self.conn.close(silent)
