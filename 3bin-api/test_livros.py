from unittest.mock import MagicMock

from fastapi.testclient import TestClient

from main import app, get_db
from models import Livro

client = TestClient(app)


def usar_banco_mockado(db_mock):
    app.dependency_overrides[get_db] = lambda: db_mock


def limpar_banco_mockado():
    app.dependency_overrides.clear()


def test_criar_livro_com_mock():
    db_mock = MagicMock()

    def simular_refresh(livro):
        livro.id = 1

    db_mock.refresh.side_effect = simular_refresh
    usar_banco_mockado(db_mock)
    resposta = client.post("/livros", json={
        "titulo": "O Hobbit",
        "autor": "J. R. R. Tolkien",
        "ano_publicacao": 1937,
        "disponivel": True,
    })
    assert resposta.status_code == 201
    assert resposta.json()["titulo"] == "O Hobbit"
    db_mock.add.assert_called_once()
    db_mock.commit.assert_called_once()
    limpar_banco_mockado()


def test_listar_livros_com_mock():
    db_mock = MagicMock()
    db_mock.query.return_value.all.return_value = [
        Livro(id=1, titulo="O Hobbit", autor="J. R. R. Tolkien", ano_publicacao=1937, disponivel=True)
    ]
    usar_banco_mockado(db_mock)
    resposta = client.get("/livros")
    assert resposta.status_code == 200
    assert resposta.json()[0]["titulo"] == "O Hobbit"
    limpar_banco_mockado()


def test_atualizar_livro_com_mock():
    db_mock = MagicMock()
    livro = Livro(id=1, titulo="O Hobbit", autor="Tolkien", ano_publicacao=1937, disponivel=True)
    db_mock.query.return_value.filter.return_value.first.return_value = livro
    usar_banco_mockado(db_mock)
    resposta = client.put("/livros/1", json={
        "titulo": "O Hobbit - Edição revisada",
        "autor": "J. R. R. Tolkien",
        "ano_publicacao": 1937,
        "disponivel": False,
    })
    assert resposta.status_code == 200
    assert livro.disponivel is False
    assert livro.titulo == "O Hobbit - Edição revisada"
    db_mock.commit.assert_called_once()
    limpar_banco_mockado()


def test_excluir_livro_com_mock():
    db_mock = MagicMock()
    livro = Livro(id=1, titulo="O Hobbit", autor="Tolkien", ano_publicacao=1937, disponivel=True)
    db_mock.query.return_value.filter.return_value.first.return_value = livro
    usar_banco_mockado(db_mock)
    resposta = client.delete("/livros/1")
    assert resposta.status_code == 200
    assert resposta.json()["mensagem"] == "Livro excluído com sucesso"
    db_mock.delete.assert_called_once_with(livro)
    db_mock.commit.assert_called_once()
    limpar_banco_mockado()


def test_rotas_de_livro_inexistente_retorna_404():
    db_mock = MagicMock()
    db_mock.query.return_value.filter.return_value.first.return_value = None
    usar_banco_mockado(db_mock)
    dados = {"titulo": "Livro", "autor": "Autor", "ano_publicacao": 2020, "disponivel": True}
    assert client.get("/livros/999").status_code == 404
    assert client.put("/livros/999", json=dados).status_code == 404
    assert client.delete("/livros/999").status_code == 404
    limpar_banco_mockado()


def test_validacao_de_livro_retorna_422():
    dados = {"titulo": "", "autor": "Autor", "ano_publicacao": 2101, "disponivel": True}
    resposta = client.post("/livros", json=dados)
    assert resposta.status_code == 422
