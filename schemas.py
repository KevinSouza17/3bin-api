# schemas.py
from pydantic import BaseModel, ConfigDict



class ProdutoBase(BaseModel):
    nome: str
    preco: float
    quantidade: int


class ProdutoCreate(ProdutoBase):
    pass


class ProdutoResponse(ProdutoBase):
    id: int

    model_config = ConfigDict(from_attributes=True)



# class LivroBase(BaseModel):
#     titulo: str
#     autor: str
#     ano_publicacao: int
#     preco: float


# class LivroCreate(LivroBase):
#     pass


# class LivroResponse(LivroBase):
#     id: int

#     model_config = ConfigDict(from_attributes=True)