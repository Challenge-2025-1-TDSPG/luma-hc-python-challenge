def remover_faq_memoria(lista):
    """Remove um FAQ da memória pelo ID."""
    operacao_iniciada = False

    try:
        id_str = input('ID do FAQ a remover: ').strip()
        if not id_str.isdigit():
            print('ID deve ser número.')
            return
        id = int(id_str)
        if not any(item['id'] == id for item in lista):
            print('FAQ não encontrado.')
            return

        operacao_iniciada = True

        lista[:] = [item for item in lista if item['id'] != id]
        print('FAQ removido em memória!')
    except Exception as e:
        print(f'Erro ao remover FAQ da memória: {e}')
    finally:
        if operacao_iniciada:
            print('[LOG] Operação de exclusão em memória finalizada.')
