from API_BBG import API_BBG
from SQL_Server_Connection import SQL_Server_Connection

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns
%matplotlib inline

API_BBG = API_BBG()

tickers = ['CRY Index',
    'BBG002SBKDB7',
    'CO1 Comdty',
    'IBOV Index',
    'EWZ Index',
    'MEXBOL Index',
    'EEM US Equity',
    'S 1 COMB Comdty',
    'C 1 Comdty',
    'QW1 Comdty',
    'LC1 Comdty',
    'LH1 Comdty',
    'RR1 Comdty',
    'CL1 Comdty',
    'IOE1 COMB Comdty',
    'USDBRL Curncy',
    'USDMXN Curncy',
    'USDCLP Curncy',
    'USDCOP Curncy',
    'USDZAR Curncy',
    'USDTRY Curncy',
    'USDPEN Curncy']
fields= ['PX_LAST']
iniDate = 20200101
endDate = 20210212

RawBBGData = API_BBG.BBG_POST(bbg_request='BDH'
    ,tickers=tickers
    ,fields=fields
    ,date_start=iniDate
    ,date_end=endDate)

# Pivot Data
PivotData = RawBBGData.pivot_table(index='Refdate'
    ,columns='Ticker'
    ,values='PX_LAST')
PivotData.rename(columns={'BBG002SBKDB7': 'CRY FOOD Index'}, inplace=True)
PivotData.dropna(inplace=True)

PivotData = PivotData[[
    'IBOV Index',
    'EWZ Index',
    'MEXBOL Index',
    'EEM US Equity',
    'CRY Index',
    'CRY FOOD Index',
    'CO1 Comdty',
    'S 1 COMB Comdty',
    'C 1 Comdty',
    'QW1 Comdty',
    'LC1 Comdty',
    'LH1 Comdty',
    'RR1 Comdty',
    'CL1 Comdty',
    'IOE1 COMB Comdty',
    'USDBRL Curncy',
    'USDMXN Curncy',
    'USDCLP Curncy',
    'USDCOP Curncy',
    'USDZAR Curncy',
    'USDTRY Curncy',
    'USDPEN Curncy',
    ]]

# Return Based
Return_PivotData = PivotData/PivotData.shift(1)-1
Return_PivotData.dropna(inplace=True)

Base_DF = PivotData

######### 1Y #########
startDate = '2020-02-12'
Period = '1Y'

# Slice DataFrame
Slice_DF = Base_DF.loc[Base_DF.index>=startDate]

Slice_DF.corr().to_csv('Corr_1Y.csv')

plt.figure(figsize=(16, 12))
sns_plot = sns.heatmap(Slice_DF.corr(), cmap='mako_r', annot=True)
sns_plot.set_ylim()

figure = sns_plot.get_figure()
figure.savefig(f"Corr_{Period}.jpg")

######### 5Y #########
startDate = '2016-02-12'
Period = '5Y'

# Slice DataFrame
Slice_DF = Base_DF.loc[Base_DF.index>=startDate]

Slice_DF.corr()
plt.figure(figsize=(16, 12))
sns_plot = sns.heatmap(Slice_DF.corr(), cmap='mako_r', annot=True)
sns_plot.set_ylim()

figure = sns_plot.get_figure()
figure.savefig(f"Corr_{Period}.jpg")

######### 10Y #########
startDate = '2011-02-12'
Period = '10Y'

# Slice DataFrame
Slice_DF = Base_DF.loc[Base_DF.index>=startDate]

Slice_DF.corr()
plt.figure(figsize=(16, 12))
sns_plot = sns.heatmap(Slice_DF.corr(), cmap='mako_r', annot=True)
sns_plot.set_ylim()

figure = sns_plot.get_figure()
figure.savefig(f"Corr_{Period}.jpg")