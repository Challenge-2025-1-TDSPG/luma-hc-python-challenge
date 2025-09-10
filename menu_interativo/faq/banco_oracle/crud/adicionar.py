from colorama import Fore, Style


def adicionar_faq(db):
    """Adiciona um novo FAQ ao banco de dados Oracle.

    Esta função solicita ao usuário os dados do FAQ (pergunta, resposta, categoria e status),
    valida as entradas e persiste o FAQ no banco de dados. Exibe o FAQ adicionado
    após a operação bem-sucedida.

    Args:
        db (FaqDB): Instância de conexão com o banco de dados
    """
    operacao_iniciada = False

    try:
        pergunta = input(f'{Fore.CYAN}Digite a pergunta: {Style.RESET_ALL}').strip()
        resposta = input(f'{Fore.CYAN}Digite a resposta: {Style.RESET_ALL}').strip()
        categoria = input(
            f'{Fore.CYAN}Digite o nome da categoria: {Style.RESET_ALL}'
        ).strip()
        ativo_str = input(
            f'{Fore.CYAN}Ativo? (1-Sim, 0-Não): {Style.RESET_ALL}'
        ).strip()
        if not (pergunta and resposta and categoria):
            print(f'{Fore.RED}Todos os campos são obrigatórios!{Style.RESET_ALL}')
            return
        if ativo_str not in ['0', '1']:
            print(
                f'{Fore.RED}Valor para "Ativo" deve ser 1 (Sim) ou 0 (Não).{Style.RESET_ALL}'
            )
            return

        operacao_iniciada = True

        # Converte string para inteiro para o status ativo
        ativo = int(ativo_str)

        # Adiciona o FAQ ao banco de dados
        db.adicionar(pergunta, resposta, ativo, categoria)

        # Busca o FAQ recém-adicionado para exibir ao usuário
        # Considera o de maior ID como sendo o último adicionado
        faqs = db.listar()
        if faqs:
            novo_faq = max(faqs, key=lambda f: f.id)
            print(f'{Fore.GREEN}FAQ adicionado com sucesso!{Style.RESET_ALL}')
            print(f'{Fore.CYAN}{novo_faq}{Style.RESET_ALL}')
        else:
            print(
                f'{Fore.YELLOW}FAQ adicionado, mas não foi possível exibir.{Style.RESET_ALL}'
            )
    except Exception as e:
        print(f'{Fore.RED}Erro ao adicionar FAQ: {e}{Style.RESET_ALL}')
    finally:
        if operacao_iniciada:
            print(
                f'{Fore.GREEN}[LOG] Operação de inserção finalizada.{Style.RESET_ALL}'
            )
