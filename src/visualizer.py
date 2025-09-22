"""
Módulo para visualização de dados
=================================

Este módulo contém funções para criar visualizações avançadas:
- Gráficos estáticos (matplotlib, seaborn)
- Gráficos interativos (plotly)
- Dashboards
- Relatórios visuais
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.offline as pyo
from typing import List, Dict, Any, Optional, Tuple, Union
import warnings
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configurar estilo
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")
pyo.init_notebook_mode(connected=True)


class DataVisualizer:
    """Classe principal para visualização de dados."""
    
    def __init__(self, df: pd.DataFrame):
        """
        Inicializa o DataVisualizer.
        
        Args:
            df: DataFrame para visualização
        """
        self.df = df.copy()
        self.numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
        self.categorical_columns = df.select_dtypes(include=['object', 'category']).columns.tolist()
        self.datetime_columns = df.select_dtypes(include=['datetime64']).columns.tolist()
        
        # Configurar tema padrão do plotly
        self.plotly_theme = 'plotly_white'
    
    def plot_histogram(self, 
                      column: str, 
                      bins: int = 30,
                      interactive: bool = False,
                      figsize: Tuple[int, int] = (10, 6)) -> None:
        """
        Plota histograma de uma coluna.
        
        Args:
            column: Nome da coluna
            bins: Número de bins
            interactive: Se True, usa plotly; se False, usa matplotlib
            figsize: Tamanho da figura (apenas para matplotlib)
        """
        if column not in self.df.columns:
            raise ValueError(f"Coluna '{column}' não encontrada no DataFrame")
        
        if interactive:
            fig = px.histogram(self.df, x=column, nbins=bins,
                             title=f'Histograma de {column}',
                             template=self.plotly_theme)
            fig.show()
        else:
            plt.figure(figsize=figsize)
            plt.hist(self.df[column].dropna(), bins=bins, alpha=0.7, edgecolor='black')
            plt.title(f'Histograma de {column}')
            plt.xlabel(column)
            plt.ylabel('Frequência')
            plt.grid(True, alpha=0.3)
            plt.show()
        
        logger.info(f"Histograma de {column} plotado")
    
    def plot_scatter(self, 
                    x_col: str, 
                    y_col: str,
                    color_col: Optional[str] = None,
                    size_col: Optional[str] = None,
                    interactive: bool = False,
                    figsize: Tuple[int, int] = (10, 6)) -> None:
        """
        Plota gráfico de dispersão.
        
        Args:
            x_col: Coluna para eixo X
            y_col: Coluna para eixo Y
            color_col: Coluna para colorir pontos (opcional)
            size_col: Coluna para tamanho dos pontos (opcional)
            interactive: Se True, usa plotly; se False, usa matplotlib
            figsize: Tamanho da figura (apenas para matplotlib)
        """
        if interactive:
            fig = px.scatter(self.df, x=x_col, y=y_col, 
                           color=color_col, size=size_col,
                           title=f'{y_col} vs {x_col}',
                           template=self.plotly_theme)
            fig.show()
        else:
            plt.figure(figsize=figsize)
            if color_col:
                scatter = plt.scatter(self.df[x_col], self.df[y_col], 
                                    c=self.df[color_col], alpha=0.6)
                plt.colorbar(scatter, label=color_col)
            else:
                plt.scatter(self.df[x_col], self.df[y_col], alpha=0.6)
            
            plt.title(f'{y_col} vs {x_col}')
            plt.xlabel(x_col)
            plt.ylabel(y_col)
            plt.grid(True, alpha=0.3)
            plt.show()
        
        logger.info(f"Gráfico de dispersão {y_col} vs {x_col} plotado")
    
    def plot_line_chart(self, 
                       x_col: str, 
                       y_cols: Union[str, List[str]],
                       interactive: bool = False,
                       figsize: Tuple[int, int] = (12, 6)) -> None:
        """
        Plota gráfico de linha.
        
        Args:
            x_col: Coluna para eixo X
            y_cols: Coluna(s) para eixo Y
            interactive: Se True, usa plotly; se False, usa matplotlib
            figsize: Tamanho da figura (apenas para matplotlib)
        """
        if isinstance(y_cols, str):
            y_cols = [y_cols]
        
        if interactive:
            fig = go.Figure()
            for y_col in y_cols:
                fig.add_trace(go.Scatter(x=self.df[x_col], y=self.df[y_col],
                                       mode='lines+markers', name=y_col))
            
            fig.update_layout(title=f'Gráfico de Linha: {", ".join(y_cols)} vs {x_col}',
                            xaxis_title=x_col,
                            yaxis_title='Valores',
                            template=self.plotly_theme)
            fig.show()
        else:
            plt.figure(figsize=figsize)
            for y_col in y_cols:
                plt.plot(self.df[x_col], self.df[y_col], marker='o', label=y_col)
            
            plt.title(f'Gráfico de Linha: {", ".join(y_cols)} vs {x_col}')
            plt.xlabel(x_col)
            plt.ylabel('Valores')
            plt.legend()
            plt.grid(True, alpha=0.3)
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()
        
        logger.info(f"Gráfico de linha plotado")
    
    def plot_bar_chart(self, 
                      x_col: str, 
                      y_col: str,
                      interactive: bool = False,
                      figsize: Tuple[int, int] = (10, 6)) -> None:
        """
        Plota gráfico de barras.
        
        Args:
            x_col: Coluna para eixo X
            y_col: Coluna para eixo Y
            interactive: Se True, usa plotly; se False, usa matplotlib
            figsize: Tamanho da figura (apenas para matplotlib)
        """
        if interactive:
            fig = px.bar(self.df, x=x_col, y=y_col,
                        title=f'{y_col} por {x_col}',
                        template=self.plotly_theme)
            fig.show()
        else:
            plt.figure(figsize=figsize)
            plt.bar(self.df[x_col], self.df[y_col])
            plt.title(f'{y_col} por {x_col}')
            plt.xlabel(x_col)
            plt.ylabel(y_col)
            plt.xticks(rotation=45)
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.show()
        
        logger.info(f"Gráfico de barras plotado")
    
    def plot_heatmap(self, 
                    columns: Optional[List[str]] = None,
                    correlation: bool = True,
                    figsize: Tuple[int, int] = (10, 8)) -> None:
        """
        Plota heatmap.
        
        Args:
            columns: Colunas para incluir (se None, usa todas as numéricas)
            correlation: Se True, plota correlação; se False, plota valores
            figsize: Tamanho da figura
        """
        if columns is None:
            columns = self.numeric_columns
        
        if not columns:
            logger.warning("Nenhuma coluna numérica encontrada")
            return
        
        data_to_plot = self.df[columns]
        
        if correlation:
            data_to_plot = data_to_plot.corr()
            title = 'Matriz de Correlação'
        else:
            title = 'Heatmap dos Dados'
        
        plt.figure(figsize=figsize)
        sns.heatmap(data_to_plot, annot=True, cmap='coolwarm', center=0,
                   square=True, fmt='.2f')
        plt.title(title)
        plt.tight_layout()
        plt.show()
        
        logger.info("Heatmap plotado")
    
    def plot_boxplot(self, 
                    columns: Optional[List[str]] = None,
                    interactive: bool = False,
                    figsize: Tuple[int, int] = (12, 6)) -> None:
        """
        Plota boxplots.
        
        Args:
            columns: Colunas para plotar (se None, usa todas as numéricas)
            interactive: Se True, usa plotly; se False, usa matplotlib
            figsize: Tamanho da figura (apenas para matplotlib)
        """
        if columns is None:
            columns = self.numeric_columns
        
        if not columns:
            logger.warning("Nenhuma coluna numérica encontrada")
            return
        
        if interactive:
            fig = go.Figure()
            for col in columns:
                fig.add_trace(go.Box(y=self.df[col], name=col))
            
            fig.update_layout(title='Boxplots das Variáveis Numéricas',
                            template=self.plotly_theme)
            fig.show()
        else:
            # Criar subplots para cada variável (melhor visualização)
            n_cols = min(3, len(columns))
            n_rows = (len(columns) + n_cols - 1) // n_cols
            
            fig, axes = plt.subplots(n_rows, n_cols, figsize=(figsize[0], figsize[1] * n_rows // 2))
            if n_rows == 1 and n_cols == 1:
                axes = [axes]
            elif n_rows == 1:
                axes = axes
            else:
                axes = axes.flatten()
            
            for i, col in enumerate(columns):
                if i < len(axes):
                    self.df[col].plot.box(ax=axes[i])
                    axes[i].set_title(f'Boxplot: {col}')
                    axes[i].set_ylabel('Valores')
                    axes[i].grid(True, alpha=0.3)
            
            # Remover subplots vazios
            for i in range(len(columns), len(axes)):
                fig.delaxes(axes[i])
            
            plt.suptitle('Boxplots das Variáveis Numéricas', fontsize=16)
            plt.tight_layout()
            plt.show()
        
        logger.info("Boxplots plotados")
    
    def plot_boxplot_individual(self, 
                               columns: Optional[List[str]] = None,
                               figsize: Tuple[int, int] = (15, 10)) -> None:
        """
        Plota boxplots individuais para cada variável (melhor para escalas diferentes).
        
        Args:
            columns: Colunas para plotar (se None, usa todas as numéricas)
            figsize: Tamanho da figura
        """
        if columns is None:
            columns = self.numeric_columns
        
        if not columns:
            logger.warning("Nenhuma coluna numérica encontrada")
            return
        
        # Criar subplots individuais
        n_cols = min(3, len(columns))
        n_rows = (len(columns) + n_cols - 1) // n_cols
        
        fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize)
        if n_rows == 1 and n_cols == 1:
            axes = [axes]
        elif n_rows == 1:
            axes = axes
        else:
            axes = axes.flatten()
        
        for i, col in enumerate(columns):
            if i < len(axes):
                # Boxplot individual com escala própria
                bp = axes[i].boxplot(self.df[col].dropna(), patch_artist=True)
                
                # Personalizar cores
                bp['boxes'][0].set_facecolor('lightblue')
                bp['boxes'][0].set_alpha(0.7)
                
                axes[i].set_title(f'{col}', fontsize=12, fontweight='bold')
                axes[i].set_ylabel('Valores')
                axes[i].grid(True, alpha=0.3)
                
                # Adicionar estatísticas
                stats_text = f'Média: {self.df[col].mean():.2f}\nMediana: {self.df[col].median():.2f}'
                axes[i].text(0.02, 0.98, stats_text, transform=axes[i].transAxes, 
                           verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        # Remover subplots vazios
        for i in range(len(columns), len(axes)):
            fig.delaxes(axes[i])
        
        plt.suptitle('Análise de Outliers - Boxplots Individuais', fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.show()
        
        logger.info("Boxplots individuais plotados")
    
    def plot_pie_chart(self, 
                      column: str,
                      interactive: bool = False,
                      figsize: Tuple[int, int] = (8, 8)) -> None:
        """
        Plota gráfico de pizza.
        
        Args:
            column: Coluna categórica para plotar
            interactive: Se True, usa plotly; se False, usa matplotlib
            figsize: Tamanho da figura (apenas para matplotlib)
        """
        if column not in self.categorical_columns:
            logger.warning(f"Coluna '{column}' não é categórica")
            return
        
        value_counts = self.df[column].value_counts()
        
        if interactive:
            fig = px.pie(values=value_counts.values, names=value_counts.index,
                        title=f'Distribuição de {column}',
                        template=self.plotly_theme)
            fig.show()
        else:
            plt.figure(figsize=figsize)
            plt.pie(value_counts.values, labels=value_counts.index, autopct='%1.1f%%')
            plt.title(f'Distribuição de {column}')
            plt.axis('equal')
            plt.show()
        
        logger.info(f"Gráfico de pizza de {column} plotado")
    
    def create_dashboard(self, save_html: bool = True, filename: str = "dashboard.html") -> None:
        """
        Cria dashboard interativo com múltiplos gráficos.
        
        Args:
            save_html: Se True, salva como arquivo HTML
            filename: Nome do arquivo HTML
        """
        # Criar subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Distribuições', 'Correlação', 'Boxplots', 'Séries Temporais'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # Subplot 1: Histograma da primeira coluna numérica
        if self.numeric_columns:
            col = self.numeric_columns[0]
            fig.add_trace(
                go.Histogram(x=self.df[col], name=f'Hist {col}'),
                row=1, col=1
            )
        
        # Subplot 2: Heatmap de correlação
        if len(self.numeric_columns) >= 2:
            corr_matrix = self.df[self.numeric_columns].corr()
            fig.add_trace(
                go.Heatmap(z=corr_matrix.values, 
                          x=corr_matrix.columns, 
                          y=corr_matrix.columns,
                          colorscale='RdBu',
                          name='Correlação'),
                row=1, col=2
            )
        
        # Subplot 3: Boxplot
        if self.numeric_columns:
            for i, col in enumerate(self.numeric_columns[:3]):  # Máximo 3 colunas
                fig.add_trace(
                    go.Box(y=self.df[col], name=col),
                    row=2, col=1
                )
        
        # Subplot 4: Série temporal (se houver coluna datetime)
        if self.datetime_columns and self.numeric_columns:
            date_col = self.datetime_columns[0]
            num_col = self.numeric_columns[0]
            fig.add_trace(
                go.Scatter(x=self.df[date_col], y=self.df[num_col], 
                          mode='lines+markers', name=f'{num_col} ao longo do tempo'),
                row=2, col=2
            )
        
        # Atualizar layout
        fig.update_layout(
            title_text="Dashboard de Análise de Dados",
            showlegend=False,
            template=self.plotly_theme,
            height=800
        )
        
        if save_html:
            fig.write_html(filename)
            logger.info(f"Dashboard salvo como {filename}")
        
        fig.show()
        logger.info("Dashboard criado")
    
    def plot_pairplot(self, columns: Optional[List[str]] = None) -> None:
        """
        Cria pairplot das variáveis numéricas.
        
        Args:
            columns: Colunas para incluir (se None, usa todas as numéricas)
        """
        if columns is None:
            columns = self.numeric_columns[:5]  # Máximo 5 colunas para performance
        
        if len(columns) < 2:
            logger.warning("Necessário pelo menos 2 colunas numéricas")
            return
        
        sns.pairplot(self.df[columns])
        plt.suptitle('Pairplot das Variáveis Numéricas', y=1.02)
        plt.show()
        
        logger.info("Pairplot criado")


if __name__ == "__main__":
    # Exemplo de uso
    np.random.seed(42)
    
    # Criar dados de exemplo
    dates = pd.date_range('2023-01-01', periods=100, freq='D')
    data = {
        'data': dates,
        'vendas': np.random.normal(1000, 200, 100) + np.sin(np.arange(100) * 0.1) * 100,
        'lucro': np.random.normal(150, 50, 100),
        'clientes': np.random.poisson(50, 100),
        'categoria': np.random.choice(['A', 'B', 'C'], 100),
        'regiao': np.random.choice(['Norte', 'Sul', 'Leste', 'Oeste'], 100)
    }
    
    df = pd.DataFrame(data)
    
    # Inicializar visualizer
    viz = DataVisualizer(df)
    
    # Criar visualizações
    print("Criando visualizações...")
    
    # Histograma
    viz.plot_histogram('vendas', interactive=True)
    
    # Scatter plot
    viz.plot_scatter('vendas', 'lucro', color_col='categoria', interactive=True)
    
    # Gráfico de linha
    viz.plot_line_chart('data', ['vendas', 'lucro'], interactive=True)
    
    # Heatmap de correlação
    viz.plot_heatmap()
    
    # Dashboard
    viz.create_dashboard()
    
    print("Visualizações criadas com sucesso!")
