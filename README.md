# Sistema de Gerenciamento de FAQs (CRUD) em Memória - Luma

## Tecnologias e Requisitos

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

### Menu Principal

```
--- MENU FAQ ---
1. CRUD de FAQs em memória
2. Exportar/Importar FAQs em memória (JSON)
0/s para sair
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

---

## Exportação e Importação

- Os dados podem ser exportados/importados em formato JSON na pasta `json/memoria/faq_export.json`.
- Não há integração com banco de dados ou API nesta versão (Sprint 3).

---

## Boas Práticas e Manutenção

- **Simplicidade**: Estrutura plana, fácil de entender e manter.
- **Documentação**: Todas as classes e métodos possuem docstrings explicativas.
- **Validação e Segurança**: Entradas do usuário e operações críticas são validadas e tratadas (centralizadas em `config/settings.py`).
- **Tratamento de Erros**: Uso extensivo de try/except e mensagens padronizadas.
- **Configuração Centralizada**: Variáveis de ambiente, caminhos, mensagens e utilitários em `config/settings.

---

## Configuração e Execução

### 1. Ambiente Virtual e Instalação de Dependências

```cmd
# Windows
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

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

---

## Contato

| Nome                           | RM     | GitHub                                        | LinkedIn                                                                |
| ------------------------------ | ------ | --------------------------------------------- | ----------------------------------------------------------------------- |
| Alexander Dennis Isidro Mamani | 565554 | [alex-isidro](https://github.com/alex-isidro) | [LinkedIn](https://www.linkedin.com/in/alexander-dennis-a3b48824b/)     |
| Kelson Zhang                   | 563748 | [KelsonZh0](https://github.com/KelsonZh0)     | [LinkedIn](https://www.linkedin.com/in/kelson-zhang-211456323/)         |
| Lucas Rossoni Dieder           | 563770 | [PxS00](https://github.com/PxS00)             | [LinkedIn](https://www.linkedin.com/in/lucas-rossoni-dieder-32242a353/) |
