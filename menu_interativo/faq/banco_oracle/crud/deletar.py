from colorama import Fore, Style


def deletar_faq(db):
    """Remove um FAQ pelo ID."""
    operacao_iniciada = False

    try:
        id_str = input(
            f'{Fore.CYAN}Digite o ID do FAQ a deletar: {Style.RESET_ALL}'
        ).strip()
        if not id_str.isdigit():
            print(f'{Fore.RED}ID deve ser um número inteiro.{Style.RESET_ALL}')
            return
        id = int(id_str)
        # Verifica se o FAQ existe antes de tentar deletar
        faq = db.buscar_por_id(id)
        if not faq:
            print(f'{Fore.YELLOW}FAQ não encontrado.{Style.RESET_ALL}')
            return

        operacao_iniciada = True

        confirmacao = input(
            f'{Fore.RED}{Style.BRIGHT}Pressione Enter para confirmar a exclusão ou C para cancelar: {Style.RESET_ALL}'
        ).strip().upper()
        
        if confirmacao == 'C':
            print(f'{Fore.YELLOW}Operação cancelada. Nenhuma alteração foi feita.{Style.RESET_ALL}')
            return
            
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
