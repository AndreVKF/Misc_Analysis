from API_BBG import *
from SQL_Server_Connection import SQL_Server_Connection

Bonds_Connection = SQL_Server_Connection(database='Bonds_DB')
PM_Connection = SQL_Server_Connection(database='PM')

Refdate_List = PM_Connection.getData(query="SELECT DISTINCT Refdate FROM Position WHERE Refdate<'20181008' ORDER BY Refdate DESC", dtparse=['Refdate'])

for Dt in Refdate_List['Refdate'].to_list():
    updateOctanteIndexes(Refdate=Dt, SQL_Server_Connection=PM_Connection)

def updateOctanteIndexes(Refdate, SQL_Server_Connection):
    Query=f"""
        SELECT 
        Refdate
        ,Product
        ,Monitor.ISIN
        ,Outstanding
        ,Products.Cpn
        ,Px_Mid
        ,Yield
        ,Z_Spread
    FROM 
        Bonds_DB.dbo.Monitor 
    LEFT JOIN Bonds_DB.dbo.Products ON Products.Id=Monitor.Id_Product
    LEFT JOIN Countries AS Countries ON Countries.Name=Monitor.Country
    LEFT JOIN Region AS Region ON Countries.Id_Region=Region.Id
    -- Bonds Basket
    WHERE 
        Monitor.Id_Currency=1
        AND Products.Id_SecurityType=1
        AND Monitor.Refdate='{Refdate}'
        AND Monitor.Id_Currency=1
        AND Products.Id_SecurityType=1
        AND Duration>=2
        AND Industry_Group NOT IN ('Sovereign')
        AND Region.Id IN (6, 3)
        AND Countries.Name NOT IN ('United States', 'Canada', 'Cayman Islands', 'Bermuda', 'Argentina')
        AND Monitor.Px_Mid>30
        AND Monitor.Riskfactor_Name NOT IN ('BONO GAR PROV DEL CHUBUT','CITY OF BUENOS AIRES','PROV OF TIERRA DEL FUEGO','PROVINCE OF NEUQUEN','PROVINCIA DE CORDOBA','PROVINCIA DE ENTRE RIOS','PROVINCIA DE RIO NEGRO','RIO ENERGY SA/UGEN SA','ODEBRECHT FINANCE LTD')
        AND Monitor.Rtg_Group >=4 AND Monitor.Rtg_Group <=13.3
    ORDER BY
        Refdate"""

    Main_DF = SQL_Server_Connection.getData(query=Query, dtparse=['Refdate'])

    Ret_DF = Main_DF.groupby(['Refdate']).apply(lambda x: pd.Series(sum(x.Px_Mid*x.Outstanding)/sum(x.Outstanding)))
    Ret_DF.rename(columns={0: 'Price Mid'}, inplace=True)

    Ret_DF['Z_Spread'] = Main_DF.groupby(['Refdate']).apply(lambda x: pd.Series(sum((1 + x.Z_Spread/100) * x.Outstanding)/sum(x.Outstanding)-1) * 100)

    Ret_DF.reset_index(inplace=True)
    Ret_DF.rename(columns={'Refdate': 'Date'}, inplace=True)

    colLIst = ['Date',
        'Id_RiskFactor',
        'Value',
        '1DReturn',
        '5DReturn']

    # Price Index
    Px_Index = Ret_DF
    Px_Index['Id_RiskFactor'] = 734
    Px_Index['Value'] = Px_Index['Price Mid']
    Px_Index['1DReturn'] = None
    Px_Index['5DReturn'] = None
    Px_Index = Px_Index[colLIst]

    # Z_Spread Index
    Z_Spread = Ret_DF
    Z_Spread['Id_RiskFactor'] = 735
    Z_Spread['Value'] = Z_Spread['Z_Spread']
    Z_Spread['1DReturn'] = None
    Z_Spread['5DReturn'] = None
    Z_Spread = Z_Spread[colLIst]

    Insert_DF = pd.concat([Px_Index, Z_Spread], ignore_index=True)
    print(Refdate)

    # Update DataBase
    SQL_Server_Connection.execQuery(query=f"DELETE FROM IndexesValue WHERE Date='{Refdate}' AND Id_RiskFactor IN (734, 735)")
    SQL_Server_Connection.insertDataFrame(tableDB='IndexesValue', df=Insert_DF)