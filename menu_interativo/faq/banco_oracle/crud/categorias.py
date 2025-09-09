from colorama import Fore, Style


def listar_categorias(db):
    """Lista todas as categorias disponíveis no banco."""
    operacao_iniciada = False

    try:
        operacao_iniciada = True

        categorias = db.listar_categorias()
        if categorias:
            print(f'{Fore.CYAN}{Style.BRIGHT}Categorias disponíveis:{Style.RESET_ALL}')
            for categoria in categorias:
                print(f'{Fore.WHITE}- {categoria}{Style.RESET_ALL}')
        else:
            print(f'{Fore.YELLOW}Nenhuma categoria cadastrada.{Style.RESET_ALL}')
    except Exception as e:
        print(f'{Fore.RED}Erro ao listar categorias: {e}{Style.RESET_ALL}')
    finally:
        if operacao_iniciada:
            print(
                f'{Fore.GREEN}[LOG] Operação de listagem de categorias finalizada.{Style.RESET_ALL}'
            )
