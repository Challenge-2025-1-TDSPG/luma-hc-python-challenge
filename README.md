# Sistema FAQ Python POO — Guia de Estrutura e Evolução

## Contexto Atual

Você está desenvolvendo um sistema de gerenciamento de FAQ (Frequently Asked Questions) em Python, utilizando Programação Orientada a Objetos (POO), com separação em pastas e módulos. O sistema já possui:

- **Classe FAQ** (`models.py`): representa cada item do FAQ.
- **Classe FaqDB** (`db.py`): gerencia o acesso ao banco de dados (atualmente SQLite, mas pode ser Oracle).
- **Menu interativo** (`menu.py`): permite ao usuário realizar operações CRUD, exportar dados e consumir uma API externa.
- **Consumo de API externa** (`api.py`): atualmente busca curiosidades, mas pode ser adaptado para algo mais útil.
- **Exportação para JSON**: salva os dados do FAQ em um arquivo na pasta `data/`.
- **Estrutura de pastas**:
    ```
    menu_interativo/
        main.py
        data/
        faq/
            __init__.py
            api.py
            db.py
            menu.py
            models.py
    ```

### Exemplo de Classe FAQ

```python
# models.py
class FAQ:
    """
    Classe que representa um item de FAQ (pergunta e resposta).
    """
    def __init__(self, id, pergunta, resposta, ativo, atualizado_em, pasta):
        self.id = id
        self.pergunta = pergunta
        self.resposta = resposta
        self.ativo = ativo
        self.atualizado_em = atualizado_em
        self.pasta = pasta

    def __str__(self):
        return (
            f'ID: {self.id}\nPergunta: {self.pergunta}\nResposta: {self.resposta}\n'
            f'Ativo: {self.ativo}\nAtualizado em: {self.atualizado_em}\nPasta: {self.pasta}'
        )
```

### Exemplo de Classe de Banco

```python
# db.py
import sqlite3
from datetime import datetime
from .models import FAQ

class FaqDB:
    """
    Classe responsável por gerenciar o banco de dados dos itens de FAQ.
    """
    def __init__(self, db_name='faq_perguntas.db'):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        # Criação da tabela (adapte para Oracle se necessário)
        ...

    def adicionar(self, pergunta, resposta, ativo, pasta):
        # Adiciona um novo FAQ
        ...

    def listar(self, pasta=None):
        # Lista FAQs, opcionalmente filtrando por pasta
        ...

    def atualizar(self, id, pergunta, resposta, ativo, pasta):
        # Atualiza um FAQ existente
        ...

    def deletar(self, id):
        # Remove um FAQ pelo ID
        ...
```

### Exemplo de Menu

```python
# menu.py
class Menu:
    """
    Classe responsável pelo menu interativo do sistema FAQ.
    """
    def menu_principal(self):
        # Exibe opções: CRUD, exportar JSON, consumir API, sair
        ...

    def menu_crud(self):
        # Submenu para inserir, alterar, excluir, consultar FAQs
        ...
```

### Exemplo de Consumo de API

```python
# api.py
import requests

class CuriosidadeAPI:
    """
    Classe para consumir uma API pública e retornar uma curiosidade.
    """
    @staticmethod
    def buscar_curiosidade():
        url = 'https://api.chucknorris.io/jokes/random'
        try:
            resposta = requests.get(url, timeout=5)
            if resposta.status_code == 200:
                dados = resposta.json()
                return dados.get('value', 'Curiosidade não encontrada.')
            else:
                return f'Erro ao acessar a API: {resposta.status_code}'
        except Exception as e:
            return f'Erro ao acessar a API: {e}'
```

---

## Como Podemos Evoluir

### 1. Trocar SQLite por Oracle

- Instale o driver `cx_Oracle`.
- Altere a classe `FaqDB` para conectar ao Oracle.
- Adapte comandos SQL (principalmente autoincremento, que em Oracle é feito com SEQUENCE + TRIGGER).

### 2. Criar uma API RESTful própria

- Use Flask ou FastAPI para criar endpoints como `/faqs`, `/faqs/<id>`, etc.
- Permita que o front-end consuma e altere FAQs via HTTP.
- Exemplo de endpoint Flask:
    ```python
    @app.route('/faqs', methods=['GET'])
    def listar_faqs():
        faqs = db.listar()
        return jsonify([faq.__dict__ for faq in faqs])
    ```

### 3. Tornar o consumo de API externa mais útil

- Use uma API de dicionário, tradução, perguntas técnicas, etc.
- Ou crie sua própria API para integração com outros sistemas.

### 4. Exportação e Integração

- Continue exportando para JSON na pasta `data/`.
- Garanta que o front-end consuma a API RESTful para refletir as alterações em tempo real.

### 5. Organização e Boas Práticas

- Separe cada responsabilidade em um arquivo/módulo.
- Use docstrings em todas as classes e métodos.
- Implemente tratamento de erros e validação de dados em todas as operações.

---

## Exemplo de Prompt para Evolução

> Você está desenvolvendo um sistema de FAQ em Python, orientado a objetos, com separação em pastas e módulos. O sistema deve:
> - Gerenciar FAQs (pergunta, resposta, ativo, atualizado_em, pasta/categoria) via CRUD.
> - Utilizar banco de dados Oracle (ou SQLite para testes).
> - Permitir exportação dos dados para JSON.
> - Consumir uma API externa útil (dicionário, tradução, etc) ou expor sua própria API RESTful para integração com front-end.
> - Ser organizado, com docstrings e tratamento de erros.
> - Permitir integração total com front-end via API RESTful.
> 
> Exemplo de estrutura de pastas:
> ```
> menu_interativo/
>     main.py
>     data/
>     faq/
>         __init__.py
>         api.py
>         db.py
>         menu.py
>         models.py
>         faq_api.py  # (opcional, para API RESTful)
> ```
> 
> Implemente as classes e métodos necessários, seguindo boas práticas de POO, validação, tratamento de erros e documentação.

---

"""
Alterações planejadas para o sistema FAQ:

1. Criação de uma API própria (RESTful):
    - Implementar endpoints usando Flask ou FastAPI em um novo módulo (ex: faq_api.py).
    - Endpoints para listar, adicionar, atualizar e remover FAQs.
    - Permitir integração direta com o front-end via requisições HTTP (GET, POST, PUT, DELETE).
    - Retornar e receber dados em formato JSON.

2. Ligação com banco de dados Oracle:
    - Adaptar a classe FaqDB para utilizar o driver cx_Oracle ao invés de sqlite3.
    - Ajustar comandos SQL para sintaxe Oracle (uso de SEQUENCE para autoincremento de IDs).
    - Garantir que todas as operações CRUD funcionem tanto em SQLite (para testes) quanto em Oracle (produção).
    - Manter a interface da classe FaqDB para facilitar a integração com a API e o menu.

Essas alterações vão permitir:
    - Integração total entre back-end e front-end via API.
    - Persistência dos dados em banco Oracle, atendendo requisitos corporativos.
    - Facilidade de manutenção e escalabilidade do sistema.
"""