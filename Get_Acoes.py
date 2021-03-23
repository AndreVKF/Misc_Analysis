import pandas as pd
import numpy as np
from pandas_datareader import data
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

gol_df = data.DataReader(name='GOLL4.SA'
    ,data_source='yahoo'
    ,start='2015-01-01')

# Varias acoes
acoes = ['GOLL4.SA'
    ,'CVCB3.SA'
    ,'WEGE3.SA'
    ,'MGLU3.SA'
    ,'TOTS3.SA'
    ,'BOVA11.SA']

acoes_df = pd.DataFrame()
for acao in acoes:
    acoes_df[acao] = data.DataReader(acao
        ,data_source='yahoo'
        ,start='2015-01-01')['Close']

rename_cols = {'GOLL4.SA': 'GOL'
    ,'CVCB3.SA': 'CVC'
    ,'WEGE3.SA': 'WEGE'
    ,'MGLU3.SA': 'MGLU'
    ,'TOTS3.SA': 'TOTS'
    ,'BOVA11.SA': 'BOVA'}

acoes_df.rename(columns=rename_cols
    ,inplace=True)

# Check for null
acoes_df.isnull().sum()
acoes_df.dropna(inplace=True)

# Save to csv
acoes_df.to_csv('acoes.csv')

# Graficos histograma simples
sns.histplot(acoes_df['GOL']);

# Gráfico de todas as acoes
plt.figure(figsize=(10, 50))
i = 1
for i in np.arange(1, len(acoes_df.columns)):
    plt.subplot(7, 1, i + 1)
    sns.histplot(acoes_df[acoes_df.columns[i]], bins=25, kde=True)
    plt.title(acoes_df.columns[i])

# Gráfico de boxplot
sns.boxplot(x = acoes_df['GOL']);

plt.figure(figsize=(10, 50))
i = 1
for i in np.arange(1, len(acoes_df.columns)):
    plt.subplot(7, 1, i + 1)
    sns.boxplot(x = acoes_df[acoes_df.columns[i]])
    plt.title(acoes_df.columns[i])

# Gráfico de preços
acoes_df.plot(figsize = (15, 7), title = 'Histórico do preço das ações');

# Gráfico de preços normalizado
acoes_df_normalizado = acoes_df/acoes_df.iloc[0]
acoes_df_normalizado.plot(figsize = (15, 7), title = 'Histórico do preço das ações normalizado');

# Gráficos dinâmicos
# Preços nominais
figura = px.line(title = 'Histórico do preço das ações')
for i in acoes_df.columns[0:]:
    figura.add_scatter(x=acoes_df.index, y=acoes_df[i], name=i)
figura.show()

# Preços normalizados
figura = px.line(title = 'Histórico do preço das ações')
for i in acoes_df_normalizado.columns[0:]:
    figura.add_scatter(x=acoes_df_normalizado.index, y=acoes_df_normalizado[i], name=i)
figura.show()