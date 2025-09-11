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
        # Informa ao usuário que a categoria será armazenada em maiúsculo
        if categoria:
            print(f'{Fore.BLUE}Categoria será salva como: {categoria.upper()}{Style.RESET_ALL}')
        ativo_str = input(
            f'{Fore.CYAN}Ativo? (1-Sim, 0-Não): {Style.RESET_ALL}'
        ).strip()
        if not (id_str.isdigit() and pergunta and resposta and categoria):
            print(f'{Fore.RED}Todos os campos são obrigatórios!{Style.RESET_ALL}')
            return
            
        # Verifica e solicita o valor de ativo até receber uma entrada válida
        while ativo_str not in ['0', '1']:
            print(
                f'{Fore.RED}Valor para "Ativo" deve ser 1 (Sim) ou 0 (Não).{Style.RESET_ALL}'
            )
            ativo_str = input(
                f'{Fore.CYAN}Ativo? (1-Sim, 0-Não): {Style.RESET_ALL}'
            ).strip()

        try:
            id = int(id_str)
        except ValueError:
            print(f'{Fore.RED}O ID deve ser um número inteiro válido.{Style.RESET_ALL}')
            return

        # Verifica se já existe FAQ com esse id
        if any(item['id'] == id for item in lista):
            print(f'{Fore.YELLOW}Já existe um FAQ com esse ID.{Style.RESET_ALL}')
            return

        operacao_iniciada = True
        ativo = int(ativo_str)
        atualizado_em = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # Converte categoria para maiúsculo para manter consistência com o banco de dados
        novo_faq = {
            'id': id,
            'pergunta': pergunta,
            'resposta': resposta,
            'ativo': ativo,
            'atualizado_em': atualizado_em,
            'categoria': categoria.upper(),  # Converte para maiúsculo
        }

        # Registrar dados no final do bloco try
        lista.append(novo_faq)
    except ValueError as e:
        print(f'{Fore.RED}Erro de valor ao adicionar FAQ: {e}{Style.RESET_ALL}')
    except KeyError as e:
        print(f'{Fore.RED}Erro de chave ao adicionar FAQ: {e}{Style.RESET_ALL}')
    except Exception as e:
        print(f'{Fore.RED}Erro ao adicionar FAQ em memória: {e}{Style.RESET_ALL}')
    else:
        # Este bloco só executa se não ocorrer exceção
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
    finally:
        if operacao_iniciada:
            print(
                f'{Fore.GREEN}[LOG] Operação de inserção em memória finalizada.{Style.RESET_ALL}'
            )
