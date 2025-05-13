# Sistema de Triagem para Teleconsulta

Sistema interativo em Python para triagem e acompanhamento de pacientes e médicos durante teleconsultas, com validações completas, orientações clínicas e histórico de feedbacks.

## Funcionalidades

### Área do Paciente

- Cadastro completo com:
- Validação de CPF (estrutura e dígitos verificadores)
- Validação de e-mail e telefone
- Data de nascimento com cálculo automático de idade
- Confirmação de presença (check-in)
- Orientações automáticas pré-consulta
- Envio de feedback com opção de comentário
- Visualização do histórico pessoal
- Edição de dados cadastrados
- Visualização de orientações médicas

### Área do Médico

- Cadastro com validação de CRM, CPF e telefone
- Visualização de feedbacks dos pacientes (organizados por CPF e avaliação)
- Acesso ao histórico geral dos pacientes cadastrados
- Emissão e registro de orientações médicas personalizadas

## Tecnologias Utilizadas

- Python 3.x
- Biblioteca `datetime` para manipulação de datas
- Módulo personalizado `validar_cpf` para validação de CPF

## Como Executar

1. Certifique-se de ter o Python 3.x instalado

2. Execute o programa principal:

```bash
python menu_interativo/app.py
```

## Estrutura do Projeto

```
menu_interativo/
├── app.py           # Programa principal (menus, cadastros e lógicas)
└── validar_cpf.py   # Módulo para validação e formatação de CPF
```

## Funcionalidades Detalhadas

### Validação de CPF

- Verifica se o CPF possui 11 dígitos
- Valida os dígitos verificadores
- Formata automaticamente no padrão XXX.XXX.XXX-XX

### Validação de Telefone

- Aceita formatos com e sem DDD
- Formata automaticamente no padrão (XX)XXXX-XXXX ou (XX)XXXXX-XXXX
- Validação de números com 10 ou 11 dígitos

### Feedback

- Opções de avaliação: Boa, Regular ou Ruim
- Comentário opcional
- Visualização exclusiva do paciente logado
- Visualização completa para médicos

### Registros e Histórico

- Acesso a dados detalhados do paciente logado
- Visualização de histórico de check-in e orientações médicas
- Atualização de dados pessoais (nome, telefone e email)

## Desenvolvedor

Lucas Rossoni Dieder
Aluno de Análise e Desenvolvimento de Sistemas - FIAP
Projeto desenvolvido para o Challenge 2025 – 1º Semestre
