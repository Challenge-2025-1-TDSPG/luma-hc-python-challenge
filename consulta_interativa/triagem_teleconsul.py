from datetime import datetime
import time
from validadar_cpf import validar_cpf, formatar_cpf

# Variáveis globais para armazenamento de dados
paciente_atual = None  # Armazena o paciente atualmente logado no sistema
registros = []  # Lista que armazena todos os registros de pacientes cadastrados
feedbacks = []  # Lista que armazena todos os feedbacks enviados pelos pacientes

def exibir_texto(texto):
    """Função auxiliar para exibir mensagens do sistema"""
    print(texto)

def cadastrar_paciente():
    """Função para cadastrar um novo paciente no sistema.
    Coleta informações e valida os dados e armazena no registro global."""
    global paciente_atual
    nome = input('Nome do paciente: ').strip()

    # Validação do CPF
    while True:
        cpf_input = input('Digite seu CPF: ').strip()
        if validar_cpf(cpf_input):
            cpf = formatar_cpf(cpf_input)
            print('CPF válido!')
            break
        else:
            print('CPF inválido. Tente novamente.')
    
    # Validação da data de nascimento
    while True:
        try:
         data_nascimento_str = input('Data de nascimento (DD/MM/AAAA): ').strip()
         data_nascimento = datetime.strptime(data_nascimento_str, '%d/%m/%Y')  # CORRETO: transforma em datetime
         hoje = datetime.now()
         idade = hoje.year - data_nascimento.year - ((hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day))  # CORRETO
         break
        except ValueError:
         print('Data inválida. Use o formato DD/MM/AAAA (ex: 01/01/2000)')
    
    telefone = input('Telefone: ').strip()
    
    # Validação do email
    while True:
        email = input('Email: ').strip()
        if '@' in email and '.' in email:
            break
        else:
            print('Email inválido. Digite um email válido.')

    # Validação do CEP
    while True:
        cep = input('CEP (apenas números): ').strip()
        if cep.isdigit() and len(cep) == 8:
            cep = f'{cep[:5]}-{cep[5:]}'
            break
        else:
            print('CEP inválido. Digite apenas números (8 dígitos).')

    # Verifica se todos os campos foram preenchidos
    if not nome or not cpf or not telefone or not email or not cep or not data_nascimento:
        exibir_texto('Todos os campos são obrigatórios.')
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
    exibir_texto(f'Cadastro realizado. Sessão iniciada para {nome}.')

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
        print('5 - Sair')

        opcao = input('Opção: ').strip()
        if opcao == '1':
            cadastrar_paciente()
        elif opcao == '2':
            confirmar_checkin()
        elif opcao == '3':
            enviar_feedback()
        elif opcao == '4':
            ver_historico()
        elif opcao == '5':
            exibir_texto('Sistema encerrado.')
            break
        else:
            exibir_texto('Opção inválida.')

# Inicia o programa executando o menu principal
menu()
