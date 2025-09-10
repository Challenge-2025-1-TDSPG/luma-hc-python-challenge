from colorama import Fore, Style


def remover_faq_memoria(lista):
    """Remove um FAQ da lista em memória pelo seu ID.

    Esta função solicita ao usuário o ID do FAQ a ser removido, verifica sua existência,
    pede confirmação antes de excluir, e então executa a operação de exclusão da lista.
    Inclui tratamento de erros e confirmação para prevenir exclusões acidentais.

    Args:
        lista (list): Lista de FAQs em memória de onde o FAQ será removido
    """
    operacao_iniciada = False

    try:
        id_str = input(
            f'{Fore.CYAN}Digite o ID do FAQ a deletar: {Style.RESET_ALL}'
        ).strip()
        if not id_str.isdigit():
            print(f'{Fore.RED}ID deve ser um número inteiro.{Style.RESET_ALL}')
            return

        try:
            id = int(id_str)
        except ValueError:
            print(f'{Fore.RED}O ID deve ser um número inteiro válido.{Style.RESET_ALL}')
            return

        if not any(item['id'] == id for item in lista):
            print(f'{Fore.YELLOW}FAQ não encontrado.{Style.RESET_ALL}')
            return

        operacao_iniciada = True

        confirmacao = (
            input(
                f'{Fore.YELLOW}{Style.BRIGHT}Pressione Enter para confirmar a exclusão ou C para cancelar: {Style.RESET_ALL}'
            )
            .strip()
            .upper()
        )

        if confirmacao == 'C':
            print(
                f'{Fore.GREEN}Operação cancelada. Nenhuma alteração foi feita.{Style.RESET_ALL}'
            )
            return

        # Mantém apenas os FAQs com ID diferente do informado
        lista_original = lista.copy()
        lista[:] = [item for item in lista if item['id'] != id]

        # Verifica se algum item foi removido
        if len(lista) == len(lista_original):
            raise ValueError(f'Não foi possível remover o FAQ com ID {id}')

    except ValueError as e:
        print(f'{Fore.RED}Erro de valor ao remover FAQ: {e}{Style.RESET_ALL}')
    except IndexError as e:
        print(f'{Fore.RED}Erro de índice ao remover FAQ: {e}{Style.RESET_ALL}')
    except Exception as e:
        print(f'{Fore.RED}Erro ao remover FAQ da memória: {e}{Style.RESET_ALL}')
    else:
        print(f'{Fore.GREEN}FAQ removido em memória!{Style.RESET_ALL}')
    finally:
        if operacao_iniciada:
            print(
                f'{Fore.GREEN}[LOG] Operação de exclusão em memória finalizada.{Style.RESET_ALL}'
            )
