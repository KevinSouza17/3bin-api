from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import Livro, ProdutoDB
from schemas import LivroCriacao, LivroResposta, ProdutoCreate, ProdutoResponse

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Livros",
    version="1.0.0",
    description="API didática para gerenciamento de livros e produtos.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def tratar_erro_interno(request: Request, exc: Exception):
    """Retorna 500 em vez de expor exceções internas ao cliente da API."""
    return JSONResponse(status_code=500, content={"detail": "Erro interno do servidor"})


# ==================== PRODUTOS ====================

@app.get("/produtos", response_model=list[ProdutoResponse], tags=["Produtos"])
def listar_produtos(db: Session = Depends(get_db)):
    try:
        return db.query(ProdutoDB).all()
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Erro interno do servidor") from exc


@app.post("/produtos", response_model=ProdutoResponse, status_code=201, tags=["Produtos"])
def criar_produto(produto: ProdutoCreate, db: Session = Depends(get_db)):
    try:
        novo_produto = ProdutoDB(**produto.model_dump())
        db.add(novo_produto)
        db.commit()
        db.refresh(novo_produto)
        return novo_produto
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail="Erro interno do servidor") from exc


@app.get("/produtos/{produto_id}", response_model=ProdutoResponse, tags=["Produtos"])
def obter_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = db.query(ProdutoDB).filter(ProdutoDB.id == produto_id).first()
    if produto is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto


@app.put("/produtos/{produto_id}", response_model=ProdutoResponse, tags=["Produtos"])
def atualizar_produto(produto_id: int, produto: ProdutoCreate, db: Session = Depends(get_db)):
    try:
        db_produto = db.query(ProdutoDB).filter(ProdutoDB.id == produto_id).first()
        if db_produto is None:
            raise HTTPException(status_code=404, detail="Produto não encontrado")
        for campo, valor in produto.model_dump().items():
            setattr(db_produto, campo, valor)
        db.commit()
        db.refresh(db_produto)
        return db_produto
    except HTTPException:
        raise
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail="Erro interno do servidor") from exc


@app.delete("/produtos/{produto_id}", tags=["Produtos"])
def remover_produto(produto_id: int, db: Session = Depends(get_db)):
    try:
        produto = db.query(ProdutoDB).filter(ProdutoDB.id == produto_id).first()
        if produto is None:
            raise HTTPException(status_code=404, detail="Produto não encontrado")
        db.delete(produto)
        db.commit()
        return {"mensagem": "Produto excluído com sucesso"}
    except HTTPException:
        raise
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail="Erro interno do servidor") from exc


# ==================== LIVROS ====================

@app.get("/livros", response_model=list[LivroResposta], tags=["Livros"])
def listar_livros(db: Session = Depends(get_db)):
    return db.query(Livro).all()


@app.post("/livros", response_model=LivroResposta, status_code=201, tags=["Livros"])
def criar_livro(dados_livro: LivroCriacao, db: Session = Depends(get_db)):
    novo_livro = Livro(**dados_livro.model_dump())
    db.add(novo_livro)
    db.commit()
    db.refresh(novo_livro)
    return novo_livro


@app.get("/livros/{id_livro}", response_model=LivroResposta, tags=["Livros"])
def obter_livro(id_livro: int, db: Session = Depends(get_db)):
    livro = db.query(Livro).filter(Livro.id == id_livro).first()
    if livro is None:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return livro


@app.put("/livros/{id_livro}", response_model=LivroResposta, tags=["Livros"])
def atualizar_livro(
    id_livro: int,
    dados_livro: LivroCriacao,
    db: Session = Depends(get_db),
):
    livro = db.query(Livro).filter(Livro.id == id_livro).first()
    if livro is None:
        raise HTTPException(status_code=404, detail="Livro não encontrado")

    livro.titulo = dados_livro.titulo
    livro.autor = dados_livro.autor
    livro.ano_publicacao = dados_livro.ano_publicacao
    livro.disponivel = dados_livro.disponivel

    db.commit()
    db.refresh(livro)
    return livro


@app.delete("/livros/{id_livro}", tags=["Livros"])
def excluir_livro(id_livro: int, db: Session = Depends(get_db)):
    livro = db.query(Livro).filter(Livro.id == id_livro).first()
    if livro is None:
        raise HTTPException(status_code=404, detail="Livro não encontrado")

    db.delete(livro)
    db.commit()
    return {"mensagem": "Livro excluído com sucesso"}
