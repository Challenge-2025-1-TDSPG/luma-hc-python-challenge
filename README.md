<<<<<<< HEAD
# Sistema de Gerenciamento de FAQs (CRUD) em Memória - Luma
=======
# Sistema FAQ CRUD com Integração Oracle + API REST
>>>>>>> SP4

Sistema completo de gerenciamento de perguntas e respostas frequentes (FAQs) desenvolvido em Python, com integração Oracle Database e API REST para comunicação com front-ends.

<<<<<<< HEAD
- **Linguagem:** Python 3.8+
- **Interface de Terminal:** Colorama 0.4.6
- **Gerenciador de Dependências:** venv + requirements.txt
- **Ambiente:** Windows (recomendado)

---

## Funcionalidades

- CRUD completo de FAQs em memória (adicionar, listar, atualizar, deletar, buscar por ID)
- Dados organizados em listas de objetos (classe `FAQ`) ou dicionários
- Exportação e importação dos dados em formato JSON na pasta `json/memoria/`
- Menus e submenus interativos no terminal
- Validação de dados e tratamento de erros

---

## Menus
=======
## 🚀 Características Principais

- **CRUD Completo** - Criar, ler, atualizar e deletar FAQs
- **Banco Oracle** - Integração nativa com Oracle Database 12c+
- **API REST** - Endpoints Flask para integração com front-ends (Luma)
- **Exportação JSON** - Export de dados para arquivos JSON
- **Interface Colorida** - Menu interativo com Colorama
- **Configuração Segura** - Variáveis de ambiente (.env)

## 🛠️ Tecnologias

- **Python:** 3.8+
- **Banco:** Oracle Database 12c+ (com suporte IDENTITY)
- **API:** Flask 3.1.2 + Flask-CORS 3.0.10
- **Driver:** oracledb 3.3.0 (modo Thin)
- **Interface:** Colorama 0.4.6
- **Config:** python-dotenv 1.1.1

---

## 📋 Estrutura de Menus
>>>>>>> SP4

### Menu Principal

```
<<<<<<< HEAD
--- CRUD FAQ EM MEMÓRIA ---
=======
--- MENU FAQ ---
1. CRUD de FAQs (Banco Oracle)
2. Exportar FAQs do banco para JSON
0/s para sair
```

### Submenu CRUD

```
--- CRUD FAQ (Banco Oracle) ---
>>>>>>> SP4
1. Adicionar FAQ
2. Listar FAQs
3. Atualizar FAQ
4. Deletar FAQ
5. Buscar FAQ por ID
0/v para encerrar o programa
```

---

## 🔌 API REST para Integração Luma

A API Flask fornece endpoints completos para integração com o front-end Luma:

### Endpoints Disponíveis

| Método   | Endpoint         | Descrição              |
| -------- | ---------------- | ---------------------- |
| `GET`    | `/api/faqs`      | Lista todos os FAQs    |
| `GET`    | `/api/faqs/<id>` | Busca FAQ por ID       |
| `POST`   | `/api/faqs`      | Cria novo FAQ          |
| `PUT`    | `/api/faqs/<id>` | Atualiza FAQ existente |
| `DELETE` | `/api/faqs/<id>` | Remove FAQ             |

### Exemplo de Uso da API

```json
// POST /api/faqs
{
  "pergunta": "O que é Python?",
  "resposta": "Linguagem de programação de alto nível",
  "categoria": "Programação",
  "ativo": 1,
  "user_account_id_user": 1
}
```

---
<<<<<<< HEAD

## Exportação e Importação

- Os dados podem ser exportados/importados em formato JSON na pasta `json/memoria/faq_export.json`.
- Não há integração com banco de dados ou API nesta versão (Sprint 3).
=======

## 🗄️ Banco de Dados Oracle

### Esquema da Tabela FAQ

```sql
CREATE TABLE FAQ (
   id_faq NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
   question_faq VARCHAR2(150) NOT NULL,
   answer_faq VARCHAR2(600) NOT NULL,
   active_faq NUMBER(1) NOT NULL,
   faq_updated_at VARCHAR2(50) NOT NULL,
   category_faq VARCHAR2(50) NOT NULL,
   user_account_id_user NUMBER NOT NULL
);

-- Índices e Constraints
CREATE INDEX idx_faq_categ_up ON FAQ(UPPER(category_faq));
ALTER TABLE FAQ ADD CONSTRAINT FAQ_PERGUNTA_UN UNIQUE (question_faq);
ALTER TABLE FAQ ADD CONSTRAINT CK_FAQ_ATIVO CHECK (active_faq IN (0,1));
```

### Configuração de Conexão

- Credenciais seguras via arquivo `.env`
- Conexão transacional com rollback automático
- Driver nativo `oracledb` (modo Thin)
- Suporte a Oracle 12c+ (requer IDENTITY)
>>>>>>> SP4

---

## ⚙️ Instalação e Configuração

<<<<<<< HEAD
- **Simplicidade**: Estrutura plana, fácil de entender e manter.
- **Documentação**: Todas as classes e métodos possuem docstrings explicativas.
- **Validação e Segurança**: Entradas do usuário e operações críticas são validadas e tratadas (centralizadas em `config/settings.py`).
- **Tratamento de Erros**: Uso extensivo de try/except e mensagens padronizadas.
- **Configuração Centralizada**: Variáveis de ambiente, caminhos, mensagens e utilitários em `config/settings.

---

## Configuração e Execução

### 1. Ambiente Virtual e Instalação de Dependências
=======
### 1. Ambiente Virtual
>>>>>>> SP4

```cmd
# Windows
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

<<<<<<< HEAD
### 2. Estrutura de Pastas

```
menu_interativo/
├── main.py              # Ponto de entrada do sistema (menu interativo)
├── models.py            # Classe FAQ (estrutura dos dados)
├── menu_memoria.py      # Lógica do CRUD em memória
├── exportacao.py        # Exportação/importação JSON
├── config/
│   └── settings.py      # Configurações, mensagens e utilitários
├── README.md            # Documentação
└── json/
    └── memoria/
        └── faq_export.json  # Arquivo de exportação/importação dos dados
scripts/
└── run_menu.bat         # Script para executar o menu interativo
=======
### 2. Arquivo de Configuração (.env)

Crie `.env` na raiz do projeto:

```ini
# Credenciais Oracle Database
DB_USER=seu_usuario
DB_PASS=sua_senha
DB_URL=oracle.com.br:xxxx/ORCL
>>>>>>> SP4
```

### 3. Execução

#### Menu Interativo

```cmd
cd menu_interativo
python main.py
```

#### API REST (para integração Luma)

```cmd
cd menu_interativo
python api/faq_api.py
```

<<<<<<< HEAD
- `run_menu.bat` — Executa o menu interativo
=======
#### Scripts Prontos

```cmd
# Menu CRUD
scripts\run_menu.bat

# API REST
scripts\run_api.bat
```
>>>>>>> SP4

---

## 📁 Estrutura do Projeto

```
python-challenge/
├── menu_interativo/
│   ├── main.py              # Ponto de entrada do sistema
│   ├── menu_crud.py         # Menu principal e navegação
│   ├── banco.py             # Operações CRUD Oracle
│   ├── models.py            # Classe FAQ
│   ├── exportacao.py        # Exportação JSON
│   ├── api/
│   │   └── faq_api.py       # API REST Flask
│   └── config/
│       └── settings.py      # Configurações globais
├── scripts/
│   ├── run_menu.bat         # Script menu interativo
│   └── run_api.bat          # Script API REST
├── json/banco/              # Arquivos JSON exportados
├── requirements.txt         # Dependências Python
└── README.md               # Documentação
```

## 🔄 Integração com Luma

O sistema fornece uma **API REST completa** que permite ao front-end Luma:

1. **Consultar FAQs** - `GET /api/faqs`
2. **Criar novos FAQs** - `POST /api/faqs`
3. **Atualizar FAQs** - `PUT /api/faqs/<id>`
4. **Deletar FAQs** - `DELETE /api/faqs/<id>`

### CORS Habilitado

- Permite requisições do front-end Luma
- Headers configurados para desenvolvimento
- Suporte a métodos HTTP completos

### Sincronização Bidirecional

- ✅ Alterações no CRUD → Refletem no Luma via API
- ✅ Alterações no Luma → Refletem no banco Oracle
- ✅ Dados sempre sincronizados entre sistemas

---

## 🔧 Características Técnicas

### Segurança e Validação

- Validação de entrada de dados
- Tratamento de exceções robusto
- Transações seguras com rollback
- Credenciais via variáveis de ambiente

### Performance

- Conexões otimizadas com Oracle
- Queries indexadas por categoria
- API REST leve e responsiva
- Estrutura modular escalável

### Qualidade de Código

- Docstrings em todas as funções
- Código limpo sem dead code
- Padrões de nomenclatura consistentes
- Separação clara de responsabilidades

---

## 👥 Equipe de Desenvolvimento

| Nome                           | RM     | GitHub                                        | LinkedIn                                                                |
| ------------------------------ | ------ | --------------------------------------------- | ----------------------------------------------------------------------- |
| Alexander Dennis Isidro Mamani | 565554 | [alex-isidro](https://github.com/alex-isidro) | [LinkedIn](https://www.linkedin.com/in/alexander-dennis-a3b48824b/)     |
| Kelson Zhang                   | 563748 | [KelsonZh0](https://github.com/KelsonZh0)     | [LinkedIn](https://www.linkedin.com/in/kelson-zhang-211456323/)         |
| Lucas Rossoni Dieder           | 563770 | [PxS00](https://github.com/PxS00)             | [LinkedIn](https://www.linkedin.com/in/lucas-rossoni-dieder-32242a353/) |

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
