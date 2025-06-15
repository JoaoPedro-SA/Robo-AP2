from sqlalchemy import Column, Integer, String, ForeignKey
from modelos.base import Base
from sqlalchemy.orm import relationship



class AssistenciaTecnica(Base.Base, Base):
    __tablename__ = 'assistencia_tecnica'

    nro = Column(Integer, primary_key=True, autoincrement=True)
    bairro = Column(String(100))
    cep = Column(String(10))
    ddd = Column(String(5))
    endereco = Column(String(255))
    nome_fantasia = Column(String(255))
    razao_social = Column(String(255))
    telefone = Column(String(20))
    nome_cidade = Column(String(100))
    uf_estado = Column(String(2))  # Usando o estado como UF
    classificacao_id = Column(Integer, ForeignKey('classificacao.id'))

    # Relacionamento com a tabela classificação
    classificacao = relationship('Classificacao', back_populates='assistencias_tecnicas')

    @classmethod
    def from_dataframe(cls, dataframe):
        
        assistencias = []
        for _, row in dataframe.iterrows():
            assistencia = cls(
                nro=row['nro'],
                bairro=row['bairro'],
                cep=row['cep'],
                ddd=row['ddd'],
                endereco=row['endereco'],
                nome_fantasia=row['nome_fantasia'],
                razao_social=row['razao_social'],
                telefone=row['telefone'],
                nome_cidade=row['nome_cidade'],
                uf_estado=row['uf_estado']
                # Inclua outros campos conforme necessário
            )
        assistencias.append(assistencia)
        return assistencias


class Classificacao(Base.Base, Base):
    __tablename__ = 'classificacao'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100))

    # Relacionamento com assistências técnicas
    assistencias_tecnicas = relationship('AssistenciaTecnica', back_populates='classificacao')


class Estado(Base.Base, Base):
    __tablename__ = 'estado'

    uf = Column(String(2), primary_key=True)
    nome = Column(String(100))



class Cidade(Base.Base, Base):
    __tablename__ = 'cidade'

    nome = Column(String(100), primary_key=True)
    uf_estado = Column(String(2), ForeignKey('estado.uf'))

    # Relacionamento com o estado
    estado = relationship('Estado')
