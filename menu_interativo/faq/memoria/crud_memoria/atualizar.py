from datetime import datetime


def atualizar_faq_memoria(lista):
    """Atualiza um FAQ existente em memória."""
    operacao_iniciada = False

    try:
        id_str = input('ID do FAQ a atualizar: ').strip()
        if not id_str.isdigit():
            print('ID deve ser número.')
            return
        id = int(id_str)
        # Verifica se existe FAQ com esse id
        if not any(item['id'] == id for item in lista):
            print('FAQ não encontrado.')
            return

        operacao_iniciada = True

        while True:
            print('\n--- Atualizar FAQ em Memória ---')
            print('1. Atualizar Pergunta')
            print('2. Atualizar Resposta')
            print('3. Atualizar Categoria')
            print('4. Ativar/Desativar FAQ')
            print('0. Voltar')
            opcao = input('Escolha uma opção: ').strip()
            if opcao == '1':
                atualizar_pergunta_memoria(lista, id)
            elif opcao == '2':
                atualizar_resposta_memoria(lista, id)
            elif opcao == '3':
                atualizar_categoria_memoria(lista, id)
            elif opcao == '4':
                ativar_desativar_faq_memoria(lista, id)
            elif opcao == '0':
                break
            else:
                print('Opção inválida! Digite o número da opção desejada.')
    except Exception as e:
        print(f'Erro ao atualizar FAQ em memória: {e}')
    finally:
        if operacao_iniciada:
            print('[LOG] Operação de atualização em memória finalizada.')


def atualizar_pergunta_memoria(lista, id):
    nova_pergunta = input('Nova pergunta do FAQ (ou 0 para cancelar): ').strip()
    if nova_pergunta == '0':
        print('Atualização de pergunta cancelada.')
        return
    if nova_pergunta:
        for item in lista:
            if item['id'] == id:
                item['pergunta'] = nova_pergunta
                item['atualizado_em'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print('Pergunta atualizada com sucesso!')
                break
    else:
        print('Pergunta não pode ser vazia.')


def atualizar_resposta_memoria(lista, id):
    nova_resposta = input('Nova resposta do FAQ (ou 0 para cancelar): ').strip()
    if nova_resposta == '0':
        print('Atualização de resposta cancelada.')
        return
    if nova_resposta:
        for item in lista:
            if item['id'] == id:
                item['resposta'] = nova_resposta
                item['atualizado_em'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print('Resposta atualizada com sucesso!')
                break
    else:
        print('Resposta não pode ser vazia.')


def atualizar_categoria_memoria(lista, id):
    nova_categoria = input('Nova categoria do FAQ (ou 0 para cancelar): ').strip()
    if nova_categoria == '0':
        print('Atualização de categoria cancelada.')
        return
    if nova_categoria:
        for item in lista:
            if item['id'] == id:
                item['categoria'] = nova_categoria
                item['atualizado_em'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print('Categoria atualizada com sucesso!')
                break
    else:
        print('Categoria não pode ser vazia.')


def ativar_desativar_faq_memoria(lista, id):
    ativo_str = input('Novo status Ativo? (1-Sim, 0-Não, ou 9 para cancelar): ').strip()
    if ativo_str == '9':
        print('Atualização de status cancelada.')
        return
    if ativo_str in ['0', '1']:
        novo_ativo = int(ativo_str)
        for item in lista:
            if item['id'] == id:
                item['ativo'] = novo_ativo
                item['atualizado_em'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print('Status atualizado com sucesso!')
                break
    else:
        print('Valor para "Ativo" deve ser 1 (Sim) ou 0 (Não).')
