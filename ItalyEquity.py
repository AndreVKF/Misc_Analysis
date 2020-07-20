from API_BBG import *

############# Italy #############

tckList = ['A2A IM Equity','AMP IM Equity','ATL IM Equity','AZM IM Equity','BGN IM Equity','BAMI IM Equity','BPE IM Equity','BRE IM Equity','BZU IM Equity','CPR IM Equity','CNHI IM Equity','DIA IM Equity','ENEL IM Equity','ENI IM Equity','EXO IM Equity','RACE IM Equity','FCA IM Equity','FBK IM Equity','G IM Equity','ISP IM Equity','IG IM Equity','JUVE IM Equity','LDO IM Equity','MB IM Equity','MONC IM Equity','PIRC IM Equity','PST IM Equity','PRY IM Equity','REC IM Equity','SPM IM Equity','SFER IM Equity','SRG IM Equity','STM IM Equity','TIT IM Equity','TEN IM Equity','TRN IM Equity','UBI IM Equity','UCG IM Equity','UNI IM Equity','US IM Equity']

sectorDF = BBG_POST('BDP', tckList, ['INDUSTRY_SECTOR', 'CUR_MKT_CAP'])
sectorDF.reset_index(inplace=True)
sectorDF.rename(columns={'index': 'Ticker'}, inplace=True)

sectorDF[(sectorDF['INDUSTRY_SECTOR']=='Consumer, Non-cyclical')]
sectorDF[(sectorDF['INDUSTRY_SECTOR']=='Energy')]

priceDF = BBG_POST('BDH', tckList, 'PX_LAST', 20200101, 20200312)
priceDF = priceDF.dropna()


# Consolidate priceDF #
consDF = priceDF.merge(sectorDF, how='left', on='Ticker')

consDF = consDF.groupby(['Refdate', 'INDUSTRY_SECTOR']).apply(lambda x: pd.Series([sum(x.PX_LAST)*sum(x.CUR_MKT_CAP)/sum(x.CUR_MKT_CAP)]))
consDF.reset_index(inplace=True)
consDF.rename(columns={0 : 'Index_Value'}, inplace=True)

consDF['Country'] = 'Italy'

consDF.to_csv('C:\\Users\\andre\\Documents\\Python\\Analysis\\Italy_Tableau.csv')

pd.pivot_table(consDF, values=['Index_Value'], index='Refdate', columns='INDUSTRY_SECTOR').to_csv('C:\\Users\\andre\\Documents\\Python\\Analysis\\Italy_Equity.csv')

############# Brazil #############
tckList = ['VALE3 BS Equity','ITUB4 BS Equity','BBDC4 BS Equity','B3SA3 BS Equity','PETR4 BS Equity','ABEV3 BS Equity','BBAS3 BS Equity','ITSA4 BS Equity','PETR3 BS Equity','LREN3 BS Equity','JBSS3 BS Equity','WEGE3 BS Equity','MGLU3 BS Equity','SUZB3 BS Equity','BBDC3 BS Equity','RADL3 BS Equity','VIVT4 BS Equity','EQTL3 BS Equity','GNDI3 BS Equity','RENT3 BS Equity','BBSE3 BS Equity','RAIL3 BS Equity','SBSP3 BS Equity','UGPA3 BS Equity','BRDT3 BS Equity','CCRO3 BS Equity','HYPE3 BS Equity','BRFS3 BS Equity','LAME4 BS Equity','EGIE3 BS Equity','TIMP3 BS Equity','GGBR4 BS Equity','YDUQ3 BS Equity','COGN3 BS Equity','NTCO3 BS Equity','VVAR3 BS Equity','KLBN11 BS Equity','SULA11 BS Equity','SANB11 BS Equity','BRML3 BS Equity','CMIG4 BS Equity','BTOW3 BS Equity','IRBR3 BS Equity','HAPV3 BS Equity','EMBR3 BS Equity','CSAN3 BS Equity','ELET3 BS Equity','FLRY3 BS Equity','QUAL3 BS Equity','TOTS3 BS Equity','CRFB3 BS Equity','AZUL4 BS Equity','BPAC11 BS Equity','TAEE11 BS Equity','MULT3 BS Equity','ELET6 BS Equity','BRAP4 BS Equity','CIEL3 BS Equity','ENBR3 BS Equity','CYRE3 BS Equity','BRKM5 BS Equity','CSNA3 BS Equity','MRVE3 BS Equity','MRFG3 BS Equity','GOAU4 BS Equity','IGTA3 BS Equity','USIM5 BS Equity','HGTX3 BS Equity','CVCB3 BS Equity','ECOR3 BS Equity','GOLL4 BS Equity','SMLS3 BS Equity']

sectorDF = BBG_POST('BDP', tckList, ['INDUSTRY_SECTOR', 'CUR_MKT_CAP'])
sectorDF.reset_index(inplace=True)
sectorDF.rename(columns={'index': 'Ticker'}, inplace=True)

sectorDF[(sectorDF['INDUSTRY_SECTOR']=='Consumer, Cyclical')]

priceDF = BBG_POST('BDH', tckList, 'PX_LAST', 20200101, 20200312)
priceDF = priceDF.dropna()


# Consolidate priceDF #
consDF = priceDF.merge(sectorDF, how='left', on='Ticker')
# pd.pivot_table(consDF[(consDF['INDUSTRY_SECTOR']=='Consumer, Non-cyclical')], values='PX_LAST', columns='Ticker', index='Refdate').to_csv('C:\\Users\\andre\\Documents\\Python\\Analysis\\BZ_Consumer_Non_Cyclical.csv')

consDF = consDF.groupby(['Refdate', 'INDUSTRY_SECTOR']).apply(lambda x: pd.Series([sum(x.PX_LAST)*sum(x.CUR_MKT_CAP)/sum(x.CUR_MKT_CAP)]))
consDF.reset_index(inplace=True)
consDF.rename(columns={0 : 'Index_Value'}, inplace=True)

consDF['Country'] = 'Brazil'

consDF.to_csv('C:\\Users\\andre\\Documents\\Python\\Analysis\\BZ_Tableau.csv')

pd.pivot_table(consDF, values=['Index_Value'], index='Refdate', columns='INDUSTRY_SECTOR').to_csv('C:\\Users\\andre\\Documents\\Python\\Analysis\\BZ_Equity.csv')