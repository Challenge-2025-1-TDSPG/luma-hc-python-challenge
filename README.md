# Sistema de Triagem para Teleconsulta

Sistema interativo para gerenciamento de pacientes em teleconsultas, desenvolvido em Python.

## Funcionalidades

### Cadastro de Pacientes

- Validação completa de CPF
- Validação de email
- Validação de telefone
- Consulta automática de CEP via API ViaCEP
- Coleta de endereço completo (logradouro, número, complemento, bairro, cidade, UF)
- Confirmação de todos os dados inseridos

### Gerenciamento de Consultas

- Confirmação de presença (check-in)
- Orientações pré-consulta
- Feedback pós-consulta com opção de comentários
- Histórico completo de registros
- Visualização detalhada de registros individuais

### Edição de Registros

- Atualização de dados pessoais
- Alteração de endereço com validação de CEP
- Confirmação de alterações

## Tecnologias Utilizadas

- Python 3.x
- Biblioteca `requests` para consulta de CEP
- API ViaCEP para validação de endereços

## Como Executar

1. Instale as dependências:

```bash
pip install requests
```

2. Execute o programa principal:

```bash
python consulta_interativa/triagem_teleconsul.py
```

## Estrutura do Projeto

```
consulta_interativa/
├── triagem_teleconsul.py    # Programa principal
├── cep_validacao.py         # Validação de CEP
└── validadar_cpf.py         # Validação de CPF
```

## Funcionalidades Detalhadas

### Validação de CPF

- Verifica se o CPF possui 11 dígitos
- Valida os dígitos verificadores
- Formata automaticamente no padrão XXX.XXX.XXX-XX

### Validação de CEP

- Consulta automática via API ViaCEP
- Validação do formato do CEP
- Retorno de endereço completo
- Tratamento de erros de conexão

### Feedback

- Avaliação da experiência (Boa, Regular, Ruim)
- Campo opcional para comentários
- Armazenamento do histórico de feedbacks

### Registros

- Visualização de todos os registros
- Detalhes completos de cada paciente
- Edição de informações
- Histórico de check-ins

## Desenvolvedor

Lucas Rossoni Dieder
Aluno de Análise e Desenvolvimento de Sistemas - FIAP
Projeto desenvolvido para o Challenge 2025 – 1º Semestre
