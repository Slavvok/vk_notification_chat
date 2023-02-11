import asyncio
import json
import logging
import os
import re

from vkbottle import API
from imap_tools import MailBoxUnencrypted
from html_parser import EmailHTMLParser
from models import PaymentInfo


EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_PORT = os.environ.get("EMAIL_PORT")
EMAIL_DOMAIN = os.environ.get("EMAIL_DOMAIN")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
TOKEN = os.environ.get("API_TOKEN")
RECIPIENTS = os.environ.get("RECIPIENTS")
GREETING_TEXT = os.environ.get('GREETING_TEXT').replace('\\n', '\n')

api = API(token=TOKEN)


logger = logging.getLogger(__name__)


async def gather_messages(bodies):
    funcs = [parse_email(body) for body in bodies]
    await asyncio.gather(*funcs)


async def get_vk_id(vk_id: str) -> str:
    vk_id = re.findall(r'/\w+$', vk_id)[0].replace('/', '')
    if re.search(r'^id\d+', vk_id):
        vk_id = re.findall(r'\d+', vk_id)[0]
    else:
        user = await api.users.get(user_ids=[vk_id], fields=['id'])
        vk_id = user[0].id
    return str(vk_id)


async def parse_plain_text(email_text):
    error_ix = email_text.find("Ошибка")
    if error_ix == -1:
        logger.info("Получена успешная оплата")
    else:
        result = email_text[error_ix:]
        result = re.sub(r" №\d+", "", result)
        result = re.sub(r"ошибка:\r\n", "", result)
        price = result.find("₽")
        result = result[:price + 1]

        vk_id = re.findall(r'vk.com/\S+', email_text)

        if not vk_id:
            start_contacts = email_text.find('номер телефона:')
            end_contacts = email_text.find('доп')
            contacts = email_text[start_contacts:end_contacts]
            result = f"{result}\n{contacts}"
        else:
            vk_id = await get_vk_id(vk_id[0])
            result = f"{GREETING_TEXT}{result}"

        await send_vk_message(result, vk_id)


async def parse_dict(fetched_dict):

    if fetched_dict:
        request = json.loads(fetched_dict[0])
        logger.debug(request)
        order = PaymentInfo(**request)
        vk_id = order.customer_extra
        order_info = f"Сумма: {order.sum}\nТип: {order.payment_type}"
        if order.payment_status == 'success':
            logger.info(f"Успех! Номер заказа: {order.order_id}\n{order_info}")
        else:
            logger.info(f"Ошибка оплаты! Номер заказа: {order.order_id}\n{order_info}")
            subscription_id = order.subscription.id if order.subscription and order.subscription.id is not None else ''
            message = f"Не прошла оплата по подписке\n\n{order_info}\n"

            if not vk_id:
                message += f"Контакты клиента:\n" \
                           f"\temail: {order.customer_email}\n" \
                           f"\tтелефон: {order.customer_phone}\n\n"
            else:
                vk_id = await get_vk_id(vk_id)
                message = f"{GREETING_TEXT}{message}"

            if order.payment_status_description:
                message += f"Статус заказа:\n" \
                           f"\t{order.payment_status_description}"

            await send_vk_message(message, vk_id)
    else:
        raise Exception("No json has been found")


async def parse_email(email_text):
    fetched_dict = re.findall(r"{.*:\[{.*:.*}].*}", email_text)
    if not fetched_dict:
        fetched_dict = re.findall(r'{.*:{.*:.*}.*}', email_text)

    if not fetched_dict:
        await parse_plain_text(email_text)
    else:
        await parse_dict(fetched_dict)


async def send_vk_message(message, vk_id=None):
    if not vk_id:
        logger.info('Sending message to admin')
        await api.messages.send(message=message, user_id=RECIPIENTS, random_id=0)
    else:
        logger.info(f'Sending message to user {vk_id}')
        await api.messages.send(message=message, user_id=RECIPIENTS, random_id=0)


def fetch_emails():
    data = imaptools_fetch()
    if not data:
        logger.info("No new messages")
    else:
        logger.info(f"New messages: {len(data)}")
        asyncio.run(gather_messages(data))


def imaptools_fetch() -> list:
    messages = []
    # get email bodies from INBOX
    with MailBoxUnencrypted(EMAIL_HOST, EMAIL_PORT).login(EMAIL_DOMAIN, EMAIL_PASSWORD, 'INBOX') as mailbox:
        for msg in mailbox.fetch('UNSEEN'):
            body = msg.text
            if not body:
                body = msg.html
            html_parser = EmailHTMLParser()
            html_parser.feed(body)
            result = html_parser.result
            messages.append(result)
    return messages


if __name__ == '__main__':
    fetch_emails()
