class FAQ:
    """
    Classe que representa um item de FAQ (pergunta e resposta).
    """

    def __init__(self, id, pergunta, resposta, ativo, atualizado_em, pasta):
        self.id = id
        self.pergunta = pergunta
        self.resposta = resposta
        self.ativo = ativo
        self.atualizado_em = atualizado_em
        self.pasta = pasta

    def __str__(self):
        return f'ID: {self.id}\nPergunta: {self.pergunta}\nResposta: {self.resposta}\nAtivo: {self.ativo}\nAtualizado em: {self.atualizado_em}\nPasta: {self.pasta}'
