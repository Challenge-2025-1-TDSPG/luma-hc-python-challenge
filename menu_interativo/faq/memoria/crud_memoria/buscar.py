from colorama import Fore, Style


def buscar_faq_memoria(lista):
    """Busca e exibe um FAQ em memória pelo seu ID.

    Esta função solicita ao usuário o ID do FAQ a ser buscado, valida a entrada,
    realiza a busca na lista em memória e exibe o FAQ encontrado ou uma mensagem
    informando que o FAQ não foi encontrado.

    Args:
        lista (list): Lista de FAQs em memória onde será feita a busca
    """
    operacao_iniciada = False

    try:
        id_str = input(f'{Fore.CYAN}Digite o ID do FAQ: {Style.RESET_ALL}').strip()
        if not id_str.isdigit():
            print(f'{Fore.RED}ID deve ser um número inteiro.{Style.RESET_ALL}')
            return

        try:
            id = int(id_str)
        except ValueError:
            print(f'{Fore.RED}O ID deve ser um número inteiro válido.{Style.RESET_ALL}')
            return

        operacao_iniciada = True

        # Busca FAQs que atendem ao critério
        encontrados = [item for item in lista if item['id'] == id]

    except ValueError as e:
        print(f'{Fore.RED}Erro de valor ao buscar FAQ: {e}{Style.RESET_ALL}')
    except TypeError as e:
        print(f'{Fore.RED}Erro de tipo ao buscar FAQ: {e}{Style.RESET_ALL}')
    except Exception as e:
        print(f'{Fore.RED}Erro ao buscar FAQ em memória: {e}{Style.RESET_ALL}')
    else:
        # Este bloco só executa se a busca não lançar exceções
        if encontrados:
            for faq in encontrados:
                try:
                    ativo_texto = (
                        f'{Fore.GREEN}Sim{Style.RESET_ALL}'
                        if faq.get('ativo') == 1
                        else f'{Fore.RED}Não{Style.RESET_ALL}'
                    )
                    print(
                        f'{Fore.MAGENTA}ID:{Style.RESET_ALL} {faq["id"]}\n'
                        f'{Fore.MAGENTA}Pergunta:{Style.RESET_ALL} {faq["pergunta"]}\n'
                        f'{Fore.MAGENTA}Resposta:{Style.RESET_ALL} {faq.get("resposta", "")}\n'
                        f'{Fore.MAGENTA}Ativo:{Style.RESET_ALL} {ativo_texto}\n'
                        f'{Fore.MAGENTA}Atualizado em:{Style.RESET_ALL} {faq.get("atualizado_em", "")}\n'
                        f'{Fore.MAGENTA}Categoria:{Style.RESET_ALL} {faq.get("categoria", "")}\n'
                        f'{Fore.CYAN}{"-" * 30}{Style.RESET_ALL}'
                    )
                except KeyError as e:
                    print(
                        f'{Fore.RED}Erro ao exibir FAQ: chave ausente - {e}{Style.RESET_ALL}'
                    )
        else:
            print(
                f'{Fore.RED}FAQ com ID {id} não encontrado em memória.{Style.RESET_ALL}'
            )
    finally:
        if operacao_iniciada:
            print(
                f'{Fore.GREEN}[LOG] Operação de busca em memória finalizada.{Style.RESET_ALL}'
            )
