from datetime import datetime

from .models import FAQ


class FaqDB:
    """
    Classe responsável por gerenciar o banco de dados dos itens de FAQ (Oracle).
    """

    def __init__(self, oracle_config):
        """
        oracle_config: dict com chaves user, password, dsn
        """
        try:
            import cx_Oracle

            if oracle_config:
                self.conn = cx_Oracle.connect(
                    user=oracle_config['user'],
                    password=oracle_config['password'],
                    dsn=oracle_config['dsn'],
                )
            else:
                raise Exception('oracle_config deve ser fornecido para Oracle')
            self.cursor = self.conn.cursor()
            self.create_table_oracle()
        except ImportError:
            print('cx_Oracle não instalado. Instale com: pip install cx_Oracle')
            raise

    def create_table_oracle(self):
        try:
            # Criação da tabela com IDENTITY (Oracle 12c+)
            self.cursor.execute("""
                BEGIN
                    EXECUTE IMMEDIATE 'CREATE TABLE FAQ (
                        id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                        pergunta VARCHAR2(150) NOT NULL,
                        resposta VARCHAR2(600) NOT NULL,
                        ativo NUMBER(1) NOT NULL,
                        atualizado_em VARCHAR2(50) NOT NULL,
                        categoria VARCHAR2(50) NOT NULL
                    )';
                EXCEPTION
                    WHEN OTHERS THEN
                        IF SQLCODE != -955 THEN RAISE; END IF;
                END;
            """)
            self.conn.commit()
        except Exception as e:
            print(f'Erro ao criar tabela Oracle: {e}')

    def adicionar(self, pergunta, resposta, ativo, categoria):
        atualizado_em = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            sql = 'INSERT INTO FAQ (pergunta, resposta, ativo, atualizado_em, categoria) VALUES (:1, :2, :3, :4, :5)'
            self.cursor.execute(
                sql, (pergunta, resposta, ativo, atualizado_em, categoria)
            )
            self.conn.commit()
            print('FAQ adicionada com sucesso!')
        except Exception as e:
            print(f'Erro ao adicionar FAQ: {e}')

    def listar(self, categoria=None):
        try:
            if categoria:
                sql = 'SELECT * FROM FAQ WHERE categoria = :1'
                self.cursor.execute(sql, (categoria,))
            else:
                sql = 'SELECT * FROM FAQ'
                self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            perguntas = [FAQ(*row) for row in rows]
            return perguntas
        except Exception as e:
            print(f'Erro ao listar FAQ: {e}')
            return []

    def atualizar(self, id, pergunta, resposta, ativo, categoria):
        atualizado_em = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            sql = 'UPDATE FAQ SET pergunta=:1, resposta=:2, ativo=:3, atualizado_em=:4, categoria=:5 WHERE id=:6'
            self.cursor.execute(
                sql, (pergunta, resposta, ativo, atualizado_em, categoria, id)
            )
            self.conn.commit()
            print('FAQ atualizada com sucesso!')
        except Exception as e:
            print(f'Erro ao atualizar FAQ: {e}')

    def deletar(self, id):
        try:
            sql = 'DELETE FROM FAQ WHERE id=:1'
            self.cursor.execute(sql, (id,))
            self.conn.commit()
            print('FAQ deletada com sucesso!')
        except Exception as e:
            print(f'Erro ao deletar FAQ: {e}')

    def buscar_por_id(self, id):
        try:
            sql = 'SELECT * FROM FAQ WHERE id=:1'
            self.cursor.execute(sql, (id,))
            row = self.cursor.fetchone()
            if row:
                return FAQ(*row)
            else:
                print('FAQ não encontrada.')
                return None
        except Exception as e:
            print(f'Erro ao buscar FAQ: {e}')
            return None

    def listar_categorias(self):
        try:
            sql = 'SELECT DISTINCT categoria FROM FAQ'
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            return [row[0] for row in rows]
        except Exception as e:
            print(f'Erro ao listar categorias: {e}')
            return []

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
