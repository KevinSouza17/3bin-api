"""Configuração de persistência da API.

Em produção/aula, defina DATABASE_URL ou as variáveis DB_* do guia para usar
MySQL. Sem essas variáveis, a aplicação usa um SQLite local para facilitar
execução e testes sem um servidor de banco instalado.
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()


def _database_url() -> str:
    explicit_url = os.getenv("DATABASE_URL")
    if explicit_url:
        return explicit_url

    db_host = os.getenv("DB_HOST")
    if db_host:
        user = os.getenv("DB_USER", "root")
        password = os.getenv("DB_PASSWORD", "")
        port = os.getenv("DB_PORT", "3306")
        name = os.getenv("DB_NAME", "biblioteca_db")
        return f"mysql+pymysql://{user}:{password}@{db_host}:{port}/{name}"

    sqlite_path = Path(__file__).resolve().parent / "biblioteca.db"
    return f"sqlite:///{sqlite_path}"


DATABASE_URL = _database_url()
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Abre uma sessão por requisição e garante seu fechamento."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Nomes didáticos usados no roteiro da atividade.
BaseBanco = Base
mecanismo_banco = engine
obter_sessao_banco = get_db
