from datetime import datetime
import time
from validadar_cpf import validar_cpf, formatar_cpf
import cep_validacao 

# Variáveis globais para armazenamento de dados
paciente_atual = None  # Armazena o paciente atualmente logado no sistema
registros = []  # Lista que armazena todos os registros de pacientes cadastrados
feedbacks = []  # Lista que armazena todos os feedbacks enviados pelos pacientes

def exibir_texto(texto):
    """Função auxiliar para exibir mensagens do sistema"""
    print(texto)

def validar_telefone(telefone):
    """Valida o formato do telefone"""
    # Remove caracteres não numéricos
    telefone = ''.join(filter(str.isdigit, telefone))
    # Verifica se tem 10 ou 11 dígitos (com DDD)
    return len(telefone) in [10, 11]

def editar_registro(paciente):
    """Permite editar os dados de um registro"""
    while True:
        print("\nEscolha o campo que deseja editar:")
        print("1 - Nome")
        print("2 - Telefone")
        print("3 - Email")
        print("4 - CEP")
        print("5 - Voltar")
        
        opcao = input("Opção: \n").strip()
        
        if opcao == '1':
            novo_nome = input("Novo nome: ").strip()
            confirmacao = input(f"Confirma a alteração do nome para '{novo_nome}'? (s/n): \n").strip().lower()
            if confirmacao == 's':
                paciente['nome'] = novo_nome
                print("Nome atualizado com sucesso!")
                
        elif opcao == '2':
            while True:
                novo_telefone = input("Novo telefone: ").strip()
                if validar_telefone(novo_telefone):
                    confirmacao = input(f"Confirma a alteração do telefone para '{novo_telefone}'? (s/n): \n").strip().lower()
                    if confirmacao == 's':
                        paciente['telefone'] = novo_telefone
                        print("Telefone atualizado com sucesso!")
                        break
                else:
                    print("Telefone inválido. Use o formato (XX)XXXXX-XXXX ou (XX)XXXX-XXXX")
                    
        elif opcao == '3':
            novo_email = input("Novo email: ").strip()
            if '@' in novo_email and '.' in novo_email:
                confirmacao = input(f"Confirma a alteração do email para '{novo_email}'? (s/n): \n").strip().lower()
                if confirmacao == 's':
                    paciente['email'] = novo_email
                    print("Email atualizado com sucesso!")
            else:
                print("Email inválido!")
                
        elif opcao == '4':
            while True:
                novo_cep = input("Novo CEP (apenas números): ").strip()
                if novo_cep.isdigit() and len(novo_cep) == 8:
                    novo_cep = f'{novo_cep[:5]}-{novo_cep[5:]}'
                    cep_validacao.consultar_cep(novo_cep)
                    confirmacao = input(f"Confirma a alteração do CEP para '{novo_cep}'? (s/n): \n").strip().lower()
                    if confirmacao == 's':
                        paciente['cep'] = novo_cep
                        print("CEP atualizado com sucesso!")
                        break
                else:
                    print("CEP inválido. Digite apenas números (8 dígitos).")
                    
        elif opcao == '5':
            break
        else:
            print("Opção inválida!")

def ver_registro():
    """Exibe e permite editar um registro específico"""
    if not registros:
        exibir_texto("Nenhum registro encontrado.")
        return

    print("\nRegistros disponíveis:")
    for i, registro in enumerate(registros, 1):
        print(f"{i} - {registro['nome']} (CPF: {registro['cpf']})")

    try:
        escolha = int(input("\nEscolha o número do registro que deseja ver (ou 0 para voltar): \n").strip())
        if escolha == 0:
            return
        if 1 <= escolha <= len(registros):
            registro = registros[escolha - 1]
            print("\nDados do registro:")
            print(f"Nome: {registro['nome']}")
            print(f"CPF: {registro['cpf']}")
            print(f"Data de Nascimento: {registro['data_nascimento'].strftime('%d/%m/%Y')}")
            print(f"Idade: {registro['idade']}")
            print(f"Telefone: {registro['telefone']}")
            print(f"Email: {registro['email']}")
            print(f"CEP: {registro['cep']}")
            opcao = input("\nDeseja editar este registro? (s/n): \n").strip().lower()
            if opcao == 's':
                editar_registro(registro)
        else:
            print("Número de registro inválido!")
    except ValueError:
        print("Por favor, digite um número válido!")

def cadastrar_paciente():
    """Função para cadastrar um novo paciente no sistema.
    Coleta informações e valida os dados e armazena no registro global."""
    global paciente_atual
    
    # Nome
    while True:
        nome = input('Nome do paciente: ').strip()
        confirmacao = input(f'Confirma o nome "{nome}"? (s/n): ').strip().lower()
        if confirmacao == 's':
            break
        print('\nPor favor, digite o nome novamente.')

    # Validação do CPF
    while True:
        cpf_input = input('\nDigite seu CPF: ').strip()
        if validar_cpf(cpf_input):
            cpf = formatar_cpf(cpf_input)
            print('\nCPF válido!')
            break
        else:
            print('\nCPF inválido. Tente novamente.')
    
    # Validação da data de nascimento
    while True:
        try:
            data_nascimento_str = input('\nData de nascimento (DD/MM/AAAA): ').strip()
            data_nascimento = datetime.strptime(data_nascimento_str, '%d/%m/%Y')
            hoje = datetime.now()
            idade = hoje.year - data_nascimento.year - ((hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day))
            break
        except ValueError:
            print('\nData inválida. Use o formato DD/MM/AAAA (ex: 01/01/2000)')
    
    # Telefone
    while True:
        telefone = input('\nTelefone: ').strip()
        
        if validar_telefone(telefone):
            confirmacao = input(f'Confirma o telefone "{telefone}"? (s/n): ').strip().lower()
            if confirmacao == 's':
                break
            print('\nPor favor, digite o telefone novamente.')
        else:
            print('\nTelefone inválido. Use o formato (XX)XXXXX-XXXX ou (XX)XXXX-XXXX')
    
    # Validação do email
    while True:
        email = input('\nEmail: ').strip()
        if '@' in email and '.' in email:
            confirmacao = input(f'Confirma o email "{email}"? (s/n): ').strip().lower()
            if confirmacao == 's':
                break
            print('\nPor favor, digite o email novamente.')
        else:
            print('\nEmail inválido. Digite um email válido.')

    # Validação do CEP
    while True:
        cep = input('\nCEP (apenas números): ').strip()
        if cep.isdigit() and len(cep) == 8:
            cep = f'{cep[:5]}-{cep[5:]}'
            # Consulta o CEP usando a função do cep_validacao.py
            cep_validacao.consultar_cep(cep)
            confirmacao = input(f'Confirma o CEP "{cep}"? (s/n): ').strip().lower()
            if confirmacao == 's':
                break
            print('\nPor favor, digite o CEP novamente.')
        else:
            print('\nCEP inválido. Digite apenas números (8 dígitos).')

    # Verifica se todos os campos foram preenchidos
    if not nome or not cpf or not telefone or not email or not cep or not data_nascimento:
        exibir_texto('\nTodos os campos são obrigatórios.')
        return

    # Cria o registro do paciente
    paciente_atual = {
        'nome': nome,
        'cpf': cpf,
        'data_nascimento': data_nascimento,
        'idade': idade,
        'telefone': telefone,
        'email': email,
        'cep': cep,
        'checkin': False,
        'checkin_data': None
    }

    # Adiciona o registro à lista global
    registros.append(paciente_atual)
    exibir_texto(f'\nCadastro realizado. Sessão iniciada para {nome}.')

def confirmar_checkin():
    """Função que confirma a presença do paciente para a teleconsulta.
    Atualiza o status de check-in e fornece orientações para a consulta."""
    if not paciente_atual:
        exibir_texto('Você precisa se cadastrar antes de confirmar presença.')
        return

    if paciente_atual['checkin']:
        exibir_texto('Você já confirmou sua presença.')
    else:
        paciente_atual['checkin'] = True
        paciente_atual['checkin_data'] = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        exibir_texto('Check-in confirmado com sucesso.')
        exibir_texto(
            'Agora que sua presença foi confirmada, prepare-se para a sua teleconsulta.\n'
            '• Escolha um ambiente calmo e bem iluminado.\n'
            '• Mantenha seu celular ou computador com bateria e internet estável.\n'
            '• Teste sua câmera e microfone com antecedência.\n'
            '• Tenha seus documentos e exames em mãos.\n'
            '• Aguarde o contato da equipe médica no horário agendado.'
        )

def enviar_feedback():
    """Função que permite ao paciente enviar feedback sobre a consulta.
    Oferece opções de avaliação e armazena o feedback no sistema."""
    if not paciente_atual:
        exibir_texto('Você precisa se cadastrar primeiro.')
        return
    if not paciente_atual['checkin']:
        exibir_texto('Confirme sua presença antes de enviar o feedback.')
        return

    while True:
        exibir_texto('Como foi sua consulta?')
        print('1 - Boa\n2 - Regular\n3 - Ruim')
        escolha = input('Escolha (ou \'voltar\'): ').strip()

        if escolha == 'voltar':
            break

        opcoes = {'1': 'Boa', '2': 'Regular', '3': 'Ruim'}

        if escolha in opcoes:
            feedbacks.append(f'{paciente_atual["nome"]}: {opcoes[escolha]}')
            exibir_texto('Feedback registrado.')
            break
        else:
            exibir_texto('Opção inválida.')

def ver_historico():
    """Função que exibe o histórico completo de registros e feedbacks.
    Mostra informações detalhadas de todos os pacientes cadastrados."""
    if not registros:
        exibir_texto('Nenhum registro encontrado.')
        return

    for usuario in registros:
        print(f'{usuario["nome"]} | CPF: {usuario["cpf"]} | Idade: {usuario["idade"]} | Tel: {usuario["telefone"]} | Email: {usuario["email"]} | CEP: {usuario["cep"]}')
        if usuario['checkin']:
            print(f' • Check-in realizado em: {usuario["checkin_data"]}')
        else:
            print(' • Check-in: Não realizado')

    if feedbacks:
        print('\nFeedbacks:')
        for i, f in enumerate(feedbacks, 1):
            print(f'{i}. {f}')
    else:
        exibir_texto('Nenhum feedback registrado.')

def menu():
    """Função principal que exibe o menu interativo do sistema.
    Permite ao usuário navegar entre as diferentes funcionalidades."""
    while True:
        print('\n---- SISTEMA DE TRIAGEM BÁSICA ----')
        exibir_texto('\nEscolha uma opção:')
        print('1 - Cadastrar paciente')
        print('2 - Confirmar presença')
        print('3 - Enviar feedback')
        print('4 - Ver histórico')
        print('5 - Ver registro')
        print('6 - Sair')

        opcao = input('\nOpção: ').strip()
        if opcao == '1':
            cadastrar_paciente()
        elif opcao == '2':
            confirmar_checkin()
        elif opcao == '3':
            enviar_feedback()
        elif opcao == '4':
            ver_historico()
        elif opcao == '5':
            ver_registro()
        elif opcao == '6':
            exibir_texto('Sistema encerrado.')
            break
        else:
            exibir_texto('Opção inválida.')

# Inicia o programa executando o menu principal
menu()
