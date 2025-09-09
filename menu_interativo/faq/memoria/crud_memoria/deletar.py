def remover_faq_memoria(lista):
    id_str = input('ID do FAQ a remover: ').strip()
    if not id_str.isdigit():
        print('ID deve ser número.')
        return
    id = int(id_str)
    lista[:] = [item for item in lista if item['id'] != id]
    print('FAQ removido em memória!')
