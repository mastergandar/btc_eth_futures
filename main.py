import asyncio

from binance import AsyncHandler, DataHandler
from pricing import PriceHandler


if __name__ == "__main__":
    price_handler = PriceHandler()
    data_handler = DataHandler()
    # Единожды обновляем данные об коэффициенте влияния
    # Можно добавить таймер на обновление этого параметра или вызывать его при каждой проверке данных
    price_handler.set_impact_ratio(data_handler.get_impact_ratio())
    # Запускаем цикл событий который будет работать пока нас не отключит от websocket канала по той или иной причине
    asyncio.get_event_loop().run_until_complete(AsyncHandler.connect(price_handler))
