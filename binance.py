from time import time

import numpy as np
import requests
import websockets
import json


class AsyncHandler:

    base_url = "wss://fstream.binance.com/stream?streams="
    btc_price = None
    eth_price = None

    # Используем асинхронное подключение к websocket Binance API для получения текущих цен BTCUSDT и ETHUSDT
    @classmethod
    async def connect(cls, price_handler):
        # Подключаемя к стримам данных btcusdt@aggTrade и ethusdt@aggTrade | скорость получения данных: 100ms
        # Также можно использовать стримы btcusdt@markPrice и ethusdt@markPrice | скорость получения данных: 1s или 3s
        async with websockets.connect(cls.base_url + "btcusdt@aggTrade" + "/" + "ethusdt@aggTrade") as ws:
            while True:
                msg = await ws.recv()
                jsoned_msg = json.loads(msg)
                if jsoned_msg['data']['s'] == 'BTCUSDT':
                    cls.btc_price = float(jsoned_msg['data']['p'])
                else:
                    cls.eth_price = float(jsoned_msg['data']['p'])

                # Раскомментировать чтобы увидеть спам из получаемых по websocket каналу данных
                # print(f"PRICE {jsoned_msg['data']['s']}: {jsoned_msg['data']['p']} | TIME: {jsoned_msg['data']['E']}")

                # Обрабатываем текущие и прошлые цены с ипользованием коэффициента линейной регрессии
                # для получения решения задачи

                await price_handler.handle_prices(cls.btc_price, cls.eth_price)


class DataHandler:

    def __init__(self):
        self.btc_data_response = self.get_symbol_data('BTCUSDT')
        self.eth_data_response = self.get_symbol_data('ETHUSDT')

    # Singleton
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(DataHandler, cls).__new__(cls)
        return cls.instance

    @staticmethod
    def get_symbol_data(symbol: str):
        params = {
            'symbol': symbol,
            'interval': '1h',  # интервал данных
            'startTime': int(1000 * time() - 24 * 60 * 60 * 1000),  # начало периода
            'endTime': int(1000 * time())  # конец периода
        }

        response = requests.get('https://api.binance.com/api/v3/klines', params=params).json()

        return response

    def get_btc_prices(self):

        btc_prices = np.array([float(x[4]) for x in self.btc_data_response])  # цены на BTCUSDT

        return btc_prices

    def get_eth_prices(self):

        eth_prices = np.array([float(x[4]) for x in self.eth_data_response])  # цены на ETHUSDT

        return eth_prices

    def get_correlation(self):

        # Вычисление коэффициента корреляции
        correlation = np.corrcoef(self.get_btc_prices(), self.get_eth_prices())[0, 1]

        print(f"Коэффициент корреляции между BTCUSDT и ETHUSDT равен {round(correlation, 3)}")

        return round(correlation, 3)

    def get_impact_ratio(self):

        btc_data = np.array(self.btc_data_response)
        eth_data = np.array(self.eth_data_response)

        btc_close = np.std(btc_data[:, 4].astype(float))
        eth_close = np.std(eth_data[:, 4].astype(float))

        impact_ratio = self.get_correlation() * (eth_close / btc_close)

        print(f"Коэффициент влияния BTCUSDT на ETHUSDT равен {round(impact_ratio, 3)}")

        return impact_ratio
