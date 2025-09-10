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
- **Estrutura Modular**: organização por pacotes para facilitar evolução.


---

## Estrutura de Pastas

```
python-challenge/
    README.md             # Este arquivo de documentação
    requirements.txt      # Dependências do projeto
    LICENSE               # Licença de uso 
    scripts/              # Scripts auxiliares para execução
        run_menu.bat      # Script para iniciar o menu interativo (Windows)
        run_api.bat       # Script para iniciar a API RESTful (Windows)
    menu_interativo/
        main.py           # Ponto de entrada do sistema (menu interativo)
        .env              # Arquivo de configuração com credenciais (não versionado)
        data/             # Exportações e arquivos auxiliares
            .gitkeep      # Mantém a pasta no git mesmo vazia
        api/
            faq_api.py    # Implementação da API RESTful com Flask
        faq/
            __init__.py        # Facilita importações de todo o módulo
            db.py              # Camada de acesso Oracle
            models.py          # Modelos de dados (FAQ)
            menu.py            # Menu principal (orquestrador)
            banco_oracle/
                __init__.py    # Exporta operações do banco
                menu_crud.py   # Orquestrador do menu CRUD
                crud/
                    __init__.py    # Exporta todas as funções CRUD
                    adicionar.py   # Adiciona FAQ
                    listar.py      # Lista FAQs
                    atualizar.py   # Atualiza FAQ
                    deletar.py     # Deleta FAQ
                    buscar.py      # Busca FAQ por ID
                    categorias.py  # Lista categorias
            exportacao/
                __init__.py
                menu_exportacao.py # Exportação para JSON
                exportar_banco.py  # Função de exportação
            memoria/
                __init__.py        # Exporta operações de memória
                menu_memoria.py    # Menu de operações em memória
                crud_memoria/
                    __init__.py    # Exporta funções CRUD de memória
                    adicionar.py   # Adiciona FAQ em memória
                    listar.py      # Lista FAQs em memória
                    atualizar.py   # Atualiza FAQ em memória
                    deletar.py     # Remove FAQ em memória
                    buscar.py      # Busca FAQ em memória
```

---

## Fluxo de Funcionamento

1. **Inicialização**: O sistema carrega as configurações Oracle do arquivo `.env` e valida a conexão.
2. **Menu Interativo**: O usuário navega pelo menu principal, podendo acessar:
   - CRUD de FAQs (cada operação em um arquivo próprio em `banco_oracle/crud/`)
   - Listagem e manipulação de FAQs em memória (via `memoria/menu_memoria.py` e módulos em `memoria/crud_memoria/`)
   - Exportação para JSON (via `exportacao/menu_exportacao.py`)
3. **API RESTful**: Opcionalmente, o sistema pode ser executado como API para integração com front-ends (via `api/faq_api.py`).

---

## Integração com Oracle

- O acesso ao banco é feito exclusivamente via Oracle, utilizando o driver `oracledb` (sucessor oficial do cx_Oracle).
- As credenciais e parâmetros de conexão são lidos do arquivo `.env`, nunca hardcoded.
- Todas as operações CRUD são transacionais e seguras.

### Esquema do Banco de Dados (DDL)

```sql
-- Script de criação da tabela FAQ com suporte a IDENTITY (Oracle 12c+)
CREATE TABLE FAQ (
    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    pergunta VARCHAR2(150) NOT NULL,
    resposta VARCHAR2(600) NOT NULL,
    ativo NUMBER(1) NOT NULL,
    atualizado_em VARCHAR2(50) NOT NULL,
    categoria VARCHAR2(50) NOT NULL
);

-- Índice para otimizar pesquisas por categoria
CREATE INDEX idx_faq_categoria ON FAQ(categoria);

-- Índice para otimizar pesquisas por status de ativação
CREATE INDEX idx_faq_ativo ON FAQ(ativo);

-- ComentárioBLE FAQ IS 'Tabela que armazena as perguntas frequentes do sistema';
COMMENT ON COLUMN FAQ.id IS 'Identificador único do FAQ (gerado automaticamente)';
COMMENT ON COLUMN FAQ.pergunta IS 'Texto da pergunta (máximo 150 caracteres)';
COMMENT ON COLUMN FAQ.resposta IS 'Texto da resposta (máximo 600 caracteres)';
COMMENT ON COLUMN FAQ.ativo IS 'Status de ativação (1=ativo, 0=inativo)';
COMMENT ON COLUMN FAQ.atualizado_em IS 'Data e hora da última atualização (formato YYYY-MM-DD HH:MM:SS)';
COMMENT ON COLUMN FAQ.categoria IS 'Categoria para agrupamento e filtragem';
```

---

## Exportação e Integração

- Os dados podem ser exportados para JSON na pasta `data/faq_export.json`.
- A API RESTful permite integração total com front-ends, sistemas legados e automações.

## API RESTful

A aplicação oferece uma API RESTful implementada com Flask para integração com outras aplicações. 

### Endpoints Disponíveis

| Método | Rota | Descrição | Parâmetros |
|--------|------|-----------|------------|
| GET | `/faqs` | Lista todos os FAQs | - |
| GET | `/faqs/<id>` | Obtém um FAQ específico | ID na URL |
| POST | `/faqs` | Adiciona um novo FAQ | JSON no body |
| PUT | `/faqs/<id>` | Atualiza um FAQ existente | ID na URL, JSON no body |
| DELETE | `/faqs/<id>` | Remove um FAQ | ID na URL |

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

- **Modularidade**: Cada responsabilidade está em um módulo próprio, facilitando testes e manutenção.
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

   O prompt deve mostrar `(venv)` indicando que o ambiente está ativo.

2. **Instale as dependências do projeto:**
   ```cmd
   pip install -r requirements.txt
   ```

   Lista completa de dependências (arquivo `requirements.txt`):
   ```
    blinker==1.9.0
    click==8.2.1
    colorama==0.4.6
    oracledb==1.4.1
    Flask==3.1.2
    flask-cors==3.0.10
    itsdangerous==2.2.0
    Jinja2==3.1.6
    MarkupSafe==3.0.2
    python-dotenv==1.1.1
    Werkzeug==3.1.3

   ```

### 2. Configuração do Arquivo .env

Crie um arquivo `.env` na pasta `menu_interativo/` com as seguintes variáveis:

```ini
# Credenciais Oracle
DB_USER=seu_usuario
DB_PASS=sua_senha
DB_URL=oracle.com.br:xxxx/ORCL
# DB_URL segue o formato: hostname:porta/service_name ou usando tnsnames.ora
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

Para facilitar o uso do sistema, os seguintes scripts estão disponíveis na pasta `scripts/` do projeto:

**Windows (batch):**

`scripts/run_menu.bat`:
```batch
@echo off
start cmd.exe /k "chcp 65001 > nul && call venv\Scripts\activate && cd menu_interativo && python main.py"
```

`scripts/run_api.bat`:
```batch
@echo off
start cmd.exe /k "chcp 65001 > nul && call venv\Scripts\activate && cd menu_interativo && python api/faq_api.py"
```

Estes scripts configuram automaticamente a codificação para UTF-8 (para exibir caracteres especiais corretamente) e abrem uma nova janela de terminal para melhor visualização dos resultados.

---

## Contato

| Nome                           | GitHub                                        | LinkedIn                                                                |
| ------------------------------ | --------------------------------------------- | ----------------------------------------------------------------------- |
| Alexander Dennis Isidro Mamani | [alex-isidro](https://github.com/alex-isidro) | [LinkedIn](https://www.linkedin.com/in/alexander-dennis-a3b48824b/)     |
| Kelson Zhang                   | [KelsonZh0](https://github.com/KelsonZh0)     | [LinkedIn](https://www.linkedin.com/in/kelson-zhang-211456323/)         |
| Lucas Rossoni Dieder           | [PxS00](https://github.com/PxS00)             | [LinkedIn](https://www.linkedin.com/in/lucas-rossoni-dieder-32242a353/) |
