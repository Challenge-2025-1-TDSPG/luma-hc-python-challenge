from datetime import datetime

from colorama import Fore, Style


def adicionar_faq_memoria(lista):
    """Adiciona um novo FAQ na lista em memória.

    Esta função solicita ao usuário os dados do FAQ (ID, pergunta, resposta, categoria e status),
    valida as entradas e adiciona o FAQ à lista em memória. Exibe o FAQ adicionado
    após a operação bem-sucedida.

    Args:
        lista (list): Lista de FAQs em memória onde o novo FAQ será adicionado
    """
    operacao_iniciada = False

    try:
        id_str = input(f'{Fore.CYAN}Digite o ID do FAQ: {Style.RESET_ALL}').strip()
        pergunta = input(f'{Fore.CYAN}Digite a pergunta: {Style.RESET_ALL}').strip()
        resposta = input(f'{Fore.CYAN}Digite a resposta: {Style.RESET_ALL}').strip()
        categoria = input(
            f'{Fore.CYAN}Digite o nome da categoria: {Style.RESET_ALL}'
        ).strip()
        ativo_str = input(
            f'{Fore.CYAN}Ativo? (1-Sim, 0-Não): {Style.RESET_ALL}'
        ).strip()
        if not (
            id_str.isdigit()
            and pergunta
            and resposta
            and categoria
            and ativo_str in ['0', '1']
        ):
            print(
                f'{Fore.RED}Todos os campos são obrigatórios e "Ativo" deve ser 1 ou 0.{Style.RESET_ALL}'
            )
            return
        id = int(id_str)
        # Verifica se já existe FAQ com esse id
        if any(item['id'] == id for item in lista):
            print(f'{Fore.YELLOW}Já existe um FAQ com esse ID.{Style.RESET_ALL}')
            return

        operacao_iniciada = True

        ativo = int(ativo_str)
        atualizado_em = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        novo_faq = {
            'id': id,
            'pergunta': pergunta,
            'resposta': resposta,
            'ativo': ativo,
            'atualizado_em': atualizado_em,
            'categoria': categoria,
        }
        lista.append(novo_faq)
        print(f'{Fore.GREEN}FAQ adicionado com sucesso!{Style.RESET_ALL}')

        ativo_texto = (
            f'{Fore.GREEN}Sim{Style.RESET_ALL}'
            if novo_faq['ativo'] == 1
            else f'{Fore.RED}Não{Style.RESET_ALL}'
        )

        print(
            f'{Fore.MAGENTA}ID:{Style.RESET_ALL} {novo_faq["id"]}\n'
            f'{Fore.MAGENTA}Pergunta:{Style.RESET_ALL} {novo_faq["pergunta"]}\n'
            f'{Fore.MAGENTA}Resposta:{Style.RESET_ALL} {novo_faq["resposta"]}\n'
            f'{Fore.MAGENTA}Ativo:{Style.RESET_ALL} {ativo_texto}\n'
            f'{Fore.MAGENTA}Atualizado em:{Style.RESET_ALL} {novo_faq["atualizado_em"]}\n'
            f'{Fore.MAGENTA}Categoria:{Style.RESET_ALL} {novo_faq["categoria"]}'
        )
    except Exception as e:
        print(f'{Fore.RED}Erro ao adicionar FAQ em memória: {e}{Style.RESET_ALL}')
    finally:
        if operacao_iniciada:
            print(
                f'{Fore.GREEN}[LOG] Operação de inserção em memória finalizada.{Style.RESET_ALL}'
            )
