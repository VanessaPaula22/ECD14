from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas, database

app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/contatos/", response_model=schemas.Contato)
def criar_contato(contato: schemas.ContatoCreate, db: Session = Depends(get_db)):
    db_contato = models.Contato(nome=contato.nome, categoria=contato.categoria)
    db.add(db_contato)
    db.commit()
    db.refresh(db_contato)
    for tel in contato.telefones:
        db_telefone = models.Telefone(numero=tel.numero, tipo=tel.tipo, contato_id=db_contato.id)
        db.add(db_telefone)
    db.commit()
    db.refresh(db_contato)
    db_contato.telefones = db.query(models.Telefone).filter_by(contato_id=db_contato.id).all()
    return db_contato

@app.get("/contatos/{contato_id}", response_model=schemas.Contato)
def consultar_contato(contato_id: int, db: Session = Depends(get_db)):
    contato = db.query(models.Contato).filter(models.Contato.id == contato_id).first()
    if not contato:
        raise HTTPException(status_code=404, detail="Contato não encontrado")
    return contato

@app.get("/contatos/", response_model=List[schemas.Contato])
def listar_contatos(db: Session = Depends(get_db)):
    return db.query(models.Contato).all()