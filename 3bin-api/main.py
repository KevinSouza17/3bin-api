from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import Livro
from schemas import LivroCriacao, LivroResposta

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Livros",
    version="1.0.0",
    description="API didática para gerenciamento de livros.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type"],
)


@app.exception_handler(Exception)
async def tratar_erro_interno(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content={"detail": "Erro interno do servidor"})


@app.get("/livros", response_model=list[LivroResposta], tags=["Livros"])
def listar_livros(db: Session = Depends(get_db)):
    try:
        return db.query(Livro).all()
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Erro interno do servidor") from exc


@app.post("/livros", response_model=LivroResposta, status_code=201, tags=["Livros"])
def criar_livro(dados_livro: LivroCriacao, db: Session = Depends(get_db)):
    try:
        novo_livro = Livro(**dados_livro.model_dump())
        db.add(novo_livro)
        db.commit()
        db.refresh(novo_livro)
        return novo_livro
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail="Erro interno do servidor") from exc


@app.get("/livros/{id_livro}", response_model=LivroResposta, tags=["Livros"])
def obter_livro(id_livro: int, db: Session = Depends(get_db)):
    try:
        livro = db.query(Livro).filter(Livro.id == id_livro).first()
        if livro is None:
            raise HTTPException(status_code=404, detail="Livro não encontrado")
        return livro
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Erro interno do servidor") from exc


@app.put("/livros/{id_livro}", response_model=LivroResposta, tags=["Livros"])
def atualizar_livro(
    id_livro: int,
    dados_livro: LivroCriacao,
    db: Session = Depends(get_db),
):
    try:
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
    except HTTPException:
        raise
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail="Erro interno do servidor") from exc


@app.delete("/livros/{id_livro}", tags=["Livros"])
def excluir_livro(id_livro: int, db: Session = Depends(get_db)):
    try:
        livro = db.query(Livro).filter(Livro.id == id_livro).first()
        if livro is None:
            raise HTTPException(status_code=404, detail="Livro não encontrado")

        db.delete(livro)
        db.commit()
        return {"mensagem": "Livro excluído com sucesso"}
    except HTTPException:
        raise
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail="Erro interno do servidor") from exc
