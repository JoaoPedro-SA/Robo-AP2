import pandas as pd
from sqlalchemy import create_engine
from abstract_etl import AbstractETL
import os
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
from modelos.base import Base
from modelos.user import AssistenciaTecnica, Classificacao, Estado, Cidade

# Carregar variáveis do .env
load_dotenv()

class ETL(AbstractETL):
    origem = "E:/Praticando programacao/Projetos/ATV POO/atividade de ap2/tentativa 433/dados.csv"
    
    def extract(self):
        """Extrai os dados da origem e os armazena na variável _dados_extraidos."""
        try:
            # Supondo que a origem seja um caminho para um arquivo CSV
            self._dados_extraidos = pd.read_csv(self.origem)
            print("Dados extraídos com sucesso.")
            print(self._dados_extraidos)
        except Exception as e:
            print(f"Erro ao extrair dados: {e}")

    def transform(self, session):
        """Transforma os dados extraídos para as outras tabelas do banco."""
        try:
            dados_transformados = []  # Armazena os dados transformados para posterior carregamento

            for _, row in self._dados_extraidos.iterrows():
                # Verifica ou cria a classificação
                classificacao = session.query(Classificacao).filter_by(nome=row['classificacao_nome']).first()
                if not classificacao:
                    classificacao = Classificacao(nome=row['classificacao_nome'])
                    session.add(classificacao)
                    session.flush()  # Garante que o ID é gerado para uso imediato

                # Verifica ou cria o estado
                estado = session.query(Estado).filter_by(uf=row['uf_estado']).first()
                if not estado:
                    estado = Estado(uf=row['uf_estado'], nome=row['uf_estado'])
                    session.add(estado)

                # Verifica ou cria a cidade
                cidade = session.query(Cidade).filter_by(nome=row['nome_cidade'], uf_estado=row['uf_estado']).first()
                if not cidade:
                    cidade = Cidade(nome=row['nome_cidade'], uf_estado=row['uf_estado'])
                    session.add(cidade)

                # Cria a assistência técnica e associa as chaves estrangeiras
                assistencia = AssistenciaTecnica(
                    nro=row['nro'], bairro=row['bairro'], cep=row['cep'],
                    ddd=row['ddd'], endereco=row['endereco'],
                    nome_fantasia=row['nome_fantasia'], razao_social=row['razao_social'],
                    telefone=row['telefone'], nome_cidade=row['nome_cidade'],
                    uf_estado=row['uf_estado'], classificacao_id=classificacao.id
                )
                session.add(assistencia)
                
                # Adiciona os dados transformados para o carregamento
                dados_transformados.append(row)

            session.commit()  # Confirma todas as inserções
            self._dados_transformados = pd.DataFrame(dados_transformados)  # Guarda os dados transformados
            print("Dados transformados com sucesso.")
        except Exception as e:
            print(f"Erro ao transformar dados: {e}")
            session.rollback()  # Reverte as operações em caso de erro

    def load(self):
        """Carrega os dados transformados para o destino especificado."""
        try:
            if hasattr(self, '_dados_transformados') and not self._dados_transformados.empty:
                # Construindo a URI de conexão para o SQL Server com as variáveis do .env
                usuario = os.getenv("USUARIO")
                senha = os.getenv("SENHA")
                host = os.getenv("HOST")
                banco_de_dados = os.getenv("BANCO_DE_DADOS")
                
                destino = f"mssql+pyodbc://{usuario}:{senha}@{host}/{banco_de_dados}?driver=ODBC+Driver+17+for+SQL+Server"

                # Criando a conexão e carregando os dados
                engine = create_engine(destino)
                self._dados_transformados.to_sql('dados_transformados', con=engine, if_exists='replace', index=False)
                print("Dados carregados com sucesso no banco de dados.")
            else:
                print("Nenhum dado para carregar. Execute primeiro o método 'transform'.")
        except Exception as e:
            print(f"Erro ao carregar dados: {e}")
