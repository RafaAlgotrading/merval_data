import yfinance as yf
import datetime as dt
import pandas as pd


beginnings = "2024-01-01"
today = dt.datetime.now()

merval_ars = "M.BA"

#Cómo el periodo que especifíco es "max", no hace falta que ponga start y end.
merval = yf.download(merval_ars, interval="1wk", period="max")
merval = merval['Adj Close']

#Hago el resample porque vía yf.download() con interval="1mo" no me traía 
#   bien los datos.
merval_resample = merval.copy().resample('M').last()


datetime_years_index = []
months = ["Enero", "Febrero", "Marzo", "Abril", "Mayo",
    "Junio", "Julio", "Agosto", "Septiembre", "Octubre",
    "Noviembre", "Diciembre"]
months_lists = {}

for index in merval_resample.index:
    if index.year not in datetime_years_index:
        datetime_years_index.append(index.year)
    merval_historical_monthly_state = pd.DataFrame(
        index=datetime_years_index,
        columns=months
        )
    months_lists[
        months[index.month - 1]
        ] = merval_resample[index]
    
    for key, value in enumerate(months_lists):
        print("Key: {} - {}".format(value, months_lists[value]))
        












#for index in merval_resample.index:
    # if index.year not in datetime_years_index:
    #     datetime_years_index.append(index.year)
    # merval_historical_monthly_state = pd.DataFrame(
    #     index=datetime_years_index,
    #     columns=months
    #     )
    # months_lists[
    #     months[index.month - 1]
    #     ] = merval_resample[index]
    
    # for key, value in enumerate(months_lists):
    #     print("Key: {} - {}".format(value, months_lists[value]))
        





        