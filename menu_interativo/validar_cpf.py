import re

def validar_cpf(cpf):
    # Remove caracteres não numéricos
    cpf = ''.join(filter(str.isdigit, cpf))
    
    # Verifica se tem 11 dígitos
    if len(cpf) != 11:
        return False
    
    # Verifica se todos os dígitos são iguais
    if cpf == cpf[0] * 11:
        return False
    
    # Calcula primeiro dígito verificador
    soma = 0
    for i in range(9):
        soma += int(cpf[i]) * (10 - i)
    resto = soma % 11
    digito1 = 0 if resto < 2 else 11 - resto
    
    # Calcula segundo dígito verificador
    soma = 0
    for i in range(10):
        soma += int(cpf[i]) * (11 - i)
    resto = soma % 11
    digito2 = 0 if resto < 2 else 11 - resto
    
    # Verifica se os dígitos calculados são iguais aos do CPF
    return int(cpf[9]) == digito1 and int(cpf[10]) == digito2

#Formata um CPF no padrão XXX.XXX.XXX-XX.
def formatar_cpf(cpf):
    # Remove caracteres não numéricos
    cpf = ''.join(filter(str.isdigit, cpf))
    
    # Formata o CPF
    return f'{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}'

def validar_e_formatar_cpf(cpf: str) -> str: #Valida e formata o CPF.
    if validar_cpf(cpf):
        cpf_formatado = formatar_cpf(cpf)
        print(f'CPF válido: {cpf_formatado}')
        return cpf_formatado
    else:
        print('CPF inválido.')
        return 'CPF inválido'
 