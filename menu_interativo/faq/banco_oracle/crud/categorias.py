def listar_categorias(db):
    categorias = db.listar_categorias()
    if categorias:
        print('Categorias disponíveis:')
        for categoria in categorias:
            print(f'- {categoria}')
    else:
        print('Nenhuma categoria cadastrada.')
