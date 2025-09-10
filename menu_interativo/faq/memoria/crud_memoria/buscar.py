from colorama import Fore, Style


def buscar_faq_memoria(lista):
    """Busca um FAQ em memória pelo ID."""
    operacao_iniciada = False

    try:
        id_str = input(f'{Fore.CYAN}Digite o ID do FAQ: {Style.RESET_ALL}').strip()
        if not id_str.isdigit():
            print(f'{Fore.RED}ID deve ser um número inteiro.{Style.RESET_ALL}')
            return
        id = int(id_str)

        operacao_iniciada = True

        encontrados = [item for item in lista if item['id'] == id]
        if encontrados:
            for faq in encontrados:
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
        else:
            print(
                f'{Fore.YELLOW}FAQ com ID {id} não encontrado em memória.{Style.RESET_ALL}'
            )
    except Exception as e:
        print(f'{Fore.RED}Erro ao buscar FAQ em memória: {e}{Style.RESET_ALL}')
    finally:
        if operacao_iniciada:
            print(
                f'{Fore.GREEN}[LOG] Operação de busca em memória finalizada.{Style.RESET_ALL}'
            )
