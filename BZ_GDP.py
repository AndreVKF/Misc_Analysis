from SQL_Server_Connection import SQL_Server_Connection

from sklearn.svm import SVR
from sklearn.linear_model import LinearRegression
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.impute import KNNImputer

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

########## Latest ##########
# Merge Data
Merge_Data = base_GDP.merge(MoM_Adj_DF, how='left', left_index=True, right_index=True)
Merge_Data = Merge_Data.merge(Monthly_DF, how='left', left_index=True, right_index=True)

########## Fill Null with KNN ##########
imputer = KNNImputer(n_neighbors=2)
Merge_Filled = imputer.fit_transform(Merge_Data)
Merge_Data = pd.DataFrame(Merge_Filled, columns=Merge_Data.columns)

########## Testes ##########
# Todos os dados
Base_DF = Merge_Data.dropna()

# Drop Consumer Prices / Producer Prices
Base_DF = Merge_Data.drop(columns={'Consumer Prices', 'Producer Prices'}).dropna()

# Drop Markit PMI Columns
Base_DF = Merge_Data.drop(columns={'Markit Brazil Composite PMI Ou',
    'Markit Brazil Manufacturing PM',
    'Markit Brazil Services PMI Bus'}).dropna()

# Drop Markit PMI Columns/Unemployment Rate
Base_DF = Merge_Data.drop(columns={'Markit Brazil Composite PMI Ou',
    'Markit Brazil Manufacturing PM',
    'Markit Brazil Services PMI Bus',
    'Unemployment Rate'}).dropna()

# Only with Retail Sales/Industrial Production
Base_DF = Merge_Data[['Real GDP',
    'Retail Sales',
    'Brazil Indus Prod SA MoM 2012']].dropna()

# Correlation heatmap
Base_DF.corr()

# Test Data
x_Test = Base_DF.iloc[-1, 1:].values
y_Test = Base_DF.iloc[-1, 0:1].values

# DataFrame to np.values
x = Base_DF.iloc[:, 1:].values
y = Base_DF.iloc[:, 0:1].values

# Escalonamento
scaler_x = StandardScaler()
x_scaled = scaler_x.fit_transform(x)
x_Test_scaled = scaler_x.fit_transform(x_Test.reshape(1, -1))

scaler_y = StandardScaler()
y_scaled = scaler_y.fit_transform(y.reshape(-1, 1))

# Split
x_treinamento, x_teste, y_treinamento, y_teste = train_test_split(x_scaled, y_scaled, test_size=0.2, random_state=0)

######################## Linear Regression ########################
regressor_Linear = LinearRegression()
regressor_Linear.fit(x_scaled, y_scaled)

regressor_Linear.score(x_scaled, y_scaled)

previsao = regressor_Linear.predict(x_Test_scaled)
scaler_y.inverse_transform(previsao)

######################## Polynomial Regression ########################
poly = PolynomialFeatures(3)
x_scaled_poly = poly.fit_transform(x_scaled)
x_test_poly = poly.fit_transform(x_Test.reshape(1, -1))

regressor_Poly = LinearRegression()
regressor_Poly.fit(x_scaled_poly, y_scaled)

regressor_Poly.score(x_scaled_poly, y_scaled)

previsao = regressor_Poly.predict(scaler_x.fit_transform(x_test_poly))
scaler_y.inverse_transform(previsao)

######################## SVR ########################
regressor_SVM = SVR(kernel='rbf', C=2)
regressor_SVM.fit(x_scaled, y_scaled)

regressor_SVM.score(x_scaled, y_scaled)

previsao = regressor_SVM.predict(scaler_x.fit_transform(x_Test.reshape(1, -1)))
scaler_y.inverse_transform(previsao)


plot_DF = scaler_y.inverse_transform(regressor_SVM.predict(x_scaled))
y.reshape(1, -1)

plt.scatter(Base_DF.index, Base_DF['Real GDP'].values, s=5, c="b", label="Real GDP")
plt.plot(Base_DF.index, scaler_y.inverse_transform(regressor_SVM.predict(x_scaled)), c="r", label="Estimado")
plt.legend(loc='best')
plt.show()

############ SVR Linear ############
regressor_SVM_Linear = SVR(kernel='linear', C=2)
regressor_SVM_Linear.fit(x_scaled, y_scaled)

regressor_SVM_Linear.score(x_scaled, y_scaled)

previsao = regressor_SVM_Linear.predict(scaler_x.fit_transform(x_Test.reshape(1, -1)))
scaler_y.inverse_transform(previsao)

############ SVR Polynomial ############
regressor_SVM_Poly = SVR(kernel='poly', degree=3, C=1)
regressor_SVM_Poly.fit(x_scaled, y_scaled)

regressor_SVM_Poly.score(x_scaled, y_scaled)

previsao = regressor_SVM_Poly.predict(scaler_x.fit_transform(x_Test.reshape(1, -1)))
scaler_y.inverse_transform(previsao)

############ NN ############
regressor_NN = MLPRegressor(verbose=True, hidden_layer_sizes=(6, 6), tol=0.0001, max_iter=1000)
regressor_NN.fit(x_scaled, y_scaled)

previsao = regressor_NN.predict(scaler_x.fit_transform(x_Test.reshape(1, -1)))
scaler_y.inverse_transform(previsao)

plt.scatter(Base_DF.index, Base_DF['Real GDP'].values, s=5, c="b", label="Real GDP")
plt.plot(Base_DF.index, scaler_y.inverse_transform(regressor_NN.predict(x_scaled)), c="r", label="Estimado")
plt.legend(loc='best')
plt.show()

