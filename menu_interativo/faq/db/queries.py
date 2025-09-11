"""
Constantes e definições SQL para operações no banco de dados FAQ.
"""

# Constantes para os valores SQL
FAQ_TABLE_NAME = 'FAQ'
MAX_PERGUNTA_LEN = 150
MAX_RESPOSTA_LEN = 600
MAX_CATEGORIA_LEN = 50
ATIVO_TYPE = 'NUMBER(1)'

# SQL para operações de inserção
# Não inclui ATUALIZADO_EM pois o banco define automaticamente via DEFAULT SYSDATE
SQL_INSERT = f"""
    INSERT INTO {FAQ_TABLE_NAME}
    (PERGUNTA, RESPOSTA, ATIVO, CATEGORIA)
    VALUES (:1, :2, :3, :4)
"""

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

# Comando para excluir um FAQ pelo ID
SQL_DELETE = f'DELETE FROM {FAQ_TABLE_NAME} WHERE ID_FAQ=:1'

# Busca completa de um FAQ pelo ID (todas as colunas listadas explicitamente)
SQL_SELECT_BY_ID = f'SELECT ID_FAQ, PERGUNTA, RESPOSTA, ATIVO, ATUALIZADO_EM, CATEGORIA FROM {FAQ_TABLE_NAME} WHERE ID_FAQ=:1'

# Lista todas as categorias distintas para popular menus/filtros
SQL_SELECT_DISTINCT_CATEGORIES = f'SELECT DISTINCT CATEGORIA FROM {FAQ_TABLE_NAME}'
