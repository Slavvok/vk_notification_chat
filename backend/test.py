import json

import requests
from pydantic import BaseModel

# from pytest import MonkeyPatch
# from pytest_mock import mocker
from aiohttp import web


class ServerRequest(BaseModel):
    payment_status: str


async def index(request: web.Request):
    request = await request.text()
    request = json.loads(request)
    print(request)
    request = ServerRequest(**request)
    # logger.info(request)
    print(request.json())
    # await api.messages.send(message=request.json(), user_id=94957881, random_id=0)


# def test_index(mocker):
#     main_mock = mocker.patch('main')
#     main_mock.return_value = '{}'


def send_request(data):
    response = requests.post(url='http://localhost:8080', data=data)
    print(response)


if __name__ == '__main__':
    data = {
        "date": "2020-07-27T12:31:01+03:00",  "order_id": "300155",  "order_num": "test",  "domain": "demo.payform.ru",
        "sum": "100.00", "customer_phone": "+79999999999",  "customer_email": "test@domain.ru", "customer_extra": "тест",
        "payment_type": "Пластиковая карта Visa, MasterCard, МИР", "commission": "3.5",  "commission_sum": "0.03",
        "attempt": "1", "sys": "demo", "vk_user_id": "1234567890",
        "products": [{"name": "Доступ в клуб Девелопер клаб", "price": "100.00", "quantity": "1", "sum": "100.00"}],
        "payment_status": "failure",  "payment_status_description": "Успешная оплата"
    }
    send_request(json.dumps(data))
