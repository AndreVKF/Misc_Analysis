from fbprophet import Prophet
import pandas as pd

from SQL_Server_Connection import SQL_Server_Connection

import matplotlib.pyplot as plt

dataset = pd.read_csv('acoes.csv')
# dataset.set_index(keys=['Date'], inplace=True)

dataset = dataset[['Date', 'BOVA']].rename(columns={'Date': 'ds', 'BOVA': 'y'})

# Modelo
modelo = Prophet()
modelo.fit(dataset)

futuro = modelo.make_future_dataframe(periods=90)
previsoes = modelo.predict(futuro)

# Gráfico das previsões
modelo.plot(previsoes, xlabel='Data', ylabel='Preço');

########## UST Test ##########
SQL_Server_Connection = SQL_Server_Connection(database='PM')
Q = """
SELECT 
	IndexesValue.Date 
	,RiskFactor.Name
	,IndexesValue.Value
FROM 
	IndexesValue 
LEFT JOIN 
	RiskFactor ON RiskFactor.Id=IndexesValue.Id_RiskFactor 
WHERE 
	Id_RiskFactor=101 
ORDER BY 
	Date"""

UST10Y = SQL_Server_Connection.getData(query=Q, dtparse=['Date'])
plt.plot(UST10Y['Date'], UST10Y['Value'])

dataset = UST10Y[['Date', 'Value']].rename(columns={'Date': 'ds', 'Value': 'y'})

# Model Training
modelo = Prophet()
modelo.fit(dataset)

futuro = modelo.make_future_dataframe(periods=90)
previsoes = modelo.predict(futuro)

modelo.plot(previsoes, xlabel='Data', ylabel='UST10Y');