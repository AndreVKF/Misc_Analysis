import pandas as pd
from SQL_Server_Connection import SQL_Server_Connection

PM = SQL_Server_Connection(database='PM')

FIC_II_DB = PM.getData(query="""SELECT 
        Refdate
        ,Share_Subscriptions.Id_ShareMov
        ,Share_Subscriptions.Quote_Date
        ,Shareholders.Id AS Id_Shareholder
        ,Shareholders.Name AS Shareholder
        ,Shareholders.Info1
        ,Share_Subscriptions.Td_OpenShares
        ,Share_Subscriptions.Td_CloseShares
    FROM 
        Share_Subscriptions 
    LEFT JOIN Shareholders ON Shareholders.Id=Share_Subscriptions.Id_Shareholder
    LEFT JOIN Entities ON Entities.Id=Share_Subscriptions.Id_Entity
    WHERE 
        Refdate='20201130' 
        AND Id_Shareholder IN (SELECT Id FROM Shareholders WHERE Id_Shareholders_Distribuidores=1)
        AND Id_Entity=18""", dtparse=['Refdate', 'Quote_Date'])
FIC_II_DB['Info1'] = pd.to_numeric(FIC_II_DB['Info1'])

FIC_II = pd.read_excel('C:/Users/andre/Desktop/2020-11-30 - Come Cotas/2020-03-12 - Ajuste Final.xls', sheet_name='Plan1')

Merge_FIC_II = FIC_II.merge(FIC_II_DB, how='left', on=['Quote_Date', 'Info1'])
Adj = Merge_FIC_II.loc[(~Merge_FIC_II['Id_ShareMov'].isnull())]

Adj.to_csv('C:/Users/andre/Desktop/2020-11-30 - Come Cotas/Adj_FIC_II.csv')

