import json
import logging
import os
from datetime import datetime
from typing import List, Optional

from aiohttp import web
from pydantic import BaseModel
from vkbottle import API
from urllib.parse import parse_qs

logger = logging.getLogger(__name__)

TOKEN = os.environ.get("API_TOKEN")
RECIPIENTS = os.environ.get("RECIPIENTS")

api = API(token=TOKEN)


class ProductsModel(BaseModel):
    name: str
    price: float
    quantity: int
    sum: float


class PaymentInfo(BaseModel):
    date: datetime
    order_id: str
    order_num: str
    domain: str
    sum: float
    customer_phone: str
    customer_email: str
    customer_extra: Optional[str]
    payment_type: str
    commission: float
    commission_sum: float
    attempt: int
    sys: Optional[str]
    vk_user_id: Optional[int]
    products: Optional[List[ProductsModel]]
    payment_status: str
    payment_status_description: str


async def process_request(request):
    try:
        request = json.loads(request)
    except Exception:
        request = parse_qs(request)
        request = {k: v[0] for k, v in request.items()}

    return request


async def update_order_status(request: web.Request) -> web.Response:
    logging.debug(request)
    request = await request.text()
    request = await process_request(request)
    logging.debug(request)
    order = PaymentInfo(**request)

    if order.payment_status == 'success':
        logger.info(f"Успех! Номер заказа: {order.order_id}\nСумма: {order.sum}\nТип: {order.payment_type}")
    else:
        logger.info(f"Информация по заказу: {order.json()}")
        message = f"Не прошла оплата для заказа {order.order_id}.\n\n" \
                  f"Контакты клиента:\n" \
                  f"\temail: {order.customer_email}\n" \
                  f"\tтелефон: {order.customer_phone}\n" \
                  f"\tдополнительные контакты: {order.customer_extra}.\n\n" \
                  f"Статус заказа:\n" \
                  f"\t{order.payment_status_description}"
        if order.vk_user_id:
            await api.messages.send(message=message, user_id=order.vk_user_id, random_id=0)
        else:
            logger.info("No vk id")
            await api.messages.send(message=message, user_id=RECIPIENTS, random_id=0)
    return web.Response()


async def main_page(request: web.Request) -> web.Response:
    return web.Response(text="Hi")
