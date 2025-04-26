'''
“A base do projeto foi estruturada inicialmente com um menu simples que realiza cadastros, consultas e buscas. A partir dessa estrutura, ampliamos as funcionalidades para simular um sistema realista de apoio à teleconsulta, com foco no desafio proposto pelo HC.”
'''

import time

# Lista para armazenar dados 
registros = []


# Função 1: Cadastrar um nome
def cadastrar_nome(lista):
    nome = input("Digite um nome para cadastrar: ").strip()
    if nome:
        lista.append(nome)
        print(f"Nome '{nome}' cadastrado com sucesso!")
    else:
        print("Nome inválido!")

# Função 2: Ver todos os nomes cadastrados
def ver_registros(lista):
    if lista:
        print("\n--- Registros Cadastrados ---")
        for i, nome in enumerate(lista, start=1):
            print(f"{i}. {nome}")
    else:
        print("Nenhum registro encontrado.")

# Função 3: Buscar um nome específico
def buscar_nome(lista):
    busca = input("Digite o nome que deseja buscar: ").strip()
    if busca in lista:
        print(f"O nome '{busca}' está cadastrado.")
    else:
        print(f"O nome '{busca}' não foi encontrado.")

# Função para mostrar o menu
def menu():
    while True:
        print("\n=== MENU PRINCIPAL ===")
        print("1 - Cadastrar nome")
        print("2 - Ver registros")
        print("3 - Buscar nome")
        print("4 - Sair")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            cadastrar_nome(registros)
        elif opcao == "2":
            ver_registros(registros)
        elif opcao == "3":
            buscar_nome(registros)
        elif opcao == "4":
            print("Encerrando o programa...")
            time.sleep(1)
            break
        else:
            print("Opção inválida. Tente novamente.")

# Execução do programa
menu()
