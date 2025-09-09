def atualizar_faq(db):
    """Atualiza um FAQ existente."""
    try:
        id_str = input('Digite o ID do FAQ a atualizar: ').strip()
        if not id_str.isdigit():
            print('ID deve ser um número inteiro.')
            return
        id = int(id_str)
        pergunta = input('Nova pergunta: ').strip()
        resposta = input('Nova resposta: ').strip()
        categoria = input('Nova categoria: ').strip()
        ativo_str = input('Ativo? (1-Sim, 0-Não): ').strip()
        if not (pergunta and resposta and categoria):
            print('Todos os campos são obrigatórios!')
            return
        if ativo_str not in ['0', '1']:
            print('Valor para "Ativo" deve ser 1 (Sim) ou 0 (Não).')
            return
        ativo = int(ativo_str)
        db.atualizar(id, pergunta, resposta, ativo, categoria)
    except Exception as e:
        print(f'Erro ao atualizar FAQ: {e}')
    else:
        print('FAQ atualizado com sucesso!')
    finally:
        print('[LOG] Operação de atualização finalizada.')
