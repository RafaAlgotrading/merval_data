import yfinance as yf
import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt


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
                    )['Adj Close'][-90:]
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

ccl_prices = pd.DataFrame(columns=usa)
ccl_list= []

for i, value in enumerate(usa):
    ccl_list.append(get_ccl(argy_prices[i], argy_ratios[i], usa_prices[i]))
   
    

ccl_by_ticker = pd.DataFrame()
#Traigo todas las series con los últimos precios de CCL y los pongo en columnas
#   según su activo.
for index, ccl_df in enumerate(ccl_list):
    ccl_by_ticker[usa[index]] = ccl_df['CCL']


#Voy a Argy_prices, agarro el primer activo (puede ser cualquiera),
#tomo su índice y se lo seteo al Df ccl_by_ticker porque quiero que los precios
#que tenga el CCL, tengan fecha minuto a minuto en base al mercado argy.
ccl_by_ticker.set_index(argy_prices[0].index, inplace=True)


ccl_by_ticker.plot(figsize=(12, 8))

plt.title("CCL Prices by asset -in real time-", fontsize=24)
plt.suptitle("Last 90 minutes (01:30hs)")

ccl_prices_day = argy_prices[0].index[-1].strftime('%Y-%m-%d')
plt.xlabel(f"{ccl_prices_day}", fontsize=20)


#Muestro exactamente los valores que toma cáda activo.
for asset in ccl_by_ticker:
    last_value = ccl_by_ticker[asset][-1]
    plt.text(ccl_by_ticker.index[-1],
             last_value,
             f'{asset}- {last_value:.2f}', 
             fontsize=10,
             verticalalignment='center'
             )
    #Al ser muchos activos, la tabla, interfiere en la visualización.
    plt.legend().set_visible(False)






