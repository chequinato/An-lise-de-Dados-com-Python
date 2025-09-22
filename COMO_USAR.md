# 🚀 Como Usar o Projeto

## ⚡ Início Rápido

### 1. Ativar o Ambiente Virtual
```cmd
.venv\Scripts\activate.bat
```

### 2. Iniciar Jupyter Lab
```cmd
jupyter lab
```

**OU use o script automático:**
```cmd
run_jupyter.bat
```

## 📊 Testando o Projeto

### Opção 1: Notebooks Interativos
1. Execute `run_jupyter.bat`
2. Abra `notebooks/01_introducao_analise_dados.ipynb`
3. Execute as células uma por uma

### Opção 2: Linha de Comando
```cmd
# Ativar ambiente
.venv\Scripts\activate.bat

# Teste com dados de exemplo
python src/main.py --sample --dashboard --report
```

### Opção 3: Usar os Módulos
```python
from src.data_loader import DataLoader
from src.data_analyzer import DataAnalyzer
from src.visualizer import DataVisualizer

# Seu código aqui...
```

## 🛠️ Scripts Úteis

- `install.bat` - Instala todas as dependências
- `run_jupyter.bat` - Inicia Jupyter Lab
- `src/main.py` - Script principal para análises

## 🔧 Comandos Importantes

```cmd
# Ativar ambiente virtual
.venv\Scripts\activate.bat

# Desativar ambiente virtual
deactivate

# Instalar nova biblioteca
pip install nome-da-biblioteca

# Atualizar requirements.txt
pip freeze > requirements.txt

# Executar testes
pytest tests/
```

## 📁 Estrutura de Arquivos

```
Python Analise/
├── src/                    # Módulos Python
├── notebooks/              # Jupyter notebooks
├── data/                   # Seus dados
├── tests/                  # Testes
├── install.bat            # Instalar dependências
├── run_jupyter.bat        # Iniciar Jupyter
└── requirements.txt       # Dependências
```

## 🎯 Próximos Passos

1. **Teste os notebooks** - Comece com `01_introducao_analise_dados.ipynb`
2. **Use seus dados** - Coloque seus arquivos CSV/Excel na pasta `data/`
3. **Personalize** - Modifique os módulos conforme suas necessidades

## ❓ Problemas Comuns

**Erro de caminho com espaços?**
- Use aspas: `"caminho com espaços"`
- Ou use os scripts .bat que já resolvem isso

**Biblioteca não encontrada?**
- Certifique-se que o ambiente virtual está ativado
- Execute `install.bat` novamente

**Jupyter não abre?**
- Execute `run_jupyter.bat`
- Ou ative o ambiente e execute `jupyter lab`
