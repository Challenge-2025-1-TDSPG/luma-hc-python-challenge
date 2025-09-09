from colorama import Fore, Style


def listar_faqs(db):
    """Lista todas as FAQs cadastradas, com opção de filtro por categoria."""
    operacao_iniciada = False

    try:
        categoria = input(
            f'{Fore.CYAN}Filtrar por categoria (deixe vazio para todas): {Style.RESET_ALL}'
        ).strip()

        operacao_iniciada = True

        faqs = db.listar(categoria if categoria else None)
        if faqs:
            for faq in faqs:
                print(f'{Fore.CYAN}{faq}{Style.RESET_ALL}')
                print(f'{Fore.CYAN}{"-" * 30}{Style.RESET_ALL}')
        else:
            print(f'{Fore.YELLOW}Nenhum FAQ cadastrado.{Style.RESET_ALL}')
    except Exception as e:
        print(f'{Fore.RED}Erro ao listar FAQs: {e}{Style.RESET_ALL}')
    finally:
        if operacao_iniciada:
            print(
                f'{Fore.GREEN}[LOG] Operação de listagem finalizada.{Style.RESET_ALL}'
            )
