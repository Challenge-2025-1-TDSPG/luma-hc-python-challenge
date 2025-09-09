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
            # Criação da tabela
            self.cursor.execute("""
                BEGIN
                    EXECUTE IMMEDIATE 'CREATE TABLE FAQ (
                        id NUMBER PRIMARY KEY,
                        pergunta VARCHAR2(4000) NOT NULL,
                        resposta VARCHAR2(4000) NOT NULL,
                        ativo NUMBER(1) NOT NULL,
                        atualizado_em VARCHAR2(50) NOT NULL,
                        categoria VARCHAR2(255) NOT NULL
                    )';
                EXCEPTION
                    WHEN OTHERS THEN
                        IF SQLCODE != -955 THEN RAISE; END IF;
                END;
            """)
            # Criação da sequence
            self.cursor.execute("""
                BEGIN
                    EXECUTE IMMEDIATE 'CREATE SEQUENCE faq_seq START WITH 1 INCREMENT BY 1';
                EXCEPTION
                    WHEN OTHERS THEN
                        IF SQLCODE != -955 THEN RAISE; END IF;
                END;
            """)
            # Criação do trigger para autoincremento
            self.cursor.execute("""
                BEGIN
                    EXECUTE IMMEDIATE '
                        CREATE OR REPLACE TRIGGER faq_bi
                        BEFORE INSERT ON FAQ
                        FOR EACH ROW
                        WHEN (new.id IS NULL)
                        BEGIN
                            SELECT perguntas_seq.NEXTVAL INTO :new.id FROM dual;
                        END;';
                EXCEPTION
                    WHEN OTHERS THEN
                        IF SQLCODE != -4080 THEN RAISE; END IF;
                END;
            """)
            self.conn.commit()
        except Exception as e:
            print(f'Erro ao criar tabela Oracle: {e}')

    def adicionar(self, pergunta, resposta, ativo, categoria):
        atualizado_em = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            sql = 'INSERT INTO perguntas (id, pergunta, resposta, ativo, atualizado_em, categoria) VALUES (perguntas_seq.NEXTVAL, :1, :2, :3, :4, :5)'
            self.cursor.execute(
                sql, (pergunta, resposta, ativo, atualizado_em, categoria)
            )
            self.conn.commit()
            print('Pergunta adicionada com sucesso!')
        except Exception as e:
            print(f'Erro ao adicionar pergunta: {e}')

    def listar(self, categoria=None):
        try:
            if categoria:
                sql = 'SELECT * FROM perguntas WHERE categoria = :1'
                self.cursor.execute(sql, (categoria,))
            else:
                sql = 'SELECT * FROM perguntas'
                self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            perguntas = [FAQ(*row) for row in rows]
            return perguntas
        except Exception as e:
            print(f'Erro ao listar perguntas: {e}')
            return []

    def atualizar(self, id, pergunta, resposta, ativo, categoria):
        atualizado_em = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            sql = 'UPDATE perguntas SET pergunta=:1, resposta=:2, ativo=:3, atualizado_em=:4, categoria=:5 WHERE id=:6'
            self.cursor.execute(
                sql, (pergunta, resposta, ativo, atualizado_em, categoria, id)
            )
            self.conn.commit()
            print('Pergunta atualizada com sucesso!')
        except Exception as e:
            print(f'Erro ao atualizar pergunta: {e}')

    def deletar(self, id):
        try:
            sql = 'DELETE FROM perguntas WHERE id=:1'
            self.cursor.execute(sql, (id,))
            self.conn.commit()
            print('Pergunta deletada com sucesso!')
        except Exception as e:
            print(f'Erro ao deletar pergunta: {e}')

    def buscar_por_id(self, id):
        try:
            sql = 'SELECT * FROM perguntas WHERE id=:1'
            self.cursor.execute(sql, (id,))
            row = self.cursor.fetchone()
            if row:
                return FAQ(*row)
            else:
                print('Pergunta não encontrada.')
                return None
        except Exception as e:
            print(f'Erro ao buscar pergunta: {e}')
            return None

    def listar_categorias(self):
        try:
            sql = 'SELECT DISTINCT categoria FROM perguntas'
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
