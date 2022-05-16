# # Risk and Return for all Stocks selected. In adittion, efficient frontier Markowitz is calculated.
#
# ## Author: Pablo Calatayud
# ## Email: pablocalatayudpelayo@gmail.com
# ## git-hub: pcalatayud-prog
# ## Linkedin; https://www.linkedin.com/in/pablo-calatayud-pelayo/

# ### 0. Loading Libraries

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
plt.style.use("seaborn")


# ### 1. Markowitz Border Function

# +

def markowitz_border(summary):
    '''The input is the pair risk/return for each stock
    With those values the best return for each risk value is calculated and plotted
    '''
    step=0.05  
    min_risk=summary["std"].min()+step
    #max_risk=summary["std"].max()
    max_risk=1
    rang = np.arange(min_risk,max_risk,step)

    #print("Min RisK:",min_risk)
    #print("Max RisK:",max_risk)   
    #print("Range:",rang)
    #del border
    border = pd.DataFrame(columns = summary.columns)
    #i=0.6
    for i in rang:
        #print(i)
        label = summary.loc[summary["std"]<i]["mean"].idxmax()
        if label not in border.index:
            add = summary.loc[label:label]
            border=pd.concat([border,add])
        #print(border)
    return(border)
markowitz_border.__doc__ = "The input is a Data Frame. The index is the stock ticker, first colum is the return-mean, second column = risk-std"


# -

# ### 2. Risk/Return for stock selected

# +

def function_risk_return(starts,ends,tickers):
    '''They inputs are a startDate and endDate. With those values it is calculated the pair 
        return/risk for each stock in the sp500
    '''
    
    #tikers = pd.read_csv(filename)
    #ticker = list(tikers["Ticker"])

    stocks = yf.download(tickers, start = starts, end = ends)


    close = stocks.loc[:, "Adj Close"].copy()
    close = close.iloc[1: , :]
    close.fillna(method='bfill',inplace=True)
    close.dropna(axis=1, inplace=True)

    ret = close.pct_change()
    ret = ret.iloc[1: , :]


    summary = ret.describe().T.loc[:, ["mean", "std"]]
    summary["mean"] = summary["mean"]*252
    summary["std"] = summary["std"] * np.sqrt(252)

    #Removing any stock with risk higher than 1
    summary = summary[summary["std"]<1]
    
    df_border = markowitz_border(summary)
    
    title_plot = "Risk/Return. From" + " " + starts + " to " + ends + "."
    summary.plot(kind = "scatter", x = "std", y = "mean", figsize = (15,12), s = 50, fontsize = 15)
    
    for i in summary.index:
        plt.annotate(i, xy=(summary.loc[i, "std"]+0.002, summary.loc[i, "mean"]+0.002), size = 15,color = "black")
    
    for i in df_border.index:
        plt.annotate(i, xy=(df_border.loc[i, "std"]+0.002, df_border.loc[i, "mean"]+0.002), size = 15,color="red")
    
    
    plt.xlabel("ann. Risk(std)", fontsize = 15)
    plt.ylabel("ann. Return", fontsize = 15)
    plt.title(title_plot, fontsize = 20)
    plt.show()

    #
    print("efficient frontier Data Frame")
    print(df_border)
    df_border.plot(kind = "scatter", x = "std", y = "mean", figsize = (15,12), s = 50, fontsize = 15)
    for i in df_border.index:
        plt.annotate(i, xy=(df_border.loc[i, "std"]+0.002, df_border.loc[i, "mean"]+0.002), size = 15,color="red")
    plt.xlabel("ann. Risk(std)", fontsize = 15)
    plt.ylabel("ann. Return", fontsize = 15)
    plt.title(title_plot, fontsize = 20)
    plt.show()

    return (summary,df_border)

function_risk_return.__doc__ ="They inputs are a startDate, endDate and the fileName where the ticker stocks are stored. With those values it is calculated the pair return/risk for each stock in the file."

