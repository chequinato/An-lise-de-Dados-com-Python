"""
Testes unitários para o módulo data_loader.
"""

import pytest
import pandas as pd
import numpy as np
import tempfile
import os
from pathlib import Path
import sys

# Adicionar src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from data_loader import DataLoader, create_sample_data


class TestDataLoader:
    """Testes para a classe DataLoader."""
    
    def setup_method(self):
        """Setup executado antes de cada teste."""
        self.temp_dir = tempfile.mkdtemp()
        self.loader = DataLoader(data_dir=self.temp_dir)
        
        # Criar dados de teste
        self.test_data = pd.DataFrame({
            'id': [1, 2, 3, 4, 5],
            'nome': ['A', 'B', 'C', 'D', 'E'],
            'valor': [10.5, 20.3, 30.1, 40.8, 50.2],
            'categoria': ['X', 'Y', 'X', 'Y', 'X']
        })
    
    def test_init(self):
        """Testa a inicialização do DataLoader."""
        assert self.loader.data_dir == Path(self.temp_dir)
        assert self.loader.data_dir.exists()
    
    def test_load_csv(self):
        """Testa o carregamento de arquivos CSV."""
        # Criar arquivo CSV temporário
        csv_path = os.path.join(self.temp_dir, 'test.csv')
        self.test_data.to_csv(csv_path, index=False)
        
        # Carregar dados
        df = self.loader.load_csv(csv_path)
        
        # Verificar se os dados foram carregados corretamente
        assert df.shape == self.test_data.shape
        assert list(df.columns) == list(self.test_data.columns)
        pd.testing.assert_frame_equal(df, self.test_data)
    
    def test_load_excel(self):
        """Testa o carregamento de arquivos Excel."""
        # Criar arquivo Excel temporário
        excel_path = os.path.join(self.temp_dir, 'test.xlsx')
        self.test_data.to_excel(excel_path, index=False)
        
        # Carregar dados
        df = self.loader.load_excel(excel_path)
        
        # Verificar se os dados foram carregados corretamente
        assert df.shape == self.test_data.shape
        assert list(df.columns) == list(self.test_data.columns)
    
    def test_load_json(self):
        """Testa o carregamento de arquivos JSON."""
        # Criar arquivo JSON temporário
        json_path = os.path.join(self.temp_dir, 'test.json')
        self.test_data.to_json(json_path, orient='records')
        
        # Carregar dados
        df = self.loader.load_json(json_path)
        
        # Verificar se os dados foram carregados corretamente
        assert df.shape == self.test_data.shape
        assert list(df.columns) == list(self.test_data.columns)
    
    def test_save_data_csv(self):
        """Testa o salvamento de dados em CSV."""
        filename = 'saved_test.csv'
        self.loader.save_data(self.test_data, filename, format='csv')
        
        # Verificar se o arquivo foi criado
        saved_path = self.loader.data_dir / filename
        assert saved_path.exists()
        
        # Verificar se os dados foram salvos corretamente
        loaded_df = pd.read_csv(saved_path)
        pd.testing.assert_frame_equal(loaded_df, self.test_data)
    
    def test_save_data_excel(self):
        """Testa o salvamento de dados em Excel."""
        filename = 'saved_test.xlsx'
        self.loader.save_data(self.test_data, filename, format='excel')
        
        # Verificar se o arquivo foi criado
        saved_path = self.loader.data_dir / filename
        assert saved_path.exists()
    
    def test_save_data_json(self):
        """Testa o salvamento de dados em JSON."""
        filename = 'saved_test.json'
        self.loader.save_data(self.test_data, filename, format='json')
        
        # Verificar se o arquivo foi criado
        saved_path = self.loader.data_dir / filename
        assert saved_path.exists()
    
    def test_save_data_invalid_format(self):
        """Testa o salvamento com formato inválido."""
        with pytest.raises(ValueError):
            self.loader.save_data(self.test_data, 'test.txt', format='invalid')
    
    def test_load_csv_file_not_found(self):
        """Testa o carregamento de arquivo CSV inexistente."""
        with pytest.raises(FileNotFoundError):
            self.loader.load_csv('arquivo_inexistente.csv')


class TestCreateSampleData:
    """Testes para a função create_sample_data."""
    
    def test_create_sample_data(self):
        """Testa a criação de dados de exemplo."""
        df = create_sample_data()
        
        # Verificar estrutura
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 1000
        assert 'id' in df.columns
        assert 'nome' in df.columns
        assert 'idade' in df.columns
        assert 'salario' in df.columns
        assert 'categoria' in df.columns
        assert 'data_cadastro' in df.columns
        assert 'ativo' in df.columns
        
        # Verificar tipos de dados
        assert df['id'].dtype == 'int64'
        assert df['idade'].dtype == 'int64'
        assert df['salario'].dtype == 'float64'
        assert df['categoria'].dtype == 'object'
        assert pd.api.types.is_datetime64_any_dtype(df['data_cadastro'])
        assert df['ativo'].dtype == 'bool'
        
        # Verificar ranges
        assert df['idade'].min() >= 18
        assert df['idade'].max() <= 79
        assert df['categoria'].isin(['A', 'B', 'C']).all()
        assert df['ativo'].isin([True, False]).all()


if __name__ == "__main__":
    pytest.main([__file__])
