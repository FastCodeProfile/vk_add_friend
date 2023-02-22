import asyncio
import json
from contextlib import suppress

import aiohttp
from loguru import logger


class VkApi:
    def __init__(self, access_token: str) -> None:
        self.host = 'https://api.vk.com/method/'
        self.params = {'v': 5.131}
        self.headers = {'Authorization': f"Bearer {access_token}"}

    async def add_friend(self, user_id: str) -> bool:
        method = 'friends.add'
        self.params["user_id"] = user_id
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.get(self.host + method, params=self.params) as response:
                json_response = await response.json()
                return 'error' not in json_response


def load_data(filename: str) -> dict:
    with open(filename, encoding='utf-8') as file:
        return json.load(file)


async def main() -> None:
    data = load_data('data.json')
    for key, user in data.items():
        next_key = str(int(key) + 1)
        if next_key in data:
            next_user = data[next_key]
            vk_api = VkApi(user["access_token"])
            next_vk_api = VkApi(next_user["access_token"])
            result = await vk_api.add_friend(next_user["user_id"])
            next_result = await next_vk_api.add_friend(user["user_id"])
            if result and next_result:
                logger.success(f'{user["url_profile"]} <- ТЕПЕРЬ ДРУЗЬЯ -> {next_user["url_profile"]}')
            else:
                logger.error(f'{user["url_profile"]} <- ЦЕПЬ РАЗОРВАНА -> {next_user["url_profile"]}')
                logger.warning('Используйте скрипт, что бы отсеять невалидные аккаунты. '
                               'Ссылка на скрипт: https://github.com/FastCodeProfile/vk_check_token.git')
                break


if __name__ == '__main__':
    with suppress(KeyboardInterrupt):
        asyncio.run(main())
