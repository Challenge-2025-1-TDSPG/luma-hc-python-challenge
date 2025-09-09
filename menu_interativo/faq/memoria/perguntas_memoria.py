"""
Módulo utilitário para operações em memória com perguntas do FAQ usando lista de dicionários.
"""

def adicionar_pergunta(lista, id, pergunta):
    """Adiciona uma pergunta à lista de dicionários."""
    lista.append({'id': id, 'pergunta': pergunta})
    return lista


def remover_pergunta(lista, id_remover):
    """Remove pergunta pelo id em lista de dicionários."""
    return [item for item in lista if item['id'] != id_remover]


def buscar_pergunta(lista, id_busca):
    """Busca perguntas pelo id em lista de dicionários."""
    return [item for item in lista if item['id'] == id_busca]


def atualizar_pergunta(lista, id_atualizar, novo_texto):
    """Atualiza pergunta pelo id em lista de dicionários."""
    for item in lista:
        if item['id'] == id_atualizar:
            item['pergunta'] = novo_texto
    return lista


if __name__ == '__main__':
    perguntas = []
    adicionar_pergunta(perguntas, 1, 'Pergunta 1')
    atualizar_pergunta(perguntas, 1, 'Pergunta 1 atualizada')
    print('Perguntas:', perguntas)
