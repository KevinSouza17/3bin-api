from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from main import app, get_db
from models import ProdutoDB

client = TestClient(app)


def test_listar_produtos_com_mock():
    db_mock = MagicMock()
    db_mock.query.return_value.all.return_value = [
        ProdutoDB(id=1, nome='Teclado', preco=89.90, quantidade=15)
    ]
    app.dependency_overrides[get_db] = lambda: db_mock

    resposta = client.get('/produtos')

    assert resposta.status_code == 200
    assert resposta.json()[0]['nome'] == 'Teclado'

    app.dependency_overrides.clear()


def test_criar_produto_com_mock():
    db_mock = MagicMock()

    def simular_refresh(produto):
        produto.id = 1  # simula o banco atribuindo um id ao registro

    db_mock.refresh.side_effect = simular_refresh
    app.dependency_overrides[get_db] = lambda: db_mock

    novo_produto = {'nome': 'Monitor', 'preco': 799.90, 'quantidade': 5}
    resposta = client.post('/produtos', json=novo_produto)

    assert resposta.status_code == 201
    db_mock.add.assert_called_once()
    db_mock.commit.assert_called_once()

    app.dependency_overrides.clear()

def test_listar_produtos_vazio_com_mock():
    db_mock = MagicMock()
    db_mock.query.return_value.all.return_value = []
    app.dependency_overrides[get_db] = lambda: db_mock

    resposta = client.get('/produtos')

    assert resposta.status_code == 200
    assert resposta.json() == []

    app.dependency_overrides.clear()

def test_criar_produto_invalido_com_mock():
    db_mock = MagicMock()
    app.dependency_overrides[get_db] = lambda: db_mock

    produto_invalido = {'nome': '', 'preco': -10, 'quantidade': -5}
    resposta = client.post('/produtos', json=produto_invalido)

    assert resposta.status_code == 422  # Unprocessable Entity

    app.dependency_overrides.clear()

def test_criar_produto_sem_nome_com_mock():
    db_mock = MagicMock()
    app.dependency_overrides[get_db] = lambda: db_mock

    produto_sem_nome = {'preco': 100, 'quantidade': 10}
    resposta = client.post('/produtos', json=produto_sem_nome)

    assert resposta.status_code == 422  # Unprocessable Entity

    app.dependency_overrides.clear()

def test_criar_produto_sem_preco_com_mock():
    db_mock = MagicMock()
    app.dependency_overrides[get_db] = lambda: db_mock

    produto_sem_preco = {'nome': 'Mouse', 'quantidade': 10}
    resposta = client.post('/produtos', json=produto_sem_preco)

    assert resposta.status_code == 422  # Unprocessable Entity

    app.dependency_overrides.clear()

def test_criar_produto_sem_quantidade_com_mock():
    db_mock = MagicMock()
    app.dependency_overrides[get_db] = lambda: db_mock

    produto_sem_quantidade = {'nome': 'Mouse', 'preco': 50.0}
    resposta = client.post('/produtos', json=produto_sem_quantidade)

    assert resposta.status_code == 422  # Unprocessable Entity

    app.dependency_overrides.clear()

def test_criar_produto_com_quantidade_negativa_com_mock():
    db_mock = MagicMock()
    app.dependency_overrides[get_db] = lambda: db_mock

    produto_quantidade_negativa = {'nome': 'Mouse', 'preco': 50.0, 'quantidade': -5}
    resposta = client.post('/produtos', json=produto_quantidade_negativa)

    assert resposta.status_code == 422  # Unprocessable Entity

    app.dependency_overrides.clear()

def test_criar_produto_com_preco_negativo_com_mock():
    db_mock = MagicMock()
    app.dependency_overrides[get_db] = lambda: db_mock

    produto_preco_negativo = {'nome': 'Mouse', 'preco': -50.0, 'quantidade': 5}
    resposta = client.post('/produtos', json=produto_preco_negativo)

    assert resposta.status_code == 422  # Unprocessable Entity

    app.dependency_overrides.clear()

def test_criar_produto_com_nome_vazio_com_mock():
    db_mock = MagicMock()
    app.dependency_overrides[get_db] = lambda: db_mock

    produto_nome_vazio = {'nome': '', 'preco': 50.0, 'quantidade': 5}
    resposta = client.post('/produtos', json=produto_nome_vazio)

    assert resposta.status_code == 422  # Unprocessable Entity

    app.dependency_overrides.clear()

def test_listar_produtos_com_erro_no_banco_com_mock():
    db_mock = MagicMock()
    db_mock.query.side_effect = Exception("Erro no banco de dados")
    app.dependency_overrides[get_db] = lambda: db_mock

    resposta = client.get('/produtos')

    assert resposta.status_code == 500  # Internal Server Error

    app.dependency_overrides.clear()

def test_criar_produto_com_erro_no_banco_com_mock():
    db_mock = MagicMock()
    db_mock.add.side_effect = Exception("Erro ao adicionar produto")
    app.dependency_overrides[get_db] = lambda: db_mock

    novo_produto = {'nome': 'Monitor', 'preco': 799.90, 'quantidade': 5}
    resposta = client.post('/produtos', json=novo_produto)

    assert resposta.status_code == 500  # Internal Server Error

    app.dependency_overrides.clear()

def test_remover_produto_com_mock():
    db_mock = MagicMock()
    produto_existente = ProdutoDB(id=1, nome='Teclado', preco=89.90, quantidade=15)
    db_mock.query.return_value.filter.return_value.first.return_value = produto_existente
    app.dependency_overrides[get_db] = lambda: db_mock

    resposta = client.delete('/produtos/1')

    assert resposta.status_code == 200
    db_mock.delete.assert_called_once_with(produto_existente)
    db_mock.commit.assert_called_once()

    app.dependency_overrides.clear()

def test_remover_produto_inexistente_com_mock():
    db_mock = MagicMock()
    db_mock.query.return_value.filter.return_value.first.return_value = None
    app.dependency_overrides[get_db] = lambda: db_mock

    resposta = client.delete('/produtos/999')

    assert resposta.status_code == 404  # Not Found

    app.dependency_overrides.clear()

def test_remover_produto_com_erro_no_banco_com_mock():
    db_mock = MagicMock()
    produto_existente = ProdutoDB(id=1, nome='Teclado', preco=89.90, quantidade=15)
    db_mock.query.return_value.filter.return_value.first.return_value = produto_existente
    db_mock.delete.side_effect = Exception("Erro ao remover produto")
    app.dependency_overrides[get_db] = lambda: db_mock

    resposta = client.delete('/produtos/1')

    assert resposta.status_code == 500  # Internal Server Error

    app.dependency_overrides.clear()

def test_atualizar_produto_com_mock():
    db_mock = MagicMock()
    produto_existente = ProdutoDB(id=1, nome='Teclado', preco=89.90, quantidade=15)
    db_mock.query.return_value.filter.return_value.first.return_value = produto_existente
    app.dependency_overrides[get_db] = lambda: db_mock

    dados_atualizados = {'nome': 'Teclado Mecânico', 'preco': 99.90, 'quantidade': 10}
    resposta = client.put('/produtos/1', json=dados_atualizados)

    assert resposta.status_code == 200
    assert produto_existente.nome == 'Teclado Mecânico'
    assert produto_existente.preco == 99.90
    assert produto_existente.quantidade == 10
    db_mock.commit.assert_called_once()

    app.dependency_overrides.clear()

def test_atualizar_produto_inexistente_com_mock():
    db_mock = MagicMock()
    db_mock.query.return_value.filter.return_value.first.return_value = None
    app.dependency_overrides[get_db] = lambda: db_mock

    dados_atualizados = {'nome': 'Teclado Mecânico', 'preco': 99.90, 'quantidade': 10}
    resposta = client.put('/produtos/999', json=dados_atualizados)

    assert resposta.status_code == 404  # Not Found

    app.dependency_overrides.clear()
