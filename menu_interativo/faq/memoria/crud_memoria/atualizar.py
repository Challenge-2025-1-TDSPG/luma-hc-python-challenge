from datetime import datetime

from colorama import Fore, Style


def atualizar_faq_memoria(lista):
    """Atualiza um FAQ existente em memória."""
    operacao_iniciada = False

    try:
        id_str = input(
            f'{Fore.CYAN}Digite o ID do FAQ a atualizar: {Style.RESET_ALL}'
        ).strip()
        if not id_str.isdigit():
            print(f'{Fore.RED}ID deve ser um número inteiro.{Style.RESET_ALL}')
            return
        id = int(id_str)
        # Verifica se existe FAQ com esse id
        if not any(item['id'] == id for item in lista):
            print(f'{Fore.YELLOW}FAQ não encontrado.{Style.RESET_ALL}')
            return

        operacao_iniciada = True

        while True:
            print(
                f'\n{Fore.BLUE}{Style.BRIGHT}--- Atualizar FAQ em Memória ---{Style.RESET_ALL}'
            )
            print(f'{Fore.WHITE}1. Atualizar Pergunta')
            print(f'{Fore.WHITE}2. Atualizar Resposta')
            print(f'{Fore.WHITE}3. Atualizar Categoria')
            print(f'{Fore.WHITE}4. Ativar/Desativar FAQ')
            print(f'{Fore.YELLOW}0. Voltar{Style.RESET_ALL}')
            opcao = input(f'{Fore.GREEN}Escolha uma opção: {Style.RESET_ALL}').strip()
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
                print(
                    f'{Fore.RED}Opção inválida! Digite o número da opção desejada.{Style.RESET_ALL}'
                )
    except Exception as e:
        print(f'{Fore.RED}Erro ao atualizar FAQ em memória: {e}{Style.RESET_ALL}')
    finally:
        if operacao_iniciada:
            print(
                f'{Fore.GREEN}[LOG] Operação de atualização em memória finalizada.{Style.RESET_ALL}'
            )


def atualizar_pergunta_memoria(lista, id):
    nova_pergunta = input(
        f'{Fore.CYAN}Nova pergunta do FAQ (ou 0 para cancelar): {Style.RESET_ALL}'
    ).strip()
    if nova_pergunta == '0':
        print(f'{Fore.YELLOW}Atualização de pergunta cancelada.{Style.RESET_ALL}')
        return
    if nova_pergunta:
        for item in lista:
            if item['id'] == id:
                item['pergunta'] = nova_pergunta
                item['atualizado_em'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(f'{Fore.GREEN}Pergunta atualizada com sucesso!{Style.RESET_ALL}')
                break
    else:
        print(f'{Fore.RED}Pergunta não pode ser vazia.{Style.RESET_ALL}')


def atualizar_resposta_memoria(lista, id):
    nova_resposta = input(
        f'{Fore.CYAN}Nova resposta do FAQ (ou 0 para cancelar): {Style.RESET_ALL}'
    ).strip()
    if nova_resposta == '0':
        print(f'{Fore.YELLOW}Atualização de resposta cancelada.{Style.RESET_ALL}')
        return
    if nova_resposta:
        for item in lista:
            if item['id'] == id:
                item['resposta'] = nova_resposta
                item['atualizado_em'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(f'{Fore.GREEN}Resposta atualizada com sucesso!{Style.RESET_ALL}')
                break
    else:
        print(f'{Fore.RED}Resposta não pode ser vazia.{Style.RESET_ALL}')


def atualizar_categoria_memoria(lista, id):
    nova_categoria = input(
        f'{Fore.CYAN}Nova categoria do FAQ (ou 0 para cancelar): {Style.RESET_ALL}'
    ).strip()
    if nova_categoria == '0':
        print(f'{Fore.YELLOW}Atualização de categoria cancelada.{Style.RESET_ALL}')
        return
    if nova_categoria:
        for item in lista:
            if item['id'] == id:
                item['categoria'] = nova_categoria
                item['atualizado_em'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(f'{Fore.GREEN}Categoria atualizada com sucesso!{Style.RESET_ALL}')
                break
    else:
        print(f'{Fore.RED}Categoria não pode ser vazia.{Style.RESET_ALL}')


def ativar_desativar_faq_memoria(lista, id):
    # Busca o FAQ para verificar status atual
    faq = None
    for item in lista:
        if item['id'] == id:
            faq = item
            break

    if not faq:
        print(
            f'{Fore.RED}Erro: FAQ com ID {id} não está mais disponível.{Style.RESET_ALL}'
        )
        return

    # Mostra o status atual
    status_atual = 'ativado' if faq['ativo'] == 1 else 'desativado'
    status_cor = Fore.GREEN if faq['ativo'] == 1 else Fore.RED
    print(
        f'\n{Fore.CYAN}Status atual do FAQ: {status_cor}{status_atual}{Style.RESET_ALL}'
    )

    print(
        f'{Fore.WHITE}Opções: {Fore.GREEN}1-Ativar FAQ | {Fore.RED}0-Desativar FAQ | {Fore.YELLOW}C-Cancelar{Style.RESET_ALL}'
    )
    ativo_str = (
        input(f'{Fore.CYAN}Escolha uma opção: {Style.RESET_ALL}').strip().upper()
    )

    if ativo_str == 'C':
        print(
            f'{Fore.YELLOW}Operação cancelada. Nenhuma alteração foi feita.{Style.RESET_ALL}'
        )
        return

    if ativo_str not in ['1', '0']:
        print(
            f'{Fore.RED}Valor para status deve ser 1 (Ativar), 0 (Desativar) ou C (Cancelar).{Style.RESET_ALL}'
        )
        return

    novo_ativo = int(ativo_str)

    # Verifica se já está no estado desejado
    if (novo_ativo == 1 and faq['ativo'] == 1) or (
        novo_ativo == 0 and faq['ativo'] == 0
    ):
        print(
            f'{Fore.YELLOW}FAQ já está {status_atual}. Nenhuma alteração necessária.{Style.RESET_ALL}'
        )
        return

    # Atualiza o FAQ
    for item in lista:
        if item['id'] == id:
            item['ativo'] = novo_ativo
            item['atualizado_em'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            novo_status = 'ativado' if novo_ativo == 1 else 'desativado'
            status_cor = Fore.GREEN if novo_ativo == 1 else Fore.RED
            print(
                f'{Fore.GREEN}Status do FAQ atualizado com sucesso! FAQ agora está {status_cor}{novo_status}.{Style.RESET_ALL}'
            )
            break
