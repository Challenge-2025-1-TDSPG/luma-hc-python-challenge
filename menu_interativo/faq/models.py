from colorama import Fore, Style


class FAQ:
    """
    Classe que representa um item de FAQ (pergunta e resposta).
    """

    def __init__(self, id, pergunta, resposta, ativo, atualizado_em, categoria):
        self.id = id
        self.pergunta = pergunta
        self.resposta = resposta
        self.ativo = ativo
        self.atualizado_em = atualizado_em
        self.categoria = categoria

    def __str__(self):
        ativo_texto = (
            f'{Fore.GREEN}Sim{Style.RESET_ALL}'
            if self.ativo
            else f'{Fore.RED}Não{Style.RESET_ALL}'
        )
        return (
            f'{Fore.MAGENTA}ID:{Style.RESET_ALL} {self.id}\n'
            f'{Fore.MAGENTA}Pergunta:{Style.RESET_ALL} {self.pergunta}\n'
            f'{Fore.MAGENTA}Resposta:{Style.RESET_ALL} {self.resposta}\n'
            f'{Fore.MAGENTA}Ativo:{Style.RESET_ALL} {ativo_texto}\n'
            f'{Fore.MAGENTA}Atualizado em:{Style.RESET_ALL} {self.atualizado_em}\n'
            f'{Fore.MAGENTA}Categoria:{Style.RESET_ALL} {self.categoria}'
        )
