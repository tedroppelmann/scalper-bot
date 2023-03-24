import config
from binance.client import Client

monedas = ['ETHUSDT',
           'BNBUSDT',
           'ADAUSDT',
           'XRPUSDT',
           'LTCUSDT',
           'BTCUSDT',
           'COTIUSDT',
           'VETUSDT',
           'DOGEUSDT',
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

proporciones = [2.30925195e-01, 1.25069497e-16, 1.44947457e-01, 9.17793376e-02,
                0.00000000e+00, 9.18319240e-17, 7.39637262e-02, 0.00000000e+00,
                4.49835301e-02, 6.30056987e-17, 0.00000000e+00, 0.00000000e+00,
                3.37986189e-03, 9.72902717e-19, 1.27145969e-01, 1.74515892e-16,
                0.00000000e+00, 0.00000000e+00, 5.36947968e-02, 2.29180127e-01]

client = Client(config.API_KEY, config.API_SECRET, tld='com')
tiempo = "1 minute ago UTC"
intervalo = Client.KLINE_INTERVAL_1MINUTE

precios_iniciales = [3900.91, 645.93, 1.6193, 1.5614, 346.44, 58793.26, 0.3826, 0.2231, 0.6358, 48.62,
                     38.3, 0.11264, 0.14306, 39.871, 40.417, 116.476, 2.1599, 10.3234, 16.992, 12.285]

precios_cierre = []
for moneda in monedas:
    klines = client.get_historical_klines(moneda, intervalo, tiempo)
    for valor in klines:
        precios_cierre.append(float(valor[4]))

retornos = []
for i in range(0, len(precios_iniciales)):
    ret = (precios_cierre[i] - precios_iniciales[i]) / precios_iniciales[i]
    retornos.append(ret)

print("CRYPTO   RETORNO(%)")
print("*" * 30)
retorno_final = 0
for i in range(0, len(retornos)):
    retorno_peso = retornos[i]*proporciones[i]
    print(f"{monedas[i]}: {retorno_peso * 100}%")
    retorno_final += retorno_peso

print("*" * 30)
print(f"RENTABILIDAD TOTAL: {retorno_final * 100}%")
