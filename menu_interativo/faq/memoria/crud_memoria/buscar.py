def buscar_faq_memoria(lista):
    """Busca um FAQ em memória pelo ID."""
    operacao_iniciada = False

    try:
        id_str = input('ID do FAQ a buscar: ').strip()
        if not id_str.isdigit():
            print('ID deve ser número.')
            return
        id = int(id_str)

        operacao_iniciada = True

        encontrados = [item for item in lista if item['id'] == id]
        if encontrados:
            for faq in encontrados:
                print(
                    f'ID: {faq["id"]}\nPergunta: {faq["pergunta"]}\nResposta: {faq.get("resposta", "")}\nAtivo: {faq.get("ativo", "")}\nAtualizado em: {faq.get("atualizado_em", "")}\nCategoria: {faq.get("categoria", "")}\n'
                    + '-' * 30
                )
        else:
            print('Nenhum FAQ encontrado com esse ID.')
    except Exception as e:
        print(f'Erro ao buscar FAQ em memória: {e}')
    finally:
        if operacao_iniciada:
            print('[LOG] Operação de busca em memória finalizada.')
