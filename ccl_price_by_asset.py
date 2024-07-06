import yfinance as yf
import datetime as dt
import pandas as pd


def get_prices(market):
    today = dt.datetime.now()
    yesterday = today - dt.timedelta(days=2)
    prices = []
    for index, ticker in enumerate(market):
        try:
            prices.append(
                yf.download(
                    ticker,
                    interval='1m',
                    period='1d'
                    )['Adj Close'][-250:]
                )
        except Exception as e:
            print("No se pudo traer los datos", e)
    #Retorna una lista de las series de precios para cada activo
    return prices 


def get_ccl(argy_series, ratios, usa_series):
    
    #Podría hacerlo con un for y más facil? Si
    argy_df = pd.DataFrame(columns=['Argy'])
    usa_df = pd.DataFrame(columns=['USA'])
    
    
    argy_df['Argy'] = argy_series
    argy_df['Index'] = pd.RangeIndex(start=0, stop=len(argy_df))
    
    usa_df['USA'] = usa_series
    usa_df['Index'] = pd.RangeIndex(start=0, stop=len(usa_df))
    
    #No sirve hacer concat porque al no coincidir los indices, no "matchean"
    
    ccl_df = pd.merge(
          argy_df,
          usa_df,
          on='Index',
          ).drop(columns='Index')
    
    ccl_df['CCL'] = (ccl_df['Argy']*ratios)/ccl_df['USA']
    return ccl_df
    
#bma_argy = yf.download('BMA.BA', interval='1d', period='ytd')['Adj Close'][-1]
#bma_usa = yf.download('SPY', interval='1d', period='ytd')['Adj Close'][-1]

   

#==================== PROGRAMA INICIAL ====================
argy = ['SPY.BA', 'QQQ.BA', 'AAPL.BA', 'AMZN.BA', 'GOOGL.BA',
         'MSFT.BA', 'MELI.BA', 'NIO.BA', 'KO.BA', 'TSLA.BA', 'TSM.BA']
argy_ratios = [20, 20, 20, 144, 58, 30, 120, 4, 5, 15, 9]

usa = ['SPY', 'QQQ', 'AAPL', 'AMZN', 'GOOGL', 'MSFT',
       'MELI', 'NIO', 'KO', 'TSLA', 'TSM']

argy_prices = []
usa_prices = []

#Una lista de series de datos con precios para cada activo.
argy_prices = get_prices(argy)
usa_prices = get_prices(usa)

FALOPA = (argy_prices[0] * argy_ratios[0]) / usa_prices[0] 

ccl_prices = pd.DataFrame(columns=usa)
ccl_list= []

for i, value in enumerate(usa):
    print(usa[i])
    ccl_list.append(get_ccl(argy_prices[i], argy_ratios[i], usa_prices[i]))
   
    

ccl_by_ticker = pd.DataFrame()
#Traigo todas las series con los últimos precios de CCL y los pongo en columnas
#   según su activo.
for index, ccl_df in enumerate(ccl_list):
    ccl_by_ticker[usa[index]] = ccl_df['CCL']


































#for i in range(len(argy_prices)):
#    #print(argy[i], usa[i])
#    ccl_prices = {
#       f'{argy[i]} CCL' : (
#       #Le mando, por posición, la serie argy y usa.    
#       get_ccl(argy_prices[i], argy_ratios[i], usa_prices[i])
#       )
#    }
    
    

#for i_series, series in enumerate(argy_prices):
#    #print(f"{argy[i]}\n", argy_prices[i])
#    print(argy[i_series])
#    for i, value in enumerate(series):
#        print(value)
    
    
# ccl_prices = {
#     f'{argy[i_series]} CCL' : (
#         (series[i]*argy_ratios[i_series])/usa_prices[i]
#     ) for i, value in enumerate(argy)
#     }




#for index, ticker in enumerate(argy):
#    hola = yf.download(ticker, start=yesterday, end=today, interval='1m')['Adj Close']

#print(hola)


