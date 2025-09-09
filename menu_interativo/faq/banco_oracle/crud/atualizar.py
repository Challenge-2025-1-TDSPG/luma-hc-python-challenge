def atualizar_faq(db):
    """Atualiza um FAQ existente."""
    operacao_iniciada = False

    try:
        id_str = input('Digite o ID do FAQ a atualizar: ').strip()
        if not id_str.isdigit():
            print('ID deve ser um número inteiro.')
            return
        id = int(id_str)

        # Verifica se o FAQ existe antes de mostrar o menu
        faq = db.buscar_por_id(id)
        if not faq:
            print(f'FAQ com ID {id} não encontrado no banco de dados.')
            return

        operacao_iniciada = True

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
    finally:
        if operacao_iniciada:
            print('[LOG] Operação de atualização finalizada.')


def atualizar_pergunta(db, id):
    nova_pergunta = input('Digite a nova pergunta (ou 0 para cancelar): ').strip()
    if nova_pergunta == '0':
        print('Operação cancelada. Pergunta não foi alterada.')
        return
    if nova_pergunta:
        # Não busca novamente, pois já foi verificado antes
        faq = db.buscar_por_id(id)
        if not faq:
            print(f'Erro: FAQ com ID {id} não está mais disponível.')
            return
        if db.atualizar(id, nova_pergunta, faq.resposta, faq.ativo, faq.categoria):
            print('Pergunta atualizada com sucesso!')
        else:
            print('Falha ao atualizar pergunta. Verifique se o FAQ ainda existe.')
    else:
        print('Pergunta não pode ser vazia.')


def atualizar_resposta(db, id):
    nova_resposta = input('Digite a nova resposta (ou 0 para cancelar): ').strip()
    if nova_resposta == '0':
        print('Operação cancelada. Resposta não foi alterada.')
        return
    if nova_resposta:
        faq = db.buscar_por_id(id)
        if not faq:
            print(f'Erro: FAQ com ID {id} não está mais disponível.')
            return
        if db.atualizar(id, faq.pergunta, nova_resposta, faq.ativo, faq.categoria):
            print('Resposta atualizada com sucesso!')
        else:
            print('Falha ao atualizar resposta. Verifique se o FAQ ainda existe.')
    else:
        print('Resposta não pode ser vazia.')


def atualizar_categoria(db, id):
    nova_categoria = input('Digite a nova categoria (ou 0 para cancelar): ').strip()
    if nova_categoria == '0':
        print('Operação cancelada. Categoria não foi alterada.')
        return
    if nova_categoria:
        faq = db.buscar_por_id(id)
        if not faq:
            print(f'Erro: FAQ com ID {id} não está mais disponível.')
            return
        if db.atualizar(id, faq.pergunta, faq.resposta, faq.ativo, nova_categoria):
            print('Categoria atualizada com sucesso!')
        else:
            print('Falha ao atualizar categoria. Verifique se o FAQ ainda existe.')
    else:
        print('Categoria não pode ser vazia.')


def ativar_desativar_faq(db, id):
    # Busca o FAQ para verificar status atual
    faq = db.buscar_por_id(id)
    if not faq:
        print(f'Erro: FAQ com ID {id} não está mais disponível.')
        return

    # Mostra o status atual
    status_atual = 'ativado' if faq.ativo == 1 else 'desativado'
    print(f'\nStatus atual do FAQ: {status_atual}')

    print('Opções: 1-Ativar FAQ, 0-Desativar FAQ, C-Cancelar')
    ativo_str = input('Escolha uma opção: ').strip().upper()

    if ativo_str == 'C':
        print('Operação cancelada. Nenhuma alteração foi feita.')
        return

    if ativo_str not in ['1', '0']:
        print('Valor para status deve ser 1 (Ativar), 0 (Desativar) ou C (Cancelar).')
        return

    novo_ativo = int(ativo_str)

    # Verifica se já está no estado desejado
    if (novo_ativo == 1 and faq.ativo == 1) or (novo_ativo == 0 and faq.ativo == 0):
        print(f'FAQ já está {status_atual}. Nenhuma alteração necessária.')
        return

    # Atualiza o FAQ
    if db.atualizar(id, faq.pergunta, faq.resposta, novo_ativo, faq.categoria):
        novo_status = 'ativado' if novo_ativo == 1 else 'desativado'
        print(f'Status do FAQ atualizado com sucesso! FAQ agora está {novo_status}.')
    else:
        print(
            f'Falha ao atualizar o status. Verifique se o FAQ com ID {id} ainda existe.'
        )
