from datetime import datetime

try:
    from colorama import Fore, Style

    HAS_COLORAMA = True
except ImportError:
    HAS_COLORAMA = False

from .models import FAQ

# Constantes para os valores SQL
FAQ_TABLE_NAME = 'FAQ'
MAX_PERGUNTA_LEN = 150
MAX_RESPOSTA_LEN = 600
MAX_CATEGORIA_LEN = 50
ATIVO_TYPE = 'NUMBER(1)'
DATE_COLUMN_TYPE = 'VARCHAR2(50)'


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
            self.create_table_oracle()
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

    # SQL para criar a tabela FAQ
    SQL_CREATE_TABLE = f"""
        BEGIN
            EXECUTE IMMEDIATE 'CREATE TABLE {FAQ_TABLE_NAME} (
                id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                pergunta VARCHAR2({MAX_PERGUNTA_LEN}) NOT NULL,
                resposta VARCHAR2({MAX_RESPOSTA_LEN}) NOT NULL,
                ativo {ATIVO_TYPE} NOT NULL,
                atualizado_em {DATE_COLUMN_TYPE} NOT NULL,
                categoria VARCHAR2({MAX_CATEGORIA_LEN}) NOT NULL
            )';
        EXCEPTION
            WHEN OTHERS THEN
                -- SQLCODE -955 significa que a tabela já existe
                IF SQLCODE != -955 THEN RAISE; END IF;
        END;
    """

    def create_table_oracle(self):
        """Cria a tabela FAQ no banco de dados Oracle se ela não existir.

        Utiliza o recurso de auto-incremento IDENTITY do Oracle 12c ou superior.
        A exceção ORA-00955 ("nome já usado por um objeto existente") é ignorada
        pois indica que a tabela já existe.
        """
        try:
            # Criação da tabela com IDENTITY (Oracle 12c+)
            self.cursor.execute(self.SQL_CREATE_TABLE)
            self.conn.commit()

            # Verifica se a tabela existe (não emite mensagem se silent=True)
            self.cursor.execute(
                f"SELECT COUNT(*) FROM USER_TABLES WHERE TABLE_NAME = '{FAQ_TABLE_NAME}'"
            )
            if self.cursor.fetchone()[0] > 0:
                if not self.silent:
                    print('[INFO] Tabela FAQ verificada e pronta para uso.')
            else:
                print('[AVISO] Não foi possível confirmar a existência da tabela FAQ.')
        except Exception as e:
            print(f'[ERRO] Problema ao verificar/criar tabela Oracle: {e}')

    # SQL para operações de inserção
    SQL_INSERT = f"""
        INSERT INTO {FAQ_TABLE_NAME} 
        (pergunta, resposta, ativo, atualizado_em, categoria) 
        VALUES (:1, :2, :3, :4, :5)
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
        atualizado_em = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            self.cursor.execute(
                self.SQL_INSERT, (pergunta, resposta, ativo, atualizado_em, categoria)
            )
            self.conn.commit()
            print('FAQ adicionada com sucesso!')
            return True
        except Exception as e:
            if self.conn:
                self.conn.rollback()  # Desfaz a transação em caso de erro
            print(f'Erro ao adicionar FAQ: {e}')
            return False

    # SQL templates para consultas
    SQL_SELECT_ALL = f'SELECT * FROM {FAQ_TABLE_NAME}'
    SQL_SELECT_BY_CATEGORY = f'SELECT * FROM {FAQ_TABLE_NAME} WHERE categoria = :1'
    SQL_SELECT_WITH_LIMIT = f'SELECT * FROM {FAQ_TABLE_NAME} WHERE ROWNUM <= :1'
    SQL_SELECT_BY_CATEGORY_WITH_LIMIT = (
        f'SELECT * FROM {FAQ_TABLE_NAME} WHERE categoria = :1 AND ROWNUM <= :2'
    )

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
            print(f'Erro ao listar FAQ: {e}')
            return []

    # SQL para operações de atualização
    SQL_UPDATE = f"""
        UPDATE {FAQ_TABLE_NAME} 
        SET pergunta=:1, resposta=:2, ativo=:3, atualizado_em=:4, categoria=:5 
        WHERE id=:6
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
        atualizado_em = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            self.cursor.execute(
                self.SQL_UPDATE,
                (pergunta, resposta, ativo, atualizado_em, categoria, id),
            )
            rows_affected = self.cursor.rowcount
            self.conn.commit()
            return rows_affected > 0  # Retorna True se algum registro foi atualizado
        except Exception as e:
            if self.conn:
                self.conn.rollback()  # Desfaz a transação em caso de erro
            print(f'Erro ao atualizar FAQ: {e}')
            return False

    # SQL para operações de deleção e consulta
    SQL_DELETE = f'DELETE FROM {FAQ_TABLE_NAME} WHERE id=:1'
    SQL_SELECT_BY_ID = f'SELECT * FROM {FAQ_TABLE_NAME} WHERE id=:1'
    SQL_SELECT_DISTINCT_CATEGORIES = f'SELECT DISTINCT categoria FROM {FAQ_TABLE_NAME}'

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
            print('FAQ deletada com sucesso!')
            return rows_affected > 0  # Retorna True se algum registro foi excluído
        except Exception as e:
            if self.conn:
                self.conn.rollback()  # Desfaz a transação em caso de erro
            print(f'Erro ao deletar FAQ: {e}')
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
            print(f'Erro ao buscar FAQ: {e}')
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
            print(f'Erro ao listar categorias: {e}')
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
                print(f'Erro ao fechar o cursor: {e}')

        try:
            if self.conn:
                self.conn.close()
                self.conn = None
                if not should_be_silent:
                    if HAS_COLORAMA:
                        print(
                            f'{Fore.BLUE}[INFO] Conexão com o banco Oracle fechada com sucesso.{Style.RESET_ALL}'
                        )
                    else:
                        print('[INFO] Conexão com o banco de dados fechada.')
        except Exception as e:
            if not should_be_silent:
                print(f'Erro ao fechar a conexão com o banco: {e}')
