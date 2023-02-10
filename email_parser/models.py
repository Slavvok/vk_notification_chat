from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel


class ProductsModel(BaseModel):
    name: str
    price: float
    quantity: int
    sum: float


class SubscriptionInfo(BaseModel):
    type: Optional[str]
    notification_code: Optional[str]
    id: Optional[str]
    profile_id: Optional[str]
    demo: Optional[str]
    active_manager: Optional[str]
    active_manager_date: Optional[str]
    active_user: Optional[str]
    active_user_date: Optional[str]
    cost: Optional[str]
    currency: Optional[str]
    name: Optional[str]
    limit_autopayments: Optional[str]
    autopayments_num: Optional[str]
    first_payment_discount: Optional[str]
    next_payment_discount: Optional[str]
    next_payment_discount_num: Optional[str]
    date_create: Optional[str]
    date_first_payment: Optional[str]
    date_last_payment: Optional[str]
    date_next_payment: Optional[str]
    date_alt_next_payment: Optional[str]
    date_next_payment_attempt: Optional[str]
    date_next_payment_discount: Optional[str]
    date_completion: Optional[str]
    current_attempt: Optional[str]
    payment_num: Optional[str]
    notification: Optional[str]
    process_started_at: Optional[str]
    active: Optional[str]
    subscription_interval: Optional[str]


class PaymentInfo(BaseModel):
    id: Optional[str]
    date: datetime
    order_id: str
    order_num: str
    domain: str
    sum: float
    customer_phone: str
    customer_email: str
    customer_extra: Optional[str]
    payment_type: str
    commission: Optional[float]
    commission_sum: Optional[float]
    attempt: int
    sys: Optional[str]
    vk_user_id: Optional[int]
    products: Optional[List[ProductsModel]]
    payment_status: Optional[str]
    payment_status_description: Optional[str]
    subscription: Optional[SubscriptionInfo]
