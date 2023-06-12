from time import time
from utils import send_notification


class PriceHandler:

    def __init__(self):
        self.impact_ratio = 0
        self.last_btc_price = None
        self.last_eth_price = None
        self.time_range = 3600
        self.price_range = 0.01
        self.start_time = time()
        self.deviation = 0
        self.pure_deviation = 0

    # Singleton
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(PriceHandler, cls).__new__(cls)
        return cls.instance

    # Начало блока интерфейсов
    def set_impact_ratio(self, ratio: int):
        self.impact_ratio = ratio

    def set_start_time(self, start_time):
        self.start_time = start_time

    def set_deviation(self, deviation: int):
        self.deviation = deviation

    def set_pure_deviation(self, pure_deviation: int):
        self.pure_deviation = pure_deviation

    def set_last_price(self, symbol: str, price: int):
        if symbol == 'BTC':
            self.last_btc_price = price
        elif symbol == 'ETH':
            self.last_eth_price = price
    # Конец блока интерфейсов

    async def handle_prices(self, btc_price, eth_price):

        if all((self.last_btc_price, self.last_eth_price)):

            btc_delta = (btc_price - self.last_btc_price)
            eth_delta = (eth_price - self.last_eth_price)
            eth_independent_delta = eth_delta - btc_delta * self.impact_ratio

            eth_whole_change = eth_delta / self.last_eth_price
            eth_independent_change = eth_independent_delta / self.last_eth_price
            self.set_deviation(self.deviation + eth_whole_change)
            self.set_pure_deviation(self.pure_deviation + eth_independent_change)

            now = time()
            time_passed = now - self.start_time

            if abs(self.deviation) > self.price_range or time_passed > self.time_range:

                if abs(self.deviation) > self.price_range:

                    send_notification(self.time_range, self.deviation * 100, self.pure_deviation * 100)

                self.set_start_time(now)
                self.set_deviation(0)
                self.set_pure_deviation(0)

        self.set_last_price('BTC', btc_price)
        self.set_last_price('ETH', eth_price)
