"""
Módulo para análise exploratória de dados
=========================================

Este módulo contém funções para análise estatística e exploratória:
- Estatísticas descritivas
- Análise de correlação
- Detecção de outliers
- Análise de qualidade dos dados
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from typing import List, Dict, Any, Optional, Tuple
import warnings
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configurar estilo dos gráficos
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")


class DataAnalyzer:
    """Classe principal para análise exploratória de dados."""
    
    def __init__(self, df: pd.DataFrame):
        """
        Inicializa o DataAnalyzer.
        
        Args:
            df: DataFrame para análise
        """
        self.df = df.copy()
        self.numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
        self.categorical_columns = df.select_dtypes(include=['object', 'category']).columns.tolist()
        self.datetime_columns = df.select_dtypes(include=['datetime64']).columns.tolist()
    
    def basic_info(self) -> Dict[str, Any]:
        """
        Retorna informações básicas sobre o dataset.
        
        Returns:
            Dicionário com informações básicas
        """
        info = {
            'shape': self.df.shape,
            'memory_usage': self.df.memory_usage(deep=True).sum(),
            'null_values': self.df.isnull().sum().sum(),
            'duplicate_rows': self.df.duplicated().sum(),
            'numeric_columns': len(self.numeric_columns),
            'categorical_columns': len(self.categorical_columns),
            'datetime_columns': len(self.datetime_columns),
            'data_types': self.df.dtypes.value_counts().to_dict()
        }
        
        logger.info("Informações básicas calculadas")
        return info
    
    def descriptive_statistics(self) -> pd.DataFrame:
        """
        Calcula estatísticas descritivas para colunas numéricas.
        
        Returns:
            DataFrame com estatísticas descritivas
        """
        if not self.numeric_columns:
            logger.warning("Nenhuma coluna numérica encontrada")
            return pd.DataFrame()
        
        stats_df = self.df[self.numeric_columns].describe()
        
        # Adicionar estatísticas extras
        extra_stats = pd.DataFrame({
            col: {
                'variance': self.df[col].var(),
                'skewness': self.df[col].skew(),
                'kurtosis': self.df[col].kurtosis(),
                'missing_count': self.df[col].isnull().sum(),
                'missing_percentage': (self.df[col].isnull().sum() / len(self.df)) * 100
            } for col in self.numeric_columns
        }).T
        
        result = pd.concat([stats_df.T, extra_stats], axis=1)
        logger.info("Estatísticas descritivas calculadas")
        return result
    
    def correlation_analysis(self, method: str = 'pearson') -> pd.DataFrame:
        """
        Calcula matriz de correlação.
        
        Args:
            method: Método de correlação ('pearson', 'spearman', 'kendall')
            
        Returns:
            Matriz de correlação
        """
        if not self.numeric_columns:
            logger.warning("Nenhuma coluna numérica encontrada para correlação")
            return pd.DataFrame()
        
        corr_matrix = self.df[self.numeric_columns].corr(method=method)
        logger.info(f"Matriz de correlação calculada usando método {method}")
        return corr_matrix
    
    def detect_outliers(self, method: str = 'iqr') -> Dict[str, List]:
        """
        Detecta outliers nas colunas numéricas.
        
        Args:
            method: Método de detecção ('iqr', 'zscore')
            
        Returns:
            Dicionário com outliers por coluna
        """
        outliers = {}
        
        for col in self.numeric_columns:
            if method == 'iqr':
                Q1 = self.df[col].quantile(0.25)
                Q3 = self.df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                outlier_mask = (self.df[col] < lower_bound) | (self.df[col] > upper_bound)
                outliers[col] = self.df[outlier_mask].index.tolist()
                
            elif method == 'zscore':
                z_scores = np.abs(stats.zscore(self.df[col].dropna()))
                outlier_mask = z_scores > 3
                outliers[col] = self.df[col].dropna().iloc[outlier_mask].index.tolist()
        
        logger.info(f"Outliers detectados usando método {method}")
        return outliers
    
    def data_quality_report(self) -> pd.DataFrame:
        """
        Gera relatório de qualidade dos dados.
        
        Returns:
            DataFrame com relatório de qualidade
        """
        quality_report = []
        
        for col in self.df.columns:
            col_data = {
                'column': col,
                'dtype': str(self.df[col].dtype),
                'non_null_count': self.df[col].count(),
                'null_count': self.df[col].isnull().sum(),
                'null_percentage': (self.df[col].isnull().sum() / len(self.df)) * 100,
                'unique_count': self.df[col].nunique(),
                'unique_percentage': (self.df[col].nunique() / len(self.df)) * 100
            }
            
            if col in self.numeric_columns:
                col_data.update({
                    'min_value': self.df[col].min(),
                    'max_value': self.df[col].max(),
                    'mean_value': self.df[col].mean(),
                    'std_value': self.df[col].std()
                })
            
            quality_report.append(col_data)
        
        report_df = pd.DataFrame(quality_report)
        logger.info("Relatório de qualidade dos dados gerado")
        return report_df
    
    def plot_distributions(self, figsize: Tuple[int, int] = (15, 10)) -> None:
        """
        Plota distribuições das variáveis numéricas.
        
        Args:
            figsize: Tamanho da figura
        """
        if not self.numeric_columns:
            logger.warning("Nenhuma coluna numérica para plotar")
            return
        
        n_cols = min(3, len(self.numeric_columns))
        n_rows = (len(self.numeric_columns) + n_cols - 1) // n_cols
        
        fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize)
        if n_rows == 1:
            axes = [axes] if n_cols == 1 else axes
        else:
            axes = axes.flatten()
        
        for i, col in enumerate(self.numeric_columns):
            if i < len(axes):
                sns.histplot(data=self.df, x=col, kde=True, ax=axes[i])
                axes[i].set_title(f'Distribuição de {col}')
                axes[i].tick_params(axis='x', rotation=45)
        
        # Remover subplots vazios
        for i in range(len(self.numeric_columns), len(axes)):
            fig.delaxes(axes[i])
        
        plt.tight_layout()
        plt.show()
        logger.info("Gráficos de distribuição plotados")
    
    def plot_correlation_heatmap(self, figsize: Tuple[int, int] = (10, 8)) -> None:
        """
        Plota heatmap da matriz de correlação.
        
        Args:
            figsize: Tamanho da figura
        """
        if len(self.numeric_columns) < 2:
            logger.warning("Necessário pelo menos 2 colunas numéricas para correlação")
            return
        
        corr_matrix = self.correlation_analysis()
        
        plt.figure(figsize=figsize)
        mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
        
        sns.heatmap(corr_matrix, 
                   mask=mask,
                   annot=True, 
                   cmap='coolwarm', 
                   center=0,
                   square=True,
                   fmt='.2f')
        
        plt.title('Matriz de Correlação')
        plt.tight_layout()
        plt.show()
        logger.info("Heatmap de correlação plotado")
    
    def plot_boxplots(self, figsize: Tuple[int, int] = (15, 10)) -> None:
        """
        Plota boxplots para detectar outliers.
        
        Args:
            figsize: Tamanho da figura
        """
        if not self.numeric_columns:
            logger.warning("Nenhuma coluna numérica para plotar")
            return
        
        n_cols = min(3, len(self.numeric_columns))
        n_rows = (len(self.numeric_columns) + n_cols - 1) // n_cols
        
        fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize)
        if n_rows == 1:
            axes = [axes] if n_cols == 1 else axes
        else:
            axes = axes.flatten()
        
        for i, col in enumerate(self.numeric_columns):
            if i < len(axes):
                sns.boxplot(data=self.df, y=col, ax=axes[i])
                axes[i].set_title(f'Boxplot de {col}')
        
        # Remover subplots vazios
        for i in range(len(self.numeric_columns), len(axes)):
            fig.delaxes(axes[i])
        
        plt.tight_layout()
        plt.show()
        logger.info("Boxplots plotados")
    
    def generate_report(self) -> Dict[str, Any]:
        """
        Gera relatório completo de análise.
        
        Returns:
            Dicionário com relatório completo
        """
        report = {
            'basic_info': self.basic_info(),
            'descriptive_stats': self.descriptive_statistics(),
            'correlation_matrix': self.correlation_analysis(),
            'outliers': self.detect_outliers(),
            'data_quality': self.data_quality_report()
        }
        
        logger.info("Relatório completo gerado")
        return report


if __name__ == "__main__":
    # Exemplo de uso com dados sintéticos
    np.random.seed(42)
    
    # Criar dados de exemplo
    data = {
        'vendas': np.random.normal(1000, 200, 500),
        'lucro': np.random.normal(150, 50, 500),
        'clientes': np.random.poisson(50, 500),
        'categoria': np.random.choice(['A', 'B', 'C'], 500)
    }
    
    df = pd.DataFrame(data)
    
    # Inicializar analyzer
    analyzer = DataAnalyzer(df)
    
    # Gerar relatório
    report = analyzer.generate_report()
    
    print("=== RELATÓRIO DE ANÁLISE ===")
    print(f"Shape do dataset: {report['basic_info']['shape']}")
    print(f"Valores nulos: {report['basic_info']['null_values']}")
    print(f"Linhas duplicadas: {report['basic_info']['duplicate_rows']}")
    
    print("\n=== ESTATÍSTICAS DESCRITIVAS ===")
    print(report['descriptive_stats'])
    
    # Plotar gráficos
    analyzer.plot_distributions()
    analyzer.plot_correlation_heatmap()
    analyzer.plot_boxplots()
