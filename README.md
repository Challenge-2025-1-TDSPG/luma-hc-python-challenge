# Sistema FAQ Corporativo em Python

## Visão Geral Profissional

Este projeto implementa um sistema de gerenciamento de FAQ (Frequently Asked Questions) corporativo, desenvolvido em Python com foco em modularidade, escalabilidade e integração corporativa. O sistema utiliza Programação Orientada a Objetos (POO), separação clara de responsabilidades e integração nativa com banco de dados Oracle, além de oferecer API RESTful e exportação de dados.

---

- **CRUD Completo de FAQs**: Permite criar, listar, atualizar e remover perguntas e respostas, com categorização e controle de status (ativo/inativo).
- **Exportação para JSON**: Exporta todos os dados do FAQ para um arquivo JSON, facilitando integrações e backups.
- **Operações em Memória**: Permite visualizar e manipular perguntas em memória usando lista de dicionários (estrutura recomendada para CRUD em Python), ideal para testes e simulações.
- **API RESTful**: Disponibiliza endpoints para integração com front-ends e outros sistemas corporativos (implementação em `faq_api.py`).
- **Integração Oracle**: Toda a persistência é feita via Oracle Database, utilizando o driver `cx_Oracle` e boas práticas de segurança (credenciais via `.env`).
- **Estrutura Modular**: Cada grupo de operações (CRUD, exportação, memória) está em módulos próprios, facilitando manutenção e evolução.
- **Validação Robusta**: Todas as entradas do usuário e operações críticas possuem validação e tratamento de erros.

---

## Estrutura de Pastas

```
menu_interativo/
    main.py                # Ponto de entrada do sistema
    data/                  # Exportações e arquivos auxiliares
    faq/
        __init__.py
        db.py              # Camada de acesso Oracle
        models.py          # Modelos de dados (FAQ)
        menu.py            # Menu principal (orquestrador)
        crud/
            __init__.py
            menu_crud.py   # Orquestrador do menu CRUD
            adicionar.py   # Adiciona FAQ
            listar.py      # Lista FAQs
            atualizar.py   # Atualiza FAQ
            deletar.py     # Deleta FAQ
            buscar.py      # Busca FAQ por ID
            categorias.py  # Lista categorias
        exportacao/
            __init__.py
            menu_exportacao.py # Exportação para JSON
        memoria/
            __init__.py
            menu_memoria.py    # Operações em memória
        faq_api.py         # API RESTful (Flask)
        api.py             # Consumo de APIs externas (opcional)
    # Todas as operações em memória agora estão em memoria/crud_memoria/ (adicionar, listar, atualizar, deletar, buscar)
```

---

## Fluxo de Funcionamento

1. **Inicialização**: O sistema carrega as configurações Oracle do arquivo `.env` e valida a conexão.
2. **Menu Interativo**: O usuário navega pelo menu principal, podendo acessar:
   - CRUD de FAQs (cada operação em um arquivo próprio em `crud/`)
   - Listagem e manipulação de FAQs em memória (via `memoria/menu_memoria.py` e módulos de operações em `memoria/crud_memoria/`)
   - Exportação para JSON (via `exportacao/menu_exportacao.py`)
3. **API RESTful**: Opcionalmente, o sistema pode ser executado como API para integração com front-ends modernos.

---

## Integração com Oracle

- O acesso ao banco é feito exclusivamente via Oracle, utilizando o driver `cx_Oracle`.
- As credenciais e parâmetros de conexão são lidos do arquivo `.env`, nunca hardcoded.
- Todas as operações CRUD são transacionais e seguras.

---

## Exportação e Integração

- Os dados podem ser exportados para JSON na pasta `data/faq_export.json`.
- A API RESTful permite integração total com front-ends, sistemas legados e automações.

---

## Boas Práticas e Manutenção

- **Modularidade**: Cada responsabilidade está em um módulo próprio, facilitando testes e manutenção.
- **Documentação**: Todas as classes e métodos possuem docstrings explicativas.
- **Validação e Segurança**: Entradas do usuário e operações críticas são validadas e tratadas.
- **Escalabilidade**: Estrutura pronta para expansão, seja para novos tipos de dados, integrações ou regras de negócio.

---

## Como Executar

## Ambiente Virtual e Instalação de Dependências

1. **Crie e ative o ambiente virtual (venv):**

   ```cmd
   python -m venv venv
   venv\Scripts\activate
   ```

   O prompt deve mostrar `(venv)` indicando que o ambiente está ativo.

2. **Instale as dependências do projeto:**
   ```cmd
   pip install -r requirements.txt
   ```

## Instalação do Oracle Instant Client (Obrigatório para conexão Oracle)

O driver cx_Oracle exige a biblioteca nativa Oracle Instant Client instalada na máquina.

1. Baixe o Oracle Instant Client 64-bit para Windows:

   - [Download Oracle Instant Client](https://www.oracle.com/database/technologies/instant-client/winx64-64-downloads.html)
   - Baixe o pacote "Basic" (ZIP).

2. Extraia o ZIP em uma pasta, por exemplo: `C:\oracle\instantclient_21_13`

3. Adicione o caminho dessa pasta à variável de ambiente `PATH` do Windows:

   - Pesquise por "variáveis de ambiente" no menu iniciar.
   - Edite a variável `PATH` e adicione o caminho da pasta do Instant Client.

4. Feche e reabra o terminal/VS Code para reconhecer a alteração.

5. Execute o sistema normalmente.

> **Atenção:** Todos os usuários do projeto precisam realizar este procedimento para que a conexão Oracle funcione corretamente.

---

## Como Executar

1. Configure o arquivo `.env` com as credenciais Oracle.
2. Ative o ambiente virtual e instale as dependências conforme instruções acima.
3. Execute `main.py` para usar o menu interativo.
4. (Opcional) Execute `faq_api.py` para expor a API RESTful.

---

## Contato e Suporte

Para dúvidas, sugestões ou suporte corporativo, entre em contato com o time de desenvolvimento responsável pelo projeto.
