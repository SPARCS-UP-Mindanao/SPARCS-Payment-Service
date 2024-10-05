import os
from http import HTTPStatus
from typing import Tuple

import requests

from model.payment.payment import PaymentTransactionIn, PaymentTransactionOut
from utils.logger import logger


class PaymentStorageGateway:
    def __init__(self):
        self.__callback_base_url = os.environ.get('CALLBACK_BASE_URL')
        self.__create_payment_url = f'{self.__callback_base_url}/payments'

    def create_payment(self, payment: PaymentTransactionIn) -> Tuple[HTTPStatus, PaymentTransactionOut, str]:
        try:
            payment_dict = payment.dict()
            response = requests.post(self.__create_payment_url, json=payment_dict)
            result = response.json()
            if response.status_code != HTTPStatus.OK:
                return response.status_code, None, result

            return HTTPStatus.OK, PaymentTransactionOut(**result), None

        except Exception as e:
            logger.error(f'Error creating payment: {e}')
            return HTTPStatus.INTERNAL_SERVER_ERROR, None, str(e)
