try:
    from colorama import Fore, Style

    HAS_COLORAMA = True
except ImportError:
    HAS_COLORAMA = False

import logging

from .models import FAQ

# Configuração de logging
logger = logging.getLogger(__name__)
if not logger.handlers:
    logging.basicConfig(level=logging.INFO, format='%(levelname)s %(message)s')

# Constantes para os valores SQL
FAQ_TABLE_NAME = 'FAQ'
MAX_PERGUNTA_LEN = 150
MAX_RESPOSTA_LEN = 600
MAX_CATEGORIA_LEN = 50
ATIVO_TYPE = 'NUMBER(1)'


class FaqDB:
    """
    Classe responsável por gerenciar o banco de dados dos itens de FAQ (Oracle).
    Implementa o protocolo de contexto para garantir o fechamento da conexão.
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
        self.conn = None
        self.cursor = None
        self.silent = silent

        try:
            import oracledb

            # Configurando para usar o modo Thin
            # Este modo não requer o Client instalado
            oracledb.defaults.config_dir = None

            if oracle_config:
                self.conn = oracledb.connect(
                    user=oracle_config['user'],
                    password=oracle_config['password'],
                    dsn=oracle_config['dsn'],
                )
                if not silent:
                    if HAS_COLORAMA:
                        print(
                            f'{Fore.BLUE}[INFO] Conexão com o banco de dados Oracle estabelecida (modo Thin).{Style.RESET_ALL}'
                        )
                    else:
                        print(
                            '[INFO] Conexão com o banco de dados Oracle estabelecida (modo Thin).'
                        )
            else:
                raise Exception('oracle_config deve ser fornecido para Oracle')
            self.cursor = self.conn.cursor()
            self._check_faq_schema()
        except ImportError:
            print('oracledb não instalado. Instale com: pip install oracledb')
            raise
        except Exception as e:
            print(
                '[ERRO] Não foi possível conectar ao banco Oracle. Verifique as credenciais e o DSN.'
            )
            print(f'Detalhes: {e}')
            raise

    # Implementando o protocolo de contexto para uso com 'with'
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Sempre fecha silenciosamente ao sair do contexto 'with'
        self.close(silent=True)
        return False  # Propaga exceções se houverem

    def _check_faq_schema(self):
        """Valida presença de constraints/índice essenciais da FAQ. Não altera o banco.

        Este método realiza um health check para verificar se:
        1. A tabela FAQ existe no schema atual
        2. As constraints necessárias (CHECK, UNIQUE) estão presentes
        3. O índice para busca case-insensitive por categoria está criado

        Se algo estiver faltando, apenas registra um aviso no log, sem tentar corrigir.
        """
        try:
            # Verifica se a tabela FAQ existe no dicionário de dados Oracle
            self.cursor.execute(
                'SELECT 1 FROM USER_TABLES WHERE TABLE_NAME = :t',
                {'t': FAQ_TABLE_NAME.upper()},
            )
            if not self.cursor.fetchone():
                logger.error('Tabela %s não encontrada no schema.', FAQ_TABLE_NAME)
                return

            # Helper function: verifica se uma constraint específica existe na tabela
            def exists_constraint(name: str) -> bool:
                self.cursor.execute(
                    """
                    SELECT 1 FROM USER_CONSTRAINTS
                    WHERE TABLE_NAME = :t AND CONSTRAINT_NAME = :c
                """,
                    {'t': FAQ_TABLE_NAME.upper(), 'c': name},
                )
                return bool(self.cursor.fetchone())

            # Helper function: verifica se um índice específico existe no schema
            def exists_index(name: str) -> bool:
                self.cursor.execute(
                    """
                    SELECT 1 FROM USER_INDEXES WHERE INDEX_NAME = :i
                """,
                    {'i': name},
                )
                return bool(self.cursor.fetchone())

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
                logger.warning('FAQ: itens ausentes: %s', '; '.join(missing))
            else:
                logger.info('FAQ: schema OK (UNIQUE, CHECK, índice).')
        except Exception as e:
            logger.warning('Falha ao checar schema da FAQ: %s', e)

    # SQL para operações de inserção
    # Não inclui ATUALIZADO_EM pois o banco define automaticamente via DEFAULT SYSDATE
    SQL_INSERT = f"""
        INSERT INTO {FAQ_TABLE_NAME}
        (PERGUNTA, RESPOSTA, ATIVO, CATEGORIA)
        VALUES (:1, :2, :3, :4)
    """

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
            self.cursor.execute(self.SQL_INSERT, (pergunta, resposta, ativo, categoria))
            # Confirma a transação no banco
            self.conn.commit()
            logger.info('FAQ adicionada com sucesso!')
            return True
        except Exception as e:
            if self.conn:
                self.conn.rollback()  # Desfaz a transação em caso de erro
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

    # SQL templates para consultas
    # Consulta básica: lista todos FAQs, mais recentes primeiro
    SQL_SELECT_ALL = f"""
      SELECT ID_FAQ, PERGUNTA, RESPOSTA, ATIVO, ATUALIZADO_EM, CATEGORIA
      FROM {FAQ_TABLE_NAME}
      ORDER BY ID_FAQ DESC
    """

    # Consulta com filtro por categoria (case-insensitive usando UPPER)
    # Aproveita o índice IDX_FAQ_CATEG_UP criado em UPPER(CATEGORIA)
    # Mantém consistência com ordenação (mais recentes primeiro)
    SQL_SELECT_BY_CATEGORY = f"""
      SELECT ID_FAQ, PERGUNTA, RESPOSTA, ATIVO, ATUALIZADO_EM, CATEGORIA
      FROM {FAQ_TABLE_NAME}
      WHERE UPPER(CATEGORIA) = UPPER(:1)
      ORDER BY ID_FAQ DESC
    """

    # Consulta paginada (N primeiros registros)
    # Usa subconsulta porque em Oracle, ROWNUM é aplicado antes do ORDER BY
    # Isso garante que os N registros mais recentes são retornados, não os primeiros N do banco
    SQL_SELECT_WITH_LIMIT = f"""
        SELECT ID_FAQ, PERGUNTA, RESPOSTA, ATIVO, ATUALIZADO_EM, CATEGORIA FROM (
            SELECT ID_FAQ, PERGUNTA, RESPOSTA, ATIVO, ATUALIZADO_EM, CATEGORIA FROM {FAQ_TABLE_NAME}
            ORDER BY ID_FAQ DESC
        )
        WHERE ROWNUM <= :1
    """

    # Consulta combinada: filtro por categoria + paginação
    # A estrutura de subconsulta garante que a ordem é aplicada antes do limite
    SQL_SELECT_BY_CATEGORY_WITH_LIMIT = f"""
        SELECT ID_FAQ, PERGUNTA, RESPOSTA, ATIVO, ATUALIZADO_EM, CATEGORIA FROM (
            SELECT ID_FAQ, PERGUNTA, RESPOSTA, ATIVO, ATUALIZADO_EM, CATEGORIA FROM {FAQ_TABLE_NAME}
            WHERE UPPER(CATEGORIA) = UPPER(:1)
            ORDER BY ID_FAQ DESC
        )
        WHERE ROWNUM <= :2
    """

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
            if categoria:
                if limit:
                    self.cursor.execute(
                        self.SQL_SELECT_BY_CATEGORY_WITH_LIMIT, (categoria, limit)
                    )
                else:
                    self.cursor.execute(self.SQL_SELECT_BY_CATEGORY, (categoria,))
            else:
                if limit:
                    self.cursor.execute(self.SQL_SELECT_WITH_LIMIT, (limit,))
                else:
                    self.cursor.execute(self.SQL_SELECT_ALL)
            rows = self.cursor.fetchall()
            perguntas = [FAQ(*row) for row in rows]
            return perguntas
        except Exception as e:
            logger.error(f'Erro ao listar FAQ: {e}')
            return []

    # SQL para operações de atualização
    # Utiliza SYSDATE diretamente no Oracle para atualizar o timestamp
    # Os placeholders :1, :2, etc. correspondem à ordem dos parâmetros no execute()
    SQL_UPDATE = f"""
        UPDATE {FAQ_TABLE_NAME}
        SET PERGUNTA = :1,
            RESPOSTA = :2,
            ATIVO = :3,
            ATUALIZADO_EM = SYSDATE,
            CATEGORIA = :4
        WHERE ID_FAQ = :5
    """

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
            self.cursor.execute(
                self.SQL_UPDATE,
                (pergunta, resposta, ativo, categoria, id),
            )
            # rowcount indica quantas linhas foram afetadas (deve ser 1 para sucesso)
            rows_affected = self.cursor.rowcount
            self.conn.commit()
            if rows_affected > 0:
                logger.info(f'FAQ ID {id} atualizada com sucesso.')
            return rows_affected > 0  # Retorna True se algum registro foi atualizado
        except Exception as e:
            if self.conn:
                self.conn.rollback()  # Desfaz a transação em caso de erro
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

    # SQL para operações de deleção e consulta
    # Comando para excluir um FAQ pelo ID
    SQL_DELETE = f'DELETE FROM {FAQ_TABLE_NAME} WHERE ID_FAQ=:1'

    # Busca completa de um FAQ pelo ID (todas as colunas listadas explicitamente)
    SQL_SELECT_BY_ID = f'SELECT ID_FAQ, PERGUNTA, RESPOSTA, ATIVO, ATUALIZADO_EM, CATEGORIA FROM {FAQ_TABLE_NAME} WHERE ID_FAQ=:1'

    # Lista todas as categorias distintas para popular menus/filtros
    SQL_SELECT_DISTINCT_CATEGORIES = f'SELECT DISTINCT CATEGORIA FROM {FAQ_TABLE_NAME}'

    def deletar(self, id):
        """Remove um FAQ pelo seu ID.

        Args:
            id (int): ID do FAQ a ser removido

        Returns:
            bool: True se a remoção foi bem-sucedida, False caso contrário
        """
        try:
            self.cursor.execute(self.SQL_DELETE, (id,))
            rows_affected = self.cursor.rowcount
            self.conn.commit()
            if rows_affected > 0:
                logger.info(f'FAQ ID {id} deletada com sucesso.')
            else:
                logger.warning(f'FAQ ID {id} não encontrada para exclusão.')
            return rows_affected > 0  # Retorna True se algum registro foi excluído
        except Exception as e:
            if self.conn:
                self.conn.rollback()  # Desfaz a transação em caso de erro
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
            self.cursor.execute(self.SQL_SELECT_BY_ID, (id,))
            row = self.cursor.fetchone()
            if row:
                return FAQ(*row)
            else:
                return None
        except Exception as e:
            logger.error(f'Erro ao buscar FAQ: {e}')
            return None

    def listar_categorias(self):
        """Lista todas as categorias distintas de FAQs cadastradas.

        Returns:
            list: Lista de strings com os nomes das categorias
        """
        try:
            self.cursor.execute(self.SQL_SELECT_DISTINCT_CATEGORIES)
            rows = self.cursor.fetchall()
            return [row[0] for row in rows]
        except Exception as e:
            logger.error(f'Erro ao listar categorias: {e}')
            return []

    def close(self, silent=None):
        """Fecha a conexão com o banco de dados de forma segura.

        Args:
            silent (bool, optional): Se True, não exibe mensagens de log ao fechar a conexão.
                                    Se None, usa o valor definido no construtor.
        """
        # Se silent não for explicitamente fornecido, use o valor da instância
        should_be_silent = self.silent if silent is None else silent

        try:
            if self.cursor:
                self.cursor.close()
                self.cursor = None
        except Exception as e:
            if not should_be_silent:
                logger.warning(f'Erro ao fechar o cursor: {e}')

        try:
            if self.conn:
                self.conn.close()
                self.conn = None
                if not should_be_silent:
                    logger.info('Conexão com o banco Oracle fechada com sucesso.')
        except Exception as e:
            if not should_be_silent:
                logger.warning(f'Erro ao fechar a conexão com o banco: {e}')
