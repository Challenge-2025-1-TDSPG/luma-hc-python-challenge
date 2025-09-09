"""
API RESTful para gerenciamento de FAQs usando Flask.
"""

import os

from dotenv import load_dotenv
from flask import Flask, abort, jsonify, request

from ...menu_interativo.faq.db import FaqDB

app = Flask(__name__)

load_dotenv()
oracle_config = {
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASS'),
    'dsn': os.environ.get('DB_URL'),
}
# Validação das credenciais Oracle
try:
    test_db = FaqDB(oracle_config)
    test_db.close()
except Exception as e:
    import sys

    print(
        '\n[ERRO] Não foi possível conectar ao banco Oracle. Verifique as credenciais e o DSN.'
    )
    print(f'Detalhes: {e}')
    sys.exit(1)
db = FaqDB(oracle_config)


@app.route('/faqs', methods=['GET'])
def listar_faqs():
    """Retorna todos os FAQs."""
    faqs = db.listar()
    return jsonify([faq.__dict__ for faq in faqs])


@app.route('/faqs/<int:faq_id>', methods=['GET'])
def obter_faq(faq_id):
    """Retorna um FAQ pelo ID."""
    faqs = db.listar()
    for faq in faqs:
        if faq.id == faq_id:
            return jsonify(faq.__dict__)
    abort(404, description='FAQ não encontrado')


@app.route('/faqs', methods=['POST'])
def adicionar_faq():
    """Adiciona um novo FAQ."""
    data = request.get_json()
    if not data or not all(
        k in data for k in ('pergunta', 'resposta', 'ativo', 'pasta')
    ):
        abort(400, description='Dados inválidos')
    db.adicionar(data['pergunta'], data['resposta'], data['ativo'], data['pasta'])
    return jsonify({'mensagem': 'FAQ adicionado com sucesso!'}), 201


@app.route('/faqs/<int:faq_id>', methods=['PUT'])
def atualizar_faq(faq_id):
    """Atualiza um FAQ existente."""
    data = request.get_json()
    if not data or not all(
        k in data for k in ('pergunta', 'resposta', 'ativo', 'pasta')
    ):
        abort(400, description='Dados inválidos')
    db.atualizar(
        faq_id, data['pergunta'], data['resposta'], data['ativo'], data['pasta']
    )
    return jsonify({'mensagem': 'FAQ atualizado com sucesso!'})


@app.route('/faqs/<int:faq_id>', methods=['DELETE'])
def deletar_faq(faq_id):
    """Remove um FAQ pelo ID."""
    db.deletar(faq_id)
    return jsonify({'mensagem': 'FAQ removido com sucesso!'})


if __name__ == '__main__':
    app.run(debug=True)
