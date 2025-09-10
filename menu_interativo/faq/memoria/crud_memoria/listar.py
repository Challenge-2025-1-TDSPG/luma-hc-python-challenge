from colorama import Fore, Style


def listar_faqs_memoria(lista):
    """Lista todas as FAQs armazenadas em memória, com opção de filtro por categoria."""
    operacao_iniciada = False

    try:
        categoria = input(
            f'{Fore.CYAN}Filtrar por categoria (deixe vazio para todas): {Style.RESET_ALL}'
        ).strip()

        operacao_iniciada = True

        # Filtra a lista se uma categoria foi especificada
        faqs_filtrados = lista
        if categoria:
            faqs_filtrados = [
                faq
                for faq in lista
                if faq.get('categoria', '').lower() == categoria.lower()
            ]

        if not faqs_filtrados:
            print(
                f'{Fore.YELLOW}Nenhum FAQ em memória{" com esta categoria" if categoria else ""}.{Style.RESET_ALL}'
            )
        else:
            for faq in faqs_filtrados:
                print(
                    f'{Fore.CYAN}ID:{Style.RESET_ALL} {faq["id"]}\n'
                    f'{Fore.CYAN}Pergunta:{Style.RESET_ALL} {faq["pergunta"]}\n'
                    f'{Fore.CYAN}Resposta:{Style.RESET_ALL} {faq.get("resposta", "")}\n'
                    f'{Fore.CYAN}Ativo:{Style.RESET_ALL} {faq.get("ativo", "")}\n'
                    f'{Fore.CYAN}Atualizado em:{Style.RESET_ALL} {faq.get("atualizado_em", "")}\n'
                    f'{Fore.CYAN}Categoria:{Style.RESET_ALL} {faq.get("categoria", "")}\n'
                    + '-'
                    * 30
                )
            print(
                f'{Fore.GREEN}Total de FAQs em memória{" nesta categoria" if categoria else ""}: {len(faqs_filtrados)}{Style.RESET_ALL}'
            )
    except Exception as e:
        print(f'{Fore.RED}Erro ao listar FAQs em memória: {e}{Style.RESET_ALL}')
    finally:
        if operacao_iniciada:
            print(
                f'{Fore.GREEN}[LOG] Operação de listagem em memória finalizada.{Style.RESET_ALL}'
            )
