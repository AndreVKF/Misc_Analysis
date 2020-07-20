from API_BBG import BBG_POST
from SQL_Server_Connection import SQL_Server_Connection

from sklearn.svm import SVR
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

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
        Id_Index IN (1691,5,6,10,1708,1740,1893,1894,1895,1724)"""

base = Macro_DB.getData(query=query, dtparse=['Date'])

# Pivot Data
base_pivot = base.pivot_table(values=['Index_Value'], index=['Date'], columns=['Index_Name'])['Index_Value']

# Base for testing
base_GDP = pd.DataFrame(base_pivot['IBC-Br Mom'].dropna())

# Adjusting for Quarterly Data
########## MoM Data ##########
# cols_MoM = ['Consumer Prices'
#     ,'Producer Prices'
#     ,'Retail Sales'
#     ,'Brazil Indus Prod SA MoM 2012']

cols_MoM = ['Retail Sales'
    ,'Brazil Indus Prod SA MoM 2012']

MoM_Adj_DF = (1 + base_pivot[cols_MoM]/100).rolling(window=3).apply(np.prod, raw=True) - 1

########## Monthly Data ##########
cols_Monthly = ['Capacity Utilization']

Monthly_DF = base_pivot[cols_Monthly].rolling(window=3).mean()

########## Latest ##########
# cols_Latest = ['Unemployment Rate']

# Latest_DF = base_pivot[cols_Latest]/100

# Merge Data
Merge_Data = base_GDP.merge(MoM_Adj_DF, how='left', left_index=True, right_index=True)
# Merge_Data = Merge_Data.merge(Monthly_DF, how='left', left_index=True, right_index=True)
# Merge_Data = Merge_Data.merge(Latest_DF, how='left', left_index=True, right_index=True)

# Test Base_DF
# Base_DF = Merge_Data.dropna()
Base_DF = base_pivot[['IBC-Br Mom',
'Brazil Indus Prod SA MoM 2012',
'Capacity Utilization',
'Retail Sales',
'Unemployment Rate']]
Base_DF = Base_DF.dropna()

# DataFrame to np.values
x = Base_DF.iloc[:, 1:].values
y = Base_DF.iloc[:, 0].values

# Escalonamento
scaler_x = StandardScaler()
x_scaled = scaler_x.fit_transform(x)

scaler_y = StandardScaler()
y_scaled = scaler_y.fit_transform(y.reshape(-1, 1))

# Split
x_treinamento, x_teste, y_treinamento, y_teste = train_test_split(x_scaled, y_scaled, test_size=0.2, random_state=0)

############ SVR ############
regressor_SVM = SVR(kernel='rbf', C=4)
regressor_SVM.fit(x_scaled, y_scaled)

regressor_SVM.score(x_scaled, y_scaled)
regressor_SVM.score(x_teste, y_teste)
regressor_SVM.score(x_treinamento, y_treinamento)

############ NN ############
regressor_NN = MLPRegressor(verbose=True, hidden_layer_sizes=(5, 5), tol=0.00001, max_iter=1000)
regressor_NN.fit(x_scaled, y_scaled)

regressor_NN.score(x_scaled, y_scaled)
regressor_NN.score(x_treinamento, y_treinamento)
regressor_NN.score(x_teste, y_teste)

base_pivot['Consumer Prices'].loc[base_pivot.index>='2000-01-01'].plot()
base_pivot['Brazil Indus Prod SA MoM 2012'].loc[base_pivot.index>='2000-01-01'].plot()