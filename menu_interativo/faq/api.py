"""
Módulo para consumo de API pública de curiosidades (exemplo: Chuck Norris jokes).
"""

import requests


class CuriosidadeAPI:
    """
    Classe para consumir uma API pública e retornar uma curiosidade.
    """

    @staticmethod
    def buscar_curiosidade():
        """
        Busca uma curiosidade aleatória da API pública.
        :return: String com a curiosidade ou mensagem de erro.
        """
        url = 'https://api.chucknorris.io/jokes/random'
        try:
            resposta = requests.get(url, timeout=5)
            if resposta.status_code == 200:
                dados = resposta.json()
                return dados.get('value', 'Curiosidade não encontrada.')
            else:
                return f'Erro ao acessar a API: {resposta.status_code}'
        except Exception as e:
            return f'Erro ao acessar a API: {e}'
