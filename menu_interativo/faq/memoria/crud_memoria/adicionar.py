from datetime import datetime

from colorama import Fore, Style


def adicionar_faq_memoria(lista):
    """Adiciona um novo FAQ na memória."""
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
        print(
            f'{Fore.CYAN}ID:{Style.RESET_ALL} {novo_faq["id"]}\n'
            f'{Fore.CYAN}Pergunta:{Style.RESET_ALL} {novo_faq["pergunta"]}\n'
            f'{Fore.CYAN}Resposta:{Style.RESET_ALL} {novo_faq["resposta"]}\n'
            f'{Fore.CYAN}Ativo:{Style.RESET_ALL} {novo_faq["ativo"]}\n'
            f'{Fore.CYAN}Categoria:{Style.RESET_ALL} {novo_faq["categoria"]}{Style.RESET_ALL}'
        )
    except Exception as e:
        print(f'{Fore.RED}Erro ao adicionar FAQ em memória: {e}{Style.RESET_ALL}')
    finally:
        if operacao_iniciada:
            print(
                f'{Fore.GREEN}[LOG] Operação de inserção em memória finalizada.{Style.RESET_ALL}'
            )
