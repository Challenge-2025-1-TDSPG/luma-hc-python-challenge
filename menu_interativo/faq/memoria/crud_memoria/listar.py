def listar_faqs_memoria(lista):
    """Lista todas as FAQs armazenadas em memória."""
    operacao_iniciada = False

    try:
        operacao_iniciada = True

        if not lista:
            print('Nenhum FAQ em memória.')
        else:
            for faq in lista:
                print(
                    f'ID: {faq["id"]}\nPergunta: {faq["pergunta"]}\nResposta: {faq.get("resposta", "")}\nAtivo: {faq.get("ativo", "")}\nAtualizado em: {faq.get("atualizado_em", "")}\nCategoria: {faq.get("categoria", "")}\n'
                    + '-' * 30
                )
            print(f'Total de FAQs em memória: {len(lista)}')
    except Exception as e:
        print(f'Erro ao listar FAQs em memória: {e}')
    finally:
        if operacao_iniciada:
            print('[LOG] Operação de listagem em memória finalizada.')
