import requests

def consultar_cep(cep):
    url = f'https://viacep.com.br/ws/{cep}/json/'
    resposta = requests.get(url)
 
    if resposta.status_code == 200:
        dados = resposta.json()
        if 'erro' in dados:
            print("CEP não encontrado.")
        else:
            print(f"\nEndereço: {dados.get('logradouro')}")
            print(f"Complemento: {dados.get('complemento')}")
            print(f"Bairro: {dados.get('bairro')}")
            print(f"Cidade: {dados.get('localidade')} - {dados.get('uf')}\n")
    else:
        print("Erro ao consultar o CEP.")
 

 
 