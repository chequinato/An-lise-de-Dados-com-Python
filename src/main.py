"""
Script principal para execução do projeto de análise de dados.
"""

import argparse
import sys
from pathlib import Path
import logging

from data_loader import DataLoader, create_sample_data
from data_analyzer import DataAnalyzer
from visualizer import DataVisualizer

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Função principal do programa."""
    parser = argparse.ArgumentParser(
        description='Projeto de Análise de Dados em Python'
    )
    
    parser.add_argument(
        '--file', '-f',
        type=str,
        help='Caminho para o arquivo de dados'
    )
    
    parser.add_argument(
        '--format',
        type=str,
        choices=['csv', 'excel', 'json'],
        default='csv',
        help='Formato do arquivo de dados'
    )
    
    parser.add_argument(
        '--output', '-o',
        type=str,
        default='outputs',
        help='Diretório de saída para relatórios'
    )
    
    parser.add_argument(
        '--sample',
        action='store_true',
        help='Usar dados de exemplo'
    )
    
    parser.add_argument(
        '--dashboard',
        action='store_true',
        help='Gerar dashboard interativo'
    )
    
    parser.add_argument(
        '--report',
        action='store_true',
        help='Gerar relatório completo'
    )
    
    args = parser.parse_args()
    
    try:
        # Criar diretório de saída
        output_dir = Path(args.output)
        output_dir.mkdir(exist_ok=True)
        
        # Carregar dados
        loader = DataLoader()
        
        if args.sample:
            logger.info("Criando dados de exemplo...")
            df = create_sample_data()
            logger.info(f"Dados de exemplo criados com {len(df)} registros")
        elif args.file:
            logger.info(f"Carregando dados de {args.file}...")
            if args.format == 'csv':
                df = loader.load_csv(args.file)
            elif args.format == 'excel':
                df = loader.load_excel(args.file)
            elif args.format == 'json':
                df = loader.load_json(args.file)
            else:
                raise ValueError(f"Formato não suportado: {args.format}")
        else:
            logger.error("Especifique um arquivo com --file ou use --sample")
            sys.exit(1)
        
        logger.info(f"Dados carregados: {df.shape}")
        
        # Inicializar analisador
        analyzer = DataAnalyzer(df)
        
        # Gerar relatório se solicitado
        if args.report:
            logger.info("Gerando relatório completo...")
            report = analyzer.generate_report()
            
            # Salvar informações básicas
            with open(output_dir / 'relatorio_basico.txt', 'w', encoding='utf-8') as f:
                f.write("=== RELATÓRIO DE ANÁLISE DE DADOS ===\n\n")
                f.write("INFORMAÇÕES BÁSICAS:\n")
                for key, value in report['basic_info'].items():
                    f.write(f"{key}: {value}\n")
                
                f.write("\nESTATÍSTICAS DESCRITIVAS:\n")
                f.write(str(report['descriptive_stats']))
                
                f.write("\n\nOUTLIERS DETECTADOS:\n")
                for col, outliers in report['outliers'].items():
                    f.write(f"{col}: {len(outliers)} outliers\n")
            
            logger.info(f"Relatório salvo em {output_dir / 'relatorio_basico.txt'}")
        
        # Gerar dashboard se solicitado
        if args.dashboard:
            logger.info("Gerando dashboard interativo...")
            viz = DataVisualizer(df)
            dashboard_path = output_dir / 'dashboard.html'
            viz.create_dashboard(save_html=True, filename=str(dashboard_path))
            logger.info(f"Dashboard salvo em {dashboard_path}")
        
        # Gerar visualizações básicas
        logger.info("Gerando visualizações...")
        viz = DataVisualizer(df)
        
        # Plotar e salvar gráficos básicos
        import matplotlib.pyplot as plt
        
        # Histograma da primeira coluna numérica
        if viz.numeric_columns:
            viz.plot_histogram(viz.numeric_columns[0])
            plt.savefig(output_dir / 'histograma.png', dpi=300, bbox_inches='tight')
            plt.close()
        
        # Correlação
        viz.plot_heatmap()
        plt.savefig(output_dir / 'correlacao.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # Boxplots individuais (melhor visualização para escalas diferentes)
        viz.plot_boxplot_individual(figsize=(15, 10))
        plt.savefig(output_dir / 'boxplots.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Visualizações salvas em {output_dir}")
        
        print("\n" + "="*50)
        print("ANÁLISE CONCLUÍDA COM SUCESSO!")
        print("="*50)
        print(f"Dados analisados: {df.shape[0]} linhas, {df.shape[1]} colunas")
        print(f"Resultados salvos em: {output_dir}")
        
        if args.dashboard:
            print(f"Dashboard disponível em: {output_dir / 'dashboard.html'}")
        
        print("="*50)
        
    except Exception as e:
        logger.error(f"Erro durante a execução: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
