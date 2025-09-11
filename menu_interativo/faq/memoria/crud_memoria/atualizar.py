from datetime import datetime

from colorama import Fore, Style


def atualizar_faq_memoria(lista):
    """Atualiza um FAQ existente na lista em memória.

    Esta função apresenta um menu com opções para atualizar diferentes
    aspectos de um FAQ (pergunta, resposta, categoria ou status de ativação).
    Primeiro valida se o FAQ existe antes de mostrar o menu de atualização.

    Args:
        lista (list): Lista de FAQs em memória onde está o FAQ a ser atualizado
    """
    operacao_iniciada = False

    try:
        id_str = input(
            f'{Fore.CYAN}Digite o ID do FAQ a atualizar: {Style.RESET_ALL}'
        ).strip()
        if not id_str.isdigit():
            print(f'{Fore.RED}ID deve ser um número inteiro.{Style.RESET_ALL}')
            return

        try:
            id = int(id_str)
        except ValueError:
            print(f'{Fore.RED}O ID deve ser um número inteiro válido.{Style.RESET_ALL}')
            return

        # Verifica se existe FAQ com esse id
        if not any(item['id'] == id for item in lista):
            print(f'{Fore.YELLOW}FAQ não encontrado.{Style.RESET_ALL}')
            return

        operacao_iniciada = True

    except ValueError as e:
        print(f'{Fore.RED}Erro de valor ao iniciar atualização: {e}{Style.RESET_ALL}')
        return
    except Exception as e:
        print(
            f'{Fore.RED}Erro ao iniciar atualização do FAQ em memória: {e}{Style.RESET_ALL}'
        )
        return
    else:
        # Este bloco só executa se a validação inicial não lançar exceções
        try:
            while True:
                print(
                    f'\n{Fore.BLUE}{Style.BRIGHT}--- Atualizar FAQ ---{Style.RESET_ALL}'
                )
                print(f'{Fore.WHITE}1. Atualizar Pergunta')
                print(f'{Fore.WHITE}2. Atualizar Resposta')
                print(f'{Fore.WHITE}3. Atualizar Categoria')
                print(f'{Fore.WHITE}4. Ativar/Desativar FAQ')
                print(f'{Fore.YELLOW}0. Voltar{Style.RESET_ALL}')
                opcao = input(
                    f'{Fore.GREEN}Escolha uma opção: {Style.RESET_ALL}'
                ).strip()
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
        except ValueError as e:
            print(f'{Fore.RED}Erro de valor ao atualizar FAQ: {e}{Style.RESET_ALL}')
        except KeyError as e:
            print(f'{Fore.RED}Erro de chave ao atualizar FAQ: {e}{Style.RESET_ALL}')
        except Exception as e:
            print(f'{Fore.RED}Erro ao atualizar FAQ em memória: {e}{Style.RESET_ALL}')
    finally:
        if operacao_iniciada:
            print(
                f'{Fore.GREEN}[LOG] Operação de atualização em memória finalizada.{Style.RESET_ALL}'
            )


def atualizar_pergunta_memoria(lista, id):
    """Atualiza a pergunta de um FAQ específico na memória.

    Args:
        lista (list): Lista de FAQs em memória
        id (int): ID do FAQ a ser atualizado
    """
    nova_pergunta = input(
        f'{Fore.CYAN}Digite a nova pergunta (ou 0 para cancelar): {Style.RESET_ALL}'
    ).strip()
    if nova_pergunta == '0':
        print(
            f'{Fore.YELLOW}Operação cancelada. Pergunta não foi alterada.{Style.RESET_ALL}'
        )
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
    """Atualiza a resposta de um FAQ específico na memória.

    Args:
        lista (list): Lista de FAQs em memória
        id (int): ID do FAQ a ser atualizado
    """
    nova_resposta = input(
        f'{Fore.CYAN}Digite a nova resposta (ou 0 para cancelar): {Style.RESET_ALL}'
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
    """Atualiza a categoria de um FAQ específico na memória.

    Args:
        lista (list): Lista de FAQs em memória
        id (int): ID do FAQ a ser atualizado
    """
    nova_categoria = input(
        f'{Fore.CYAN}Digite a nova categoria (ou 0 para cancelar): {Style.RESET_ALL}'
    ).strip()
    if nova_categoria == '0':
        print(f'{Fore.YELLOW}Atualização de categoria cancelada.{Style.RESET_ALL}')
        return
    if nova_categoria:
        # Informa ao usuário que a categoria será armazenada em maiúsculo
        print(f'{Fore.BLUE}Categoria será salva como: {nova_categoria.upper()}{Style.RESET_ALL}')
        for item in lista:
            if item['id'] == id:
                item['categoria'] = nova_categoria.upper()  # Converte para maiúsculo
                item['atualizado_em'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(f'{Fore.GREEN}Categoria atualizada com sucesso!{Style.RESET_ALL}')
                break
    else:
        print(f'{Fore.RED}Categoria não pode ser vazia.{Style.RESET_ALL}')


def ativar_desativar_faq_memoria(lista, id):
    """Altera o status de ativação de um FAQ específico na memória.

    Permite ativar ou desativar um FAQ, mostrando seu status atual e
    solicitando confirmação antes de efetuar a alteração.

    Args:
        lista (list): Lista de FAQs em memória
        id (int): ID do FAQ a ser atualizado
    """
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
    
    # Loop para garantir entrada válida
    while True:
        ativo_str = (
            input(f'{Fore.CYAN}Escolha uma opção: {Style.RESET_ALL}').strip().upper()
        )

        if ativo_str == 'C':
            print(
                f'{Fore.YELLOW}Operação cancelada. Nenhuma alteração foi feita.{Style.RESET_ALL}'
            )
            return
        
        if ativo_str in ['1', '0']:
            break
            
        print(
            f'{Fore.RED}Valor para status deve ser 1 (Ativar), 0 (Desativar) ou C (Cancelar).{Style.RESET_ALL}'
        )

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
