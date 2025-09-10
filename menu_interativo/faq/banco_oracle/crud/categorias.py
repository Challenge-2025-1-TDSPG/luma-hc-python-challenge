from colorama import Fore, Style


def listar_categorias(db):
    """Lista todas as categorias de FAQs disponíveis no banco de dados.

    Esta função busca e exibe todas as categorias distintas cadastradas
    no banco de dados, facilitando a visualização das categorias existentes
    para referência em operações de filtro ou categorização.

    Args:
        db (FaqDB): Instância de conexão com o banco de dados
    """
    operacao_iniciada = False

    try:
        # Marca que a operação foi iniciada (para controle de logs)
        operacao_iniciada = True

        # Busca todas as categorias distintas no banco de dados
        categorias = db.listar_categorias()

        # Exibe as categorias encontradas ou uma mensagem de que não há categorias
        if categorias:
            # Exibe o cabeçalho
            print(f'{Fore.CYAN}{Style.BRIGHT}Categorias disponíveis:{Style.RESET_ALL}')

            # Exibe cada categoria em uma linha com marcador
            for categoria in categorias:
                print(f'{Fore.WHITE}- {categoria}{Style.RESET_ALL}')

            # Exibe o total de categorias encontradas
            print(
                f'\n{Fore.GREEN}Total de categorias: {len(categorias)}{Style.RESET_ALL}'
            )
        else:
            # Mensagem quando nenhuma categoria é encontrada
            print(f'{Fore.YELLOW}Nenhuma categoria cadastrada.{Style.RESET_ALL}')
    except Exception as e:
        print(f'{Fore.RED}Erro ao listar categorias: {e}{Style.RESET_ALL}')
    finally:
        if operacao_iniciada:
            print(
                f'{Fore.GREEN}[LOG] Operação de listagem de categorias finalizada.{Style.RESET_ALL}'
            )
