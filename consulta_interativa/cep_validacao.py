import requests
#Consulta o CEP na API ViaCEP e retorna os dados do endereço.
def consultar_cep(cep):
    # Remove caracteres não numéricos do CEP
    cep_limpo = cep.replace('-', '')
    
    # Verifica se o CEP tem 8 dígitos
    if len(cep_limpo) != 8:
        print('CEP inválido! O CEP deve conter 8 dígitos.')
        return None
    
    # URL da API ViaCEP
    url = f'https://viacep.com.br/ws/{cep_limpo}/json/'
    
    try:
        # Faz a requisição para a API
        resposta = requests.get(url)
        
        # Verifica se a requisição foi bem sucedida
        if resposta.status_code == 200:
            dados = resposta.json()
            
            # Verifica se o CEP existe
            if 'erro' not in dados:
                # Exibe os dados do endereço
                print(f"\nDados do CEP {cep}:")
                print(f"Logradouro: {dados.get('logradouro', 'Não informado')}")
                print(f"Bairro: {dados.get('bairro', 'Não informado')}")
                print(f"Cidade: {dados.get('localidade')} - {dados.get('uf')}\n")
                return dados
            else:
                print('CEP não encontrado!')
                return None
        else:
            print('Erro ao consultar o CEP. Tente novamente mais tarde.')
            return None
            
    except requests.exceptions.RequestException as erro:
        print(f'Erro na requisição: {erro}')
        return None
 

 
 