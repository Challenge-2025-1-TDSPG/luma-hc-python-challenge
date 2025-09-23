# Sistema de Gerenciamento de FAQs (CRUD) em Python

## Tecnologias e Requisitos

- **Linguagem:** Python 3.8+
- **Banco de Dados:** Oracle Database 12c+ (requer suporte a `IDENTITY`)
- **Driver Oracle:** oracledb 1.4.1 (modo Thin)
- **API REST:** Flask 3.1.2
- **Interface de Terminal:** Colorama 0.4.6
- **Gerenciador de Dependências:** venv + requirements.txt
- **Ambiente:** Windows (recomendado)
- **Acesso:** Instância Oracle com privilégios de criação de tabelas

> **Atenção:** O sistema utiliza o recurso **IDENTITY** do Oracle, disponível apenas a partir do Oracle 12c (12.1) ou superior. 3.

---

## Menus e Submenus

### Menu Principal

```
--- MENU FAQ ---
1. CRUD de FAQs (Banco Oracle)
2. CRUD de FAQs em memória
3. Exportar FAQs do banco para JSON
0/s para sair
```

### Submenu CRUD (Banco Oracle)

```
--- CRUD FAQ (Banco Oracle) ---
1. Adicionar FAQ
2. Atualizar FAQ
3. Deletar FAQ
4. Listar FAQs
0. Voltar ao menu principal
```

### Submenu CRUD (Memória)

```
--- CRUD FAQ em Memória ---
1. Adicionar FAQ
2. Listar FAQs
3. Atualizar FAQ
4. Deletar FAQ
5. Buscar FAQ por ID
0/v para voltar
```

### Exportação

- Exporta todos os FAQs do banco Oracle para um arquivo JSON em `json/banco/faq_export.json`.

## Integração com Oracle

- O acesso ao banco é feito exclusivamente via Oracle, utilizando o driver `oracledb`.
- As credenciais e parâmetros de conexão são lidos do arquivo `.env` (nunca hardcoded), via `config/settings.py`.
- Todas as operações CRUD são transacionais, seguras e validadas.

### Esquema do Banco de Dados (DDL)

```sql
CREATE TABLE FAQ (
   id_faq NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
   question_faq VARCHAR2(150) NOT NULL,
   answer_faq VARCHAR2(600) NOT NULL,
   active_faq NUMBER(1) NOT NULL,
   faq_updated_at VARCHAR2(50) NOT NULL,
   category_faq VARCHAR2(50) NOT NULL,
   user_adm_id_user_adm NUMBER NOT NULL
);
CREATE INDEX idx_faq_categ_up ON FAQ(UPPER(category_faq));
ALTER TABLE FAQ ADD CONSTRAINT FAQ_PERGUNTA_UN UNIQUE (question_faq);
ALTER TABLE FAQ ADD CONSTRAINT CK_FAQ_ATIVO CHECK (active_faq IN (0,1));
```

---

## Exportação e Integração

- Os dados podem ser exportados para JSON na pasta `json/banco/` (banco) e `json/memoria/` (memória).
- A API RESTful permite integração total com front-ends, sistemas legados e automações.

---

## Boas Práticas e Manutenção

- **Simplicidade**: Estrutura plana, fácil de entender e manter.
- **Documentação**: Todas as classes e métodos possuem docstrings explicativas.
- **Validação e Segurança**: Entradas do usuário e operações críticas são validadas e tratadas (centralizadas em `config/settings.py`).
- **Tratamento de Erros**: Uso extensivo de try/except, mensagens padronizadas e rollback em operações críticas.
- **Configuração Centralizada**: Variáveis de ambiente, caminhos, mensagens e utilitários em `config/settings.py`.
- **Escalabilidade**: Estrutura pronta para expansão, seja para novos tipos de dados, integrações ou regras de negócio.

---

## Configuração e Execução

### 1. Ambiente Virtual e Instalação de Dependências

```cmd
# Windows
python -m venv venv
venv\Scripts\activate
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

#### Menu Interativo

```cmd
cd menu_interativo
python main.py
```

#### Scripts Auxiliares

Scripts prontos para execução rápida estão disponíveis em `scripts/`:

- `run_menu.bat` — Executa o menu interativo
- `run_api.bat` — Executa a API RESTful

---

## Contato

| Nome                           | RM     | GitHub                                        | LinkedIn                                                                |
| ------------------------------ | ------ | --------------------------------------------- | ----------------------------------------------------------------------- |
| Alexander Dennis Isidro Mamani | 565554 | [alex-isidro](https://github.com/alex-isidro) | [LinkedIn](https://www.linkedin.com/in/alexander-dennis-a3b48824b/)     |
| Kelson Zhang                   | 563748 | [KelsonZh0](https://github.com/KelsonZh0)     | [LinkedIn](https://www.linkedin.com/in/kelson-zhang-211456323/)         |
| Lucas Rossoni Dieder           | 563770 | [PxS00](https://github.com/PxS00)             | [LinkedIn](https://www.linkedin.com/in/lucas-rossoni-dieder-32242a353/) |
