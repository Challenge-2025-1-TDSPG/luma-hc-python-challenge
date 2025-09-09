def buscar_faq(db):
    """Busca um FAQ pelo ID."""
    try:
        id_str = input('Digite o ID do FAQ: ').strip()
        if not id_str.isdigit():
            print('ID deve ser um número inteiro.')
            return
        id = int(id_str)
        faq = db.buscar_por_id(id)
        if faq:
            print(faq)
    except Exception as e:
        print(f'Erro ao buscar FAQ: {e}')
