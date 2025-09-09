import sqlite3
from datetime import datetime

from .models import FAQ


class FaqDB:
    """
    Classe responsável por gerenciar o banco de dados dos itens de FAQ.
    """
    def __init__(self, db_name='faq_perguntas.db'):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        try:
            self.conn.execute("""CREATE TABLE IF NOT EXISTS perguntas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pergunta TEXT NOT NULL,
                resposta TEXT NOT NULL,
                ativo INTEGER NOT NULL,
                atualizado_em TEXT NOT NULL,
                pasta TEXT NOT NULL
            )""")
            self.conn.commit()
        except sqlite3.Error as e:
            print(f'Erro ao criar tabela: {e}')

    def adicionar(self, pergunta, resposta, ativo, pasta):
        try:
            atualizado_em = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.conn.execute(
                'INSERT INTO perguntas (pergunta, resposta, ativo, atualizado_em, pasta) VALUES (?, ?, ?, ?, ?)',
                (pergunta, resposta, ativo, atualizado_em, pasta),
            )
            self.conn.commit()
            print('Pergunta adicionada com sucesso!')
        except sqlite3.Error as e:
            print(f'Erro ao adicionar pergunta: {e}')

    def listar(self, pasta=None):
        try:
            if pasta:
                cursor = self.conn.execute(
                    'SELECT * FROM perguntas WHERE pasta=?', (pasta,)
                )
            else:
                cursor = self.conn.execute('SELECT * FROM perguntas')
            perguntas = [FAQ(*row) for row in cursor]
            return perguntas
        except sqlite3.Error as e:
            print(f'Erro ao listar perguntas: {e}')
            return []

    def atualizar(self, id, pergunta, resposta, ativo, pasta):
        try:
            atualizado_em = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.conn.execute(
                'UPDATE perguntas SET pergunta=?, resposta=?, ativo=?, atualizado_em=?, pasta=? WHERE id=?',
                (pergunta, resposta, ativo, atualizado_em, pasta, id),
            )
            self.conn.commit()
            print('Pergunta atualizada com sucesso!')
        except sqlite3.Error as e:
            print(f'Erro ao atualizar pergunta: {e}')

    def deletar(self, id):
        try:
            self.conn.execute('DELETE FROM perguntas WHERE id=?', (id,))
            self.conn.commit()
            print('Pergunta deletada com sucesso!')
        except sqlite3.Error as e:
            print(f'Erro ao deletar pergunta: {e}')

    def buscar_por_id(self, id):
        try:
            cursor = self.conn.execute('SELECT * FROM perguntas WHERE id=?', (id,))
            row = cursor.fetchone()
            if row:
                return FAQ(*row)
            else:
                print('Pergunta não encontrada.')
                return None
        except sqlite3.Error as e:
            print(f'Erro ao buscar pergunta: {e}')
            return None

    def listar_pastas(self):
        try:
            cursor = self.conn.execute('SELECT DISTINCT pasta FROM perguntas')
            return [row[0] for row in cursor]
        except sqlite3.Error as e:
            print(f'Erro ao listar pastas: {e}')
            return []

    def close(self):
        self.conn.close()
