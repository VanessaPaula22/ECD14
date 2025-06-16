from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
import enum

class TipoTelefoneEnum(str, enum.Enum):
    movel = 'movel'
    fixo = 'fixo'
    comercial = 'comercial'

class CategoriaContatoEnum(str, enum.Enum):
    familiar = 'familiar'
    pessoal = 'pessoal'
    comercial = 'comercial'

class Contato(Base):
    __tablename__ = "contatos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    categoria = Column(Enum(CategoriaContatoEnum), nullable=False)
    telefones = relationship("Telefone", back_populates="contato", cascade="all, delete-orphan")

class Telefone(Base):
    __tablename__ = "telefones"

    id = Column(Integer, primary_key=True, index=True)
    numero = Column(String, nullable=False)
    tipo = Column(Enum(TipoTelefoneEnum), nullable=False)
    contato_id = Column(Integer, ForeignKey("contatos.id"))
    contato = relationship("Contato", back_populates="telefones")