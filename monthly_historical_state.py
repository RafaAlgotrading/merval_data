import yfinance as yf
import datetime as dt
import pandas as pd


beginnings = "2024-01-01"
today = dt.datetime.now()

merval_ars = "M.BA"

#Cómo el periodo que especifíco es "max", no hace falta que ponga start y end.
merval = yf.download(merval_ars, interval="1wk", period="max")


#Hago el resample porque vía yf.download() con interval="1mo" no me traía 
#   bien los datos.
merval_resample = merval.copy().resample('M').last()



datetime_years_index = []
months = ["Enero", "Febrero", "Marzo", "Abril", "Mayo",
    "Junio", "Julio", "Agosto", "Septiembre", "Octubre",
    "Noviembre", "Diciembre"]


for index in merval_resample.index:
    if index.year not in datetime_years_index:
        datetime_years_index.append(index.year)
    merval_historical_monthly_values = pd.DataFrame(
        index=datetime_years_index, #Seteo índice eje Y
        columns=months #Seteo índice eje X
        )
    merval_historical_monthly_pct = pd.DataFrame(
        index=datetime_years_index, 
        columns=months 
        )  
    
# name = index2 para que no crashee con el de arriba    
for index2, fila in merval_resample.iterrows():
     merval_historical_monthly_values.loc[
        index2.year,
        months[index2.month - 1]
        ] = fila['Adj Close']

     

merval_pct = pd.DataFrame()

merval_pct['var price'] = merval_resample['Adj Close'].diff()
merval_pct['var pct-%'] = round(
    (
     merval_resample['Adj Close'] / merval_resample['Adj Close'].shift(1) - 1
     ) * 100,
    2)

for index3, fila_pct in merval_pct.iterrows():
     merval_historical_monthly_pct.loc[
        index3.year,
        months[index3.month - 1]
        ] = fila_pct['var pct-%']

#Hacer esto para los valores de 'merval_historical_monthly_pct' con el fin de
#   evitar los nan, es un error grave ya que el promedio queda super desfasado
#   con los valores pequeños de los primeros años. Acá es mucho más lógico.      
merval_historical_monthly_pct.fillna(
    #merval_historical_monthly_pct.mean(),
    0,
    inplace=True
    )
avg_results = pd.DataFrame()
for month in merval_historical_monthly_pct:
    #Le creo el índice con 'avg_result'
    avg_results.loc[
        'avg_result',
        month] = merval_historical_monthly_pct[month].mean()

merval_cumsum_by_year = pd.DataFrame()
for index in merval_historical_monthly_pct.index:
    merval_cumsum_by_year.loc[
        index,
        '% cumsum by year'
        ] = merval_historical_monthly_pct.loc[index].sum()
    
     

     
