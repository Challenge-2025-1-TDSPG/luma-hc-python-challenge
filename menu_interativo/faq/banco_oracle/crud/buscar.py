def buscar_faq(db):
    """Busca um FAQ pelo ID."""
    operacao_iniciada = False

    try:
        id_str = input('Digite o ID do FAQ: ').strip()
        if not id_str.isdigit():
            print('ID deve ser um número inteiro.')
            return
        id = int(id_str)

        operacao_iniciada = True

        faq = db.buscar_por_id(id)
        if faq:
            print(faq)
        else:
            print(f'FAQ com ID {id} não encontrado no banco de dados.')
    except Exception as e:
        print(f'Erro ao buscar FAQ: {e}')
    finally:
        if operacao_iniciada:
            print('[LOG] Operação de busca finalizada.')
