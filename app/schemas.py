from pydantic import BaseModel
from typing import List
import enum

class TipoTelefoneEnum(str, enum.Enum):
    movel = 'movel'
    fixo = 'fixo'
    comercial = 'comercial'

class CategoriaContatoEnum(str, enum.Enum):
    familiar = 'familiar'
    pessoal = 'pessoal'
    comercial = 'comercial'

class TelefoneBase(BaseModel):
    numero: str
    tipo: TipoTelefoneEnum

class TelefoneCreate(TelefoneBase):
    pass

class Telefone(TelefoneBase):
    id: int

    class Config:
        orm_mode = True

class ContatoBase(BaseModel):
    nome: str
    categoria: CategoriaContatoEnum

class ContatoCreate(ContatoBase):
    telefones: List[TelefoneCreate]

class Contato(ContatoBase):
    id: int
    telefones: List[Telefone] = []

    class Config:
        orm_mode = True