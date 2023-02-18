import json
import random
import asyncio
from contextlib import suppress

import aiohttp


class VK:
    """
    Класс для взаимодействия с ВК
    """

    def __init__(self, token: str) -> None:
        """
        Метод инициализации класса

        :param token: Токен аккаунта ВК
        """
        self.token = token

    async def add_friend(self, user_id: str) -> tuple[bool, str | None]:
        """
        Метод для добавления в друзья аккаунта ВК

        :return: tuple[bool, str | None]
        """
        headers = {'Authorization': f'Bearer {self.token}'}
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(f'https://api.vk.com/method/friends.add?user_id={user_id}?v=5.131') as response:
                json_response = await response.json()
                if 'error' in json_response:
                    return False, json_response["error"]["error_msg"]
                else:
                    return True, None


def file_input() -> dict:
    """
    Функция читает и возвращает словарь с данными аккаунтов

    :return: dict
    """
    with open('./input.json', 'r') as file:
        return json.load(file)


async def main() -> None:
    """
    Главная функция запуска

    :return: None
    """
    input_data = file_input()  # Получаем словарь с данными аккаунтов
    for key in input_data.keys():  # Перебираем словарь по его ключам
        account = input_data[key]
        next_account = input_data[str(int(key) + 1)]
        vk = VK(token=account["access_token"])  # Инициализируем класс
        next_vk = VK(token=next_account["access_token"])  # Инициализируем класс
        status, response = await vk.add_friend(next_account["user_id"])  # Отправляем заявку в друзья
        next_status, next_response = await next_vk.add_friend(account["user_id"])  # Принимаем заявку в друзья
        if status:  # Если отправка заявки в друзья удалась
            print(f'Отправил заявку в друзья - {account["url_profile"]}')
            if next_status:  # Если попытка добавления в друзья удалась
                print(f'Принял заявку в друзья - {next_account["url_profile"]}')
            else:  # Если попытка добавления в друзья не удалась
                print(f'Произошла ошибка аккаунта - {next_account["url_profile"]}: {response}')
        else:  # Если отправка заявки в друзья не удалась
            print(f'Произошла ошибка аккаунта - {account["url_profile"]}: {response}')


if __name__ == '__main__':
    with suppress(KeyboardInterrupt):  # Игнорирование ошибок при остановке
        asyncio.run(main())  # Запуск асинхронной функции из синхронного контекста
