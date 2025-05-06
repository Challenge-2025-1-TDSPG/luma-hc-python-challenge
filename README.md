#  Sistema de Triagem para Teleconsulta

Este projeto simula um sistema básico de triagem para pacientes que irão participar de uma **teleconsulta**. O sistema permite o cadastro completo do paciente, confirmação de presença (check-in), envio de feedback e visualização de histórico de atendimentos.

---

##  Funcionalidades

- **Cadastro de Pacientes**  
  - Nome completo  
  - CPF com validação  
  - Data de nascimento  
  - Telefone  
  - E-mail com validação  
  - CEP formatado  

- **Confirmação de Presença**  
  - Registra data e hora do check-in  
  - Exibe orientações importantes para a realização da teleconsulta

- **Envio de Feedback**  
  - Avaliação da experiência (Boa, Regular ou Ruim)

- **Histórico**  
  - Exibe dados de todos os pacientes registrados  
  - Indica se o paciente realizou o check-in e quando  
  - Lista de feedbacks enviados

---

##  Tecnologias Utilizadas

- Python 3.10+
- Validação de CPF com módulo auxiliar `validadar_cpf.py`
- Execução via terminal (modo CLI)

---

##  Como Executar

1. Abra o terminal na pasta do projeto.

2. Execute o sistema com o comando:
   ```bash
   python triagem_teleconsul.py

---

##  Possíveis Melhorias Futuras

- Login por CPF (evitar múltiplos cadastros)
- Geração de número de protocolo da consulta
- Exportação do histórico para arquivo .txt ou .csv
- Simulação de envio de e-mail ou SMS
- Integração com API de CEP

##  Desenvolvedor
Lucas Rossoni Dieder
Aluno de Análise e Desenvolvimento de Sistemas - FIAP
Projeto desenvolvido para o Challenge 2025 – 1º Semestre
