# Diretório de Dados

Este diretório contém os datasets utilizados no projeto de análise de dados.

## Estrutura

- `raw/` - Dados brutos, não processados
- `processed/` - Dados processados e limpos
- `external/` - Dados de fontes externas
- `sample/` - Dados de exemplo para testes

## Formatos Suportados

- CSV (.csv)
- Excel (.xlsx, .xls)
- JSON (.json)
- Parquet (.parquet)
- HDF5 (.h5, .hdf5)
- Pickle (.pkl, .pickle)

## Convenções de Nomenclatura

- Use nomes descritivos e em minúsculas
- Separe palavras com underscore (_)
- Inclua data quando relevante: `vendas_2023_01.csv`
- Use prefixos para categorizar: `raw_vendas.csv`, `clean_vendas.csv`

## Gitignore

Por segurança, a maioria dos arquivos de dados são ignorados pelo Git.
Apenas dados de exemplo na pasta `sample/` são versionados.
