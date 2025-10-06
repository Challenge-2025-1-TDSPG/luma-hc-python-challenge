"""
Módulo para consumo de APIs externas.
Implementa integração com DummyJSON para obter citações inspiracionais.
"""

import json
from typing import Dict, List, Optional

import requests
from config.settings import show_message


class ApiExternaQuotes:
    """
    Classe para consumir a API externa DummyJSON (Quotes).

    Esta classe implementa o requisito de consumo de API externa pública,
    fornecendo funcionalidades para buscar citações inspiracionais que
    podem ser utilizadas como conteúdo de FAQ ou para inspirar usuários.
    """

    BASE_URL = 'https://dummyjson.com'
    TIMEOUT = 10  # Timeout para requisições em segundos

    def __init__(self):
        """Inicializa o cliente da API externa."""
        self.session = requests.Session()
        self.session.timeout = self.TIMEOUT

    def buscar_citacao_aleatoria(self) -> Optional[Dict]:
        """
        Busca uma citação aleatória da API DummyJSON.

        Returns:
            Dict: Dicionário com 'id', 'quote' e 'author' ou None se houver erro.
        """
        try:
            url = f'{self.BASE_URL}/quotes/random'
            show_message(f'Buscando citação aleatória em: {url}', 'info')

            response = self.session.get(url)
            response.raise_for_status()

            data = response.json()
            show_message(
                f"Citação obtida: '{data['quote'][:50]}...' - {data['author']}",
                'success',
            )
            return data

        except requests.exceptions.RequestException as e:
            show_message(f'Erro ao conectar com a API externa: {e}', 'error')
            return None
        except json.JSONDecodeError as e:
            show_message(f'Erro ao decodificar resposta JSON: {e}', 'error')
            return None
        except KeyError as e:
            show_message(f'Estrutura de resposta inesperada: {e}', 'error')
            return None

    def buscar_citacoes(self, limite: int = 10) -> Optional[List[Dict]]:
        """
        Busca múltiplas citações da API DummyJSON.

        Args:
            limite: Número de citações a buscar (máximo 30).

        Returns:
            List[Dict]: Lista de citações ou None se houver erro.
        """
        try:
            # Limitar o número máximo conforme documentação da API
            limite = min(limite, 30)
            url = f'{self.BASE_URL}/quotes?limit={limite}'

            show_message(f'Buscando {limite} citações em: {url}', 'info')

            response = self.session.get(url)
            response.raise_for_status()

            data = response.json()
            citacoes = data.get('quotes', [])

            show_message(f'Obtidas {len(citacoes)} citações da API externa', 'success')
            return citacoes

        except requests.exceptions.RequestException as e:
            show_message(f'Erro ao conectar com a API externa: {e}', 'error')
            return None
        except json.JSONDecodeError as e:
            show_message(f'Erro ao decodificar resposta JSON: {e}', 'error')
            return None
        except KeyError as e:
            show_message(f'Estrutura de resposta inesperada: {e}', 'error')
            return None

    def buscar_citacao_por_id(self, id_citacao: int) -> Optional[Dict]:
        """
        Busca uma citação específica pelo ID.

        Args:
            id_citacao: ID da citação (1-100 conforme documentação).

        Returns:
            Dict: Dicionário com 'id', 'quote' e 'author' ou None se houver erro.
        """
        try:
            if not 1 <= id_citacao <= 100:
                show_message('ID da citação deve estar entre 1 e 100', 'warning')
                return None

            url = f'{self.BASE_URL}/quotes/{id_citacao}'
            show_message(f'Buscando citação ID {id_citacao} em: {url}', 'info')

            response = self.session.get(url)
            response.raise_for_status()

            data = response.json()
            show_message(
                f"Citação ID {id_citacao} obtida: '{data['quote'][:50]}...'", 'success'
            )
            return data

        except requests.exceptions.RequestException as e:
            show_message(f'Erro ao conectar com a API externa: {e}', 'error')
            return None
        except json.JSONDecodeError as e:
            show_message(f'Erro ao decodificar resposta JSON: {e}', 'error')
            return None
        except KeyError as e:
            show_message(f'Estrutura de resposta inesperada: {e}', 'error')
            return None

    def exportar_citacoes_json(self, arquivo: str, limite: int = 20) -> bool:
        """
        Busca citações da API externa e exporta para arquivo JSON.

        Args:
            arquivo: Caminho do arquivo onde salvar as citações.
            limite: Número de citações a buscar e exportar.

        Returns:
            bool: True se exportação foi bem-sucedida, False caso contrário.
        """
        try:
            citacoes = self.buscar_citacoes(limite)
            if not citacoes:
                show_message('Nenhuma citação foi obtida da API externa', 'warning')
                return False

            # Criar estrutura de dados para exportação
            dados_exportacao = {
                'fonte': 'DummyJSON Quotes API',
                'total_citacoes': len(citacoes),
                'url_api': self.BASE_URL,
                'citacoes': citacoes,
            }

            with open(arquivo, 'w', encoding='utf-8') as f:
                json.dump(dados_exportacao, f, ensure_ascii=False, indent=4)

            show_message(f'Citações exportadas com sucesso para: {arquivo}', 'success')
            return True

        except Exception as e:
            show_message(f'Erro ao exportar citações: {e}', 'error')
            return False

    def criar_faq_a_partir_de_citacao(
        self, id_citacao: Optional[int] = None
    ) -> Optional[Dict]:
        """
        Cria um FAQ baseado em uma citação da API externa.

        Args:
            id_citacao: ID específico da citação. Se None, usa citação aleatória.

        Returns:
            Dict: Dados do FAQ criado ou None se houver erro.
        """
        try:
            if id_citacao is not None:
                citacao = self.buscar_citacao_por_id(id_citacao)
            else:
                citacao = self.buscar_citacao_aleatoria()

            if not citacao:
                return None

            # Criar FAQ baseado na citação
            faq_data = {
                'pergunta': f'Qual é uma citação inspiracional de {citacao["author"]}?',
                'resposta': f"'{citacao['quote']}' - {citacao['author']}",
                'categoria': 'INSPIRACAO',
                'ativo': 1,
                'fonte_externa': {
                    'api': 'DummyJSON',
                    'endpoint': 'quotes',
                    'id_original': citacao['id'],
                },
            }

            show_message('FAQ criado a partir de citação da API externa', 'success')
            return faq_data

        except Exception as e:
            show_message(f'Erro ao criar FAQ a partir de citação: {e}', 'error')
            return None

    def __del__(self):
        """Fecha a sessão HTTP ao destruir o objeto."""
        if hasattr(self, 'session'):
            self.session.close()


def menu_api_externa():
    """
    Menu interativo para demonstrar o consumo da API externa.
    Implementa o requisito de 20 pontos para desenvolvimento/consumo de API externa.
    """
    from config.settings import (
        COLOR_OPTION,
        COLOR_PROMPT,
        COLOR_RESET,
        COLOR_TITLE,
    )

    api = ApiExternaQuotes()

    while True:
        print(
            f'\n{COLOR_TITLE}--- API EXTERNA: CITAÇÕES INSPIRACIONAIS ---{COLOR_RESET}'
        )
        print(f'{COLOR_OPTION}1. Buscar citação aleatória')
        print(f'{COLOR_OPTION}2. Buscar citação por ID')
        print(f'{COLOR_OPTION}3. Buscar múltiplas citações')
        print(f'{COLOR_OPTION}4. Criar FAQ a partir de citação')
        print(f'{COLOR_OPTION}5. Exportar citações para JSON')
        print(f'{COLOR_OPTION}0. Voltar ao menu principal{COLOR_RESET}')

        opcao = input(f'{COLOR_PROMPT}Escolha uma opção: {COLOR_RESET}').strip()

        if opcao == '1':
            citacao = api.buscar_citacao_aleatoria()
            if citacao:
                print(f'\n📝 Citação #{citacao["id"]}')
                print(f'💬 "{citacao["quote"]}"')
                print(f'👤 - {citacao["author"]}')

        elif opcao == '2':
            try:
                id_input = input(
                    f'{COLOR_PROMPT}Digite o ID da citação (1-100): {COLOR_RESET}'
                )
                id_citacao = int(id_input.strip())
                citacao = api.buscar_citacao_por_id(id_citacao)
                if citacao:
                    print(f'\n📝 Citação #{citacao["id"]}')
                    print(f'💬 "{citacao["quote"]}"')
                    print(f'👤 - {citacao["author"]}')
            except ValueError:
                show_message('ID deve ser um número inteiro', 'error')

        elif opcao == '3':
            try:
                limite_input = input(
                    f'{COLOR_PROMPT}Quantas citações buscar (1-30)? {COLOR_RESET}'
                )
                limite = int(limite_input.strip())
                citacoes = api.buscar_citacoes(limite)
                if citacoes:
                    print(f'\n📚 {len(citacoes)} Citações Obtidas:')
                    for i, citacao in enumerate(
                        citacoes[:5]
                    ):  # Mostrar apenas as 5 primeiras
                        print(
                            f'{i + 1}. "{citacao["quote"][:60]}..." - {citacao["author"]}'
                        )
                    if len(citacoes) > 5:
                        print(f'... e mais {len(citacoes) - 5} citações')
            except ValueError:
                show_message('Limite deve ser um número inteiro', 'error')

        elif opcao == '4':
            faq_data = api.criar_faq_a_partir_de_citacao()
            if faq_data:
                print('\n✅ FAQ Criado:')
                print(f'Pergunta: {faq_data["pergunta"]}')
                print(f'Resposta: {faq_data["resposta"]}')
                print(f'Categoria: {faq_data["categoria"]}')

        elif opcao == '5':
            try:
                limite_input = input(
                    f'{COLOR_PROMPT}Quantas citações exportar (1-30)? {COLOR_RESET}'
                )
                limite = int(limite_input.strip())
                arquivo = 'json/api_externa/citacoes_export.json'

                import os

                os.makedirs(os.path.dirname(arquivo), exist_ok=True)

                sucesso = api.exportar_citacoes_json(arquivo, limite)
                if sucesso:
                    print(f'📁 Arquivo salvo em: {arquivo}')
            except ValueError:
                show_message('Limite deve ser um número inteiro', 'error')

        elif opcao == '0':
            break

        else:
            show_message('Opção inválida!', 'error')


if __name__ == '__main__':
    # Permite executar o módulo diretamente para testes
    menu_api_externa()
