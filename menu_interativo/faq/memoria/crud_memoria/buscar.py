def buscar_faq_memoria(lista):
    id_str = input('ID do FAQ a buscar: ').strip()
    if not id_str.isdigit():
        print('ID deve ser número.')
        return
    id = int(id_str)
    encontrados = [item for item in lista if item['id'] == id]
    if encontrados:
        for faq in encontrados:
            print(
                f'ID: {faq["id"]}\nPergunta: {faq["pergunta"]}\nResposta: {faq.get("resposta", "")}\nAtivo: {faq.get("ativo", "")}\nAtualizado em: {faq.get("atualizado_em", "")}\nCategoria: {faq.get("categoria", "")}\n'
                + '-' * 30
            )
    else:
        print('Nenhum FAQ encontrado com esse ID.')
