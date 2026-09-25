# API de Livros

API REST didática desenvolvida com **FastAPI**, **SQLAlchemy** e **MySQL** para gerenciamento de uma biblioteca.

## Funcionalidades

A API possui as cinco operações do CRUD de livros:

| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/livros` | Lista todos os livros |
| `POST` | `/livros` | Cadastra um livro |
| `GET` | `/livros/{id_livro}` | Consulta um livro |
| `PUT` | `/livros/{id_livro}` | Atualiza um livro |
| `DELETE` | `/livros/{id_livro}` | Exclui um livro |

O corpo usado no cadastro e na atualização é:

```json
{
  "titulo": "O Hobbit",
  "autor": "J. R. R. Tolkien",
  "ano_publicacao": 1937,
  "disponivel": true
}
```

## Execução

Instale as dependências:

```bash
pip install -r requirements.txt
```

Configure o banco MySQL no arquivo `.env`:

```dotenv
DB_USER=root
DB_PASSWORD=sua_senha
DB_HOST=localhost
DB_PORT=3306
DB_NAME=biblioteca_db
```

Inicie a API:

```bash
uvicorn app.main:app --reload
```

A documentação Swagger estará disponível em `http://127.0.0.1:8000/docs`.

Para executar o frontend:

```bash
python -m http.server 5500 --directory frontend
```

Acesse `http://127.0.0.1:5500`.

## Testes

Execute:

```bash
pytest -q
```

O frontend consome a API e permite listar, cadastrar, editar e excluir livros.
