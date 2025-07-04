from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas, database, ariadne_graphql

app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)


def banco():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/contatos/", response_model=schemas.Contato)
def criar_contato(contato: schemas.CriarContato, db: Session = Depends(banco)) -> schemas.Contato:
    """Return schemas.Contato
    
    Param contato: schemas.CriarContato
    Param db: Session

    Cria um novo contato com telefones associados.
    """

    db_contato = models.Contato(nome=contato.nome, categoria=contato.categoria)
    db.add(db_contato)
    db.commit()
    db.refresh(db_contato)
    telefones = [models.Telefone(numero=tel.numero, tipo=tel.tipo, contato_id=db_contato.id) for tel in contato.telefones]
    db.add_all(telefones)
    db.commit()
    db.refresh(db_contato)
    db_contato.telefones = db.query(models.Telefone).filter_by(contato_id=db_contato.id).all()
    return db_contato


@app.get("/contatos/{contato_id}", response_model=schemas.Contato)
def consultar_contato(contato_id: int, db: Session = Depends(banco)) -> schemas.Contato|None:
    """Return schemas.Contato or None"""
    contato = db.query(models.Contato).filter(models.Contato.id == contato_id).first()
    if not contato:
        raise HTTPException(status_code=404, detail="Contato não encontrado")
    return contato


@app.get("/contatos/", response_model=List[schemas.Contato])
def listar_contatos(db: Session = Depends(banco)) -> List[schemas.Contato]:
    """Return List[schemas.Contato]
    Lista todos os contatos cadastrados."""
    return db.query(models.Contato).all()


app.mount("/graphql", ariadne_graphql.graphql_app)
