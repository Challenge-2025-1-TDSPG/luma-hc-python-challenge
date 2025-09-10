from colorama import Fore, Style


def listar_faqs_memoria(lista):
    """Lista todas as FAQs armazenadas em memória, com opção de filtro por categoria.

    Esta função solicita ao usuário um filtro opcional por categoria e exibe todos os
    FAQs armazenados em memória que correspondam ao critério. Se nenhum filtro
    for especificado, lista todos os FAQs.

    Args:
        lista (list): Lista de FAQs em memória a serem listados
    """
    operacao_iniciada = False

    try:
        categoria = input(
            f'{Fore.CYAN}Filtrar por categoria (deixe vazio para todas): {Style.RESET_ALL}'
        ).strip()

        operacao_iniciada = True

        # Filtra a lista se uma categoria foi especificada
        if categoria:
            faqs_filtrados = [
                faq
                for faq in lista
                if faq.get('categoria', '').lower() == categoria.lower()
            ]
        else:
            faqs_filtrados = lista

    except TypeError as e:
        print(f'{Fore.RED}Erro de tipo ao filtrar FAQs: {e}{Style.RESET_ALL}')
    except AttributeError as e:
        print(f'{Fore.RED}Erro de atributo ao filtrar FAQs: {e}{Style.RESET_ALL}')
    except Exception as e:
        print(f'{Fore.RED}Erro ao listar FAQs em memória: {e}{Style.RESET_ALL}')
    else:
        # Este bloco só executa se a filtragem não lançar exceções
        if not faqs_filtrados:
            print(
                f'{Fore.YELLOW}Nenhum FAQ em memória{" com esta categoria" if categoria else ""}.{Style.RESET_ALL}'
            )
        else:
            try:
                for faq in faqs_filtrados:
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
                print(
                    f'{Fore.GREEN}Total de FAQs em memória{" nesta categoria" if categoria else ""}: {len(faqs_filtrados)}{Style.RESET_ALL}'
                )
            except KeyError as e:
                print(
                    f'{Fore.RED}Erro ao exibir FAQ: chave ausente - {e}{Style.RESET_ALL}'
                )
    finally:
        if operacao_iniciada:
            print(
                f'{Fore.GREEN}[LOG] Operação de listagem em memória finalizada.{Style.RESET_ALL}'
            )
