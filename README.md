# Техническое задание
1. Вам нужно определить собственные движения цены фьючерса ETHUSDT, исключив из них движения вызванные влиянием цены BTCUSDT. Опишите, какую методику вы выбрали, какие параметры подобрали, и почему.

2. Напишите программу на Python, которая в реальном времени (с минимальной задержкой) следит за ценой фьючерса ETHUSDT и используя выбранный вами метод, определяет собственные движение цены ETH. При изменении цены на 1% за последние 60 минут, программа выводит сообщение в консоль. При этом программа должна продолжать работать дальше, постоянно считывая актуальную цену.

# Ответ на 1-й вопрос
1. Определил коэффициент кореляции между BTCUSDT и ETHUSDT
2. Используя линейную регрессию нашел коэффициент влияния | коэффициент влияния = коэффициент кореляции * (стандартное отклонение ETHUSDT / стандартное отклонение BTCUSDT)
3. Ипользовал данный подход т.к. это способствует большей читаемости кода и использует малое количество вычислений, что в свою очередь должно снизить задержки
