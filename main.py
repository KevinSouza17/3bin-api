from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import Base, engine, get_db
from models import ProdutoDB, LivroDB
from schemas import (
    ProdutoCreate, ProdutoResponse,
    LivroCreate, LivroResponse
)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Loja - Produtos e Livros")

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],          # em produção, restringir para o domínio real do front-end
    allow_methods=['*'],
    allow_headers=['*'],
)


# ==================== PRODUTOS ====================

@app.get('/produtos', response_model=list[ProdutoResponse])
def listar_produtos(db: Session = Depends(get_db)):
    return db.query(ProdutoDB).all()


@app.post('/produtos', response_model=ProdutoResponse, status_code=201)
def criar_produto(produto: ProdutoCreate, db: Session = Depends(get_db)):
    novo_produto = ProdutoDB(**produto.model_dump())
    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)
    return novo_produto


@app.get('/produtos/{produto_id}', response_model=ProdutoResponse)
def obter_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = db.query(ProdutoDB).filter(ProdutoDB.id == produto_id).first()
    if produto is None:
        raise HTTPException(status_code=404, detail='Produto não encontrado')
    return produto


@app.put('/produtos/{produto_id}', response_model=ProdutoResponse)
def atualizar_produto(produto_id: int, produto: ProdutoCreate, db: Session = Depends(get_db)):
    db_produto = db.query(ProdutoDB).filter(ProdutoDB.id == produto_id).first()
    if db_produto is None:
        raise HTTPException(status_code=404, detail='Produto não encontrado')
    for key, value in produto.model_dump().items():
        setattr(db_produto, key, value)
    db.commit()
    db.refresh(db_produto)
    return db_produto


@app.delete('/produtos/{produto_id}', status_code=204)
def remover_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = db.query(ProdutoDB).filter(ProdutoDB.id == produto_id).first()
    if produto is None:
        raise HTTPException(status_code=404, detail='Produto não encontrado')
    db.delete(produto)
    db.commit()


# ==================== LIVROS (novo recurso do exercício) ====================

@app.get('/livros', response_model=list[LivroResponse])
def listar_livros(db: Session = Depends(get_db)):
    return db.query(LivroDB).all()


@app.post('/livros', response_model=LivroResponse, status_code=201)
def criar_livro(livro: LivroCreate, db: Session = Depends(get_db)):
    novo_livro = LivroDB(**livro.model_dump())
    db.add(novo_livro)
    db.commit()
    db.refresh(novo_livro)
    return novo_livro


@app.get('/livros/{livro_id}', response_model=LivroResponse)
def obter_livro(livro_id: int, db: Session = Depends(get_db)):
    livro = db.query(LivroDB).filter(LivroDB.id == livro_id).first()
    if livro is None:
        raise HTTPException(status_code=404, detail='Livro não encontrado')
    return livro


@app.put('/livros/{livro_id}', response_model=LivroResponse)
def atualizar_livro(livro_id: int, livro: LivroCreate, db: Session = Depends(get_db)):
    db_livro = db.query(LivroDB).filter(LivroDB.id == livro_id).first()
    if db_livro is None:
        raise HTTPException(status_code=404, detail='Livro não encontrado')
    for key, value in livro.model_dump().items():
        setattr(db_livro, key, value)
    db.commit()
    db.refresh(db_livro)
    return db_livro


@app.delete('/livros/{livro_id}', status_code=204)
def remover_livro(livro_id: int, db: Session = Depends(get_db)):
    livro = db.query(LivroDB).filter(LivroDB.id == livro_id).first()
    if livro is None:
        raise HTTPException(status_code=404, detail='Livro não encontrado')
    db.delete(livro)
    db.commit()