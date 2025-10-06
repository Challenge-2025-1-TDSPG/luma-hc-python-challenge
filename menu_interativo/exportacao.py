"""
Módulo consolidado de exportação/importação de FAQs para o sistema FAQ.
Inclui funções para exportar FAQs do banco Oracle para arquivos JSON.
"""

import json
import os

from config.settings import (
    JSON_BANCO_PATH,
    MSG_EXPORT_BANCO_OK,
    MSG_EXPORT_JSON_ERROR,
    show_message,
)


class MenuExportacao:
    """Classe responsável pela exportação de dados do sistema FAQ."""

    def __init__(self, db):
        """
        Inicializa o menu de exportação.

        Args:
            db: Instância da classe FaqDB para acesso ao banco de dados.
        """
        self.db = db

    def exportar_json(self):
        """
        Exporta todos os FAQs do banco Oracle para um arquivo JSON.
        O arquivo é salvo em json/banco/faq_export.json.
        """
        try:
            # Buscar todos os FAQs do banco
            faqs = self.db.listar()

            if not faqs:
                show_message('Nenhum FAQ encontrado no banco para exportar.', 'warning')
                return

            # Converter objetos FAQ para dicionários
            faqs_dict = []
            for faq in faqs:
                faq_data = {
                    'id': faq.id,
                    'pergunta': faq.pergunta,
                    'resposta': faq.resposta,
                    'ativo': faq.ativo,
                    'atualizado_em': str(faq.atualizado_em),
                    'categoria': faq.categoria,
                }
                faqs_dict.append(faq_data)

            # Garantir que o diretório existe
            os.makedirs(os.path.dirname(JSON_BANCO_PATH), exist_ok=True)

            # Salvar no arquivo JSON
            with open(JSON_BANCO_PATH, 'w', encoding='utf-8') as f:
                json.dump(faqs_dict, f, ensure_ascii=False, indent=4)

            # Exibir mensagem de sucesso
            show_message(MSG_EXPORT_BANCO_OK.format(path=JSON_BANCO_PATH), 'success')
            show_message(f'Total de {len(faqs_dict)} FAQs exportados.', 'info')

        except Exception as e:
            show_message(MSG_EXPORT_JSON_ERROR.format(erro=str(e)), 'error')
