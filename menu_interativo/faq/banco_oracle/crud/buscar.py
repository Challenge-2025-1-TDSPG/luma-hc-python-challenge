from colorama import Fore, Style


def buscar_faq(db):
    """Busca um FAQ pelo ID."""
    operacao_iniciada = False

    try:
        id_str = input(f'{Fore.CYAN}Digite o ID do FAQ: {Style.RESET_ALL}').strip()
        if not id_str.isdigit():
            print(f'{Fore.RED}ID deve ser um número inteiro.{Style.RESET_ALL}')
            return
        id = int(id_str)

        operacao_iniciada = True

        faq = db.buscar_por_id(id)
        if faq:
            print(faq)
        else:
            print(
                f'{Fore.YELLOW}FAQ com ID {id} não encontrado no banco de dados.{Style.RESET_ALL}'
            )
    except Exception as e:
        print(f'{Fore.RED}Erro ao buscar FAQ: {e}{Style.RESET_ALL}')
    finally:
        if operacao_iniciada:
            print(f'{Fore.GREEN}[LOG] Operação de busca finalizada.{Style.RESET_ALL}')
