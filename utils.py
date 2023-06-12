

def send_notification(time, real, independent):
    real = round(real, 3)
    independent = round(independent, 3)
    print(
        f'За последние {time / 60} минут, собственная цена ETH изменилась на {real}%, а общая цена на {independent}%.'
    )
