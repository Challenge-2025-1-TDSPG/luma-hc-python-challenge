def deletar_faq(db):
    """Remove um FAQ pelo ID."""
    operacao_iniciada = False

    try:
        id_str = input('Digite o ID do FAQ a deletar: ').strip()
        if not id_str.isdigit():
            print('ID deve ser um número inteiro.')
            return
        id = int(id_str)
        # Verifica se o FAQ existe antes de tentar deletar
        faq = db.buscar_por_id(id)
        if not faq:
            print('FAQ não encontrado.')
            return

        operacao_iniciada = True

        input('Pressione Enter para confirmar a exclusão...')
        db.deletar(id)
    except Exception as e:
        print(f'Erro ao deletar FAQ: {e}')
    else:
        print('FAQ deletado com sucesso!')
    finally:
        if operacao_iniciada:
            print('[LOG] Operação de exclusão finalizada.')
