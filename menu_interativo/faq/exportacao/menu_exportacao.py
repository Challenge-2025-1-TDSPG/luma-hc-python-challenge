"""
Módulo que gerencia as operações de exportação de FAQs para formato JSON.
Fornece uma interface para exportar FAQs do banco de dados para um arquivo JSON.
"""

from .exportar_banco import exportar_faqs_banco


class MenuExportacao:
    """Classe responsável por gerenciar a exportação de FAQs do banco para JSON.

    Esta classe oferece métodos para exportar os FAQs armazenados no banco de dados
    para um arquivo JSON, facilitando o backup e a transferência de dados.
    """

    def __init__(self, db):
        """Inicializa o menu de exportação.

        Args:
            db (FaqDB): Instância de conexão com o banco de dados
        """
        self.db = db

    def exportar_json(self):
        """Exporta todos os FAQs do banco de dados para um arquivo JSON.

        Recupera todos os FAQs do banco de dados, converte os objetos FAQ para
        dicionários e então os exporta para um arquivo JSON formatado.
        """
        # Recupera todos os FAQs do banco de dados
        perguntas = self.db.listar()

        # Converte os objetos FAQ para dicionários usando o método vars()
        # Isso transforma os atributos do objeto em pares chave-valor em um dicionário
        lista_dict = [vars(p) for p in perguntas]

        # Exporta a lista de dicionários para um arquivo JSON
        exportar_faqs_banco(lista_dict)
