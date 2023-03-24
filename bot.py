import config
from binance.client import Client
from binance.enums import *
import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt
import math

client = Client(config.API_KEY, config.API_SECRET, tld='com')

monedas = ['ETHUSDT',
           'BNBUSDT',
           'ADAUSDT',
           'XRPUSDT',
           'LTCUSDT',
           'BTCUSDT',
           'COTIUSDT',
           'VETUSDT',
           'LINKUSDT',
           'AVAXUSDT',
           'ARPAUSDT',
           'TRXUSDT',
           'DOTUSDT',
           'UNIUSDT',
           'NEOUSDT',
           'IOTAUSDT',
           'EOSUSDT',
           'LUNAUSDT',
           'THETAUSDT']

tiempo = "7 months ago UTC"
intervalo = Client.KLINE_INTERVAL_1WEEK


def parametros_monedas(monedas, intervalo, tiempo):
    retorno = []
    riesgo = []
    retornos_para_matriz = []
    for moneda in monedas:
        klines = client.get_historical_klines(moneda, intervalo, tiempo)
        precios_cierre = []
        for valor in klines:
            precios_cierre.append(float(valor[4]))
        retornos = []
        i = 0
        while i < len(precios_cierre) - 1:
            retornos.append((precios_cierre[i+1]-precios_cierre[i])/precios_cierre[i])
            i += 1
        retorno.append(np.average(retornos))
        riesgo.append(np.std(retornos))
        retornos_para_matriz.append(retornos)
    data = np.array(retornos_para_matriz)
    covMatrix = np.cov(data, bias=True)
    return retorno, riesgo, covMatrix


retorno, riesgo, matriz_covarianza = parametros_monedas(monedas, intervalo, tiempo)


def get_ret_vol_sr(weights):
    w = np.array(weights)
    ret = np.array(retorno) @ w
    rf = 0
    vol = math.sqrt(w.T @ (matriz_covarianza @ w))
    sr = (ret - rf)/vol
    return np.array([ret, vol, sr])


# minimize negative Sharpe Ratio
def neg_sharpe(weights):
    return get_ret_vol_sr(weights)[2] * -1


# check allocation sums to 1
def check_sum(weights):
    return np.sum(weights) - 1


# create constraint variable
cons = ({'type':'eq','fun':check_sum})

# create weight boundaries
bounds = []
init_guess = []
for moneda in monedas:
    bounds.append((0,1))
    init_guess.append(float(1/len(monedas)))
init_guess = np.array(init_guess)


opt_results = minimize(neg_sharpe, init_guess, method='SLSQP', bounds=bounds, constraints=cons)

print("CRYPTO   PROPORCIÓN")
print("*" * 30)
for i in range(0, len(opt_results.x)):
    print(f"{monedas[i]}: {opt_results.x[i]*100}")
print("*" * 30)
p_retorno, p_vol, p_sr = get_ret_vol_sr(opt_results.x)
print(f"Retorno portafolio: {p_retorno}")
print(f"Volatilidad portafolio: {p_vol}")
print(f"Sharpe Ratio: {p_sr}")


fig, ax = plt.subplots()
ax.scatter(x=riesgo, y=retorno, alpha=0.5)
ax.set(title='Retorno y Riesgo', xlabel='Riesgo', ylabel='Retorno')

for i, symbol in enumerate(monedas):
    ax.annotate(symbol, (riesgo[i], retorno[i]))
ax.scatter(x=p_vol, y=p_retorno, alpha=0.5)
ax.annotate('P', (p_vol, p_retorno))

plt.show()
