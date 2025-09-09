def atualizar_faq(db):
    """Atualiza um FAQ existente."""
    try:
        id_str = input('Digite o ID do FAQ a atualizar: ').strip()
        if not id_str.isdigit():
            print('ID deve ser um número inteiro.')
            return
        id = int(id_str)
        while True:
            print('\n--- Atualizar FAQ ---')
            print('1. Atualizar Pergunta')
            print('2. Atualizar Resposta')
            print('3. Atualizar Categoria')
            print('4. Ativar/Desativar FAQ')
            print('0. Voltar')
            opcao = input('Escolha uma opção: ').strip()
            if opcao == '1':
                atualizar_pergunta(db, id)
            elif opcao == '2':
                atualizar_resposta(db, id)
            elif opcao == '3':
                atualizar_categoria(db, id)
            elif opcao == '4':
                ativar_desativar_faq(db, id)
            elif opcao == '0':
                break
            else:
                print('Opção inválida! Digite o número da opção desejada.')
    except Exception as e:
        print(f'Erro ao atualizar FAQ: {e}')
    else:
        print('FAQ atualizado com sucesso!')
    finally:
        print('[LOG] Operação de atualização finalizada.')


def atualizar_pergunta(db, id):
    nova_pergunta = input('Digite a nova pergunta (ou 0 para cancelar): ').strip()
    if nova_pergunta == '0':
        print('Atualização de pergunta cancelada.')
        return
    if nova_pergunta:
        db.atualizar(id, nova_pergunta, None, None, None)
        print('Pergunta atualizada com sucesso!')
    else:
        print('Pergunta não pode ser vazia.')


def atualizar_resposta(db, id):
    nova_resposta = input('Digite a nova resposta (ou 0 para cancelar): ').strip()
    if nova_resposta == '0':
        print('Atualização de resposta cancelada.')
        return
    if nova_resposta:
        db.atualizar(id, None, nova_resposta, None, None)
        print('Resposta atualizada com sucesso!')
    else:
        print('Resposta não pode ser vazia.')


def atualizar_categoria(db, id):
    nova_categoria = input('Digite a nova categoria (ou 0 para cancelar): ').strip()
    if nova_categoria == '0':
        print('Atualização de categoria cancelada.')
        return
    if nova_categoria:
        db.atualizar(id, None, None, None, nova_categoria)
        print('Categoria atualizada com sucesso!')
    else:
        print('Categoria não pode ser vazia.')


def ativar_desativar_faq(db, id):
    ativo_str = input('Ativo? (1-Sim, 0-Não, ou apenas 0 para cancelar): ').strip()
    if ativo_str == '0':
        print('Atualização de status cancelada.')
        return
    if ativo_str not in ['1', '0']:
        print('Valor para "Ativo" deve ser 1 (Sim) ou 0 (Não).')
        return
    ativo = int(ativo_str)
    db.atualizar(id, None, None, ativo, None)
    print('Status do FAQ atualizado com sucesso!')
