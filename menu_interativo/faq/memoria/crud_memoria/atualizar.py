from datetime import datetime


def atualizar_faq_memoria(lista):
    id_str = input('ID do FAQ a atualizar: ').strip()
    if not id_str.isdigit():
        print('ID deve ser número.')
        return
    id = int(id_str)
    nova_pergunta = input(
        'Nova pergunta do FAQ (deixe vazio para não alterar): '
    ).strip()
    nova_resposta = input(
        'Nova resposta do FAQ (deixe vazio para não alterar): '
    ).strip()
    nova_categoria = input(
        'Nova categoria do FAQ (deixe vazio para não alterar): '
    ).strip()
    ativo_str = input(
        'Novo status Ativo? (1-Sim, 0-Não, deixe vazio para não alterar): '
    ).strip()
    novo_ativo = int(ativo_str) if ativo_str in ['0', '1'] else None
    atualizado_em = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    for item in lista:
        if item['id'] == id:
            if nova_pergunta:
                item['pergunta'] = nova_pergunta
            if nova_resposta:
                item['resposta'] = nova_resposta
            if nova_categoria:
                item['categoria'] = nova_categoria
            if novo_ativo is not None:
                item['ativo'] = novo_ativo
            item['atualizado_em'] = atualizado_em
    print('FAQ atualizado em memória!')
