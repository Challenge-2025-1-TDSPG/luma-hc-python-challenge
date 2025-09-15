"""
API RESTful para gerenciamento de FAQs usando Flask.
"""

import logging
import os
import sys
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, abort, jsonify, request
from flask_cors import CORS

# Adiciona o diretório pai ao caminho de importação
sys.path.insert(0, str(Path(__file__).parent.parent))
from banco import FaqDB

# Configurar logging
# Nível INFO para produção, DEBUG apenas em desenvolvimento
if os.environ.get('API_DEBUG') == '1':
    log_level = logging.DEBUG
else:
    log_level = logging.WARNING  # Reduzindo o nível para diminuir mensagens

logging.basicConfig(
    level=log_level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('faq_api')

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas as rotas

# Constantes para validação
MAX_PERGUNTA_LEN = 500
MAX_RESPOSTA_LEN = 2000
MAX_CATEGORIA_LEN = 100
ITEMS_PER_PAGE = 10

load_dotenv()
oracle_config = {
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASS'),
    'dsn': os.environ.get('DB_URL'),
}
# Inicialização do banco de dados
try:
    # Inicialização silenciosa para evitar mensagens duplicadas
    db = FaqDB(
        oracle_config, silent=True
    )  # Usar silent=True para evitar mensagens duplicadas
except Exception as e:
    logger.critical(f'Falha na conexão com o banco Oracle. Detalhes: {e}')
    print(
        '\n[ERRO] Não foi possível conectar ao banco Oracle. Verifique as credenciais e o DSN.'
    )
    print(f'Detalhes: {e}')
    sys.exit(1)


@app.errorhandler(400)
def bad_request(error):
    return jsonify({'erro': str(error.description)}), 400


@app.errorhandler(404)
def not_found(error):
    return jsonify({'erro': str(error.description)}), 404


@app.errorhandler(500)
def server_error(error):
    logger.error(f'Erro interno: {error}')
    return jsonify({'erro': 'Erro interno do servidor'}), 500


def validate_faq_data(data):
    """Valida os dados de entrada para FAQs."""
    errors = []

    if not data:
        return ['Dados não fornecidos']

    # Verificar campos obrigatórios
    required_fields = ['pergunta', 'resposta', 'ativo', 'categoria']
    for field in required_fields:
        if field not in data:
            errors.append(f"Campo obrigatório '{field}' não fornecido")

    # Se faltar algum campo obrigatório, retorna apenas esses erros
    if errors:
        return errors

    # Validar comprimento dos campos
    if len(data['pergunta']) > MAX_PERGUNTA_LEN:
        errors.append(
            f'Pergunta excede o tamanho máximo de {MAX_PERGUNTA_LEN} caracteres'
        )

    if len(data['resposta']) > MAX_RESPOSTA_LEN:
        errors.append(
            f'Resposta excede o tamanho máximo de {MAX_RESPOSTA_LEN} caracteres'
        )

    if len(data['categoria']) > MAX_CATEGORIA_LEN:
        errors.append(
            f'Categoria excede o tamanho máximo de {MAX_CATEGORIA_LEN} caracteres'
        )

    # Validar tipo dos dados
    if not isinstance(data['ativo'], int) or data['ativo'] not in [0, 1]:
        errors.append("Campo 'ativo' deve ser 0 (inativo) ou 1 (ativo)")

    return errors


@app.route('/faqs', methods=['GET'])
def listar_faqs():
    """Retorna todos os FAQs com suporte à paginação."""
    try:
        # Parâmetros de paginação
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', ITEMS_PER_PAGE, type=int)

        # Parâmetros de filtro
        categoria = request.args.get('categoria')
        ativo = request.args.get('ativo', type=int)

        # Obter todos os FAQs
        faqs = db.listar()

        # Aplicar filtros, se houver
        if categoria:
            faqs = [faq for faq in faqs if faq.categoria.lower() == categoria.lower()]
        if ativo is not None:
            faqs = [faq for faq in faqs if faq.ativo == ativo]

        # Calcular paginação
        total = len(faqs)
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page

        # Fatiar lista de acordo com a paginação
        paginated_faqs = faqs[start_idx:end_idx]

        # Construir resposta
        response = {
            'total': total,
            'page': page,
            'per_page': per_page,
            'total_pages': (total + per_page - 1) // per_page,
            'items': [faq.__dict__ for faq in paginated_faqs],
        }

        return jsonify(response)
    except Exception as e:
        logger.error(f'Erro ao listar FAQs: {e}')
        abort(500, description=f'Erro ao processar a solicitação: {str(e)}')


@app.route('/faqs/<int:faq_id>', methods=['GET'])
def obter_faq(faq_id):
    """Retorna um FAQ pelo ID."""
    try:
        faqs = db.listar()
        for faq in faqs:
            if faq.id == faq_id:
                return jsonify(faq.__dict__)
        abort(404, description='FAQ não encontrado')
    except Exception as e:
        logger.error(f'Erro ao obter FAQ {faq_id}: {e}')
        abort(500, description=f'Erro ao processar a solicitação: {str(e)}')


@app.route('/faqs', methods=['POST'])
def adicionar_faq():
    """Adiciona um novo FAQ."""
    try:
        data = request.get_json()

        # Validar dados recebidos
        errors = validate_faq_data(data)
        if errors:
            return jsonify({'erros': errors}), 400

        try:
            novo_id = db.adicionar(
                data['pergunta'], data['resposta'], data['ativo'], data['categoria']
            )

            # Retornar o ID do FAQ recém-criado
            return jsonify(
                {'mensagem': 'FAQ adicionado com sucesso!', 'id': novo_id}
            ), 201

        except Exception as db_error:
            logger.error(f'Erro de banco ao adicionar FAQ: {db_error}')
            abort(500, description='Erro ao salvar o FAQ no banco de dados')

    except Exception as e:
        logger.error(f'Erro ao adicionar FAQ: {e}')
        abort(500, description=f'Erro ao processar a solicitação: {str(e)}')


@app.route('/faqs/<int:faq_id>', methods=['PUT'])
def atualizar_faq(faq_id):
    """Atualiza um FAQ existente."""
    try:
        # Verificar se o FAQ existe
        faqs = db.listar()
        faq_existe = any(faq.id == faq_id for faq in faqs)
        if not faq_existe:
            abort(404, description=f'FAQ com ID {faq_id} não encontrado')

        data = request.get_json()

        # Validar dados recebidos
        errors = validate_faq_data(data)
        if errors:
            return jsonify({'erros': errors}), 400

        try:
            db.atualizar(
                faq_id,
                data['pergunta'],
                data['resposta'],
                data['ativo'],
                data['categoria'],
            )
            return jsonify({'mensagem': 'FAQ atualizado com sucesso!'})

        except Exception as db_error:
            logger.error(f'Erro de banco ao atualizar FAQ {faq_id}: {db_error}')
            abort(500, description='Erro ao atualizar o FAQ no banco de dados')

    except Exception as e:
        logger.error(f'Erro ao atualizar FAQ {faq_id}: {e}')
        abort(500, description=f'Erro ao processar a solicitação: {str(e)}')


@app.route('/faqs/<int:faq_id>', methods=['DELETE'])
def deletar_faq(faq_id):
    """Remove um FAQ pelo ID."""
    try:
        # Verificar se o FAQ existe
        faqs = db.listar()
        faq_existe = any(faq.id == faq_id for faq in faqs)
        if not faq_existe:
            abort(404, description=f'FAQ com ID {faq_id} não encontrado')

        try:
            db.deletar(faq_id)
            return jsonify({'mensagem': 'FAQ removido com sucesso!'})

        except Exception as db_error:
            logger.error(f'Erro de banco ao remover FAQ {faq_id}: {db_error}')
            abort(500, description='Erro ao remover o FAQ do banco de dados')

    except Exception as e:
        logger.error(f'Erro ao remover FAQ {faq_id}: {e}')
        abort(500, description=f'Erro ao processar a solicitação: {str(e)}')


@app.route('/categorias', methods=['GET'])
def listar_categorias():
    """Retorna todas as categorias disponíveis."""
    try:
        faqs = db.listar()
        # Extrair categorias únicas
        categorias = sorted(set(faq.categoria for faq in faqs))
        return jsonify(categorias)
    except Exception as e:
        logger.error(f'Erro ao listar categorias: {e}')
        abort(500, description=f'Erro ao processar a solicitação: {str(e)}')


@app.route('/status', methods=['GET'])
def status():
    """Verifica o status da API e da conexão com o banco."""
    try:
        # Tenta executar uma consulta simples para verificar a conexão
        db.listar(limit=1)
        return jsonify(
            {
                'status': 'online',
                'database': 'connected',
                'timestamp': datetime.now().isoformat(),
                'api_version': '1.0.0',
            }
        )
    except Exception as e:
        logger.error(f'Erro ao verificar status: {e}')
        return jsonify(
            {
                'status': 'degraded',
                'database': 'error',
                'error': str(e),
                'timestamp': datetime.now().isoformat(),
            }
        ), 500


if __name__ == '__main__':
    print('\n' + '=' * 60)
    print('        API FAQ v1.0 - INICIANDO SERVIDOR')
    print('=' * 60)
    print('• Servidor: http://localhost:5000')
    print('• Endpoints: /faqs, /status, /categorias')
    print('• CORS: Habilitado para todos os domínios')
    print('• Banco de dados: Oracle')
    print('=' * 60)

    # Usa threaded=True para melhor desempenho e use_reloader=False para evitar reinicializações duplicadas
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True, use_reloader=False)
