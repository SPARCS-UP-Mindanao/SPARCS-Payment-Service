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
        self.__get_pending_payments_url = f'{self.__callback_base_url}/payments/pending'
        self.__update_payment_url = f'{self.__callback_base_url}/payments'

    def create_payment(self, payment: PaymentTransactionIn) -> Tuple[HTTPStatus, PaymentTransactionOut, str]:
        try:
            payment_dict = payment.dict()
            response = requests.post(self.__create_payment_url, json=payment_dict)
            result = response.json()
            if response.status_code != HTTPStatus.OK:
                return response.status_code, None, result

            logger.info('Payment Transaction Successfully Added')
            return HTTPStatus.OK, PaymentTransactionOut(**result), None

        except Exception as e:
            logger.error(f'Error creating payment: {e}')
            return HTTPStatus.INTERNAL_SERVER_ERROR, None, str(e)

    def get_pending_payment_transactions(self) -> Tuple[HTTPStatus, list[PaymentTransactionOut], str]:
        """
        Get pending payment transactions

        Returns:
            Tuple[HTTPStatus, list[PaymentTransactionOut], str]: Status code, list of payments, error message
        """
        try:
            response = requests.get(self.__get_pending_payments_url)
            result = response.json()

            if response.status_code != HTTPStatus.OK:
                return response.status_code, None, result.get('message', 'Unknown error')

            # Convert response to list of PaymentTransactionOut objects
            pending_payments = [PaymentTransactionOut(**payment) for payment in result]
            logger.info(f'Successfully retrieved {len(pending_payments)} pending payments')
            return HTTPStatus.OK, pending_payments, None

        except Exception as e:
            logger.error(f'Error getting pending payments: {e}')
            return HTTPStatus.INTERNAL_SERVER_ERROR, None, str(e)

    def update_payment_transaction(
        self, payment_transaction_id: str, payment: PaymentTransactionIn
    ) -> Tuple[HTTPStatus, PaymentTransactionOut, str]:
        """
        Update a payment transaction by ID

        Args:
            payment_transaction_id (str): The ID of the payment transaction to update
            payment (PaymentTransactionIn): The updated payment transaction data

        Returns:
            Tuple[HTTPStatus, PaymentTransactionOut, str]: Status code, updated payment transaction, error message
        """
        try:
            payment_dict = payment.dict()
            update_url = f'{self.__update_payment_url}/{payment_transaction_id}'
            response = requests.put(update_url, json=payment_dict)
            result = response.json()

            if response.status_code != HTTPStatus.OK:
                return response.status_code, None, result.get('message', 'Unknown error')

            logger.info(f'Payment Transaction {payment_transaction_id} Successfully Updated')
            return HTTPStatus.OK, PaymentTransactionOut(**result), None

        except Exception as e:
            logger.error(f'Error updating payment transaction {payment_transaction_id}: {e}')
            return HTTPStatus.INTERNAL_SERVER_ERROR, None, str(e)
