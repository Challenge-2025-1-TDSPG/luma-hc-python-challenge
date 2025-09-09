def listar_categorias(db):
    """Lista todas as categorias disponíveis no banco."""
    operacao_iniciada = False

    try:
        operacao_iniciada = True

        categorias = db.listar_categorias()
        if categorias:
            print('Categorias disponíveis:')
            for categoria in categorias:
                print(f'- {categoria}')
        else:
            print('Nenhuma categoria cadastrada.')
    except Exception as e:
        print(f'Erro ao listar categorias: {e}')
    finally:
        if operacao_iniciada:
            print('[LOG] Operação de listagem de categorias finalizada.')
