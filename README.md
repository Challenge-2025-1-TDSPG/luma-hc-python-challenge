# Sistema de Triagem para Teleconsulta

Sistema interativo em Python para triagem e acompanhamento de pacientes e médicos durante teleconsultas, com validações completas, orientações clínicas e histórico de feedbacks.

## Funcionalidades

### Área do Paciente

- Cadastro completo com:
  - Validação de CPF (estrutura e dígitos verificadores)
  - Validação de e-mail e telefone
  - Consulta automática de endereço via API ViaCEP
  - Coleta e confirmação de dados residenciais (logradouro, número, complemento, bairro, cidade, UF)
- Confirmação de presença (check-in)
- Orientações automáticas pré-consulta
- Envio de feedback com opção de comentário
- Visualização do histórico pessoal
- Edição de dados cadastrados

### Área do Médico

- Cadastro com validação de CRM, CPF e telefone
- Visualização de feedbacks dos pacientes (organizados por CPF e avaliação)
- Acesso ao histórico geral dos pacientes cadastrados
- Emissão e registro de orientações médicas personalizadas

## Tecnologias Utilizadas

- Python 3.x
- Biblioteca `requests` para chamadas HTTP
- API ViaCEP para validação de endereços

## Como Executar

1. Instale as dependências:

```bash
pip install requests
```

2. Execute o programa principal:

```bash
python menu_interativo/triagem_teleconsulta.py
```

## Estrutura do Projeto

```
menu_interativo/
├── triagem_teleconsul.py    # Programa principal (menus, cadastros e lógicas)
├── validar_cep.py.py         # Módulo para consulta e validação de CEP via API
└── validar_cpf.py         # Módulo para validação e formatação de CPF
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

- Opções de avaliação: Boa, Regular ou Ruim
- Comentário opcional
- Visualização exclusiva do paciente logado
- Visualização completa para médicos

### Registros e Histórico

- Acesso a dados detalhados do paciente logado
- Visualização de histórico de check-in e orientações médicas
- Atualização de dados pessoais e endereço

## Desenvolvedor

Lucas Rossoni Dieder
Aluno de Análise e Desenvolvimento de Sistemas - FIAP
Projeto desenvolvido para o Challenge 2025 – 1º Semestre
