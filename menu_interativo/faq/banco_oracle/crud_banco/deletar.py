"""
Módulo de exclusão de FAQ no banco Oracle.
Solicita o ID do FAQ, confirma e executa a exclusão no banco.
"""

from colorama import Fore, Style


def deletar_faq(db):
    """Remove um FAQ do banco de dados pelo seu ID.

    Esta função solicita ao usuário o ID do FAQ a ser removido, verifica sua existência,
    pede confirmação antes de excluir, e então executa a operação de exclusão no banco de dados.
    Inclui tratamento de erros e confirmação para prevenir exclusões acidentais.

    Args:
        db (FaqDB): Instância de conexão com o banco de dados
    """
    operacao_iniciada = False

    try:
        # Solicita o ID do FAQ a ser excluído
        id_str = input(
            f'{Fore.CYAN}Digite o ID do FAQ a deletar: {Style.RESET_ALL}'
        ).strip()

        # Valida se a entrada é um número inteiro
        if not id_str.isdigit():
            print(f'{Fore.RED}ID deve ser um número inteiro.{Style.RESET_ALL}')
            return

        # Converte para inteiro
        id = int(id_str)

        # Verifica se o FAQ existe antes de tentar deletar
        faq = db.buscar_por_id(id)
        if not faq:
            print(f'{Fore.YELLOW}FAQ não encontrado.{Style.RESET_ALL}')
            return

        # Marca que a operação foi iniciada (para controle de logs)
        operacao_iniciada = True

        # Solicita confirmação do usuário antes de prosseguir com a exclusão
        confirmacao = (
            input(
                f'{Fore.YELLOW}{Style.BRIGHT}Pressione Enter para confirmar a exclusão ou C para cancelar: {Style.RESET_ALL}'
            )
            .strip()
            .upper()
        )

        # Se o usuário cancelar, interrompe a operação
        if confirmacao == 'C':
            print(
                f'{Fore.GREEN}Operação cancelada. Nenhuma alteração foi feita.{Style.RESET_ALL}'
            )
            return

        # Executa a exclusão no banco de dados
        db.deletar(id)
    except Exception as e:
        print(f'{Fore.RED}Erro ao deletar FAQ: {e}{Style.RESET_ALL}')
    else:
        print(f'{Fore.GREEN}FAQ deletado com sucesso!{Style.RESET_ALL}')
    finally:
        if operacao_iniciada:
            print(
                f'{Fore.GREEN}[LOG] Operação de exclusão finalizada.{Style.RESET_ALL}'
            )
