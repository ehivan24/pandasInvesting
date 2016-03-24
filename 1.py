'''
Created on Feb 23, 2015

@author: edwingsantos
'''

import pandas as pd
import pandas.io.data
from pandas import DataFrame
import numpy
import matplotlib.pyplot as plt
import datetime
import math
import time


def star():
    
    #sp500 = pandas.io.data.get_data_yahoo('%5EGSPC', start= datetime.datetime(2000, 10, 1), end=datetime.datetime(2012,1,1))
    
    #sp500.to_csv('new.csv')
    
    df = pd.read_csv('new.csv', index_col='Date', parse_dates=True)
    print df.head()
    
    ts = df[['Low','Close','Open']][-10:]
    print ts
    
    df['H-L'] = df['High'] - df['Low'] #math
    
    print df.head()
    
    del df['Volume'] # remove cols
    print df.head() 
    
    close = df['Adj Close']
    ma = pd.rolling_mean(close, 50)
    
    print ma[-10:]
    
    """
    ax1 = plt.subplot(2,1,1)
    ax1.plot(close, label='sp500')
    ax1.plot(ma, label='50MA')
    plt.legend()
    plt.grid()
    
    ax2 = plt.subplot(2,1,2, sharex = ax1)
    ax2.plot(df['H-L'], label='H-L')
    plt.grid()
    plt.legend()
    plt.show()
    """


def calcPositions(ma1, ma2, ma3, ma4):
    if ma4 > ma1 > ma2 > ma3:
        return 1
    elif ma4 > ma1 > ma3 > ma2:
        return 1
    elif ma4 > ma2 > ma1> ma3:
        return 2
    elif ma1 > ma4 > ma3 > ma2:
        return 2
    elif ma1 > ma2 > ma4 > ma3:
        return 3
    elif ma1 > ma2 > ma3 > ma4:
        return 4
    elif ma2 > ma1 > ma3 > ma4:
        return 4
    elif ma1 > ma3 > ma2 > ma4:
        return 4
    elif ma1 < ma2 < ma3 < ma4:
        return -4
    elif ma4 > ma2 > ma3 > ma1:
        return -4
    elif ma1 < ma2 < ma4 < ma3:
        return -3
    elif ma4 > ma3 > ma1 > ma2:
        return -3
    elif ma1 < ma4 < ma2 < ma3:
        return - 2
    elif ma2 > ma3 > ma1 > ma4:
        return - 2
    elif ma3 > ma1 > ma4 > ma2:
        return - 2
    elif ma1 > ma3 > ma4 > ma2:
        return - 2
    elif ma4 < ma1 < ma2 < ma3:
        return -1
    elif ma2 > ma3 > ma4 > ma1:
        return -1
    elif ma3 > ma4 > ma1 > ma2:
        return -1
    elif ma1 > ma4 > ma2 > ma3:
        return 0
    else:
        return None



def modifyDataSet():
    df = pd.read_csv('stocks__.csv')
    df['time'] = pandas.to_datetime(df['time'], unit='s')
    df = df.set_index('time')
    del df['id']
    del df['value']
    print df.head()
    
    
#modifyDataSet()

##
# plot a stock
##

def singleStock(stockName):
    df = pd.read_csv('stocks_OLD.csv', index_col='time', parse_dates=True)
    df = df[df.type == stockName.lower()]
    
    _500MA = pd.rolling_mean(df['value'], 500)
    
    ax1 = plt.subplot(2,1,1)
    df['close'].plot(label='Price')
    plt.legend()
    
    ax2 = plt.subplot(2,1,2, sharex=ax1)
    _500MA.plot(label='500MA')
    plt.show()
    
#singleStock('msft')



##
# this function modifies the graph and eliminates anything bigger than the standar Deviation
# anything greater than "1.5" will be ignored
##

def outlinerFixing(stockName):
    df = pd.read_csv('stocks__.csv', index_col='time', parse_dates=True)
    df = df[df.type == stockName.lower()]
    
    df['std'] = pd.rolling_std(df['close'], 25, min_periods = 1)
    
    #df = df[df['std'] < 1.0]
    
    
    ax1 = plt.subplot(2,1,1)
    df['close'].plot(label='Price')
    plt.legend()
    ax2 =plt.subplot(2,1,2, sharex = ax1)
    df['std'].plot(label='Deviation')
    plt.legend()
    plt.show()
    

#outlinerFixing('goog')



def singleSingleStockAutoMA(stockName, div1=275,div2=110,div3=55,div4=6 ):
    
    df = pd.read_csv('stocks_OLD.csv', index_col='time', parse_dates=True)
    df = df[df.type == stockName.lower()]
    count = df['type'].value_counts()
    count = int(count[stockName])
    
    MA1 = pd.rolling_mean(df['value'], (count / div1))
    MA2 = pd.rolling_mean(df['value'], (count / div2))
    MA3 = pd.rolling_mean(df['value'], (count / div3))
    MA4 = pd.rolling_mean(df['value'], (count / div4))
    
    SP = int(math.ceil(count / div4 ))
     
    df['MA1'] = MA1
    df['MA2'] = MA2
    df['MA3'] = MA3
    df['MA4'] = MA4
    
    df= df[SP:]
    
    del df['MA100']
    del df['MA250']
    del df['MA500']
    del df['MA5000']
    
    df['Pos'] = map(calcPositions, df['MA1'], df['MA2'], df['MA3'], df['MA4'])
    
    df['Change'] = df['Pos'].diff()
    
    #print df[100:200]
    
    df.sort_index(inplace=True)
    return df
    
    """
    ax1 = plt.subplot(2,1,1)
    df['close'].plot(label='Price')
    plt.legend()
    plt.title(stockName)
    ax2 = plt.subplot(2,1,2, sharex=ax1)
    df['MA1'].plot(label=(str(count / div1)+' MA'))
    df['MA2'].plot(label=(str(count / div2)+' MA'))
    df['MA3'].plot(label=(str(count / div3)+' MA'))
    df['MA4'].plot(label=(str(count / div4)+' MA'))
    plt.legend()
    plt.show() 
    
    
    print "count: " + str(count)
    
    return None 
    
#print "\n\nCount: " + str(singleSingleStockAutoMA('aapl'))

"""



def backTest(dataS, closeI, changeI):
    stockHoldings = 0
    startingCapital = dataS['close']* 8
    
    funds = startingCapital
    currentValuation = funds 
    
    
    for row in dataS.iterrows():
        try:
            #print row
            #time.sleep(5) 
            index, data = row
            rowData = data.tolist()
            price = rowData[closeI]
            change = int(rowData[changeI])
            
            
            #
            #make a purchase
            #
            if isinstance(change, (int, long)) and change != 0:
                if change > 0:
                    if (change * price) < funds:
                        funds -= (change * price)
                        stockHoldings += change
                        currentValuation = funds + (stockHoldings * price)
                    else:
                        pass
                elif change < 0:
                    change = abs(change)
                    
                    if stockHoldings == 0:
                        pass
                    
                    elif (stockHoldings - change) < 0:
                        change = stockHoldings
                        
                    else:
                        stockHoldings -= change
                        funds += (change * price)
                        currentValuation = funds + (stockHoldings + price) 
                    
        except:
            pass    
    
    print "Holdings:  ", stockHoldings
    print "funds: ", funds
    print "Current Validation: ",  currentValuation
    percentChange = ((currentValuation - startingCapital )/ startingCapital) * 100.00
    print "Strategy Percent Growth:  ", percentChange
    
    
data = singleSingleStockAutoMA('c')
#print data['close'] * 8

backTest(data, closeI = 3, changeI = 11)

a = 12
a * a

print ("Error: {0:d}".format(a))





