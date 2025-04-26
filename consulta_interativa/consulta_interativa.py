from datetime import datetime
import time

paciente_atual = None
usuarios = []
feedbacks = []

def exibir_texto(texto):
    if not paciente_atual:
        print(texto)
        return
    tipo = paciente_atual["acesso"]
    if tipo == "visual":
        for parte in texto.split(". "):
            print(parte.strip())
            time.sleep(1)
    elif tipo == "cognitiva":
        print("Atenção:")
        for parte in texto.split(". "):
            print("- " + parte.strip())
    else:
        print(texto)

def cadastrar_paciente():
    global paciente_atual
    nome = input("Nome do paciente: ").strip()
    cpf = input("CPF: ").strip()
    telefone = input("Telefone: ").strip()

    if not nome or not cpf or not telefone:
        exibir_texto("Todos os campos são obrigatórios.")
        return

    print("Tipo de acessibilidade:")
    print("1 - Visual\n2 - Auditiva\n3 - Cognitiva\n4 - Nenhuma")
    escolha = input("Escolha: ").strip()
    tipos = {"1": "visual", "2": "auditiva", "3": "cognitiva", "4": "geral"}
    if escolha not in tipos:
        exibir_texto("Opção inválida.")
        return

    paciente_atual = {
        "nome": nome,
        "cpf": cpf,
        "telefone": telefone,
        "acesso": tipos[escolha],
        "checkin": False,
        "checkin_data": None
    }
    usuarios.append(paciente_atual)
    exibir_texto(f"Cadastro realizado. Sessão iniciada para {nome}.")

def confirmar_checkin():
    if not paciente_atual:
        exibir_texto("Você precisa se cadastrar antes de confirmar presença.")
        return

    if paciente_atual["checkin"]:
        exibir_texto("Você já confirmou sua presença.")
    else:
        paciente_atual["checkin"] = True
        paciente_atual["checkin_data"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        exibir_texto("Check-in confirmado com sucesso.")
        exibir_texto(
            "Agora que sua presença foi confirmada, prepare-se para a sua teleconsulta.\n"
            "• Escolha um ambiente calmo e bem iluminado.\n"
            "• Mantenha seu celular ou computador com bateria e internet estável.\n"
            "• Teste sua câmera e microfone com antecedência.\n"
            "• Tenha seus documentos e exames em mãos.\n"
            "• Aguarde o contato da equipe médica no horário agendado."
        )

def enviar_feedback():
    if not paciente_atual:
        exibir_texto("Você precisa se cadastrar primeiro.")
        return
    if not paciente_atual["checkin"]:
        exibir_texto("Confirme sua presença antes de enviar o feedback.")
        return

    while True:
        exibir_texto("Como foi sua consulta?")
        print("1 - Boa\n2 - Regular\n3 - Ruim")
        escolha = input("Escolha (ou 'voltar'): ").strip()
        if escolha == "voltar":
            break

        opcoes = {"1": "Boa", "2": "Regular", "3": "Ruim"}
        if escolha in opcoes:
            feedbacks.append(f"{paciente_atual['nome']}: {opcoes[escolha]}")
            exibir_texto("Feedback registrado.")
            break
        else:
            exibir_texto("Opção inválida.")

def ver_historico():
    if not usuarios:
        exibir_texto("Nenhum paciente registrado.")
        return

    for u in usuarios:
        print(f"{u['nome']} | CPF: {u['cpf']} | Tel: {u['telefone']} | Acessibilidade: {u['acesso']}")
        if u["checkin"]:
            print(f"  • Check-in realizado em: {u['checkin_data']}")
        else:
            print("  • Check-in: Não realizado")

    if feedbacks:
        print("\nFeedbacks:")
        for i, f in enumerate(feedbacks, 1):
            print(f"{i}. {f}")
    else:
        exibir_texto("Nenhum feedback registrado.")

def menu():
    while True:
        print("\n--- SISTEMA DE TRIAGEM BÁSICA ---")
        exibir_texto("Escolha uma opção:")
        print("1 - Cadastrar paciente")
        print("2 - Confirmar presença")
        print("3 - Enviar feedback")
        print("4 - Ver histórico")
        print("5 - Sair")
        opcao = input("Opção: ").strip()

        if opcao == "1":
            cadastrar_paciente()
        elif opcao == "2":
            confirmar_checkin()
        elif opcao == "3":
            enviar_feedback()
        elif opcao == "4":
            ver_historico()
        elif opcao == "5":
            exibir_texto("Sistema encerrado.")
            break
        else:
            exibir_texto("Opção inválida.")

# Executar sistema
menu()