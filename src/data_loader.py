"""
Módulo para carregamento e importação de dados
==============================================

Este módulo contém funções para carregar dados de diferentes fontes:
- Arquivos CSV, Excel, JSON
- Bancos de dados
- APIs
- Web scraping
"""

import pandas as pd
import numpy as np
import json
import sqlite3
from pathlib import Path
from typing import Optional, Dict, Any, Union
import requests
from sqlalchemy import create_engine
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataLoader:
    """Classe principal para carregamento de dados de diferentes fontes."""
    
    def __init__(self, data_dir: str = "data"):
        """
        Inicializa o DataLoader.
        
        Args:
            data_dir: Diretório base para os dados
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
    
    def load_csv(self, 
                 filepath: Union[str, Path], 
                 **kwargs) -> pd.DataFrame:
        """
        Carrega dados de um arquivo CSV.
        
        Args:
            filepath: Caminho para o arquivo CSV
            **kwargs: Argumentos adicionais para pd.read_csv()
            
        Returns:
            DataFrame com os dados carregados
        """
        try:
            df = pd.read_csv(filepath, **kwargs)
            logger.info(f"CSV carregado com sucesso: {filepath}")
            logger.info(f"Shape: {df.shape}")
            return df
        except Exception as e:
            logger.error(f"Erro ao carregar CSV {filepath}: {e}")
            raise
    
    def load_excel(self, 
                   filepath: Union[str, Path], 
                   sheet_name: Optional[str] = None,
                   **kwargs) -> pd.DataFrame:
        """
        Carrega dados de um arquivo Excel.
        
        Args:
            filepath: Caminho para o arquivo Excel
            sheet_name: Nome da planilha (opcional)
            **kwargs: Argumentos adicionais para pd.read_excel()
            
        Returns:
            DataFrame com os dados carregados
        """
        try:
            df = pd.read_excel(filepath, sheet_name=sheet_name, **kwargs)
            logger.info(f"Excel carregado com sucesso: {filepath}")
            logger.info(f"Shape: {df.shape}")
            return df
        except Exception as e:
            logger.error(f"Erro ao carregar Excel {filepath}: {e}")
            raise
    
    def load_json(self, 
                  filepath: Union[str, Path], 
                  orient: str = 'records') -> pd.DataFrame:
        """
        Carrega dados de um arquivo JSON.
        
        Args:
            filepath: Caminho para o arquivo JSON
            orient: Orientação do JSON
            
        Returns:
            DataFrame com os dados carregados
        """
        try:
            df = pd.read_json(filepath, orient=orient)
            logger.info(f"JSON carregado com sucesso: {filepath}")
            logger.info(f"Shape: {df.shape}")
            return df
        except Exception as e:
            logger.error(f"Erro ao carregar JSON {filepath}: {e}")
            raise
    
    def load_from_database(self, 
                          query: str, 
                          connection_string: str) -> pd.DataFrame:
        """
        Carrega dados de um banco de dados usando SQL.
        
        Args:
            query: Query SQL
            connection_string: String de conexão com o banco
            
        Returns:
            DataFrame com os dados carregados
        """
        try:
            engine = create_engine(connection_string)
            df = pd.read_sql(query, engine)
            logger.info(f"Dados carregados do banco com sucesso")
            logger.info(f"Shape: {df.shape}")
            return df
        except Exception as e:
            logger.error(f"Erro ao carregar dados do banco: {e}")
            raise
    
    def load_from_api(self, 
                      url: str, 
                      params: Optional[Dict[str, Any]] = None,
                      headers: Optional[Dict[str, str]] = None) -> pd.DataFrame:
        """
        Carrega dados de uma API REST.
        
        Args:
            url: URL da API
            params: Parâmetros da requisição
            headers: Headers da requisição
            
        Returns:
            DataFrame com os dados carregados
        """
        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
            
            data = response.json()
            df = pd.json_normalize(data)
            
            logger.info(f"Dados carregados da API com sucesso: {url}")
            logger.info(f"Shape: {df.shape}")
            return df
        except Exception as e:
            logger.error(f"Erro ao carregar dados da API {url}: {e}")
            raise
    
    def save_data(self, 
                  df: pd.DataFrame, 
                  filename: str, 
                  format: str = 'csv',
                  **kwargs) -> None:
        """
        Salva DataFrame em arquivo.
        
        Args:
            df: DataFrame para salvar
            filename: Nome do arquivo
            format: Formato do arquivo ('csv', 'excel', 'json', 'parquet')
            **kwargs: Argumentos adicionais para a função de salvamento
        """
        filepath = self.data_dir / filename
        
        try:
            if format.lower() == 'csv':
                df.to_csv(filepath, index=False, **kwargs)
            elif format.lower() == 'excel':
                df.to_excel(filepath, index=False, **kwargs)
            elif format.lower() == 'json':
                df.to_json(filepath, orient='records', **kwargs)
            elif format.lower() == 'parquet':
                df.to_parquet(filepath, **kwargs)
            else:
                raise ValueError(f"Formato não suportado: {format}")
            
            logger.info(f"Dados salvos com sucesso: {filepath}")
        except Exception as e:
            logger.error(f"Erro ao salvar dados: {e}")
            raise


def create_sample_data() -> pd.DataFrame:
    """
    Cria dados de exemplo para testes.
    
    Returns:
        DataFrame com dados de exemplo
    """
    np.random.seed(42)
    
    data = {
        'id': range(1, 1001),
        'nome': [f'Cliente_{i}' for i in range(1, 1001)],
        'idade': np.random.randint(18, 80, 1000),
        'salario': np.random.normal(50000, 15000, 1000),
        'categoria': np.random.choice(['A', 'B', 'C'], 1000),
        'data_cadastro': pd.date_range('2020-01-01', periods=1000, freq='D'),
        'ativo': np.random.choice([True, False], 1000, p=[0.8, 0.2])
    }
    
    df = pd.DataFrame(data)
    df['salario'] = df['salario'].round(2)
    
    return df


if __name__ == "__main__":
    # Exemplo de uso
    loader = DataLoader()
    
    # Criar dados de exemplo
    sample_df = create_sample_data()
    print("Dados de exemplo criados:")
    print(sample_df.head())
    print(f"Shape: {sample_df.shape}")
    
    # Salvar dados de exemplo
    loader.save_data(sample_df, "dados_exemplo.csv")
    print("Dados de exemplo salvos em 'data/dados_exemplo.csv'")
