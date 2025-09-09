def listar_faqs(db):
    categoria = input('Filtrar por categoria (deixe vazio para todas): ').strip()
    faqs = db.listar(categoria if categoria else None)
    if faqs:
        for faq in faqs:
            print(faq)
            print('-' * 30)
    else:
        print('Nenhum FAQ cadastrado.')
