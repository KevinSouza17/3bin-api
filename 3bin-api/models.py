from sqlalchemy import Boolean, Column, Integer, String

from database import Base


class Livro(Base):
    __tablename__ = "livros"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(150), nullable=False)
    autor = Column(String(120), nullable=False)
    ano_publicacao = Column(Integer, nullable=False)
    disponivel = Column(Boolean, nullable=False, default=True)


# Nome alternativo mantido para compatibilidade com versões anteriores do exercício.
LivroDB = Livro
