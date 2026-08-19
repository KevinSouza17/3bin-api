# models.py
from sqlalchemy import Column, Integer, String, Float
from database import Base


class ProdutoDB(Base):
    __tablename__ = 'produtos'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    preco = Column(Float, nullable=False)
    quantidade = Column(Integer, nullable=False)


# class LivroDB(Base):
#     __tablename__ = 'livros'

#     id = Column(Integer, primary_key=True, index=True)
#     titulo = Column(String(150), nullable=False)
#     autor = Column(String(100), nullable=False)
#     ano_publicacao = Column(Integer, nullable=False)
#     preco = Column(Float, nullable=False)