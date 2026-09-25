from sqlalchemy import Boolean, Column, Float, Integer, String

from database import Base


class Livro(Base):
    __tablename__ = "livros"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(150), nullable=False)
    autor = Column(String(120), nullable=False)
    ano_publicacao = Column(Integer, nullable=False)
    disponivel = Column(Boolean, nullable=False, default=True)


# Alias mantido para compatibilidade com o código/testes da versão anterior.
LivroDB = Livro
