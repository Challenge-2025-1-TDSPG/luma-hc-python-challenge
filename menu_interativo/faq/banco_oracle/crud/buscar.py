from colorama import Fore, Style


def buscar_faq(db):
    """Busca e exibe um FAQ no banco de dados pelo seu ID.

    Esta função solicita ao usuário o ID do FAQ a ser buscado, valida a entrada,
    realiza a busca no banco de dados e exibe o FAQ encontrado ou uma mensagem
    informando que o FAQ não foi encontrado.

    Args:
        db (FaqDB): Instância de conexão com o banco de dados
    """
    operacao_iniciada = False

    try:
        # Solicita o ID do FAQ a ser buscado
        id_str = input(f'{Fore.CYAN}Digite o ID do FAQ: {Style.RESET_ALL}').strip()

        # Valida se a entrada é um número inteiro
        if not id_str.isdigit():
            print(f'{Fore.RED}ID deve ser um número inteiro.{Style.RESET_ALL}')
            return

        # Converte para inteiro
        id = int(id_str)

        # Marca que a operação foi iniciada (para controle de logs)
        operacao_iniciada = True

        # Busca o FAQ no banco de dados
        faq = db.buscar_por_id(id)

        # Exibe o FAQ encontrado ou uma mensagem de que não foi encontrado
        if faq:
            # Exibe o FAQ usando sua representação em string (método __str__)
            print(faq)
        else:
            print(
                f'{Fore.RED}FAQ com ID {id} não encontrado no banco de dados.{Style.RESET_ALL}'
            )
    except Exception as e:
        print(f'{Fore.RED}Erro ao buscar FAQ: {e}{Style.RESET_ALL}')
    finally:
        if operacao_iniciada:
            print(f'{Fore.GREEN}[LOG] Operação de busca finalizada.{Style.RESET_ALL}')
