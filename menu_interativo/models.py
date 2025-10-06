from config.settings import COLOR_ERROR, COLOR_MAGENTA, COLOR_RESET, COLOR_SUCCESS


class FAQ:
    """
    Representa um item de FAQ (pergunta e resposta).

    Args:
        id (int): Identificador único do FAQ.
        pergunta (str): Texto da pergunta.
        resposta (str): Texto da resposta.
        ativo (int): Status de ativação (1 para ativo, 0 para inativo).
        atualizado_em (str): Data/hora da última atualização (YYYY-MM-DD HH:MM:SS).
        categoria (str): Categoria do FAQ.
        user_account_id_user (int): ID do usuário responsável pelo FAQ.

    Example:
        >>> faq = FAQ(1, 'O que é Python?', 'Uma linguagem de programação.', 1, '2025-09-23 10:00:00', 'Programação', 1)
        >>> print(faq)
        ID: 1
        Pergunta: O que é Python?
        Resposta: Uma linguagem de programação.
        Ativo: Sim
        Atualizado em: 2025-09-23 10:00:00
        Categoria: Programação
    """

    def __init__(
        self,
        id,
        pergunta,
        resposta,
        ativo,
        atualizado_em,
        categoria,
        user_account_id_user=None,
    ):
        """
        Inicializa um objeto FAQ.

        Args:
            id (int): Identificador único do FAQ.
            pergunta (str): Texto da pergunta.
            resposta (str): Texto da resposta.
            ativo (int): 1 para ativo, 0 para inativo.
            atualizado_em (str): Data/hora da última atualização.
            categoria (str): Categoria do FAQ.
            user_account_id_user (int, optional): ID do usuário responsável.
        """
        self.id = id
        self.pergunta = pergunta
        self.resposta = resposta
        self.ativo = ativo
        self.atualizado_em = atualizado_em
        self.categoria = categoria
        self.user_account_id_user = user_account_id_user

    def __str__(self):
        """
        Retorna uma representação formatada e colorida do FAQ.

        Returns:
            str: Representação do FAQ formatada com cores usando Colorama.
        """
        ativo_texto = (
            f'{COLOR_SUCCESS}Sim{COLOR_RESET}'
            if self.ativo
            else f'{COLOR_ERROR}Não{COLOR_RESET}'
        )
        return (
            f'{COLOR_MAGENTA}ID:{COLOR_RESET} {self.id}\n'
            f'{COLOR_MAGENTA}Pergunta:{COLOR_RESET} {self.pergunta}\n'
            f'{COLOR_MAGENTA}Resposta:{COLOR_RESET} {self.resposta}\n'
            f'{COLOR_MAGENTA}Ativo:{COLOR_RESET} {ativo_texto}\n'
            f'{COLOR_MAGENTA}Atualizado em:{COLOR_RESET} {self.atualizado_em}\n'
            f'{COLOR_MAGENTA}Categoria:{COLOR_RESET} {self.categoria}'
        )
