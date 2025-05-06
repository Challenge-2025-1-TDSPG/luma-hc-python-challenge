import re

def validar_cpf(cpf: str) -> bool:
    # Remove todos os caracteres não numéricos do CPF
    digitos_apenas = re.sub(r'\D', '', cpf)

    # Verifica se o CPF tem 11 dígitos e não é uma sequência de números iguais
    if len(digitos_apenas) != 11 or digitos_apenas == digitos_apenas[0] * 11:
        return False

    def calcular_digito(parcial: str, multiplicadores: range) -> int:
        """
        Calcula um dígito verificador do CPF.
            parcial: String com os dígitos para cálculo
            multiplicadores: Range de multiplicadores para o cálculo
        """
        # Soma o produto de cada dígito pelo seu multiplicador
        soma = sum(int(digito) * mult for digito, mult in zip(parcial, multiplicadores))
        resto = soma % 11
        return 0 if resto < 2 else 11 - resto

    # Calcula o primeiro dígito verificador
    primeiro_digito = calcular_digito(digitos_apenas[:9], range(10, 1, -1))
    # Calcula o segundo dígito verificador
    segundo_digito = calcular_digito(digitos_apenas[:10], range(11, 1, -1))

    # Verifica se os dígitos calculados correspondem aos dígitos do CPF
    eh_valido = digitos_apenas[-2:] == f'{primeiro_digito}{segundo_digito}'
    return eh_valido

def formatar_cpf(cpf: str) -> str: # Formata um CPF válido para o padrão XXX.XXX.XXX-XX.
    # Remove todos os caracteres não numéricos
    digitos_apenas = re.sub(r'\D', '', cpf)
    if len(digitos_apenas) != 11:
        return cpf  # Retorna original se o tamanho for inválido
    
    # Formata o CPF com pontos e traço
    return f'{digitos_apenas[:3]}.{digitos_apenas[3:6]}.{digitos_apenas[6:9]}-{digitos_apenas[9:]}'

def validar_e_formatar_cpf(cpf: str) -> str: #Valida e formata o CPF.
    if validar_cpf(cpf):
        cpf_formatado = formatar_cpf(cpf)
        print(f'CPF válido: {cpf_formatado}')
        return cpf_formatado
    else:
        print('CPF inválido.')
        return 'CPF inválido'
 