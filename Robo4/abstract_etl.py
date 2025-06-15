from abc import ABC, abstractmethod

class AbstractETL(ABC):
    def __init__(self, origem: str, destino: str):
        self.origem = origem
        self.destino = destino
        self._dados_extraidos = None
        self._dados_transformados = None

    @abstractmethod
    def extract(self):
        """
        Extrai dados do local de origem. Este método deve ser implementado pela classe filha.
        """
        pass

    @abstractmethod
    def transform(self):
        """
        Transforma os dados extraídos em um formato adequado para inserção. Este método deve ser implementado pela classe filha.
        """
        pass

    @abstractmethod
    def load(self):
        """
        Carrega os dados transformados no destino especificado. Este método deve ser implementado pela classe filha.
        """
        pass
