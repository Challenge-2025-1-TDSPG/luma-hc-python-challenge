from datetime import datetime


def adicionar_faq_memoria(lista):
    id_str = input('ID do FAQ: ').strip()
    pergunta = input('Pergunta do FAQ: ').strip()
    resposta = input('Resposta do FAQ: ').strip()
    categoria = input('Categoria do FAQ: ').strip()
    ativo_str = input('Ativo? (1-Sim, 0-Não): ').strip()
    if not (
        id_str.isdigit()
        and pergunta
        and resposta
        and categoria
        and ativo_str in ['0', '1']
    ):
        print('Todos os campos são obrigatórios e "Ativo" deve ser 1 ou 0.')
        return
    id = int(id_str)
    ativo = int(ativo_str)
    atualizado_em = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    lista.append(
        {
            'id': id,
            'pergunta': pergunta,
            'resposta': resposta,
            'ativo': ativo,
            'atualizado_em': atualizado_em,
            'categoria': categoria,
        }
    )
    print('FAQ adicionado em memória!')
