from flask import Flask, request, jsonify, abort
from sqlalchemy.orm import scoped_session
from typing import List
from database import *
from models import *
from ariadne_graphql import *

app = Flask(__name__)
Base.metadata.create_all(bind=engine)
db_session = scoped_session(SessionLocal)

def contato_to_dict(contato):
    return {
        "id": contato.id,
        "nome": contato.nome,
        "categoria": contato.categoria.value if contato.categoria else None,
        "telefones": [
            {
                "id": tel.id,
                "numero": tel.numero,
                "tipo": tel.tipo.value if tel.tipo else None
            } for tel in contato.telefones
        ]
    }

@app.route("/contatos/", methods=["POST"])
def criar_contato():
    data = request.get_json()
    if not data or not data.get("nome") or not data.get("categoria") or not data.get("telefones"):
        abort(400, "Dados incompletos.")
    try:
        contato = models.Contato(
            nome=data["nome"],
            categoria=models.CategoriaContato(data["categoria"])
        )
        db_session.add(contato)
        db_session.commit()
        for tel_data in data["telefones"]:
            tel = models.Telefone(
                numero=tel_data["numero"],
                tipo=models.TipoTelefone(tel_data["tipo"]),
                contato_id=contato.id
            )
            db_session.add(tel)
        db_session.commit()
        db_session.refresh(contato)
        return jsonify(contato_to_dict(contato)), 201
    except Exception as e:
        db_session.rollback()
        abort(400, str(e))

@app.route("/contatos/<int:contato_id>", methods=["GET"])
def get_contato(contato_id):
    contato = db_session.query(models.Contato).filter_by(id=contato_id).first()
    if not contato:
        abort(404, "Contato não encontrado.")
    return jsonify(contato_to_dict(contato)), 200

@app.route("/contatos/", methods=["GET"])
def listar_contatos():
    contatos = db_session.query(models.Contato).all()
    return jsonify([contato_to_dict(c) for c in contatos]), 200

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == "__main__":
    app.run(debug=True)

app.mount("/graphql", ariadne_graphql.graphql_app)