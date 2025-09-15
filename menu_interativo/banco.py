"""
Módulo consolidado de operações Oracle (CRUD, conexão, categorias) para o sistema FAQ.
Inclui FaqDB, OracleConnection, helpers de conexão, funções CRUD, constantes SQL e helpers de schema.
"""

import logging
from colorama import Fore, Style

# --- Constantes e SQL ---
FAQ_TABLE_NAME = 'FAQ'
MAX_PERGUNTA_LEN = 150
MAX_RESPOSTA_LEN = 600
MAX_CATEGORIA_LEN = 50
ATIVO_TYPE = 'NUMBER(1)'

SQL_INSERT = f"""
    INSERT INTO {FAQ_TABLE_NAME}
    (PERGUNTA, RESPOSTA, ATIVO, CATEGORIA)
    VALUES (:1, :2, :3, :4)
"""
SQL_SELECT_ALL = f"""
  SELECT ID_FAQ, PERGUNTA, RESPOSTA, ATIVO, ATUALIZADO_EM, CATEGORIA
  FROM {FAQ_TABLE_NAME}
  ORDER BY ID_FAQ DESC
"""
SQL_SELECT_BY_CATEGORY = f"""
  SELECT ID_FAQ, PERGUNTA, RESPOSTA, ATIVO, ATUALIZADO_EM, CATEGORIA
  FROM {FAQ_TABLE_NAME}
  WHERE UPPER(CATEGORIA) = UPPER(:1)
  ORDER BY ID_FAQ DESC
"""
SQL_SELECT_WITH_LIMIT = f"""
    SELECT ID_FAQ, PERGUNTA, RESPOSTA, ATIVO, ATUALIZADO_EM, CATEGORIA FROM (
        SELECT ID_FAQ, PERGUNTA, RESPOSTA, ATIVO, ATUALIZADO_EM, CATEGORIA FROM {FAQ_TABLE_NAME}
        ORDER BY ID_FAQ DESC
    )
    WHERE ROWNUM <= :1
"""
SQL_SELECT_BY_CATEGORY_WITH_LIMIT = f"""
    SELECT ID_FAQ, PERGUNTA, RESPOSTA, ATIVO, ATUALIZADO_EM, CATEGORIA FROM (
        SELECT ID_FAQ, PERGUNTA, RESPOSTA, ATIVO, ATUALIZADO_EM, CATEGORIA FROM {FAQ_TABLE_NAME}
        WHERE UPPER(CATEGORIA) = UPPER(:1)
        ORDER BY ID_FAQ DESC
    )
    WHERE ROWNUM <= :2
"""
SQL_UPDATE = f"""
    UPDATE {FAQ_TABLE_NAME}
    SET PERGUNTA = :1,
        RESPOSTA = :2,
        ATIVO = :3,
        ATUALIZADO_EM = SYSDATE,
        CATEGORIA = :4
    WHERE ID_FAQ = :5
"""
SQL_DELETE = f'DELETE FROM {FAQ_TABLE_NAME} WHERE ID_FAQ=:1'
SQL_SELECT_BY_ID = f'SELECT ID_FAQ, PERGUNTA, RESPOSTA, ATIVO, ATUALIZADO_EM, CATEGORIA FROM {FAQ_TABLE_NAME} WHERE ID_FAQ=:1'
SQL_SELECT_DISTINCT_CATEGORIES = f'SELECT DISTINCT CATEGORIA FROM {FAQ_TABLE_NAME}'

# --- Helpers de conexão ---
_oracle_config = None

def configurar_conexao(config):
    global _oracle_config
    _oracle_config = config
    logging.info(f'{Fore.BLUE}Configuração de conexão Oracle definida com sucesso.{Style.RESET_ALL}')

def obter_conexao(silent=False):
    if _oracle_config is None:
        error_msg = f'{Fore.RED}Conexão não configurada. Chame configurar_conexao antes.{Style.RESET_ALL}'
        raise ValueError(error_msg)
    return OracleConnection(_oracle_config, silent)

class OracleConnection:
    def __init__(self, oracle_config, silent=False):
        self.conn = None
        self.cursor = None
        self.silent = silent
        try:
            import oracledb
            oracledb.defaults.config_dir = None
            if oracle_config:
                self.conn = oracledb.connect(
                    user=oracle_config['user'],
                    password=oracle_config['password'],
                    dsn=oracle_config['dsn'],
                )
                if not silent:
                    print(f'{Fore.BLUE}[INFO] Conexão com o banco de dados Oracle estabelecida (modo Thin).{Style.RESET_ALL}')
            else:
                error_msg = f'{Fore.RED}oracle_config deve ser fornecido para Oracle{Style.RESET_ALL}'
                raise Exception(error_msg)
            self.cursor = self.conn.cursor()
            check_faq_schema(self.cursor)
        except ImportError:
            print(f'{Fore.RED}oracledb não instalado. Instale com: pip install oracledb{Style.RESET_ALL}')
            raise
        except Exception as e:
            print(f'{Fore.RED}[ERRO] Não foi possível conectar ao banco Oracle. Verifique as credenciais e o DSN.{Style.RESET_ALL}')
            print(f'{Fore.RED}Detalhes: {e}{Style.RESET_ALL}')
            raise

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close(silent=True)
        return False

    def close(self, silent=None):
        should_be_silent = self.silent if silent is None else silent
        try:
            if self.cursor:
                self.cursor.close()
                self.cursor = None
        except Exception as e:
            if not should_be_silent:
                logging.warning(f'{Fore.YELLOW}Erro ao fechar o cursor: {e}{Style.RESET_ALL}')
        try:
            if self.conn:
                self.conn.close()
                self.conn = None
                if not should_be_silent:
                    logging.info(f'{Fore.GREEN}Conexão com o banco Oracle fechada com sucesso.{Style.RESET_ALL}')
        except Exception as e:
            if not should_be_silent:
                logging.warning(f'{Fore.RED}Erro ao fechar a conexão com o banco: {e}{Style.RESET_ALL}')

# --- Helpers de schema ---
def check_faq_schema(cursor):
    try:
        cursor.execute('SELECT 1 FROM USER_TABLES WHERE TABLE_NAME = :t', {'t': FAQ_TABLE_NAME.upper()})
        if not cursor.fetchone():
            logging.error('Tabela %s não encontrada no schema.', FAQ_TABLE_NAME)
            return
        def exists_constraint(name: str) -> bool:
            cursor.execute('SELECT 1 FROM USER_CONSTRAINTS WHERE TABLE_NAME = :t AND CONSTRAINT_NAME = :c', {'t': FAQ_TABLE_NAME.upper(), 'c': name})
            return bool(cursor.fetchone())
        def exists_index(name: str) -> bool:
            cursor.execute('SELECT 1 FROM USER_INDEXES WHERE INDEX_NAME = :i', {'i': name})
            return bool(cursor.fetchone())
        missing = []
        if not exists_constraint('FAQ_PERGUNTA_UN'):
            missing.append('UNIQUE( PERGUNTA ) -> FAQ_PERGUNTA_UN')
        if not exists_constraint('CK_FAQ_ATIVO'):
            missing.append('CHECK ATIVO IN (0,1) -> CK_FAQ_ATIVO')
        if not exists_index('IDX_FAQ_CATEG_UP'):
            missing.append('INDEX UPPER(CATEGORIA) -> IDX_FAQ_CATEG_UP')
        if missing:
            logging.warning(f'{Fore.YELLOW}FAQ: itens ausentes: {'; '.join(missing)}{Style.RESET_ALL}')
        else:
            logging.info(f'{Fore.GREEN}FAQ: schema OK (UNIQUE, CHECK, ÍNDICE).{Style.RESET_ALL}')
    except Exception as e:
        logging.warning(f'{Fore.RED}Falha ao checar schema da FAQ: {str(e)}{Style.RESET_ALL}')

# --- Funções CRUD ---
def adicionar(conn, pergunta, resposta, ativo, categoria):
    pergunta = pergunta.strip()
    resposta = resposta.strip()
    categoria = categoria.strip().upper()
    if ativo not in (0, 1):
        raise ValueError(f'{Fore.RED}ativo deve ser 0 ou 1{Style.RESET_ALL}')
    if len(pergunta) > MAX_PERGUNTA_LEN:
        raise ValueError(f'{Fore.RED}pergunta excede {MAX_PERGUNTA_LEN} caracteres{Style.RESET_ALL}')
    if len(resposta) > MAX_RESPOSTA_LEN:
        raise ValueError(f'{Fore.RED}resposta excede {MAX_RESPOSTA_LEN} caracteres{Style.RESET_ALL}')
    if len(categoria) > MAX_CATEGORIA_LEN:
        raise ValueError(f'{Fore.RED}categoria excede {MAX_CATEGORIA_LEN} caracteres{Style.RESET_ALL}')
    try:
        conn.cursor.execute(SQL_INSERT, (pergunta, resposta, ativo, categoria))
        conn.conn.commit()
        logging.info(f'{Fore.GREEN}FAQ adicionada com sucesso!{Style.RESET_ALL}')
        return True
    except Exception as e:
        if conn.conn:
            conn.conn.rollback()
        msg = str(e)
        if 'ORA-00001' in msg:
            logging.warning(f'{Fore.YELLOW}Pergunta já cadastrada (violação de UNIQUE).{Style.RESET_ALL}')
        elif 'ORA-12899' in msg:
            logging.warning(f'{Fore.YELLOW}Valor excede o tamanho permitido para a coluna (ORA-12899).{Style.RESET_ALL}')
        else:
            logging.error(f'{Fore.RED}Erro ao adicionar FAQ: {e}{Style.RESET_ALL}')
        return False

def listar(conn, categoria=None, limit=None):
    from .models import FAQ
    try:
        if categoria:
            if limit:
                conn.cursor.execute(SQL_SELECT_BY_CATEGORY_WITH_LIMIT, (categoria, limit))
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
        logging.error(f'{Fore.RED}Erro ao listar FAQ: {e}{Style.RESET_ALL}')
        return []

def atualizar(conn, id, pergunta, resposta, ativo, categoria):
    pergunta = pergunta.strip()
    resposta = resposta.strip()
    categoria = categoria.strip().upper()
    if ativo not in (0, 1):
        raise ValueError(f'{Fore.RED}ativo deve ser 0 ou 1{Style.RESET_ALL}')
    if len(pergunta) > MAX_PERGUNTA_LEN:
        raise ValueError(f'{Fore.RED}pergunta excede {MAX_PERGUNTA_LEN} caracteres{Style.RESET_ALL}')
    if len(resposta) > MAX_RESPOSTA_LEN:
        raise ValueError(f'{Fore.RED}resposta excede {MAX_RESPOSTA_LEN} caracteres{Style.RESET_ALL}')
    if len(categoria) > MAX_CATEGORIA_LEN:
        raise ValueError(f'{Fore.RED}categoria excede {MAX_CATEGORIA_LEN} caracteres{Style.RESET_ALL}')
    try:
        conn.cursor.execute(SQL_UPDATE, (pergunta, resposta, ativo, categoria, id))
        rows_affected = conn.cursor.rowcount
        conn.conn.commit()
        if rows_affected > 0:
            logging.info(f'{Fore.GREEN}FAQ ID {id} atualizada com sucesso.{Style.RESET_ALL}')
        return rows_affected > 0
    except Exception as e:
        if conn.conn:
            conn.conn.rollback()
        msg = str(e)
        if 'ORA-00001' in msg:
            logging.warning(f'{Fore.YELLOW}Pergunta já cadastrada (violação de UNIQUE).{Style.RESET_ALL}')
        elif 'ORA-12899' in msg:
            logging.warning(f'{Fore.YELLOW}Valor excede o tamanho permitido para a coluna (ORA-12899).{Style.RESET_ALL}')
        else:
            logging.error(f'{Fore.RED}Erro ao atualizar FAQ: {e}{Style.RESET_ALL}')
        return False

def deletar(conn, id):
    try:
        conn.cursor.execute(SQL_DELETE, (id,))
        rows_affected = conn.cursor.rowcount
        conn.conn.commit()
        if rows_affected > 0:
            logging.info(f'{Fore.GREEN}FAQ ID {id} deletada com sucesso.{Style.RESET_ALL}')
        else:
            logging.warning(f'{Fore.YELLOW}FAQ ID {id} não encontrada para exclusão.{Style.RESET_ALL}')
        return rows_affected > 0
    except Exception as e:
        if conn.conn:
            conn.conn.rollback()
        logging.error(f'{Fore.RED}Erro ao deletar FAQ: {e}{Style.RESET_ALL}')
        return False

def buscar_por_id(conn, id):
    from .models import FAQ
    try:
        conn.cursor.execute(SQL_SELECT_BY_ID, (id,))
        row = conn.cursor.fetchone()
        if row:
            return FAQ(*row)
        else:
            return None
    except Exception as e:
        logging.error(f'{Fore.RED}Erro ao buscar FAQ: {e}{Style.RESET_ALL}')
        return None

def listar_categorias(conn):
    try:
        conn.cursor.execute(SQL_SELECT_DISTINCT_CATEGORIES)
        rows = conn.cursor.fetchall()
        return [row[0] for row in rows]
    except Exception as e:
        logging.error(f'{Fore.RED}Erro ao listar categorias: {e}{Style.RESET_ALL}')
        return []

# --- Classe FaqDB (interface principal) ---
class FaqDB:
    def __init__(self, oracle_config, silent=False):
        configurar_conexao(oracle_config)
        self.conn = OracleConnection(oracle_config, silent)
        self.silent = silent

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close(silent=True)
        return False

    def adicionar(self, pergunta, resposta, ativo, categoria):
        try:
            result = adicionar(self.conn, pergunta, resposta, ativo, categoria)
            return result
        except Exception as e:
            logging.error(f'{Fore.RED}Erro ao adicionar FAQ: {e}{Style.RESET_ALL}')
            return False

    def listar(self, categoria=None, limit=None):
        try:
            return listar(self.conn, categoria, limit)
        except Exception as e:
            logging.error(f'{Fore.RED}Erro ao listar FAQ: {e}{Style.RESET_ALL}')
            return []

    def atualizar(self, id, pergunta, resposta, ativo, categoria):
        try:
            return atualizar(self.conn, id, pergunta, resposta, ativo, categoria)
        except Exception as e:
            logging.error(f'{Fore.RED}Erro ao atualizar FAQ: {e}{Style.RESET_ALL}')
            return False

    def deletar(self, id):
        try:
            return deletar(self.conn, id)
        except Exception as e:
            logging.error(f'{Fore.RED}Erro ao deletar FAQ: {e}{Style.RESET_ALL}')
            return False

    def buscar_por_id(self, id):
        try:
            return buscar_por_id(self.conn, id)
        except Exception as e:
            logging.error(f'{Fore.RED}Erro ao buscar FAQ por ID: {e}{Style.RESET_ALL}')
            return None

    def listar_categorias(self):
        try:
            return listar_categorias(self.conn)
        except Exception as e:
            logging.error(f'{Fore.RED}Erro ao listar categorias: {e}{Style.RESET_ALL}')
            return []

    def close(self, silent=None):
        if self.conn:
            self.conn.close(silent)
