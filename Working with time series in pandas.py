#usando pandas e a class em python datetime é possível criar um timestamp do pandas

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
time_stamp = pd.Timestamp(datetime(2017, 1, 1))  #pd.Timestamp é o comando base de tudo 1) esta é uma das formas de criar um timestamp
pd.Timestamp('2017-01-01') == time_stamp  #2) esta também faz a mesma coisa
print(time_stamp) # associa automaticamente com o horário de meia-noite
# o objeto timestap tem vários atributos que podem ser acessados
print(' Este o parametro year: ' + str(time_stamp.year))
print(' Este o parametro day_name: ' + str(time_stamp.day_name()))
# O Objeto Period sempre têm uma frequência (o padrão = meses)
period = pd.Period('2017-01')

print(period.asfreq('D'))  # o objeto também tem métodos de conversão da frequencia, aqui convertemos de meses para dias
print(period.to_timestamp().to_period('M')) # É possóivel converter um objeto de período em um objeto timestamp (evice versa)
# Também é possível fazer cálculos com períodos
print(period+2)
# Timestamps temabém podem ter informações de frequência. 
## Abixo criamos uma timestamp mensal e adicionamos 1. * Observação: a linha abixo não é mais suportada
#pd.Timestamp('2017-01-31', 'M') + 1
# Alternativas
print(pd.Timestamp('2017-01-31', 'M')+ pd.Timedelta(4, unit='W'))
print(pd.Timestamp('2017-01-31') + timedelta(weeks = 4))
#Para criar uma time series precisamos de uma sequência de datas, usamos a função "date_range"
# Para usá-la, precisamos especificar datas de início e fim ou um número de períodos. O padrão é a frequência da data.
# A função retorna uma sequência de datas na forma de um DateTimeindex com as informações de frequência.
index = pd.date_range(start = '2017-1-1', periods = 12, freq = 'M')
#note que, apesar de termos passado o dia 1 de janeiro como início do range, para fins mensais, ele automaticamente
# considerou como último dia de janeiro como o primeiro da série mensal.
print(str(index))
#Você pode converter  este index para um PerioIndex, assim como fizemos anteriormente com objeto timestamp
print(index[0])
print(index.to_period)
#Agora você pode criar um série temporal definido o DateTimeIndex como o índice do seu DataFrame.

#As coluna do DataFrame conendo datas serão atribuídas ao tipo de dados datetime64, onde 'ns' significa nanossegundos
pd.DataFrame({'data':index}).info()
#Vamos criar 12 linhas com duas colunas de dados aleatórios para corresponder ao DateTimeindex
data = np.random.random(size =(12, 2))
print(data)
pd.DataFrame(data = data, index = index).info()
# O pandas permite criar e converter entre várias frequências diferentes.
# As mais importantes estão listadas aqui <ver Frequency Aliases & Time Info>:
# https://datascience103579984.wordpress.com/2019/09/20/manipulating-time-series-data-in-python-from-datacamp/
# Também podermos usar pd.Timestamp() attributes para trabalhar com dias úteis, semanas do ano ou dia do ano.

#__________________________
# You have learned in the video how to create a sequence of dates using pd.date_range().
# You have also seen that each date in the resulting pd.DatetimeIndex is a pd.Timestamp
# with various attributes that you can access to obtain information about the date.
#
# Now, you'll create a week of data, iterate over the result, and obtain the dayofweek
# and day_name() for each date.

# Create the range of dates here
seven_days = pd.date_range(start = '2017-1-1', periods = 7, freq = 'D')

# Iterate over the dates and print the number and name of the weekday
for day in seven_days:
    print(day.dayofweek, day.day_name())

#____________

#Indexing & resampling time series
# Passar datas como strings e converter para datetime64 (pandas data type)
# selecionar sub períodos da série temporal
# Definir e Alterar a frequência do DateTimeIndex
#  Você pode mudar a frequência para um valor maior ou menor
# upsampling: aumetar a frequência temporal, requer gerar dados novos /
# Downsampling: diminiur a frequência temporal, requer agregar os dados
# O primeiro dataset é um dataset com dois anos de preços diários da ação do google.
# você com frequência terá que lidar com datas que são do tipo ojeto ou string

path = r'D:\Rafael\OneDrive\Documentos\projetos_pycharm\Times Series in Python\Data\stock_data\google.csv'
google = pd.read_csv(path)
google.info()
# quando se imprime as primeiras colunas é possível notar que estão no formato string
google.head
# para converter para o formato correto, o pandas tem a funçã to_datetime, basta passar uma coluna ou série de dados
google.Date = pd.to_datetime(google.Date)
# depois de consertada, a coluna pode ser passada para .set_index()
google.set_index('Date', inplace = True)
google.info()
google. rename(columns = {'Close':'price'}, inplace = True)
# O data frame resultante trata toda a série temporal como uma dado de série temporl
# Plotar o preço da ação mostra que ela vem se saindo bem nos últimos dois anos
# com base no datimeindex o pandas já crias rótulos razoáveis para os eixos
import matplotlib.pyplot as plt
google.price.plot(title = 'Google Stock Price')  # Se o dataset tiver muitas colunas, além da de séries de dados, usar subplots = True plota cada uma contra a série temporal.

plt.tight_layout(); plt.show(block=False)
plt.pause(0.001)
# Para selecionar subconjuntos da série temporal você pode usar strings que representam
# todas as datas ou só partes das datas que sejam relevantes. Se passar um ano, retornará todas
# as datas deste ano
google['2015'].info()
# Se passar uma fatia que começa em um mês e termina em outro, obterá todas as datas deste intervalo
google['2015-3': '2016-2'].info()
# observe que o intervalo incluirá as datas de término diferente de outros intervalos no python
# Também é possível selecionar o preço em uma data específica usado .loc
google.loc['2016-6-1','price']
# Nosso DateTimeIndex não tinha informações de frequencia, podemos definilas usando .asfrq
google.asfreq('D').info() # ajusta para dias corridos
# Como rsultado, o DateTimeIndex agora contém muitas datas em que as ações não foram compradas ou vendidas
# Essas novas datas não tem valores da ação correspondentes
google.asfreq('D').head()
# ISto é chamado de upsamplig porque o novo DataFrame tem mais datas (maior frequencia) que o original

# Também é possível converter o DateTimeIndex em frequencia de dias úteis
google = google.asfreq('B')
google.info()
# è possível usar o método isnull para verificar em quais datas os valores estão nulos porque nao houve negociação
google[google.price.isnull()]


#__________
#Exercício
#_______
#We have already imported pandas as pd and matplotlib.pyplot as plt and we have already loaded the 'yahoo.csv'
# file in a variable yahoo with DateTimeIndex and a single column price.
#Create an empty pd.DataFrame() called prices.
#Iterate over a list containing the three years, 2013, 2014, and 2015, as string, and in each loop:
#Use the iteration variable to select the data for this year and the column price.
#Use .reset_index() with drop=True to remove the DatetimeIndex.
#Rename the column price column to the appropriate year.
#Use pd.concat() to combine the yearly data with the data in prices along axis=1.
#Plot prices.

#Import data
path = r'D:\Rafael\OneDrive\Documentos\projetos_pycharm\Times Series in Python\Data\stock_data\yahoo.csv'
yahoo = pd.read_csv(path, parse_dates = ['date'], index_col='date')
yahoo.info()
# Create dataframe prices here



prices = pd.DataFrame()

# Select data for each year and concatenate with prices here
for year in ['2013', '2014', '2015']:
    price_per_year = yahoo.loc[year, ['price']].reset_index(drop=True)   # Esta linha do código filtra somente as linhas do dataset que contém na string o valor do ano que está sendo iterado. O resultado é um dicionário cmom duas colunas, uma com a data (que fucniona como índice = index e a outra com o preço. Quando se aplico, ao final, o étodo reset-index, a coluna de data é removida, sendo gerada uma nova coluna de índice que coça em 0 e vai até a última linha
    price_per_year.rename(columns={'price': year}, inplace=True) # Nesta iteração, há duas colunas, uma de índide (sem nome) e outra com os preços, 'price'. O que esta linha faz a substituir o nome da coluna "price" pelo ano respectivo.
    prices = pd.concat([prices, price_per_year], axis=1) # Antes da primiera iteração, prices é um DF vazio. Após a primeira, terá um index e os preços de 2013. Após a segunda, a colunas com os preços de 2014 será contenada após 2013, e assim por diante. Ou seja, ao final o DF não tinha mais datas.

# Plot prices
prices.plot()
plt.show(block = False)
plt.pause(0.001)

#exercicio
#Calculating stock price changes
# You have learned in the video how to calculate returns using current and shifted prices
# #as input. Now you'll practice a similar calculation to calculate absolute changes from
# current and shifted prices, and compare the result to the function .diff().
# Created shifted_30 here
yahoo['shifted_30'] = yahoo.price.shift(periods = 30)

# Subtract shifted_30 from price
yahoo['change_30'] =  yahoo['price'] - yahoo['shifted_30'] #__________
#Exercício - COm o código abaixo é muito fácil a serie em dias ou meses.
# Get the 30-day price difference#_______
yahoo['diff_30'] = yahoo.price.diff(periods = 30)
#Set and change time series frequency
# Inspect the last five rows of price#In the video, you have seen how to assign a frequency to a
print(yahoo.tail(5))# DateTimeIndex, and then change this frequency.

# Show the value_counts of the difference between change_30 and diff_30#Now, you'll use data on the daily carbon monoxide concentration
print(yahoo.change_30.sub(yahoo.diff_30).value_counts())# in NYC, LA and Chicago from 2005-17.

#You'll set the frequency to calendar daily and then resample
# to monthly frequency, and visualize both series to see how the
# different frequencies affect the data.

#We have already imported pandas as pd and matplotlib.pyplot as plt and we
# have already loaded the co_cities.csv file in a variable co.

#Inspect co using .info().
#Use .asfreq() to set the frequency to calendar daily.
#Show a plot of 'co' using subplots=True.
#Change the the frequency to monthly using the alias 'M'.
#Show another plot of co using subplots=True.


# path = r'D:\Rafael\OneDrive\Documentos\projetos_pycharm\Times Series in Python\Data\air_quality_data\co_cities.csv'
# co = pd.read_csv(path)
#
#
# # Inspect data
# print(co.info())
# co.head()
# # Set the frequency to calendar daily
# co = co.asfreq('D')
#
# # Plot the data
# co.plot()
# plt.show()
#
#
# # Set frequency to monthly
# co = co.asfreq('M')
#
# # Plot the data
# co.plot()
# plt.show()
#_____________
#Lags, changes and returns for stock price series
# É possível movimentar os dados no tempo, de forma que a gente possa comprar valores em diferentes pontos do tempo.
# Isto envolve mover os dados para o futuro ou a criação de defasagens ao mover os dados para o passado.
# Também podemos calcular as variações nos valores em diferentes momentos, incluindo em termos percentuais.


#Vamos importar noavemente a série tempora de preços de ações do Google

path = r'D:\Rafael\OneDrive\Documentos\projetos_pycharm\Times Series in Python\Data\stock_data\google.csv'

google = pd.read_csv(path, parse_dates = ['Date'], index_col='Date')
google.info()
# ao invés de usarmos pdtodate, podemos já dizer ao comando read_csv para carregar algumas das colunas ocmo datas.
# para isto basta fornecê-las como uma lista.
#Também é possível definir uma coluna como índice forcenedno o parâmtero index_col
#Como resultado, obtemos uma série temporal já formatada
google.head()
google['price'] = google['Close']
#O primeito métodos de séries temporais é o .shift():, que permite deslocar todos os dados da séie ou dataframe para
#o passado ou futuro. A versão deslocada em um período para o futuro  dos dados da série temporal  ficaria assim:
google['shifted'] = google.price.shift() # padrão: period = 1
google.head(3)
# Como reusltado, o primeiro valor da série agora está ausente:
#Em contraste, a versão defasa pra o passado (lagged) em 1 período
google['lagged'] = google.price.shift(periods = -1)
google[['price','lagged','shifted']].tail(3)
#Neste caso,o último valor está faltando.
# Note que para mover para o passado usamos um valor negativo em periods


#Deslocar os dados é útil para podermos compará-los em diferentes momentos od tempo.
# Você pode calcular a taxa de variação de período a período, o que chamamos de retorno financeiro.

# O método .div permite não apenas dividir uma série por um valor, mas por uma série inteira. Por exemplo,
# dividindo por uma outra coluna do mesmo dataFrame.
# O pandas se assegura que ambas séries sejam correspondam e dividirá os valores alinhados de acordo.
# Xt / Xt-1
google['change'] = google.price.div(google.shifted)
google[['price', 'shifted', 'change']].head(3)

#Como vimos antes, é possível encadear todos os métodos de DataFrame que retornam um DataFrame
#O DataFRame retornado será usado como entrada para o próximo cálculo.
google['return'] = google.change.sub(1).mul(100)
google[['price','change','return']].head(3)
# Aqui estamos subtraindo 1 e multiplicando o resultado por 100 para obter a varuação em termos percentuais

# Outro método de séries temporais é o .diff()., que calcula a mudança entre os valores em diferentes pontos do tempo.
# Xt - Xt-1

#Por padrão, a versão .diff do preço de fechamento é a diferença de valor desde o último dia em que as ações foram negociadas
google['diff'] = google.price.diff()
google[['price','diff']].head(3)
# Você pode usar esta informação para calcular também o retorno obtido em um período específico, basta dividir
# a mudança absoluta pelo preço e, em seguida, multiplicar por 100 para obter o mesmo resultado de antes.

#Finalmente, por ser uma operação tão comun, pandas tem um método embutido para calcular a variação percentual diretamente.
#Xt / Xt-1
google['pct_change'] = google.price.pct_change().mul(100)
google[['price','return','pct_change']].head(3)

# Nos exemplos usamos o default period = 1, mas é possível usar outros valores para cancular em relação à períodos mais distantes
google['return_3d'] = google.price.pct_change(periods = 3).mul(100)
google[['price','return_3d']].head()
# Este exemplo mostra a diferença entre preços com 3 dias de diferença

##___
##Exercício

#Shifting stock prices across time
#The first method to manipulate time series that you saw in the video was .shift(), which allows you shift all values in a Series or DataFrame by a number of periods to a different time along the DateTimeIndex.

#Let's use this to visually compare a stock price series for Google shifted 90 business days into both past and future.

# Import data here
path = r'D:\Rafael\OneDrive\Documentos\projetos_pycharm\Times Series in Python\Data\stock_data\google.csv'
google = pd.read_csv(path, parse_dates = ['Date'], index_col='Date')
# Set data frequency to business daily
google = google.asfreq('B')

# Create 'lagged' and 'shifted'
google['lagged'] = google.Close.shift(periods = -90)
google['shifted'] = google.Close.shift(periods = 90)

# Plot the google price series

google.plot()
plt.show(block = False)
plt.pause(0.001)

#exercício

# #Plotting multi-period returns
# The last time series method you have learned about in the
# video was .pct_change(). Let's use this function to calculate returns ' \
# 'for various calendar day periods, and plot the result to compare the different patterns.
#
# We'll be using Google stock prices from 2014-2016.

# Create daily_return
google['daily_return'] = google.Close.pct_change().mul(100)

# Create monthly_return
google['monthly_return'] = google.Close.pct_change(30).mul(100)

# Create annual_return
google['annual_return'] = google.Close.pct_change(360).mul(100)

# Plot the result
google.plot(subplots=True)
plt.show()


#____________
#Normalizing a single series

path = r'D:\Rafael\OneDrive\Documentos\projetos_pycharm\Times Series in Python\Data\stock_data\google.csv'
google = pd.read_csv(path, parse_dates = ['Date'], index_col='Date')
google.head(3)
first_price = google.Close.iloc[0]
first_price
# It was posible to use iloc with the first date, but in this way we do not need to know the exact day
first_price == google.loc['2014-01-02', "Close"]
# Now we divide the series by the first price and multiply by 100 to normalize
normalized = google.Close.div(first_price).mul(100)
normalized.plot(title = 'Google Normalized Price Series')

#Let's now compare several stocks
# Normalize multiple series (1)
#Lets import prices fr google, yahoo and apple
path = r'D:\Rafael\OneDrive\Documentos\projetos_pycharm\Times Series in Python\Data\stock_data\stock_data.csv'
prices = pd.read_csv(path, parse_dates = ['Date'], index_col=['Date'], sep =',')
prices.info()
prices.head(5)
prices.iloc[0]
# se você dividir um DataFrame por uma série usando o método div, o pandas garante que os rótulos das linhas da
# série se alinhem com os cabeçalhos de coluna do DataFrame. Ou Seja, Os dados dos preços das diferenets ações podem estar
# todos na mesma coluna, se eu tiver uma coluna que diz a qual ação pertencem (categoria), ao fazer
# a noramlização com .div() o pandas gerará uma coluna para daca um normalizada. Ou seja, parte de single values para
# varias colunas e DataFrame(s)

normalized_1 = prices.div(prices.iloc[0])
normalized_1.head(3)


# Comparing to a benchmark

#Adicionando um benchmark para comparar a performance destas ações com um índice

path = r'D:\Rafael\OneDrive\Documentos\projetos_pycharm\Times Series in Python\Data\stock_data\index.csv'
index = pd.read_csv(path, parse_dates = ['Date'], index_col='Date')
#index. rename(columns = {'0':'S&P500'}, inplace = True)
index.info()
index.head(5)
# Uma vez que o dado vem de fontes diferentes, usamos dropna() para remover os registros nulos e combinamos as duas fontes de dados em um DF
prices_full = pd.concat([prices, index], axis = 1).dropna()
prices_full.info()
prices_full.head(5)


# Podemos dividir as 4 séries pelo primeiro preço de cada, respectivamente, multiplicar por 100 e facilmnete
# Verificar como cada uma performou contra o S&P500 e em relação a cada uma.

normalized = prices_full.div(prices_full.iloc[0]).mul(100)
normalized.plot()
plt.show()

# Para mostrar a performance de cada ação em relação aoa benchmark em termos percentuais, podemos subtrair
# o S&p500 normalizado dos valores das ações normalizados.
# Use .sub() com a keyword axis - 0 para alinhar o indice da série com o índice do dataframe.
# Isto faz ocm que o pandas subtraia a série de cada um das colunas

diff_1 = normalized.loc[:,normalized.columns != 'Unnamed: 1'].sub(normalized['Unnamed: 1'], axis =0)
diff_f =  pd.concat([diff_1, normalized.iloc[: , -1]], axis = 1)
diff_f.rename(columns={'Unnamed: 1':'SP500'}, inplace=True)
# Como resultado, podemos ver como cada ação performou contra o benchmark
diff_f.plot()
plt.show()


#__________

# Compare the performance of several asset classes
# To broaden your perspective on financial markets, let's compare four key assets: stocks, bonds, gold, and oil.
# Import data here
path = r'D:\Rafael\OneDrive\Documentos\projetos_pycharm\Times Series in Python\Data\stock_data\asset_classes.csv'
prices = pd.read_csv(path, parse_dates = ['DATE'], index_col='DATE')

# Inspect prices here
print(prices.info())

# Select first prices
first_prices = prices.iloc[0]

# Create normalized
normalized = prices.div(first_prices).mul(100)
# Plot normalized
normalized.plot()
plt.show()

#_____________

# Comparing stock prices with a benchmark
# You also learned in the video how to compare the performance of various stocks against a benchmark.
# Now you'll learn more about the stock market by comparing the three largest stocks on the NYSE to the
# Dow Jones Industrial Average, which contains the 30 largest US companies.
#
# The three largest companies on the NYSE are:
#
# Company	Stock Ticker
# Johnson & Johnson	JNJ
# Exxon Mobil	XOM
# JP Morgan Chase	JPM

# Import stock prices and index here
path_1 = r'D:\Rafael\OneDrive\Documentos\projetos_pycharm\Times Series in Python\Data\stock_data\nyse.csv'
path_2 = r'D:\Rafael\OneDrive\Documentos\projetos_pycharm\Times Series in Python\Data\stock_data\dow_jones.csv'
stocks =  pd.read_csv(path_1, parse_dates = ['date'], index_col='date')
dow_jones = pd.read_csv(path_2, parse_dates = ['date'], index_col='date')

# Concatenate data and inspect result here
data = pd.concat([stocks,dow_jones], axis = 1)
print(data.info())

# Normalize and plot your data here

normalized = data.div(data.iloc[0]).mul(100).plot()

plt.show()

#___________

# Plot performance difference vs benchmark index
# In the video, you learned how to calculate and plot the performance difference of a
# stock in percentage points relative to a benchmark index.
#
# Let's compare the performance of Microsoft (MSFT) and Apple (AAPL) to the S&P 500 over the last 10 years.

# Create tickers
tickers = ['MSFT', 'AAPL']

# Import stock data here
path_1 = r'D:\Rafael\OneDrive\Documentos\projetos_pycharm\Times Series in Python\Data\stock_data\msft_aapl.csv'
stocks = pd.read_csv(path_1, parse_dates=['date'], index_col='date')

# Import index here
path_2 = r'D:\Rafael\OneDrive\Documentos\projetos_pycharm\Times Series in Python\Data\stock_data\sp500.csv'
sp500 = pd.read_csv(path_2 , parse_dates=['date'], index_col='date')


# Concatenate stocks and index here
data = pd.concat([stocks, sp500], axis=1).dropna()

# Normalize data
normalized = data.div(data.iloc[0]).mul(100)

# Subtract the normalized index from the normalized stock prices, and plot the result
normalized[tickers].sub(normalized['SP500'], axis=0).plot()
plt.show()
