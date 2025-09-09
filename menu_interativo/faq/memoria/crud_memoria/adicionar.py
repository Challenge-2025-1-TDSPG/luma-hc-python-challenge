from datetime import datetime


def adicionar_faq_memoria(lista):
    """Adiciona um novo FAQ na memória."""
    operacao_iniciada = False

    try:
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
        # Verifica se já existe FAQ com esse id
        if any(item['id'] == id for item in lista):
            print('Já existe um FAQ com esse ID.')
            return

        operacao_iniciada = True

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
    except Exception as e:
        print(f'Erro ao adicionar FAQ em memória: {e}')
    finally:
        if operacao_iniciada:
            print('[LOG] Operação de inserção em memória finalizada.')
