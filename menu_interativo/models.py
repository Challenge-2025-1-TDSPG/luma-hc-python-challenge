from colorama import Fore, Style


class FAQ:
    """
    Classe que representa um item de FAQ (pergunta e resposta).
    """

    def __init__(self, id, pergunta, resposta, ativo, atualizado_em, categoria):
        """Inicializa um objeto FAQ com as informações fornecidas.

        Args:
                id (int): Identificador único do FAQ
                pergunta (str): Texto da pergunta
                resposta (str): Texto da resposta
                ativo (int): Status de ativação (1 para ativo, 0 para inativo)
                atualizado_em (str): Data e hora da última atualização no formato 'YYYY-MM-DD HH:MM:SS'
                categoria (str): Categoria do FAQ para agrupamento
        """
        self.id = id
        self.pergunta = pergunta
        self.resposta = resposta
        self.ativo = ativo
        self.atualizado_em = atualizado_em
        self.categoria = categoria

    def __str__(self):
        """Retorna uma representação formatada e colorida do FAQ.

        Returns:
                str: Representação do FAQ formatada com cores usando Colorama
        """
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
