def deletar_faq(db):
    """Remove um FAQ pelo ID."""
    try:
        id_str = input('Digite o ID do FAQ a deletar: ').strip()
        if not id_str.isdigit():
            print('ID deve ser um número inteiro.')
            return
        id = int(id_str)
        input('Pressione Enter para confirmar a exclusão...')
        db.deletar(id)
    except Exception as e:
        print(f'Erro ao deletar FAQ: {e}')
    else:
        print('FAQ deletado com sucesso!')
    finally:
        print('[LOG] Operação de exclusão finalizada.')
