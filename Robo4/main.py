from etl import ETL
from modelos.base import Base
from modelos.user import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Carregar variáveis do .env
load_dotenv()

def main():
    # Configuração de conexão para o SQL Server
    server = os.getenv("HOST")
    database = os.getenv("BANCO_DE_DADOS")
    username = os.getenv("USUARIO")
    password = os.getenv("SENHA")
    destino = f"mssql+pyodbc://{username}:{password}@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server"

    # Configurando a sessão com o SQL Server
    engine = create_engine(destino)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Criando as tabelas no SQL Server (se não existirem)
    Base.Base.metadata.create_all(engine)

    # # Definindo o caminho do arquivo CSV de origem
    origem = "E:/Praticando programacao/Projetos/ATV POO/atividade de ap2/tentativa 433/dados.csv"

    # Inicializando o processo ETL
    etl = ETL(origem=origem, destino=destino)
    try:
        # # # Executando o processo ETL
        etl.extract()    # Extrai os dados
        etl.transform(session)  # Passa a sessão para o método transform
        etl.load()       # Carrega os dados no banco

        # # Agora que os dados foram carregados no banco, você pode fazer a inserção

        # Obter as assistências técnicas a partir do DataFrame
        assistencias = AssistenciaTecnica.from_dataframe(etl._dados_transformados)
        
        # Inserir os dados com verificação de duplicidade
        for assistencia in assistencias:
            # Verifica se já existe um registro com o mesmo nro
            existe = session.query(AssistenciaTecnica).filter_by(nro=assistencia.nro).first()
            if existe:
                print(f"Registro com nro={assistencia.nro} já existe e será ignorado.")
            else:
                session.add(assistencia)
        
        # Confirmar as mudanças no banco de dados
        session.commit()
        print("Dados carregados com sucesso no banco de dados.")
        
    except Exception as e:
        print(f"Erro ao carregar dados: {e}")
        session.rollback()
    
    finally:
        # Fechar a sessão
        session.close()

    # print("Dados ETL carregados com sucesso e inseridos no banco de dados.")

if __name__ == "__main__":
    main()
