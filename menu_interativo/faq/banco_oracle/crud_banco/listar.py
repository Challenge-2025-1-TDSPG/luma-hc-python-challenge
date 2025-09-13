"""
Módulo de listagem de FAQs no banco Oracle.
Permite listar todos os FAQs ou filtrar por categoria.
"""

from colorama import Fore, Style


def listar_faqs(db):
    """Lista todas as FAQs cadastradas no banco de dados, com opção de filtro por categoria.

    Esta função solicita ao usuário um filtro opcional por categoria e exibe todos os
    FAQs cadastrados no banco de dados que correspondam ao critério. Se nenhum filtro
    for especificado, lista todos os FAQs.

    Args:
        db (FaqDB): Instância de conexão com o banco de dados
    """
    operacao_iniciada = False

    try:
        # Solicita ao usuário uma categoria para filtrar (opcional)
        categoria = input(
            f'{Fore.CYAN}Filtrar por categoria (deixe vazio para todas): {Style.RESET_ALL}'
        ).strip()

        # Marca que a operação foi iniciada (para controle de logs)
        operacao_iniciada = True

        # Busca os FAQs no banco de dados, com filtro opcional por categoria
        faqs = db.listar(categoria if categoria else None)

        # Exibe os FAQs encontrados ou uma mensagem de que não há FAQs cadastrados
        if faqs:
            for faq in faqs:
                # Exibe cada FAQ com formatação colorida
                print(f'{Fore.CYAN}{faq}{Style.RESET_ALL}')
                # Adiciona uma linha separadora entre os FAQs
                print(f'{Fore.CYAN}{"-" * 30}{Style.RESET_ALL}')

            # Exibe o total de FAQs encontrados
            print(f'{Fore.GREEN}Total de FAQs: {len(faqs)}{Style.RESET_ALL}')
        else:
            # Mensagem quando nenhum FAQ é encontrado
            print(
                f'{Fore.YELLOW}Nenhum FAQ cadastrado{" nesta categoria" if categoria else ""}.{Style.RESET_ALL}'
            )
    except Exception as e:
        print(f'{Fore.RED}Erro ao listar FAQs: {e}{Style.RESET_ALL}')
    finally:
        if operacao_iniciada:
            print(
                f'{Fore.GREEN}[LOG] Operação de listagem finalizada.{Style.RESET_ALL}'
            )
