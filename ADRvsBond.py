import pandas as pd
from API_BBG import *

# ADR
ADR_tckList = ['PBR US Equity','GGB US Equity','ITUB US Equity','VALE US Equity','BRFS US Equity','SUZ US Equity','BAK US Equity']

ADR_DF = pd.read_csv('C:\\Users\\andre\\Documents\\Python\\Analysis\\csv\\ADRs.csv', sep=';')

ARD_priceDF = BBG_POST('BDH', ADR_DF['Ticker'].to_list(), 'PX_LAST', 20200101, 20200406)
ARD_priceDF = ARD_priceDF.merge(ADR_DF, how='left', on='Ticker')

# Corp
Corp_DF = pd.read_csv('C:\\Users\\andre\\Documents\\Python\\Analysis\\csv\\CorpBonds.csv', sep=';')

Corp_priceDF = BBG_POST('BDH', Corp_DF['Ticker'].to_list(), 'PX_LAST', 20200101, 20200406)
Corp_priceDF = Corp_priceDF.merge(Corp_DF, how='left', on='Ticker')
Corp_priceDF.rename(columns={'Z_SPRD_MID': 'PX_LAST'}, inplace=True)
Corp_priceDF['Field'] = 'Z_SPREAD'


result = pd.concat([ARD_priceDF, Corp_priceDF])
result['Field'] = 'PX_LAST'

tst = result

tst = pd.concat([tst, Corp_priceDF])

priceDF = priceDF.dropna()

Z_SPRD_MID

tst.to_csv('C:\\Users\\andre\\Documents\\Python\\Analysis\\csv\\ADR_Corp.csv')