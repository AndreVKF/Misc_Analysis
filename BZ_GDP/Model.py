from SQL_Server_Connection import SQL_Server_Connection

from sklearn.svm import SVR
from sklearn.linear_model import LinearRegression
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.impute import KNNImputer
from sklearn.metrics import mean_absolute_error


import matplotlib.pyplot as plt
import seaborn as sns

import pandas as pd
import numpy as np

# Imports
Macro_DB = SQL_Server_Connection(database='Macro')

# Get data
query = f"""
    SELECT
        *
    FROM
        v_MainMonitor
    WHERE
        Id_Index IN (2,5,6,10,1708,1740,1893,1894,1895,1724)"""

base = Macro_DB.getData(query=query, dtparse=['Date'])

# Pivot Data
base_pivot = base.pivot_table(values=['Index_Value'], index=['Date'], columns=['Index_Name'])['Index_Value']
# base_pivot.loc['2020-09-30', 'Unemployment Rate'] = 14.4
# base_pivot.to_csv('C:\\Users\\andre\\Documents\\Python\\Analysis\\csv\\All_data.csv')

# Base for testing
base_GDP = pd.DataFrame(base_pivot['Real GDP'].dropna())

# Adjusting for Quarterly Data
########## MoM Data ##########
cols_MoM = ['Consumer Prices'
    ,'Producer Prices'
    ,'Retail Sales'
    ,'Brazil Indus Prod SA MoM 2012']

# base_pivot[cols_MoM].to_csv('C:\\Users\\andre\\Documents\\Python\\Analysis\\csv\\MoM.csv')

# cols_MoM = ['Retail Sales'
#     ,'Brazil Indus Prod SA MoM 2012']

MoM_Adj_DF = ((1 + base_pivot[cols_MoM]/100).rolling(window=3).apply(np.prod, raw=True) - 1)*100

########## Monthly Data ##########
cols_Monthly = ['Capacity Utilization'
    ,'Unemployment Rate'
    ,'Markit Brazil Composite PMI Ou'
    ,'Markit Brazil Manufacturing PM'
    ,'Markit Brazil Services PMI Bus']

Monthly_DF = base_pivot[cols_Monthly].rolling(window=3).mean()

########## Base Data Merged ##########
Monthly_Merge_DF = MoM_Adj_DF.merge(Monthly_DF, how='left', left_index=True, right_index=True)
Monthly_Merge_DF = Monthly_Merge_DF[
    ['Consumer Prices',
    'Producer Prices',
    'Retail Sales',
    'Brazil Indus Prod SA MoM 2012',
    'Capacity Utilization',
    'Unemployment Rate',
    'Markit Brazil Composite PMI Ou',
    'Markit Brazil Manufacturing PM',
    'Markit Brazil Services PMI Bus']]

########## Merged Data ##########
# Merge Data
Merge_Data = base_GDP.merge(MoM_Adj_DF, how='left', left_index=True, right_index=True)
Merge_Data = Merge_Data.merge(Monthly_DF, how='left', left_index=True, right_index=True)

# Merge_Data = Merge_Data.iloc[0:-1, :]

# Fill Null with KNN proxy
imputer = KNNImputer(n_neighbors=2)
Merge_Filled = imputer.fit_transform(Merge_Data)
Merge_Data = pd.DataFrame(Merge_Filled, columns=Merge_Data.columns)

# Drop na data
Base_DF = Merge_Data.dropna()
Base_DF = Base_DF[
    ['Real GDP',
    # 'Consumer Prices',
    # 'Producer Prices',
    'Retail Sales',
    'Brazil Indus Prod SA MoM 2012',
    'Capacity Utilization',
    'Unemployment Rate',
    'Markit Brazil Composite PMI Ou',
    'Markit Brazil Manufacturing PM',
    'Markit Brazil Services PMI Bus']]

########## Using Whole Data ##########
x = Base_DF.iloc[:, 1:].values
y = Base_DF.iloc[:, 0:1].values

# Escalonamento dos Dados
scaler_x = StandardScaler()
x_scaled = scaler_x.fit_transform(x)

scaler_y = StandardScaler()
y_scaled = scaler_y.fit_transform(y.reshape(-1, 1))

########## SVR ##########
regressor_SVM = SVR(kernel='rbf', C=2.5)
regressor_SVM.fit(x_scaled, y_scaled)

regressor_SVM.score(x_scaled, y_scaled)

plt.scatter(Base_DF.index, Base_DF['Real GDP'].values, s=5, c="b", label="Real GDP")
plt.plot(Base_DF.index, scaler_y.inverse_transform(regressor_SVM.predict(x_scaled)), c="r", label="SVR Estimado")
plt.legend(loc='best')
plt.show()

########## NN ##########
regressor_NN = MLPRegressor(verbose=True, hidden_layer_sizes=(10, 10, 10), tol=0.0001, max_iter=1000)
regressor_NN.fit(x_scaled, y_scaled)

regressor_NN.score(x_scaled, y_scaled)

plt.scatter(Base_DF.index, Base_DF['Real GDP'].values, s=5, c="b", label="Real GDP")
plt.plot(Base_DF.index, scaler_y.inverse_transform(regressor_NN.predict(x_scaled)), c="r", label="NN Estimado")
plt.legend(loc='best')
plt.show()

# Teste

# scaler_y.inverse_transform(regressor_NN.predict(scaler_x.fit_transform(Merge_Data.iloc[-1:, 1:].values).reshape(1, -1)))
# scaler_y.inverse_transform(regressor_NN.predict(scaler_x.fit_transform((Monthly_Merge_DF.loc['2020-09-30', :].values).reshape(1, -1))))

mae = mean_absolute_error(y_scaled, regressor_NN.predict(x_scaled))

########## Train Test Split NN ##########
# Split
x_treinamento, x_teste, y_treinamento, y_teste = train_test_split(x_scaled, y_scaled, test_size=0.2, random_state=0)

# Regressor
regressorTeste_NN = MLPRegressor(verbose=True, hidden_layer_sizes=(10, 10), tol=0.0001, max_iter=1000)
regressorTeste_NN.fit(x_treinamento, y_treinamento)

# Score on training set
regressorTeste_NN.score(x_treinamento, y_treinamento)

# Score on test set
plt.scatter(np.linspace(1,len(x_teste), num=len(x_teste)), scaler_y.inverse_transform(y_teste), s=5, c="b", label="Real GDP")
plt.plot(np.linspace(1,len(x_teste), num=len(x_teste)), scaler_y.inverse_transform(regressorTeste_NN.predict(x_teste)), c="r", label="NN Estimado")
plt.legend(loc='best')
plt.show()

