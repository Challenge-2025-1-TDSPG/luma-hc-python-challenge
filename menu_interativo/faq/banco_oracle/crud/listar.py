def listar_faqs(db):
    """Lista todas as FAQs cadastradas, com opção de filtro por categoria."""
    operacao_iniciada = False

    try:
        categoria = input('Filtrar por categoria (deixe vazio para todas): ').strip()

        operacao_iniciada = True

        faqs = db.listar(categoria if categoria else None)
        if faqs:
            for faq in faqs:
                print(faq)
                print('-' * 30)
        else:
            print('Nenhum FAQ cadastrado.')
    except Exception as e:
        print(f'Erro ao listar FAQs: {e}')
    finally:
        if operacao_iniciada:
            print('[LOG] Operação de listagem finalizada.')
