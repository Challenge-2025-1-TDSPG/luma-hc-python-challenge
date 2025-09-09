def adicionar_faq(db):
    """Adiciona um novo FAQ (pergunta, resposta, categoria, ativo) ao banco."""
    operacao_iniciada = False

    try:
        pergunta = input('Digite a pergunta: ').strip()
        resposta = input('Digite a resposta: ').strip()
        categoria = input('Digite o nome da categoria: ').strip()
        ativo_str = input('Ativo? (1-Sim, 0-Não): ').strip()
        if not (pergunta and resposta and categoria):
            print('Todos os campos são obrigatórios!')
            return
        if ativo_str not in ['0', '1']:
            print('Valor para "Ativo" deve ser 1 (Sim) ou 0 (Não).')
            return

        operacao_iniciada = True

        ativo = int(ativo_str)
        db.adicionar(pergunta, resposta, ativo, categoria)
        # Buscar o último FAQ adicionado (assumindo que o maior id é o último)
        faqs = db.listar()
        if faqs:
            novo_faq = max(faqs, key=lambda f: f.id)
            print('FAQ adicionado com sucesso!')
            print(novo_faq)
        else:
            print('FAQ adicionado, mas não foi possível exibir.')
    except Exception as e:
        print(f'Erro ao adicionar FAQ: {e}')
    finally:
        if operacao_iniciada:
            print('[LOG] Operação de inserção finalizada.')
