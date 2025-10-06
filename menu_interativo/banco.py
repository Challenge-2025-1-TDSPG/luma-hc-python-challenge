import logging

from config.settings import COLOR_ERROR, COLOR_RESET, COLOR_SUCCESS, COLOR_WARNING

FAQ_TABLE_NAME = 'faq'

SQL_UPDATE = f"""
    UPDATE {FAQ_TABLE_NAME}
    SET question_faq = :1, answer_faq = :2, active_faq = :3, category_faq = :4, faq_updated_at = SYSDATE, user_account_id_user = :5
    WHERE id_faq = :6
"""
SQL_DELETE = f"""
    DELETE FROM {FAQ_TABLE_NAME} WHERE id_faq = :1
"""
SQL_SELECT_BY_ID = f"""
    SELECT id_faq, question_faq, answer_faq, active_faq, faq_updated_at, category_faq, user_account_id_user
    FROM {FAQ_TABLE_NAME}
    WHERE id_faq = :1
"""
SQL_SELECT_DISTINCT_CATEGORIES = f"""
    SELECT DISTINCT category_faq FROM {FAQ_TABLE_NAME} ORDER BY category_faq
"""


# --- Autenticação de usuário/admin ---
def autenticar_admin(conn, cpf, nascimento):
    """
    Autentica um admin pelo CPF e data de nascimento (formato: YYYY-MM-DD).
    Retorna o id_user_adm e nome do usuário se sucesso, ou None se falhar.
    """
    sql = """
        SELECT ua.id_user, ua.name_user, ua.cpf_user, ua.birth_date, adm.id_user_adm
        FROM user_account ua
        JOIN user_adm adm ON adm.user_account_id_user = ua.id_user
        WHERE ua.cpf_user = :cpf AND TO_CHAR(ua.birth_date, 'YYYY-MM-DD') = :nasc
    """
    conn.cursor.execute(sql, {'cpf': cpf, 'nasc': nascimento})
    row = conn.cursor.fetchone()
    if row:
        return {
            'id_user': row[0],
            'name_user': row[1],
            'cpf_user': row[2],
            'birth_date': row[3],
            'id_user_adm': row[4],
        }

FAQ_TABLE_NAME = 'faq'
MAX_PERGUNTA_LEN = 150
MAX_RESPOSTA_LEN = 600
MAX_CATEGORIA_LEN = 50
ATIVO_TYPE = 'NUMBER(1)'

SQL_INSERT = f"""
    INSERT INTO {FAQ_TABLE_NAME}
    (question_faq, answer_faq, active_faq, category_faq, user_account_id_user)
    VALUES (:1, :2, :3, :4, :5)
"""
SQL_SELECT_ALL = f"""
  SELECT id_faq, question_faq, answer_faq, active_faq, faq_updated_at, category_faq, user_account_id_user
  FROM {FAQ_TABLE_NAME}
  ORDER BY id_faq DESC
"""
SQL_SELECT_BY_CATEGORY = f"""
  SELECT id_faq, question_faq, answer_faq, active_faq, faq_updated_at, category_faq, user_account_id_user
  FROM {FAQ_TABLE_NAME}
  WHERE UPPER(category_faq) = UPPER(:1)
  ORDER BY id_faq DESC
"""
SQL_SELECT_WITH_LIMIT = f"""
    SELECT id_faq, question_faq, answer_faq, active_faq, faq_updated_at, category_faq, user_account_id_user FROM (
        SELECT id_faq, question_faq, answer_faq, active_faq, faq_updated_at, category_faq, user_account_id_user FROM {FAQ_TABLE_NAME}
        ORDER BY id_faq DESC
    )
    WHERE ROWNUM <= :1
"""
SQL_SELECT_BY_CATEGORY_WITH_LIMIT = f"""
    SELECT id_faq, question_faq, answer_faq, active_faq, faq_updated_at, category_faq, user_account_id_user FROM (
        SELECT id_faq, question_faq, answer_faq, active_faq, faq_updated_at, category_faq, user_account_id_user FROM {FAQ_TABLE_NAME}
        WHERE UPPER(category_faq) = UPPER(:1)
        ORDER BY id_faq DESC
    )
    WHERE ROWNUM <= :2
"""


class OracleConnection:
    def __init__(self, oracle_config, silent=False):
        self.conn = None
        self.cursor = None
        self.silent = silent
        from config.settings import show_message

        try:
            import oracledb

            self.conn = oracledb.connect(**oracle_config)
            self.cursor = self.conn.cursor()
        except ImportError:
            show_message(
                'oracledb não instalado. Instale com: pip install oracledb', 'error'
            )
            raise
        except Exception as e:
            show_message(
                '[ERRO] Não foi possível conectar ao banco Oracle. Verifique as credenciais e o DSN.',
                'error',
            )
            show_message(f'Detalhes: {e}', 'error')
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
        except Exception:
            if not should_be_silent:
                logging.warning(
                    f'{COLOR_WARNING}Erro ao fechar o cursor.' + COLOR_RESET
                )
        try:
            if self.conn:
                self.conn.close()
                self.conn = None
                if not should_be_silent:
                    logging.info(
                        f'{COLOR_SUCCESS}Conexão com o banco Oracle fechada com sucesso.{COLOR_RESET}'
                    )
        except Exception:
            if not should_be_silent:
                logging.warning(
                    f'{COLOR_ERROR}Erro ao fechar a conexão com o banco.' + COLOR_RESET
                )

def adicionar(conn, pergunta, resposta, ativo, categoria, user_adm_id_user_adm):
    pergunta = pergunta.strip()
    resposta = resposta.strip()
    categoria = categoria.strip().upper()
    if ativo not in (0, 1):
        raise ValueError(f'{COLOR_ERROR}ativo deve ser 0 ou 1{COLOR_RESET}')
    if len(pergunta) > MAX_PERGUNTA_LEN:
        raise ValueError(
            f'{COLOR_ERROR}pergunta excede {MAX_PERGUNTA_LEN} caracteres{COLOR_RESET}'
        )
    if len(resposta) > MAX_RESPOSTA_LEN:
        raise ValueError(
            f'{COLOR_ERROR}resposta excede {MAX_RESPOSTA_LEN} caracteres{COLOR_RESET}'
        )
    if len(categoria) > MAX_CATEGORIA_LEN:
        raise ValueError(
            f'{COLOR_ERROR}categoria excede {MAX_CATEGORIA_LEN} caracteres{COLOR_RESET}'
        )
    try:
        conn.cursor.execute(
            SQL_INSERT, (pergunta, resposta, ativo, categoria, user_adm_id_user_adm)
        )
        conn.conn.commit()
        from config.settings import show_message

        show_message('FAQ adicionada com sucesso!', 'success')
        return True
    except Exception as e:
        if conn.conn:
            conn.conn.rollback()
        msg = str(e)
        from config.settings import show_message

        if 'ORA-00001' in msg:
            show_message('Pergunta já cadastrada (violação de UNIQUE).', 'warning')
        elif 'ORA-12899' in msg:
            show_message(
                'Valor excede o tamanho permitido para a coluna (ORA-12899).', 'warning'
            )
        else:
            show_message('Erro ao adicionar FAQ: ' + str(e), 'error')
        return False


def listar(conn, categoria=None, limit=None):
    from models import FAQ

    try:
        if categoria:
            categoria = categoria.strip().upper()
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
        from config.settings import show_message

        show_message('Erro ao listar FAQ: ' + str(e), 'error')
        return []


def atualizar(conn, id, pergunta, resposta, ativo, categoria, user_adm_id_user_adm):
    pergunta = pergunta.strip()
    resposta = resposta.strip()
    categoria = categoria.strip().upper()
    if ativo not in (0, 1):
        raise ValueError((COLOR_ERROR + 'ativo deve ser 0 ou 1' + COLOR_RESET))
    if len(pergunta) > MAX_PERGUNTA_LEN:
        raise ValueError(
            (
                COLOR_ERROR
                + 'pergunta excede '
                + str(MAX_PERGUNTA_LEN)
                + ' caracteres'
                + COLOR_RESET
            )
        )
    if len(resposta) > MAX_RESPOSTA_LEN:
        raise ValueError(
            (
                COLOR_ERROR
                + 'resposta excede '
                + str(MAX_RESPOSTA_LEN)
                + ' caracteres'
                + COLOR_RESET
            )
        )
    if len(categoria) > MAX_CATEGORIA_LEN:
        raise ValueError(
            (
                COLOR_ERROR
                + 'categoria excede '
                + str(MAX_CATEGORIA_LEN)
                + ' caracteres'
                + COLOR_RESET
            )
        )
    try:
        conn.cursor.execute(
            SQL_UPDATE, (pergunta, resposta, ativo, categoria, user_adm_id_user_adm, id)
        )
        rows_affected = conn.cursor.rowcount
        conn.conn.commit()
        from config.settings import show_message

        if rows_affected > 0:
            show_message('FAQ ID ' + str(id) + ' atualizada com sucesso.', 'success')
        return rows_affected > 0
    except Exception as e:
        if conn.conn:
            conn.conn.rollback()
        msg = str(e)
        from config.settings import show_message

        if 'ORA-00001' in msg:
            show_message('Pergunta já cadastrada (violação de UNIQUE).', 'warning')
        elif 'ORA-12899' in msg:
            show_message(
                'Valor excede o tamanho permitido para a coluna (ORA-12899).', 'warning'
            )
        else:
            show_message('Erro ao atualizar FAQ: ' + msg, 'error')
        return False


def deletar(conn, id):
    try:
        conn.cursor.execute(SQL_DELETE, (id,))
        rows_affected = conn.cursor.rowcount
        conn.conn.commit()
        from config.settings import show_message

        if rows_affected > 0:
            show_message('FAQ ID ' + str(id) + ' deletada com sucesso.', 'success')
        else:
            show_message(
                'FAQ ID ' + str(id) + ' não encontrada para exclusão.', 'warning'
            )
        return rows_affected > 0
    except Exception:
        if conn.conn:
            conn.conn.rollback()
        from config.settings import show_message

        show_message('Erro ao deletar FAQ.', 'error')
        return False


def buscar_por_id(conn, id):
    from models import FAQ

    try:
        conn.cursor.execute(SQL_SELECT_BY_ID, (id,))
        row = conn.cursor.fetchone()
        if row:
            return FAQ(*row)
        else:
            return None
    except Exception:
        from config.settings import show_message

        show_message('Erro ao buscar FAQ.', 'error')
        return None


def listar_categorias(conn):
    try:
        conn.cursor.execute(SQL_SELECT_DISTINCT_CATEGORIES)
        rows = conn.cursor.fetchall()
        return [row[0] for row in rows]
    except Exception:
        from config.settings import show_message

        show_message('Erro ao listar categorias.', 'error')
        return []

class FaqDB:
    def menu_crud(self):
        from config.settings import (
            COLOR_OPTION,
            COLOR_PROMPT,
            COLOR_RESET,
            COLOR_TITLE,
            show_message,
        )

        while True:
            from config.settings import (
                PROMPT_ATIVO,
                PROMPT_CATEGORIA,
                PROMPT_PERGUNTA,
                PROMPT_RESPOSTA,
            )

            print(f'\n{COLOR_TITLE}--- CRUD FAQ (Banco Oracle) ---{COLOR_RESET}')
            print(f'{COLOR_OPTION}1. Adicionar FAQ{COLOR_RESET}')
            print(f'{COLOR_OPTION}2. Atualizar FAQ{COLOR_RESET}')
            print(f'{COLOR_OPTION}3. Deletar FAQ{COLOR_RESET}')
            print(f'{COLOR_OPTION}4. Listar FAQs{COLOR_RESET}')
            print(f'{COLOR_OPTION}0. Voltar ao menu principal{COLOR_RESET}')
            opcao = input(f'{COLOR_PROMPT}Escolha uma opção: {COLOR_RESET}').strip()
            if opcao == '1':
                from config.settings import input_id, validar_campos_obrigatorios

                try:
                    pergunta = input(PROMPT_PERGUNTA).strip()
                    resposta = input(PROMPT_RESPOSTA).strip()
                    ativo_str = input(PROMPT_ATIVO).strip()
                    categoria = input(PROMPT_CATEGORIA).strip()
                    user_adm_id_user_adm = input_id('ID do admin responsável: ')
                    if not validar_campos_obrigatorios(pergunta, resposta, categoria):
                        return
                    while ativo_str not in ['0', '1']:
                        show_message(
                            'Valor para "Ativo" deve ser 1 (Sim) ou 0 (Não).', 'error'
                        )
                        ativo_str = input(PROMPT_ATIVO).strip()
                    ativo = int(ativo_str)
                    self.adicionar(
                        pergunta, resposta, ativo, categoria, user_adm_id_user_adm
                    )
                except Exception as e:
                    show_message(f'Erro ao adicionar FAQ: {e}', 'error')
            elif opcao == '2':
                from config.settings import input_id, validar_campos_obrigatorios

                try:
                    id_faq = input_id('ID do FAQ a atualizar: ')
                    pergunta = input(PROMPT_PERGUNTA).strip()
                    resposta = input(PROMPT_RESPOSTA).strip()
                    ativo_str = input(PROMPT_ATIVO).strip()
                    categoria = input(PROMPT_CATEGORIA).strip()
                    user_adm_id_user_adm = input_id('ID do admin responsável: ')
                    if not validar_campos_obrigatorios(pergunta, resposta, categoria):
                        return
                    while ativo_str not in ['0', '1']:
                        show_message(
                            'Valor para "Ativo" deve ser 1 (Sim) ou 0 (Não).', 'error'
                        )
                        ativo_str = input(PROMPT_ATIVO).strip()
                    ativo = int(ativo_str)
                    self.atualizar(
                        id_faq,
                        pergunta,
                        resposta,
                        ativo,
                        categoria,
                        user_adm_id_user_adm,
                    )
                except Exception as e:
                    show_message(f'Erro ao atualizar FAQ: {e}', 'error')
            elif opcao == '3':
                from config.settings import input_id

                try:
                    id_faq = input_id('ID do FAQ a deletar: ')
                    self.deletar(id_faq)
                except Exception as e:
                    show_message(f'Erro ao deletar FAQ: {e}', 'error')
            elif opcao == '4':
                faqs = self.listar()
                from config.settings import show_message

                if not faqs:
                    show_message('Nenhum FAQ encontrado.', 'warning')
                else:
                    for faq in faqs:
                        show_message(str(faq), 'info')
            elif opcao == '0':
                break
            else:
                show_message('Opção inválida.', 'error')

    def __init__(self, oracle_config, silent=False):
        self.conn = OracleConnection(oracle_config, silent)
        self.silent = silent

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close(silent=True)
        return False

    def adicionar(self, pergunta, resposta, ativo, categoria, user_adm_id_user_adm):
        return adicionar(
            self.conn, pergunta, resposta, ativo, categoria, user_adm_id_user_adm
        )

    def listar(self, categoria=None, limit=None):
        return listar(self.conn, categoria, limit)

    def atualizar(self, id, pergunta, resposta, ativo, categoria, user_adm_id_user_adm):
        return atualizar(
            self.conn, id, pergunta, resposta, ativo, categoria, user_adm_id_user_adm
        )

    def deletar(self, id):
        return deletar(self.conn, id)

    def buscar_por_id(self, id):
        return buscar_por_id(self.conn, id)

    def listar_categorias(self):
        return listar_categorias(self.conn)

    def close(self, silent=None):
        if self.conn:
            self.conn.close(silent)
