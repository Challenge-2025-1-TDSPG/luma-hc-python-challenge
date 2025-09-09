def listar_faqs(db):
    """Lista todas as FAQs cadastradas, com opção de filtro por categoria."""
    categoria = input('Filtrar por categoria (deixe vazio para todas): ').strip()
    faqs = db.listar(categoria if categoria else None)
    if faqs:
        for faq in faqs:
            print(faq)
            print('-' * 30)
    else:
        print('Nenhum FAQ cadastrado.')
