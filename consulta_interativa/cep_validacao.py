import requests
 
def consultar_cep(cep):
    url = f'https://viacep.com.br/ws/{cep}/json/'
    resposta = requests.get(url)
 
    if resposta.status_code == 200:
        dados = resposta.json()
        if 'erro' in dados:
            print("CEP não encontrado.")
        else:
            print(f"CEP: {dados.get('cep')}")
            print(f"Logradouro: {dados.get('logradouro')}")
            print(f"Complemento: {dados.get('complemento')}")
            print(f"Bairro: {dados.get('bairro')}")
            print(f"Cidade: {dados.get('localidade')}")
            print(f"Estado (UF): {dados.get('uf')}")
            #{"cep":"01404-003","logradouro":"Alameda Campinas","complemento":"de 1271 ao fim - lado ímpar","unidade":"","bairro":"Jardim Paulista","localidade":"São Paulo","uf":"SP","estado":"São Paulo"
    else:
        print("Erro ao consultar o CEP.")
 

 
 