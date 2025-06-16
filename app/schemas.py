from pydantic import BaseModel
from typing import List
import enum

class TipoTelefone(str, enum.Enum):
    movel = 'movel'
    fixo = 'fixo'
    comercial = 'comercial'

class CategoriaContato(str, enum.Enum):
    familiar = 'familiar'
    pessoal = 'pessoal'
    comercial = 'comercial'

class TelefoneBase(BaseModel):
    numero: str
    tipo: TipoTelefone

class CriarTelefone(TelefoneBase):
    pass

class Telefone(TelefoneBase):
    id: int

    class Config:
        orm_mode = True

class ContatoBase(BaseModel):
    nome: str
    categoria: CategoriaContato

class CriarContato(ContatoBase):
    telefones: List[CriarTelefone] = []

class Contato(ContatoBase):
    id: int
    telefones: List[Telefone] = []

    class Config:
        orm_mode = True