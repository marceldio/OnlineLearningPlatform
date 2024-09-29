from decimal import Decimal

import requests
import stripe
from forex_python.converter import CurrencyRates, RatesNotAvailableError

from config.settings import STRIPE_SECRET_KEY

stripe.api_key = STRIPE_SECRET_KEY


def create_stripe_product(payment):
    """Создать продукт в Stripe для курса или урока."""
    if payment.paid_course:
        product_name = payment.paid_course.title
    elif payment.paid_lesson:
        product_name = payment.paid_lesson.title
    else:
        raise ValueError("Необходимо указать либо курс, либо урок для оплаты.")

    product = stripe.Product.create(name=product_name)
    return product.id


def convert_rub_to_dollars(amount):
    """Конвертировать рубли в доллары. Используем резервный курс в случае ошибки."""
    try:
        c = CurrencyRates()
        rate = c.get_rate("RUB", "USD")
        return int(Decimal(amount) * Decimal(rate))
    except (RatesNotAvailableError, requests.exceptions.RequestException):
        # Используем фиксированный курс для тестирования
        fallback_rate = Decimal(
            "0.011"
        )  # Пример фиксированного курса (1 RUB = 0.011 USD на 29.09.2024)
        return int(Decimal(amount) * fallback_rate)
    except Exception as e:
        raise ValueError(f"Ошибка при конвертации валюты: {str(e)}")


def create_stripe_price(product_id, amount):
    """Создать цену для продукта в Stripe."""
    price = stripe.Price.create(
        product=product_id,
        unit_amount=int(amount * 100),  # сумму в центах приводим к доллару
        currency="usd",
    )
    return price.id


def create_stripe_checkout_session(price_id, success_url, cancel_url):
    """Создать сессию оплаты в Stripe."""
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price": price_id,
                "quantity": 1,
            },
        ],
        mode="payment",
        success_url=success_url,
        cancel_url=cancel_url,
    )
    return session.id, session.url
