from ariadne import QueryType, MutationType, make_executable_schema, ObjectType, gql
from ariadne.asgi import GraphQL
from sqlalchemy.orm import Session
from app import models
from app.database import SessionLocal
from typing import List


type_defs = gql("""
    type Query {
        contatos: [Contato!]!
        contato(id: Int!): Contato
    }

    type Mutation {
        criarContato(
            nome: String!,
            categoria: String!,
            telefones: [TelefoneInput!]!
        ): Contato!
    }

    input TelefoneInput {
        numero: String!
        tipo: String!
    }

    type Contato {
        id: Int!
        nome: String!
        categoria: String!
        telefones: [Telefone!]!
    }
    type Telefone {
        id: Int!
        numero: String!
        tipo: String!
    }
""")

query = QueryType()
mutation = MutationType()
contato_obj = ObjectType("Contato")


@query.field("contatos")
def resolve_contatos(_, _info):
    db: Session = SessionLocal()
    contatos = db.query(models.Contato).all()
    return contatos


@query.field("contato")
def resolve_contato(_, _info, id:int):
    db: Session = SessionLocal()
    return db.query(models.Contato).filter(models.Contato.id == id).first()


@mutation.field("criarContato")
def resolve_criar_contato(_, _info, nome:str, categoria:str, telefones:List[dict]):
    db: Session = SessionLocal()
    novo_contato = models.Contato(nome=nome, categoria=categoria)
    db.add(novo_contato)
    db.commit()
    db.refresh(novo_contato)
    for tel in telefones:
        novo_tel = models.Telefone(
            numero=tel["numero"], tipo=tel["tipo"], contato_id=novo_contato.id
        )
        db.add(novo_tel)
    db.commit()
    db.refresh(novo_contato)
    return novo_contato


@contato_obj.field("telefones")
def resolve_telefones(contato_obj, _info):
    db: Session = SessionLocal()
    contato = db.query(models.Contato).filter(models.Contato.id == contato_obj.id).first()
    return contato.telefones


schema = make_executable_schema(
    type_defs, [query, mutation, contato_obj]
)


graphql_app = GraphQL(schema, debug=True)
