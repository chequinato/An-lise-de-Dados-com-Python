# 📊 Projeto de Análise de Dados

Um projeto completo e profissional para análise de dados em Python, com módulos organizados, notebooks interativos e visualizações avançadas.

## 🚀 Características

- **Estrutura Modular**: Código organizado em módulos reutilizáveis
- **Análise Exploratória**: Ferramentas completas para EDA (Exploratory Data Analysis)
- **Visualizações Avançadas**: Gráficos estáticos e interativos com Matplotlib, Seaborn e Plotly
- **Notebooks Interativos**: Exemplos práticos e tutoriais em Jupyter
- **Carregamento de Dados**: Suporte para múltiplas fontes (CSV, Excel, JSON, APIs, Bancos de Dados)
- **Relatórios Automatizados**: Geração automática de relatórios de qualidade dos dados

## 📁 Estrutura do Projeto

```
Python Analise/
├── src/                          # Código fonte
│   ├── __init__.py              # Inicialização do pacote
│   ├── data_loader.py           # Carregamento de dados
│   ├── data_analyzer.py         # Análise exploratória
│   └── visualizer.py            # Visualizações
├── notebooks/                    # Jupyter notebooks
│   ├── 01_introducao_analise_dados.ipynb
│   └── 02_visualizacoes_avancadas.ipynb
├── data/                        # Dados do projeto
│   ├── raw/                     # Dados brutos
│   ├── processed/               # Dados processados
│   ├── external/                # Dados externos
│   └── sample/                  # Dados de exemplo
├── tests/                       # Testes unitários
├── docs/                        # Documentação
├── outputs/                     # Resultados e relatórios
├── requirements.txt             # Dependências
├── .gitignore                  # Arquivos ignorados pelo Git
└── README.md                   # Este arquivo
```

## 🛠️ Instalação

### 1. Clone o repositório
```bash
git clone <url-do-repositorio>
cd "Python Analise"
```

### 2. Crie um ambiente virtual
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Inicie o Jupyter Lab
```bash
jupyter lab
```

## 📚 Módulos Principais

### 🔄 DataLoader (`src/data_loader.py`)
Responsável pelo carregamento de dados de diferentes fontes:

```python
from src.data_loader import DataLoader

loader = DataLoader(data_dir='data')

# Carregar CSV
df = loader.load_csv('dados.csv')

# Carregar Excel
df = loader.load_excel('planilha.xlsx', sheet_name='Sheet1')

# Carregar de API
df = loader.load_from_api('https://api.exemplo.com/dados')

# Carregar de banco de dados
df = loader.load_from_database('SELECT * FROM tabela', 'sqlite:///banco.db')
```

### 📈 DataAnalyzer (`src/data_analyzer.py`)
Ferramentas para análise exploratória de dados:

```python
from src.data_analyzer import DataAnalyzer

analyzer = DataAnalyzer(df)

# Informações básicas
info = analyzer.basic_info()

# Estatísticas descritivas
stats = analyzer.descriptive_statistics()

# Matriz de correlação
corr = analyzer.correlation_analysis()

# Detecção de outliers
outliers = analyzer.detect_outliers()

# Relatório completo
report = analyzer.generate_report()
```

### 📊 DataVisualizer (`src/visualizer.py`)
Criação de visualizações estáticas e interativas:

```python
from src.visualizer import DataVisualizer

viz = DataVisualizer(df)

# Histograma
viz.plot_histogram('coluna', interactive=True)

# Scatter plot
viz.plot_scatter('x', 'y', color_col='categoria', interactive=True)

# Heatmap de correlação
viz.plot_heatmap()

# Dashboard completo
viz.create_dashboard(save_html=True)
```

## 📓 Notebooks Disponíveis

### 1. Introdução à Análise de Dados
- Carregamento básico de dados
- Análise exploratória inicial
- Visualizações fundamentais
- Geração de relatórios

### 2. Visualizações Avançadas
- Gráficos interativos com Plotly
- Dashboards personalizados
- Animações e gráficos 3D
- Temas e personalização

## 🔧 Funcionalidades

### Carregamento de Dados
- ✅ Arquivos CSV, Excel, JSON
- ✅ APIs REST
- ✅ Bancos de dados SQL
- ✅ Web scraping
- ✅ Dados de exemplo

### Análise Exploratória
- ✅ Estatísticas descritivas
- ✅ Análise de correlação
- ✅ Detecção de outliers
- ✅ Análise de qualidade dos dados
- ✅ Relatórios automatizados

### Visualizações
- ✅ Gráficos estáticos (Matplotlib/Seaborn)
- ✅ Gráficos interativos (Plotly)
- ✅ Dashboards
- ✅ Heatmaps
- ✅ Gráficos 3D
- ✅ Animações

## 🎯 Casos de Uso

Este projeto é ideal para:

- **Análise de Vendas**: Análise de performance, tendências e padrões
- **Análise Financeira**: Indicadores, correlações e riscos
- **Marketing Analytics**: Comportamento do cliente, campanhas
- **Análise Operacional**: Eficiência, qualidade, processos
- **Pesquisa e Desenvolvimento**: Experimentos, A/B testing

## 📊 Exemplo Rápido

```python
# Importar módulos
from src.data_loader import DataLoader
from src.data_analyzer import DataAnalyzer
from src.visualizer import DataVisualizer

# Carregar dados
loader = DataLoader()
df = loader.load_csv('data/sample/exemplo_vendas.csv')

# Analisar
analyzer = DataAnalyzer(df)
report = analyzer.generate_report()

# Visualizar
viz = DataVisualizer(df)
viz.plot_correlation_heatmap()
viz.create_dashboard()

print("Análise completa realizada!")
```

## 🧪 Testes

Execute os testes unitários:

```bash
pytest tests/
```

## 📖 Documentação

A documentação completa está disponível na pasta `docs/` e inclui:

- Guia de instalação detalhado
- Referência da API
- Tutoriais avançados
- Exemplos de uso
- Melhores práticas

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👨‍💻 Autor

**Miguel** - Desenvolvedor e Analista de Dados

## 🙏 Agradecimentos

- Comunidade Python
- Desenvolvedores das bibliotecas utilizadas
- Contribuidores do projeto

---

⭐ **Se este projeto foi útil para você, considere dar uma estrela!**

## 📞 Suporte

Se você encontrar algum problema ou tiver dúvidas:

1. Verifique a documentação
2. Procure em issues existentes
3. Crie uma nova issue com detalhes do problema
4. Entre em contato através dos canais disponíveis

---

**Última atualização**: Setembro 2024
