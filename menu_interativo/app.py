from datetime import datetime
from validar_cpf import validar_cpf, formatar_cpf
import random  # Adicionando import para números aleatórios

# Variáveis globais para armazenamento de dado
paciente_atual = None  # Armazena o paciente atualmente logado no sistema
registros_pacientes = []  # Lista que armazena todos os registros de pacientes cadastrados
historico_feedbacks = []  # Lista que armazena todos os feedbacks enviados pelos pacientes
numeros_prontuarios_usados = set()  # Conjunto para controlar números de prontuário únicos
numeros_consultas_usados = set()  # Conjunto para controlar números de consulta únicos

# Variáveis para médicos
medico_atual = None  # Armazena o médico atualmente logado no sistema
registros_medicos = []  # Lista que armazena todos os registros de médicos cadastrados
orientacoes_medicas = []  # Lista que armazena todas as orientações médicas

def exibir_mensagem(mensagem):
    """Função auxiliar para exibir mensagens do sistema"""
    print(mensagem)

def validar_telefone(numero_telefone): #Valida e formata o número de telefone
    # Remove caracteres não numéricos
    numero_limpo = ''.join(filter(str.isdigit, numero_telefone))
    # Verifica se tem 10 ou 11 dígitos (com DDD)
    if len(numero_limpo) in [10, 11]:
        # Formata o telefone
        if len(numero_limpo) == 10:  # (XX)XXXX-XXXX
            return f"({numero_limpo[:2]}){numero_limpo[2:6]}-{numero_limpo[6:]}"
        else:  # (XX)XXXXX-XXXX
            return f"({numero_limpo[:2]}){numero_limpo[2:7]}-{numero_limpo[7:]}"
    return None

def validar_crm(crm):
    """Valida o número do CRM"""
    # Lista de siglas de estados válidas
    estados_validos = ['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO']
    
    # Verifica se o CRM tem o formato correto (sigla do estado + espaço + 6 dígitos)
    partes = crm.strip().split()
    if len(partes) != 2:
        return None
    
    sigla_estado = partes[0].upper()
    numero = partes[1]
    
    # Verifica se a sigla do estado é válida
    if sigla_estado not in estados_validos:
        return None
    
    # Verifica se o número tem exatamente 6 dígitos
    if not numero.isdigit() or len(numero) != 6:
        return None
    
    # Retorna o CRM formatado
    return f"{sigla_estado} {numero}"

def gerar_numero_unico(min_val, max_val, numeros_usados):
    """Gera um número único que não está no conjunto de números usados"""
    while True:
        numero = random.randint(min_val, max_val)
        if numero not in numeros_usados:
            numeros_usados.add(numero)
            return numero

def cadastrar_paciente():
    """Função para cadastrar um novo paciente no sistema.
    Coleta informações e valida os dados e armazena no registro global."""
    global paciente_atual
    
    # Coleta e valida nome
    while True:
        nome_paciente = input('Nome do paciente: ').strip()
        confirmacao = input(f'Confirma o nome "{nome_paciente}"? (s/n): ').strip().lower()
        if confirmacao == 's':
            break
        exibir_mensagem('\nPor favor, digite o nome novamente.')

    # Validação do CPF
    while True:
        cpf_input = input('\nDigite seu CPF: ').strip()
        if validar_cpf(cpf_input):
            cpf_formatado = formatar_cpf(cpf_input)
            exibir_mensagem('\nCPF válido!')
            break
        else:
            exibir_mensagem('\nCPF inválido. Tente novamente.')
    
    # Validação da data de nascimento
    while True:
        try:
            data_nascimento_str = input('\nData de nascimento (DD/MM/AAAA): ').strip()
            data_nascimento = datetime.strptime(data_nascimento_str, '%d/%m/%Y')
            data_atual = datetime.now()
            idade_paciente = data_atual.year - data_nascimento.year - ((data_atual.month, data_atual.day) < (data_nascimento.month, data_nascimento.day))
            break
        except ValueError:
            exibir_mensagem('\nData inválida. Use o formato DD/MM/AAAA (ex: 01/01/2000)')
    
    # Validação do telefone
    while True:
        numero_telefone = input('\nTelefone: ').strip()
        telefone_formatado = validar_telefone(numero_telefone)
        if telefone_formatado:
            confirmacao = input(f'Confirma o telefone "{telefone_formatado}"? (s/n): ').strip().lower()
            if confirmacao == 's':
                numero_telefone = telefone_formatado
                break
            exibir_mensagem('\nPor favor, digite o telefone novamente.')
        else:
            exibir_mensagem('\nTelefone inválido. Use o formato (XX)XXXXX-XXXX ou (XX)XXXX-XXXX')
    
    # Validação do email
    while True:
        email_paciente = input('\nEmail: ').strip().lower()  # Converte para minúsculas
        if '@' in email_paciente and '.' in email_paciente and email_paciente.isascii():  # Verifica se tem @, . e se é ASCII
            confirmacao = input(f'Confirma o email "{email_paciente}"? (s/n): ').strip().lower()
            if confirmacao == 's':
                break
            exibir_mensagem('\nPor favor, digite o email novamente.')
        else:
            exibir_mensagem('\nEmail inválido. Digite um email válido.')

    # Verifica se todos os campos foram preenchidos
    if not nome_paciente or not cpf_formatado or not numero_telefone or not email_paciente or not data_nascimento:
        exibir_mensagem('\nTodos os campos são obrigatórios.')
        return

    # Gera um número de prontuário único para o paciente
    prontuario_paciente = gerar_numero_unico(100000, 999999, numeros_prontuarios_usados)

    # Cria o registro do paciente
    paciente_atual = {
        'nome': nome_paciente,
        'cpf': cpf_formatado,
        'data_nascimento': data_nascimento,
        'idade': idade_paciente,
        'telefone': numero_telefone,
        'email': email_paciente,
        'checkin': False,
        'checkin_data': None,
        'prontuario': prontuario_paciente
    }

    # Adiciona o registro à lista global
    registros_pacientes.append(paciente_atual)
    exibir_mensagem(f'\nCadastro realizado. Sessão iniciada para {nome_paciente}.')

def cadastrar_medico():
    """Função para cadastrar um novo médico no sistema"""
    global medico_atual, historico_feedbacks, orientacoes_medicas
    
    # Limpa o histórico de feedbacks e orientações quando um novo médico é cadastrado
    historico_feedbacks = []
    orientacoes_medicas = []
    
    # Coleta e valida nome
    while True:
        nome_medico = input('Nome do médico: ').strip()
        confirmacao = input(f'Confirma o nome "{nome_medico}"? (s/n): ').strip().lower()
        if confirmacao == 's':
            break
        exibir_mensagem('\nPor favor, digite o nome novamente.')

    # Validação do CRM
    while True:
        crm_input = input('\nDigite seu CRM: ').strip()
        crm_validado = validar_crm(crm_input)
        if crm_validado:
            confirmacao = input(f'Confirma o CRM "{crm_validado}"? (s/n): ').strip().lower()
            if confirmacao == 's':
                break
        exibir_mensagem('\nCRM inválido. Tente novamente.')

    # Validação do CPF
    while True:
        cpf_input = input('\nDigite seu CPF: ').strip()
        if validar_cpf(cpf_input):
            cpf_formatado = formatar_cpf(cpf_input)
            exibir_mensagem('\nCPF válido!')
            break
        else:
            exibir_mensagem('\nCPF inválido. Tente novamente.')

    # Cria o registro do médico
    medico_atual = {
        'nome': nome_medico,
        'crm': crm_validado,
        'cpf': cpf_formatado
    }

    # Adiciona o registro à lista global
    registros_medicos.append(medico_atual)
    exibir_mensagem(f'\nCadastro realizado. Sessão iniciada para Dr(a). {nome_medico}.')

def confirmar_checkin():
    """Função que confirma a presença do paciente para a teleconsulta.
    Atualiza o status de check-in e fornece orientações para a consulta."""
    if not paciente_atual:
        exibir_mensagem('Você precisa se cadastrar antes de confirmar presença.')
        return

    if paciente_atual['checkin']:
        exibir_mensagem('Você já confirmou sua presença.')
    else:
        paciente_atual['checkin'] = True
        data_hora_atual = datetime.now()
        paciente_atual['checkin_data'] = data_hora_atual.strftime('%d/%m/%Y %H:%M')
        exibir_mensagem('Check-in confirmado com sucesso.')
        exibir_mensagem(
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
        exibir_mensagem('Você precisa se cadastrar primeiro.')
        return
    if not paciente_atual['checkin']:
        exibir_mensagem('Confirme sua presença antes de enviar o feedback.')
        return

    while True:
        exibir_mensagem('Como foi o processo todo até a consulta?')
        print('1 - Boa\n2 - Regular\n3 - Ruim')
        opcao_escolhida = input('Escolha (ou \'voltar\'): ').strip()

        if opcao_escolhida == 'voltar':
            break

        opcoes_avaliacao = {'1': 'Boa', '2': 'Regular', '3': 'Ruim'}

        if opcao_escolhida in opcoes_avaliacao:
            comentario_feedback = input('Digite seu comentário e nos ajude a melhorar a sua experiência (ou pressione Enter para pular): ').strip()
            data_hora_atual = datetime.now()
            # Gera um número de consulta único
            numero_consulta = gerar_numero_unico(10000, 99999, numeros_consultas_usados)
            feedback = {
                "cpf": paciente_atual["cpf"],
                "nome": paciente_atual["nome"],
                "prontuario": paciente_atual["prontuario"],
                "avaliacao": opcoes_avaliacao[opcao_escolhida],
                "comentario": comentario_feedback,
                "data_hora": data_hora_atual.strftime('%d/%m/%Y %H:%M'),
                "consulta": numero_consulta
            }

            historico_feedbacks.append(feedback)
            # Reseta o status de check-in após enviar o feedback
            paciente_atual['checkin'] = False
            paciente_atual['checkin_data'] = None
            exibir_mensagem('Feedback registrado.')
            break
        else:
            exibir_mensagem('Opção inválida.')

def ver_historico():
    """Função que exibe o histórico completo de registros e feedbacks.
    Mostra informações detalhadas de todos os pacientes cadastrados."""
    if not paciente_atual:
        exibir_mensagem('Nenhum registro encontrado.')
        return

    paciente = paciente_atual
    print(f'{paciente["nome"]} | CPF: {paciente["cpf"]} | Idade: {paciente["idade"]}')
    if paciente['checkin']:
        print(f' • Check-in realizado em: {paciente["checkin_data"]}')
    else:
        print(' • Check-in atual: Não realizado')

    # Filtra apenas os feedbacks do paciente atual
    feedbacks_do_paciente = [f for f in historico_feedbacks if f["cpf"] == paciente["cpf"]]

    if feedbacks_do_paciente:
        print('\nSeus Feedbacks:')
        for i, f in enumerate(feedbacks_do_paciente, 1):
            comentario = f["comentario"] if f["comentario"] else "Sem comentário."
            print(f"Consulta #{f['consulta']} - {f['data_hora']}")
            print(f"Avaliação: {f['avaliacao']}")
            print(f"Comentário: {comentario}\n")
    else:
        exibir_mensagem('\nVocê ainda não enviou feedback.')

def ver_registro():
    """Exibe os dados cadastrais do paciente logado.
    Permite editar informações como nome, telefone e email."""
    if not paciente_atual:
        exibir_mensagem("Nenhum paciente encontrado.")
        return

    paciente = paciente_atual
    print("\nDados do registro:")
    print(f"Nome: {paciente['nome']}")
    print(f"CPF: {paciente['cpf']}")
    print(f"Data de Nascimento: {paciente['data_nascimento'].strftime('%d/%m/%Y')}")
    print(f"Idade: {paciente['idade']}")
    print(f"Telefone: {paciente['telefone']}")
    print(f"Email: {paciente['email']}")

    opcao = input("\nDeseja editar este registro? (s/n): \n").strip().lower()
    if opcao == 's':
        editar_registro(paciente)    

def editar_registro(paciente):
    """Permite editar os dados de um registro de paciente"""
    while True:
        print("\nEscolha o campo que deseja editar:")
        print("1 - Nome")
        print("2 - Telefone")
        print("3 - Email")
        print("4 - Voltar")
        
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
                telefone_formatado = validar_telefone(novo_telefone)
                if telefone_formatado:
                    confirmacao = input(f"Confirma a alteração do telefone para '{telefone_formatado}'? (s/n): \n").strip().lower()
                    if confirmacao == 's':
                        paciente['telefone'] = telefone_formatado
                        print("Telefone atualizado com sucesso!")
                        break
                else:
                    print("Telefone inválido. Use o formato (XX)XXXXX-XXXX ou (XX)XXXX-XXXX")
                    
        elif opcao == '3':
            novo_email = input("Novo email: ").strip().lower()  # Converte para minúsculas
            if '@' in novo_email and '.' in novo_email and novo_email.isascii():  # Verifica se tem @, . e se é ASCII
                confirmacao = input(f"Confirma a alteração do email para '{novo_email}'? (s/n): \n").strip().lower()
                if confirmacao == 's':
                    paciente['email'] = novo_email
                    print("Email atualizado com sucesso!")
            else:
                print("Email inválido!")
                    
        elif opcao == '4':
            break
        else:
            print("Opção inválida!")

def ver_feedbacks_medico():
    """Função que permite ao médico visualizar os feedbacks dos pacientes"""
    if not medico_atual:
        exibir_mensagem('Você precisa se cadastrar primeiro.')
        return

    if not historico_feedbacks:
        exibir_mensagem('Nenhum feedback registrado.')
        return

    print('\nFeedbacks dos Pacientes:')
    for i, feedback in enumerate(historico_feedbacks, 1):
         nome = feedback.get('nome', 'Desconhecido')
         avaliacao = feedback.get('avaliacao', '---')
         comentario = feedback.get('comentario') or 'Nenhum'
         data_hora = feedback.get('data_hora', '---')
         prontuario = feedback.get('prontuario', '---')
         consulta = feedback.get('consulta', '---')
         print(f"\n{i}. Paciente: {nome} (Prontuário: #{prontuario})")
         print(f"   Consulta #{consulta} - {data_hora}")
         print(f"   Avaliação: {avaliacao}")
         print(f"   Comentário: {comentario}")

def ver_historico_medico():
    """Função que permite ao médico visualizar o histórico de pacientes"""
    if not medico_atual:
        exibir_mensagem('Você precisa se cadastrar primeiro.')
        return

    if not registros_pacientes:
        exibir_mensagem('Nenhum registro de paciente encontrado.')
        return

    print('\nHistórico de Pacientes:')
    for paciente in registros_pacientes:
        print(f'\nPaciente: {paciente["nome"]}')
        print(f'Prontuário: #{paciente["prontuario"]}')
        print(f'Idade: {paciente["idade"]}')
        if paciente['checkin']:
            print(f'Check-in realizado em: {paciente["checkin_data"]}')
        else:
            print('Check-in: Não realizado')

def adicionar_orientacao():
    """Função que permite ao médico adicionar orientações para os pacientes"""
    if not medico_atual:
        exibir_mensagem('Você precisa se cadastrar primeiro.')
        return

    if not registros_pacientes:
        exibir_mensagem('Nenhum paciente cadastrado.')
        return

    print('\nPacientes disponíveis:')
    for i, paciente in enumerate(registros_pacientes, 1):
        print(f'{i} - {paciente["nome"]} (Prontuário: #{paciente["prontuario"]})')

    try:
        escolha = int(input('\nEscolha o número do paciente (ou 0 para voltar): ').strip())
        if escolha == 0:
            return
        if 1 <= escolha <= len(registros_pacientes):
            paciente = registros_pacientes[escolha - 1]
            orientacao = input('\nDigite a orientação médica: ').strip()
            data_orientacao = datetime.now().strftime('%d/%m/%Y %H:%M')
            
            orientacao_completa = {
                'paciente': paciente['nome'],
                'prontuario': paciente['prontuario'],
                'medico': medico_atual['nome'],
                'crm': medico_atual['crm'],
                'orientacao': orientacao,
                'data': data_orientacao
            }
            
            orientacoes_medicas.append(orientacao_completa)
            exibir_mensagem('\nOrientação registrada com sucesso!')
        else:
            exibir_mensagem('Número de paciente inválido!')
    except ValueError:
        exibir_mensagem('Por favor, digite um número válido!')

def ver_orientacoes_paciente():
    """Função que permite ao paciente visualizar suas orientações médicas"""
    if not paciente_atual:
        exibir_mensagem('Você precisa se cadastrar primeiro.')
        return

    # Filtra as orientações para mostrar apenas as do paciente atual
    orientacoes_do_paciente = [
        orientacao for orientacao in orientacoes_medicas 
        if orientacao['prontuario'] == paciente_atual['prontuario']
    ]

    if not orientacoes_do_paciente:
        exibir_mensagem('\nNenhuma orientação médica registrada para você.')
        return

    print('\nSuas Orientações Médicas:')
    for i, orientacao in enumerate(orientacoes_do_paciente, 1):
        print(f'\n{i}. Data: {orientacao["data"]}')
        print(f'   Médico: Dr(a). {orientacao["medico"]} (CRM: {orientacao["crm"]})')
        print(f'   Prontuário: #{orientacao["prontuario"]}')
        print(f'   Orientação: {orientacao["orientacao"]}')

def menu():
    """Função principal que exibe o menu interativo do sistema.
    Permite ao usuário navegar entre as diferentes funcionalidades."""
    while True:
        print('\n---- Sistema de Triagem ----')
        exibir_mensagem('Escolha uma opção:')
        print('1 - Área do Médico')
        print('2 - Área do Paciente')
        print('3 - Sair')

        opcao = input('\nOpção: ').strip()
        if opcao == '1':
            menu_medico()
        elif opcao == '2':
            menu_paciente()
        elif opcao == '3':
            exibir_mensagem('Sistema encerrado.')
            break
        else:
            exibir_mensagem('Opção inválida.')

def menu_paciente():
    """Menu específico para pacientes"""
    while True:
        print('\n---- Menu Paciente ----')
        exibir_mensagem('Escolha uma opção:')
        print('1 - Cadastrar paciente')
        print('2 - Confirmar presença')
        print('3 - Enviar feedback')
        print('4 - Ver histórico')
        print('5 - Ver registro')
        print('6 - Ver orientações médicas')
        print('7 - Sair')

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
            ver_orientacoes_paciente()
        elif opcao == '7':
            break
        else:
            exibir_mensagem('Opção inválida.')

def menu_medico():
    """Menu específico para médicos"""
    while True:
        print('\n---- Menu Médico ----')
        exibir_mensagem('Escolha uma opção:')
        print('1 - Cadastrar médico')
        print('2 - Ver feedbacks')
        print('3 - Ver histórico de pacientes')
        print('4 - Adicionar orientação')
        print('5 - Voltar ao menu principal')

        opcao = input('\nOpção: ').strip()
        if opcao == '1':
            cadastrar_medico()
        elif opcao == '2':
            ver_feedbacks_medico()
        elif opcao == '3':
            ver_historico_medico()
        elif opcao == '4':
            adicionar_orientacao()
        elif opcao == '5':
            break
        else:
            exibir_mensagem('Opção inválida.')

# Inicia o programa executando o menu principal
menu()
