# Sistema de Gerenciamento de CRUD de FAQs em Python com Integração Oracle para Luma HC

## Tecnologias e Requisitos de Sistema

- **Linguagem:** Python 3.8+
- **Banco de Dados:** Oracle Database 12c ou superior (requer suporte a `IDENTITY`)
- **Driver Oracle:** Modo Thin do oracledb
- **Driver Oracle:** oracledb 1.4.1
- **API REST:** Flask 3.1.2
- **Interface de Terminal:** Colorama 0.4.6
- **Gerenciador de Dependências:** venv + requirements.txt
- **Ferramentas adicionais:** pip (instalador)
- **Ambiente de Execução:** Windows (recomendado)
- **Acesso:** Conexão a uma instância Oracle com privilégios de criação de tabelas

> **Atenção:** O sistema utiliza o recurso **IDENTITY** do Oracle, disponível apenas a partir do Oracle 12c (12.1) ou superior.

---

## Visão Geral Profissional

Este projeto implementa um sistema de gerenciamento de FAQ (Frequently Asked Questions) para a aplicação **Luma HC** (Challenge 2025 – FIAP, Hospital das Clínicas).
Foi desenvolvido em Python, priorizando **POO**, modularidade, escalabilidade e integração corporativa.

- **CRUD Completo de FAQs**: criar, listar, atualizar e remover perguntas e respostas, com categorização e status (ativo/inativo).
- **Exportação para JSON**: gera backups e integrações.
- **Operações em Memória**: CRUD em lista de dicionários para testes e simulações.
- **API RESTful**: endpoints para integração com front-ends (`api/faq_api.py`).
- **Integração Oracle**: persistência no Oracle via `oracledb` e `.env`.
- **Validação Robusta**: entradas do usuário com tratamento de erros.
- **Estrutura Simples**: organização plana para facilitar manutenção e evolução.

---

## Estrutura de Pastas

```
menu_interativo/
    main.py            # Ponto de entrada do sistema (menu interativo)
    menu.py            # Menu principal
    banco.py           # Operações Oracle (CRUD, conexão, categorias)
    memoria.py         # CRUD em memória
    exportacao.py      # Exportação/importação de dados
    models.py          # Modelos de dados
    api/
        faq_api.py     # API RESTful com Flask
    json/              # Exportações JSON
    data/              # Dados auxiliares
    .env               # Configuração (não versionado)
    requirements.txt   # Dependências do projeto
    README.md          # Este arquivo
    LICENSE            # Licença de uso
    scripts/           # Scripts auxiliares para execução
```

---

## Fluxo de Funcionamento

1. **Inicialização**: O sistema carrega as configurações Oracle do arquivo `.env` e valida a conexão.
2. **Menu Interativo**: O usuário navega pelo menu principal, podendo acessar:
   - CRUD de FAQs (banco Oracle)
   - Listagem e manipulação de FAQs em memória
   - Exportação para JSON
3. **API RESTful**: Opcionalmente, o sistema pode ser executado como API para integração com front-ends (`api/faq_api.py`).

---

## Integração com Oracle

- O acesso ao banco é feito exclusivamente via Oracle, utilizando o driver `oracledb`.
- As credenciais e parâmetros de conexão são lidos do arquivo `.env`, nunca hardcoded.
- Todas as operações CRUD são transacionais e seguras.

### Esquema do Banco de Dados (DDL)

```sql
CREATE TABLE FAQ (
    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    pergunta VARCHAR2(150) NOT NULL,
    resposta VARCHAR2(600) NOT NULL,
    ativo NUMBER(1) NOT NULL,
    atualizado_em VARCHAR2(50) NOT NULL,
    categoria VARCHAR2(50) NOT NULL
);

CREATE INDEX idx_faq_categoria ON FAQ(categoria);
CREATE INDEX idx_faq_ativo ON FAQ(ativo);

COMMENT ON COLUMN FAQ.id IS 'Identificador único do FAQ (gerado automaticamente)';
COMMENT ON COLUMN FAQ.pergunta IS 'Texto da pergunta (máximo 150 caracteres)';
COMMENT ON COLUMN FAQ.resposta IS 'Texto da resposta (máximo 600 caracteres)';
COMMENT ON COLUMN FAQ.ativo IS 'Status de ativação (1=ativo, 0=inativo)';
COMMENT ON COLUMN FAQ.atualizado_em IS 'Data e hora da última atualização (formato YYYY-MM-DD HH:MM:SS)';
COMMENT ON COLUMN FAQ.categoria IS 'Categoria para agrupamento e filtragem';
```

---

## Exportação e Integração

- Os dados podem ser exportados para JSON na pasta `json/`.
- A API RESTful permite integração total com front-ends, sistemas legados e automações.

## API RESTful

A aplicação oferece uma API RESTful implementada com Flask para integração com outras aplicações.

### Endpoints Disponíveis

| Método | Rota         | Descrição                 | Parâmetros              |
| ------ | ------------ | ------------------------- | ----------------------- |
| GET    | `/faqs`      | Lista todos os FAQs       | -                       |
| GET    | `/faqs/<id>` | Obtém um FAQ específico   | ID na URL               |
| POST   | `/faqs`      | Adiciona um novo FAQ      | JSON no body            |
| PUT    | `/faqs/<id>` | Atualiza um FAQ existente | ID na URL, JSON no body |
| DELETE | `/faqs/<id>` | Remove um FAQ             | ID na URL               |

### Exemplos de Uso

**Listar todos os FAQs:**

```bash
curl -X GET http://localhost:5000/faqs
```

**Obter um FAQ específico:**

```bash
curl -X GET http://localhost:5000/faqs/1
```

**Adicionar um novo FAQ:**

```bash
curl -X POST http://localhost:5000/faqs \
  -H "Content-Type: application/json" \
  -d '{"pergunta": "Como funciona o sistema?", "resposta": "Este é um sistema de gerenciamento de FAQs.", "ativo": 1, "categoria": "Geral"}'
```

**Atualizar um FAQ existente:**

```bash
curl -X PUT http://localhost:5000/faqs/1 \
  -H "Content-Type: application/json" \
  -d '{"pergunta": "Como funciona o sistema?", "resposta": "Este é um sistema de gerenciamento de FAQs atualizado.", "ativo": 1, "categoria": "Geral"}'
```

**Remover um FAQ:**

```bash
curl -X DELETE http://localhost:5000/faqs/1
```

---

## Boas Práticas e Manutenção

- **Simplicidade**: Estrutura plana, fácil de entender e manter.
- **Documentação**: Todas as classes e métodos possuem docstrings explicativas.
- **Validação e Segurança**: Entradas do usuário e operações críticas são validadas e tratadas.
- **Escalabilidade**: Estrutura pronta para expansão, seja para novos tipos de dados, integrações ou regras de negócio.

---

## Configuração e Execução

### 1. Ambiente Virtual e Instalação de Dependências

1. **Crie e ative o ambiente virtual (venv):**

   ```cmd
   # Windows
   python -m venv venv
   venv\Scripts\activate
   ```

2. **Instale as dependências do projeto:**
   ```cmd
   pip install -r requirements.txt
   ```

### 2. Configuração do Arquivo .env

Crie um arquivo `.env` na pasta `menu_interativo/` com as seguintes variáveis:

```ini
# Credenciais Oracle
DB_USER=seu_usuario
DB_PASS=sua_senha
DB_URL=oracle.com.br:xxxx/ORCL
```

### 3. Execução do Sistema

1. **Menu Interativo:**

   ```cmd
   cd menu_interativo
   python main.py
   ```

2. **API RESTful:**
   ```cmd
   cd menu_interativo
   python api/faq_api.py
   ```
   A API estará disponível em http://localhost:5000/

### Scripts

Scripts auxiliares podem ser criados na pasta `scripts/` para facilitar a execução.

---

## Contato

| Nome                           | RM     | GitHub                                        | LinkedIn                                                                |
| ------------------------------ | ------ | --------------------------------------------- | ----------------------------------------------------------------------- |
| Alexander Dennis Isidro Mamani | 565554 | [alex-isidro](https://github.com/alex-isidro) | [LinkedIn](https://www.linkedin.com/in/alexander-dennis-a3b48824b/)     |
| Kelson Zhang                   | 563748 | [KelsonZh0](https://github.com/KelsonZh0)     | [LinkedIn](https://www.linkedin.com/in/kelson-zhang-211456323/)         |
| Lucas Rossoni Dieder           | 563770 | [PxS00](https://github.com/PxS00)             | [LinkedIn](https://www.linkedin.com/in/lucas-rossoni-dieder-32242a353/) |
